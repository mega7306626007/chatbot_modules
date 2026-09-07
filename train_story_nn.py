#!/usr/bin/env python3
"""train_story_nn.py - train a real neural-network story language model.

Downloads the Project Gutenberg public-domain books listed in
data/gutenberg_books.csv (a catalog of verified, download-compatible
english books), strips the Project Gutenberg header/footer boilerplate
from each one, builds a word-level training corpus, and trains an
offline, dependency-light NEURAL language model (a small vanilla LSTM,
written in plain NumPy) that learns to predict the next word the way
those stories actually continue.

WHY PLAIN NUMPY (rather than torch/tensorflow):
- The deployed chatbot (Render, free plan) installs only the small
  requirements.txt - torch would balloon the build and add a stack that
  none of the runtime code needs.
- This is a genuine neural network - an embedding layer, an LSTM
  recurrence, a softmax output head - trained with real
  backpropagation-through-time and gradient clipping. Compact,
  inspectable, CPU-only, and easy to reason about line by line.
- It matches the project's existing "no GPU, no huge weights" philosophy
  (see 20_language_models.py Section 14B docstring).

The trained model (weights + vocab) is saved into model_cache/ where the
runtime StoryLanguageModel (35_story_nn.py) picks it up automatically;
when no trained model exists, the chatbot's story generation falls back
to its existing hand-written story banks unchanged. Running this script
is purely additive.

Usage:
    python train_story_nn.py                  # full run: all books
    python train_story_nn.py --max-books 3    # quick smoke test on 3 books
    python train_story_nn.py --epochs 12 --hidden 128
"""

import argparse
import html
import json
import os
import random
import re
import sys
import urllib.request

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BOOKS_CSV = os.path.join(HERE, "data", "gutenberg_books.csv")
DEFAULT_CORPUS_DIR = os.path.join(HERE, "story_corpus")
DEFAULT_OUT_WEIGHTS = os.path.join(HERE, "model_cache", "story_nn.npz")
DEFAULT_OUT_VOCAB = os.path.join(HERE, "model_cache", "story_nn_vocab.json")

# Special tokens. Kept identical to the runtime vocab in 35_story_nn.py
# so a saved model loads into the chatbot with no re-tokenizing surprises.
PAD = "<pad>"
UNK = "<unk>"
BOS = "<bos>"
EOS = "<eos>"
SPECIAL = (PAD, UNK, BOS, EOS)

# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

# A pragmatic English word tokenizer: letters (incl. common accented
# latin from loanwords) plus digits, with punctuation kept as its own
# tokens so the LSTM learns where sentences end.
_TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ']+|[0-9]+|[.,!?;:\"'()\[\]\-]+")


def tokenize(text):
    """Lowercased tokens incl. punctuation. Identical to the runtime
    tokenizer in 35_story_nn.py so save/load round-trips cleanly."""
    return _TOKEN_RE.findall(text.lower())


def sentences_from_text(text, max_tokens=120):
    """Returns a list of token-lists, one per sentence of the cleaned
    prose, dropping anything too short (chapter headings, page numbers)
    or too long to be a useful training window."""
    sentences = []
    for para in re.split(r"\n\s*\n", text):
        for raw in re.split(r"(?<=[.!?])\s+", para.strip()):
            toks = tokenize(raw)
            if 4 <= len(toks) <= max_tokens:
                sentences.append(toks)
    return sentences


# ---------------------------------------------------------------------------
# Gutenberg download + boilerplate stripping
# ---------------------------------------------------------------------------

_START_RE = re.compile(
    r"\*{3}\s*START OF (?:THIS|THE) PROJECT GUTENBERG EBOOK.*?\*{3}", re.IGNORECASE
)
_END_RE = re.compile(
    r"\*{3}\s*END OF (?:THIS|THE) PROJECT GUTENBERG EBOOK.*?\*{3}", re.IGNORECASE
)


def html_unescape_safe(text):
    try:
        return html.unescape(text)
    except Exception:
        return text


def strip_gutenberg_boilerplate(text):
    """Returns only the actual story body.

    Some volumes contain several texts, each with its own START/END
    marker pair. We keep everything from the LAST START to the FIRST END
    so the true book body survives intact and trailers disappear."""
    starts = [m.end() for m in _START_RE.finditer(text)]
    ends = [m.start() for m in _END_RE.finditer(text)]
    body_start = starts[-1] if starts else 0
    body_end = ends[0] if ends else len(text)
    body = text[body_start:body_end]

    # Blank lines delimit paragraphs; hard-wrapped single lines inside a
    # paragraph are re-joined so prose flows like real sentences.
    paragraphs = []
    for raw_para in re.split(r"\n\s*\n", body):
        lines = [ln.strip() for ln in raw_para.splitlines() if ln.strip()]
        if lines:
            paragraphs.append(" ".join(lines))
    return "\n\n".join(html_unescape_safe(p) for p in paragraphs)


def download_book(bookno, out_dir):
    """Downloads pg{bookno}.txt to out_dir; returns path or None. Keeps
    going on failure rather than aborting the whole run."""
    out_path = os.path.join(out_dir, f"pg{bookno}.txt")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        return out_path
    os.makedirs(out_dir, exist_ok=True)
    url = f"https://www.gutenberg.org/cache/epub/{bookno}/pg{bookno}.txt"
    request = urllib.request.Request(url, headers={"User-Agent": "pychat-story-trainer/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as resp:
            content = resp.read()
        if len(content) < 1000:
            return None  # stub/404 page is not a book
        with open(out_path, "wb") as f:
            f.write(content)
        return out_path
    except Exception:
        return None


def build_corpus(books_csv, corpus_dir, max_books=None, max_sentences=None, seed=42):
    """Reads the catalog, downloads each book, strips boilerplate, and
    returns the flattened list of sentence token-lists. Unavailable
    books are skipped with a stderr note.

    max_sentences caps the total number of training sentences with a
    deterministic, FAIR share to every book (evenly-spaced picks, seeded),
    so a run with several hundred per book still learns all of Gutenberg
    in reasonable wall-clock time from pure numpy."""
    with open(books_csv, encoding="utf-8") as f:
        rows = [ln.strip() for ln in f if ln.strip() and not ln.startswith("bookno")]
    if max_books:
        rows = rows[:max_books]

    per_book = []
    for row in rows:
        parts = [p.strip().strip('"') for p in row.split(",")]
        if not parts or not parts[0]:
            continue
        bookno = parts[0]
        path = download_book(bookno, corpus_dir)
        if not path:
            print(f"  [skip] book {bookno} unavailable", file=sys.stderr)
            continue
        with open(path, encoding="utf-8", errors="replace") as f:
            raw = f.read()
        cleaned = strip_gutenberg_boilerplate(raw)
        per_book.append(sentences_from_text(cleaned))
        print(f"  [ok]   book {bookno}: {sum(len(b) for b in per_book):>6} sentences so far")

    rng = random.Random(seed)
    sentences = []
    if max_sentences is not None and max_sentences > 0:
        # Give every book an equal share of the budget, then spread the
        # picks evenly through that book's prose (start/middle/end all
        # represented) instead of just taking the first N.
        share_positions = []
        remaining = max_sentences
        for toks_list in per_book:
            share = max(1, remaining // max(len(per_book), 1))
            remaining = max(0, remaining - share)
            step = max(1.0, len(toks_list) / share)
            picks = []
            j = 0.0
            while len(picks) < share and int(j) < len(toks_list):
                picks.append(toks_list[int(j)])
                j += step
            share_positions.extend(picks)
        rng.shuffle(share_positions)
        sentences = share_positions
        print(f"  [fair-sample] {len(sentences)} sentences across {len(per_book)} books "
              f"(budget {max_sentences})", file=sys.stderr)
    else:
        for toks_list in per_book:
            sentences.extend(toks_list)
        rng.shuffle(sentences)
    return sentences


# ---------------------------------------------------------------------------
# Vocab
# ---------------------------------------------------------------------------

def build_vocab(sentences, max_vocab=8000):
    """Most-frequent words after the four special tokens."""
    counts = {}
    for toks in sentences:
        for t in toks:
            counts[t] = counts.get(t, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    vocab = list(SPECIAL) + [w for w, _ in ranked[: max_vocab - len(SPECIAL)]]
    return {w: i for i, w in enumerate(vocab)}


def encode(tokens, word2id):
    unk = word2id[UNK]
    return [word2id.get(t, unk) for t in tokens]


# ---------------------------------------------------------------------------
# The neural model: a small LSTM in plain NumPy
# ---------------------------------------------------------------------------

def init_params(embed_dim, hidden_dim, vocab_size, seed=42):
    import numpy as np
    rng = np.random.default_rng(seed)
    g4 = 4 * hidden_dim
    # float32 throughout: pure-numpy training is memory-bandwidth bound,
    # and the LSTM math has no precision needs beyond fp32.
    return {
        "W_emb": rng.normal(0, embed_dim ** -0.5, (vocab_size, embed_dim)).astype("float32"),
        "W_x": rng.normal(0, embed_dim ** -0.5, (g4, embed_dim)).astype("float32"),
        "W_h": rng.normal(0, hidden_dim ** -0.5, (g4, hidden_dim)).astype("float32"),
        "b": np.zeros((g4,), dtype="float32"),
        "W_hy": rng.normal(0, hidden_dim ** -0.5, (vocab_size, hidden_dim)).astype("float32"),
        "b_y": np.zeros((vocab_size,), dtype="float32"),
    }


def sigmoid(z):
    import numpy as np
    return 1.0 / (1.0 + np.exp(-z))


def softmax(z):
    import numpy as np
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def _gate_split(gates, size):
    """Splits concatenated (B,4H) pre-activations into i,f,g,o blocks."""
    return (gates[:, :size], gates[:, size:2 * size],
            gates[:, 2 * size:3 * size], gates[:, 3 * size:])


def lstm_step(x_b, h_prev, c_prev, params):
    """One LSTM timestep on a batch. Returns (h, c, cache) where cache
    holds everything backprop needs."""
    import numpy as np
    H = params["W_h"].shape[1]
    gates = x_b @ params["W_x"].T + h_prev @ params["W_h"].T + params["b"]
    i, f, g, o = _gate_split(gates, H)
    i, f, g, o = sigmoid(i), sigmoid(f), np.tanh(g), sigmoid(o)
    c = f * c_prev + i * g
    h = o * np.tanh(c)
    cache = (x_b, h_prev, c_prev, i, f, g, o, c)
    return h, c, cache


def forward(x_emb, params, h0=None, c0=None):
    """x_emb: (B, T, D). Returns the stack of hidden states (T, B, H)
    along with the per-step caches for backprop."""
    import numpy as np
    B, T, D = x_emb.shape
    H = params["W_h"].shape[1]
    h = h0 if h0 is not None else np.zeros((B, H))
    c = c0 if c0 is not None else np.zeros((B, H))
    hs = np.empty((T, B, H))
    caches = []
    for t in range(T):
        h, c, cache = lstm_step(x_emb[:, t], h, c, params)
        hs[t] = h
        caches.append(cache)
    return hs, caches


def backprop(x_emb, hs, caches, d_logits, params, x_ids):
    """Standard truncated BPTT. d_logits: (T, B, V) gradient at each
    timestep's output logits; x_ids: (B, T) the input token indices used
    to scatter the embedding gradient. Returns accumulated gradients.

    All the matrix products stay at per-timestep size (cache-friendly,
    and this is the dominant cost at full Gutenberg-corpus scale), but
    the per-position embedding gradients are buffered and flattened so a
    single np.add.at does the scatter instead of B*T tiny calls."""
    import numpy as np
    B, T, D = x_emb.shape
    H = params["W_h"].shape[1]

    grads = {k: np.zeros_like(v) for k, v in params.items()}
    dh_next = np.zeros((B, H))
    dc_next = np.zeros((B, H))
    d_emb_all = np.empty((T, B, D), dtype=x_emb.dtype)

    for t in reversed(range(T)):
        # d_logits[t] is (B, V); dW_hy += d_logits^T @ hs[t]
        grads["W_hy"] += d_logits[t].T @ hs[t]              # (V,H)
        grads["b_y"] += d_logits[t].sum(axis=0)             # (V,)
        dh = d_logits[t] @ params["W_hy"] + dh_next          # (B,H)

        x_b, h_prev, c_prev, i, f, g, o, c = caches[t]
        dhc = dh * o * (1.0 - np.tanh(c) ** 2) + dc_next    # gradient of c_t

        dg = dhc * i * (1.0 - g ** 2)                        # candidate grad
        di = dhc * g * i * (1.0 - i)
        df = dhc * c_prev * f * (1.0 - f)
        do = dh * np.tanh(c) * o * (1.0 - o)

        gates_grad = np.concatenate((di, df, dg, do), axis=1)  # (B,4H)
        grads["W_x"] += gates_grad.T @ x_b                   # (4H,D)
        grads["W_h"] += gates_grad.T @ h_prev                # (4H,H)
        grads["b"] += gates_grad.sum(axis=0)                 # (4H,)
        d_emb_all[t] = gates_grad @ params["W_x"]            # (B,D)

        dh_next = gates_grad @ params["W_h"]
        dc_next = dhc * f

    np.add.at(grads["W_emb"], x_ids.ravel(), d_emb_all.reshape(T * B, -1))
    return grads


def train(sentences, word2id, params, epochs=20, seq_len=32, batch_size=32,
          lr=0.01, seed=1337, progress=True):
    """Truncated BPTT minibatch training of the LSTM. Returns the list
    of per-epoch mean cross-entropy values."""
    import numpy as np
    V = len(word2id)
    D = params["W_emb"].shape[1]
    H = params["W_h"].shape[1]
    pad_id = word2id[PAD]

    # Flatten the corpus into a stream of ids, BOS/EOS wrapped per
    # sentence, so windows can span soft boundaries naturally.
    stream = []
    for toks in sentences:
        ids = encode(toks, word2id)
        if len(ids) >= 3:
            stream.extend([word2id[BOS]] + ids + [word2id[EOS]])
    if len(stream) < seq_len * 10:
        raise ValueError("corpus too small to train on")

    rng = np.random.default_rng(seed)
    S = len(stream)
    window = seq_len + 1  # input window + the target token shifted by one

    def make_batch():
        starts = rng.integers(0, max(1, S - window), size=batch_size)
        xs = np.stack([stream[s:s + window - 1] for s in starts])
        ys = np.stack([stream[s + 1:s + window] for s in starts])
        return xs, ys

    def logit_loss(hs, ys):
        # hs: (T, B, H), ys: (B, T) - mean cross-entropy per predicted token.
        # Fully vectorized (no per-timestep Python loop): the vocab softmax
        # is computed once over the whole window, which is ~10x faster than
        # the naive loop and is the dominant cost per training step.
        logits = hs @ params["W_hy"].T + params["b_y"]  # (T,B,V)
        probs = softmax(logits)
        # Masks are (T,B): probs[t,b,ys[b,t]] is the predicted prob of the
        # true next token at each position.
        T = hs.shape[0]
        idx = ys.T  # (T,B) - ys[b,t] -> idx[t,b]
        gathers = probs[np.arange(T)[:, None], np.arange(idx.shape[1])[None, :], idx]
        ce_t = -np.log(np.clip(gathers, 1e-9, 1.0))  # (T,B)
        d = probs.copy()
        d[np.arange(T)[:, None], np.arange(idx.shape[1])[None, :], idx] -= 1.0
        d /= float(idx.shape[1])  # scale by B to match the mean
        return float(ce_t.mean()), d, logits

    losses = []
    steps_per_epoch = max(1, S // (window * batch_size))
    for epoch in range(epochs):
        total = 0.0
        done = 0
        for _ in range(min(steps_per_epoch, 2000)):
            xs, ys = make_batch()
            # embed
            x_emb = params["W_emb"][xs]  # (B,T,D)
            hs, caches = forward(x_emb, params)
            loss, d_logits, _ = logit_loss(hs, ys)

            grads = backprop(x_emb, hs, caches, d_logits, params, xs)
            # Standard global-norm gradient clipping (clip to 5.0) so a
            # single bad batch can't destabilize the recurrence.
            norm = 0.0
            for k in ("W_emb", "W_x", "W_h", "b", "W_hy", "b_y"):
                norm += float((grads[k] ** 2).sum())
            norm = norm ** 0.5
            scale = min(1.0, 5.0 / norm) if norm > 0 else 1.0
            for k in ("W_emb", "W_x", "W_h", "b", "W_hy", "b_y"):
                params[k] -= lr * grads[k] * scale
            total += float(loss)
            done += 1
        mean = total / max(done, 1)
        losses.append(mean)
        if progress:
            print(f"  epoch {epoch + 1}/{epochs}: mean loss = {mean:.4f}")
    return losses


def generate(params, word2id, seed_text="", max_words=40, temperature=0.9):
    """Greedy/tempered sampling from the trained LSTM."""
    import numpy as np
    D = params["W_emb"].shape[1]
    toks = tokenize(seed_text) if seed_text else []
    ids = [word2id[BOS]] + encode(toks, word2id)
    h = np.zeros((1, params["W_h"].shape[1]))
    c = np.zeros_like(h)

    for idx in ids:
        x_emb = params["W_emb"][np.array([idx])]
        h, c, _ = lstm_step(x_emb, h, c, params)

    out = list(toks)
    for _ in range(max_words):
        x_emb = params["W_emb"][np.array([ids[-1]])]
        h, c, _ = lstm_step(x_emb, h, c, params)
        logits = h @ params["W_hy"].T + params["b_y"]
        logits = logits[0] / max(temperature, 1e-3)
        probs = softmax(logits)
        # exclude specials
        for sp in (PAD, UNK, BOS, EOS):
            probs[word2id[sp]] = 0.0
        if probs.sum() > 0:
            probs /= probs.sum()
        nxt = int(np.random.choice(len(probs), 1, p=probs)[0])
        word = _id_to_word(nxt, word2id)
        if word == EOS:
            break
        out.append(word)
        ids.append(nxt)
    return detokenize(out)


def _id_to_word(i, word2id):
    for w, v in word2id.items():
        if v == i:
            return w
    return UNK


def detokenize(tokens):
    """Joins tokens into readable text: no spaces before punctuation."""
    text = ""
    for tok in tokens:
        if re.fullmatch(r"[.,!?;:\"'()\[\]\-]+", tok):
            text = text.rstrip() + tok
        elif text:
            text += " " + tok
        else:
            text = tok
    return text[0].upper() + text[1:] if text else text


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def save_model(params, word2id, weights_path, vocab_path):
    import numpy as np
    os.makedirs(os.path.dirname(weights_path), exist_ok=True)
    np.savez(weights_path, **params)
    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump(word2id, f, ensure_ascii=False)
    print(f"  saved weights -> {weights_path}")
    print(f"  saved vocab   -> {vocab_path}")


# ---------------------------------------------------------------------------
# Torch backend
# ---------------------------------------------------------------------------

def train_torch(sentences, word2id, hidden=128, embed=64, seq_len=32,
                batch_size=96, epochs=10, lr=0.002, seed=1337, progress=True):
    """Trains the same LSTM architecture with PyTorch (fast, BLAS-backed)
    on the FULL corpus, then exports the weights back into the identical
    npz schema the numpy runtime (35_story_nn.py) loads - the saved model
    is torch-agnostic, so the deployed chatbot never needs torch at all.

    Gate layout is deliberately kept identical to the numpy LSTM above:
    torch's (i, f, g, o) ordering equals _gate_split's output, so a
    torch-fit model drops straight into the numpy forward pass."""
    import numpy as np
    import torch
    import torch.nn as nn

    torch.manual_seed(seed)

    V = len(word2id)

    class StoryLSTM(nn.Module):
        def __init__(self):
            super().__init__()
            self.embed = nn.Embedding(V, embed, padding_idx=None)
            self.lstm = nn.LSTM(embed, hidden, batch_first=True)
            self.head = nn.Linear(hidden, V)

        def forward(self, xs):
            h = self.embed(xs)            # (B,T,D)
            h, _ = self.lstm(h)           # (B,T,H)
            return self.head(h)           # (B,T,V)

    model = StoryLSTM()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    crit = nn.CrossEntropyLoss()

    # Flatten the corpus into a stream of ids, per-sentence BOS/EOS wrap.
    stream = []
    for toks in sentences:
        ids = encode(toks, word2id)
        if len(ids) >= 3:
            stream.extend([word2id[BOS]] + ids + [word2id[EOS]])
    if len(stream) < seq_len * 10:
        raise ValueError("corpus too small to train on")

    # Sample overlapping random windows per step (exactly like the numpy
    # backend): each step picks batch_size random window starts, so the
    # epoch has many more gradient updates than the non-overlapping
    # scheme previously used (~76/epoch), which was far too few updates
    # to learn coherent prose.
    rng = np.random.default_rng(seed)
    S = len(stream)
    window = seq_len + 1                       # input window + target shift
    steps_per_epoch = max(1, S // (window * batch_size))
    max_start = S - window

    def batch_at(starts):
        xs = np.stack([stream[s:s + seq_len] for s in starts])
        ys = np.stack([stream[s + 1:s + seq_len + 1] for s in starts])
        return (torch.tensor(xs, dtype=torch.long),
                torch.tensor(ys, dtype=torch.long))

    losses = []
    for epoch in range(epochs):
        total, done = 0.0, 0
        for _ in range(min(steps_per_epoch, 2000)):
            starts = rng.integers(0, max_start, size=batch_size)
            xs, ys = batch_at(starts)
            opt.zero_grad()
            logits = model(xs)                       # (B,T,V)
            loss = crit(logits.reshape(-1, V), ys.reshape(-1))
            loss.backward()
            # Gradient clipping keeps the recurrence stable early on.
            nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            opt.step()
            total += float(loss.detach())
            done += 1
        losses.append(total / max(done, 1))
        if progress:
            print(f"  epoch {epoch + 1}/{epochs}: mean loss = {losses[-1]:.4f}")
    del crit

    # Export to the same npz schema as init_params/backprop uses:
    #   W_emb (V,D), W_x (4H,D), W_h (4H,H), b (4H,),
    #   W_hy (V,H), b_y (V,).
    # torch LSTM weights are (4H, D); state dict names weight_ih_l0 etc.
    params = {
        "W_emb": model.embed.weight.detach().cpu().numpy().astype("float32"),
        "W_x": model.lstm.weight_ih_l0.detach().cpu().numpy().astype("float32"),
        "W_h": model.lstm.weight_hh_l0.detach().cpu().numpy().astype("float32"),
        "b": (model.lstm.bias_ih_l0 + model.lstm.bias_hh_l0).detach().cpu().numpy().astype("float32"),
        "W_hy": model.head.weight.detach().cpu().numpy().astype("float32"),
        "b_y": model.head.bias.detach().cpu().numpy().astype("float32"),
    }
    return losses, params


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Train the Gutenberg story NN.")
    ap.add_argument("--books", default=DEFAULT_BOOKS_CSV)
    ap.add_argument("--corpus-dir", default=DEFAULT_CORPUS_DIR)
    ap.add_argument("--out-weights", default=DEFAULT_OUT_WEIGHTS)
    ap.add_argument("--out-vocab", default=DEFAULT_OUT_VOCAB)
    ap.add_argument("--max-books", type=int, default=None)
    ap.add_argument("--max-sentences", type=int, default=None,
                    help="fair per-corpus sentence budget (default None = use the FULL corpus)")
    ap.add_argument("--backend", choices=("torch", "numpy"), default="torch",
                    help="training engine: torch needs PyTorch installed, numpy is the "
                         "portable fallback (slower, used automatically if torch is missing)")
    ap.add_argument("--epochs", type=int, default=12)
    ap.add_argument("--hidden", type=int, default=128)
    ap.add_argument("--embed", type=int, default=64)
    ap.add_argument("--seq-len", type=int, default=32)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--max-vocab", type=int, default=8000)
    ap.add_argument("--samples", type=int, default=3,
                    help="print this many NN-generated openings after training")
    args = ap.parse_args()

    try:
        import numpy as np
    except ImportError:
        print("numpy is required to train the story NN.", file=sys.stderr)
        return 1

    if args.backend == "torch":
        try:
            import torch
        except ImportError:
            print("torch not available - falling back to the numpy backend.",
                  file=sys.stderr)
            args.backend = "numpy"

    print("Step 1/3: download + clean the catalog books")
    sentences = build_corpus(args.books, args.corpus_dir, max_books=args.max_books,
                             max_sentences=args.max_sentences)
    if len(sentences) < 500:
        print(f"  only {len(sentences)} sentences - too little to train on.", file=sys.stderr)
        return 1
    print(f"  corpus: {len(sentences)} sentences (backend={args.backend})")

    print("Step 2/3: build vocab + init LSTM")
    word2id = build_vocab(sentences, max_vocab=args.max_vocab)
    print(f"  vocab: {len(word2id)} word types")

    print("Step 3/3: train")
    if args.backend == "torch":
        losses, params = train_torch(
            sentences, word2id,
            hidden=args.hidden, embed=args.embed, seq_len=args.seq_len,
            batch_size=args.batch_size, epochs=args.epochs, lr=0.002)
    else:
        params = init_params(args.embed, args.hidden, len(word2id), seed=42)
        losses = train(sentences, word2id, params,
                       epochs=args.epochs, seq_len=args.seq_len,
                       batch_size=args.batch_size, lr=0.01)
    print(f"  final loss: {losses[-1]:.4f}")

    if args.samples:
        print("\nSample continuations from the trained NN:")
        for seedi in ("once upon a time", "the old house stood", "there was a strange"):
            print(f"  > '{seedi}':")
            print("    " + generate(params, word2id, seed_text=seedi,
                                    max_words=12, temperature=0.9))
    print()

    save_model(params, word2id, args.out_weights, args.out_vocab)
    print("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())