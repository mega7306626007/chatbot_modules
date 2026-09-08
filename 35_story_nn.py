"""StoryLanguageModel (Section 14C) - the trained neural story generator.

Trained OFFLINE by train_story_nn.py on the public-domain Project
Gutenberg books listed in data/gutenberg_books.csv (see that file's
docstring for the full WHY). At runtime this class only LOADS the saved
weights + vocab from model_cache/ and samples continuation text from the
learned distribution - no training happens during a chat session, so
startup stays fast and the freed model stays tiny (~a plain NumPy LSTM).

The backend mirrors the project's existing optional-ML pattern (see
TransformerLanguageModel in 20_language_models.py, Section 14B):

  * If the saved model exists AND numpy is importable -> a real neural
    network generates the story text.
  * Otherwise the class reports available=False and callers fall back to
    the hand-written story banks (StoryTeller) unchanged - running this
    module is purely additive, never a regression.

All generation math lives here (small enough to keep visible); the
training script reproduces the identical tokenizer + LSTM equations so a
saved .npz loads with zero re-tokenizing surprises. Torch is NOT used at
runtime: train_story_nn.py trains the LSTM in torch (fast, BLAS-backed)
and exports the weights into this module's exact NumPy schema, so the
deployed bot stays dependency-light while still being a genuine LSTM
trained by gradient descent on all the Gutenberg books.
"""

import json
import os
import random
import re

# The same special-token layout train_story_nn.py saves with, so the
# saved vocab indexes match exactly.
PAD = "<pad>"
UNK = "<unk>"
BOS = "<bos>"
EOS = "<eos>"

_TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ']+|[0-9]+|[.,!?;:\"'()\[\]\-]+")


class StoryLanguageModel:
    """A small LSTM language model trained on Gutenberg book prose.

    Public surface is intentionally tiny: available(), next_token(), and
    generate(). The rest is the quiet machinery of loading saved weights
    and running the LSTM recurrence forward."""

    HIDDEN = 128
    EMBED = 64

    def __init__(self, weights_path=None, vocab_path=None):
        self.HIDDEN = 128
        self.EMBED = 64
        base = os.path.dirname(os.path.abspath(__file__))
        self.weights_path = weights_path or os.path.join(base, "model_cache", "story_nn.npz")
        self.vocab_path = vocab_path or os.path.join(base, "model_cache", "story_nn_vocab.json")

        self.word2id = {}
        self.id2word = {}
        self.params = None
        self.backend = "unavailable"
        self.last_training_info = None
        self._load()

    # ------------------------------------------------------------------
    # Loading / probing
    # ------------------------------------------------------------------

    def _load(self):
        """Loads saved weights + vocab if both exist and numpy is usable.
        Fails fast and silent to available=False, never crashing startup."""
        try:
            import numpy as np  # noqa: F401
        except ImportError:
            self.backend = "unavailable"
            return
        if not (os.path.exists(self.weights_path) and os.path.exists(self.vocab_path)):
            self.backend = "unavailable"
            return
        try:
            loaded = np.load(self.weights_path, allow_pickle=False)
            self.params = {k: loaded[k] for k in loaded.files}
            with open(self.vocab_path, "r", encoding="utf-8") as f:
                self.word2id = json.load(f)
            self.id2word = {int(i): w for w, i in self.word2id.items()}
            self.HIDDEN = self.params["W_h"].shape[1]
            self.EMBED = self.params["W_emb"].shape[1]
            self.backend = "lstm"
            self.last_training_info = (
                f"gutenberg LSTM: vocab {len(self.word2id)}, hidden {self.HIDDEN}"
            )
        except Exception as exc:
            # Corrupt/mismatched artifact must never break the bot.
            self.params = None
            self.word2id = {}
            self.backend = "unavailable"
            self.last_training_info = f"could not load story nn: {exc}"

    def available(self) -> bool:
        return self.backend == "lstm"

    # ------------------------------------------------------------------
    # Tokenizer (identical to the training script)
    # ------------------------------------------------------------------

    @staticmethod
    def tokenize(text: str):
        return _TOKEN_RE.findall(text.lower())

    def _encode(self, tokens):
        unk = self.word2id.get(UNK, 0)
        return [self.word2id.get(t, unk) for t in tokens]

    def _id_to_word(self, i):
        return self.id2word.get(i, UNK)

    # ------------------------------------------------------------------
    # LSTM forward
    # ------------------------------------------------------------------

    def _step(self, x_emb, h, c):
        import numpy as np
        H = self.HIDDEN
        gates = x_emb @ self.params["W_x"].T + h @ self.params["W_h"].T + self.params["b"]
        i = 1.0 / (1.0 + np.exp(-gates[:, :H]))
        f = 1.0 / (1.0 + np.exp(-gates[:, H:2 * H]))
        g = np.tanh(gates[:, 2 * H:3 * H])
        o = 1.0 / (1.0 + np.exp(-gates[:, 3 * H:4 * H]))
        c = f * c + i * g
        h = o * np.tanh(c)
        return h, c

    def next_token_logits(self, token_id, h, c):
        """One forward step for a single token; returns (logits, h, c)."""
        import numpy as np
        x_emb = self.params["W_emb"][np.array([token_id])]
        h, c = self._step(x_emb, h, c)
        logits = h @ self.params["W_hy"].T + self.params["b_y"]
        return logits[0], h, c

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def generate(self, seed_text="", max_words=60, temperature=0.6, seed=None,
                 rep_penalty=1.4, rep_window=12,
                 top_k=100, top_p=0.90, min_sentence_words=25,
                 block_ngrams=True):
        """Samples a short coherent passage from the learned distribution,
        seeded by seed_text (or from a bare start marker). Stops on a
        sampled <eos>, or at the first sentence-ending punctuation after
        at least min_sentence_words, so the prose never trails off in the
        middle of a sentence. Returns an empty string if the model is
        unavailable.

        temperature < 1.0 sharpens the distribution; rep_penalty
        suppresses recently-sampled words to avoid loops; top_k/top_p
        (nucleus) sampling cut the long ungrammatical tail of the vocab;
        block_ngrams hard-bans any candidate continuation that would
        complete a trigram already seen in the passage, which kills the
        "and the other and the other" style loops small models fall into."""
        if not self.available():
            return ""
        import numpy as np
        rng = np.random.default_rng(seed) if seed is not None else np.random.default_rng()

        tokens = self.tokenize(seed_text) if seed_text else []
        ids = [self.word2id.get(BOS, 0)] + self._encode(tokens)
        H = self.HIDDEN
        h = np.zeros((1, H))
        c = np.zeros((1, H))

        for tid in ids:
            _, h, c = self.next_token_logits(tid, h, c)

        output = list(tokens)
        recent = []
        for _ in range(max_words):
            logits, h, c = self.next_token_logits(ids[-1], h, c)
            logits = logits / max(temperature, 1e-3)
            # Repetition penalty: softly penalize tokens sampled recently.
            seen = set()
            for tok in recent[-rep_window:]:
                if tok in self.id2word and self.id2word[tok] not in seen:
                    seen.add(self.id2word[tok])
                    logits[tok] -= rep_penalty * max(temperature, 1e-3)
            # Mask the specials so generated text stays actual prose.
            for sp in (PAD, UNK, BOS, EOS):
                if sp in self.word2id:
                    logits[self.word2id[sp]] = -1e9
            # Nucleus (top-p) + top-k truncation: drop the long tail of
            # near-zero-probability words that make small models ramble.
            soft = np.exp(logits - logits.max())
            soft /= soft.sum()
            order = np.argsort(-logits)
            kept = np.zeros_like(logits, dtype=bool)
            s = 0.0
            for rank, j in enumerate(order):
                kept[j] = True
                s += soft[j]
                if rank >= top_k or s >= top_p:
                    break
            logits = np.where(kept, logits, -1e9)
            # Hard trigram block: refuse any candidate that completes a
            # 3-gram already used in the passage, so generation must keep
            # making progress instead of looping on a phrase.
            if block_ngrams and len(recent) >= 2:
                prefix = tuple(ids[-2:])
                for w in set(recent):
                    if any(recent[k:k + 3] == (*prefix, w)
                           for k in range(len(recent) - 2)):
                        logits[w] = -1e9
            probs = np.exp(logits - logits.max())
            probs /= probs.sum()
            total = probs.sum()
            if total <= 0:
                break
            probs = probs / total
            nxt = int(rng.choice(len(probs), 1, p=probs)[0])
            word = self._id_to_word(nxt)
            if word == EOS:
                break
            output.append(word)
            ids.append(nxt)
            recent.append(nxt)
            # End the passage at a complete sentence once it's long enough.
            if (len(output) - len(tokens)) >= min_sentence_words and word in ".!?":
                break

        return self._detokenize(output)

    @staticmethod
    def _detokenize(tokens):
        text = ""
        for tok in tokens:
            if re.fullmatch(r"[.,!?;:\"'()\[\]\-]+", tok):
                text = text.rstrip() + tok
            elif text:
                text += " " + tok
            else:
                text = tok
        return text[0].upper() + text[1:] if text else text

    # ------------------------------------------------------------------
    # Chatbot-facing convenience
    # ------------------------------------------------------------------

    def format_continuation(self, seed_text="", max_words=60):
        result = self.generate(seed_text=seed_text, max_words=max_words)
        if not result:
            return None  # caller falls back to the rule-based path
        return result