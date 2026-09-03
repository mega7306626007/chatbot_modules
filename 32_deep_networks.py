"""Section 6H4: FIVE MORE TRAINED NETWORKS (urgency, politeness, question-type,
text-complexity regression, emoji prediction) - deep dense architectures,
bringing this file's total to 10 genuinely distinct trained models.
"""
import random

# ==============================================================================
# SECTION 6H4: FIVE ADDITIONAL DEEP NETWORKS
# ==============================================================================
#
# The five networks above this file (NeuralIntentClassifier,
# SentimentClassifier, SmartSuggestionEngine, MoodTrendForecaster,
# SemanticMemoryIndex) each solve a genuinely different problem. These
# five continue that pattern rather than just being five copies of the
# same classifier with different label names:
#
#   6. UrgencyClassifier          - how time-sensitive is this message?
#   7. PolitenessClassifier       - how is it being asked (register)?
#   8. QuestionTypeClassifier     - what KIND of question is this
#                                    (yes/no vs what/why/how/...)?
#   9. TextComplexityRegressor    - a REGRESSION network (continuous
#                                    0-1 output), not a classifier at
#                                    all - genuinely different training
#                                    objective (MSE, not cross-entropy).
#  10. EmojiPredictor             - which single emoji best matches the
#                                    emotional content of this text?
#
# All five share one deep, dense architecture family (_DeepDenseHead
# below - mean-pooled word embeddings through FIVE stacked Linear+
# BatchNorm+GELU+Dropout layers) rather than the dual word+char-branch
# design used by NeuralIntentClassifier/SentimentClassifier - that
# design was earned by those two networks' much larger datasets
# (~1,100 and ~155 examples); these five are newer, smaller-data tasks
# (40-70 examples each), where the simpler single-branch design is the
# more honest choice - the same "don't add complexity the data can't
# support" principle already documented on the sklearn side elsewhere
# in this file, just applied to which architecture to reach for. Each
# still falls back to a real sklearn MLP (MLPClassifier/MLPRegressor)
# if torch isn't installed, so every feature works either way.


def _mean_pool_numpy_free(token_ids_batch, vocab_size, embed_dim, embedding_weight):
    """Not used directly - see the torch _DeepDenseHead classes below.
    Placeholder kept out of the hot path; real pooling happens inside
    each nn.Module's forward() via the same masked-mean-pool pattern
    used by every other network in this file."""
    raise NotImplementedError


class _DeepDenseTextClassifier:
    """
    Shared scaffolding for the four CLASSIFICATION networks in this
    section (urgency/politeness/question-type/emoji) - word-level
    mean-pooled embeddings through a deep 5-layer dense stack, softmax
    head. Deliberately simpler than _BaseNeuralClassifier (Section 6G):
    no user-correction/online-retraining machinery, since these five
    networks are fit once from a fixed dataset and aren't wired into
    the "no, i meant..." correction flow the way intent/sentiment are.
    """

    EMBED_DIM = 32
    HIDDEN_DIMS = (64, 64, 48, 32, 16)  # 5 hidden layers - "many and dense", narrowed
    # from an initial (128,128,96,64,32) after measurement showed that
    # width (not depth) was overfitting these ~40-70-example datasets -
    # 5 layers stayed, per an explicit request for depth, but each
    # layer has fewer units so there are fewer parameters overall.
    MAX_EPOCHS = 120
    EARLY_STOP_PATIENCE = 15
    VAL_FRACTION = 0.2

    def __init__(self, examples):
        self.examples = list(examples)
        self.backend = "torch" if TORCH_AVAILABLE else "sklearn"
        self.vocab = None
        self.vectorizer = None
        self.label_list = []
        self.label_to_idx = {}
        self.model = None
        self.last_val_accuracy = None
        self.last_training_info = None
        self._fit()

    def _split(self, X, y):
        try:
            return train_test_split(X, y, test_size=self.VAL_FRACTION, random_state=42, stratify=y)
        except ValueError:
            # A label with only 1 example can't be stratified - fall
            # back to a plain (non-stratified) split rather than crash.
            return train_test_split(X, y, test_size=self.VAL_FRACTION, random_state=42)

    def _fit(self):
        texts = [t for t, _l in self.examples]
        labels = [l for _t, l in self.examples]
        self.label_list = sorted(set(labels))
        self.label_to_idx = {l: i for i, l in enumerate(self.label_list)}

        if self.backend == "torch":
            self._fit_torch(texts, labels)
        else:
            self._fit_sklearn(texts, labels)

    def _build_torch_model(self, vocab_size, num_classes):
        embed_dim = self.EMBED_DIM
        hidden_dims = self.HIDDEN_DIMS

        class _DeepDenseNet(nn.Module):
            """Mean-pooled word embeddings -> 5 stacked Linear+
            BatchNorm1d+GELU+Dropout layers -> Linear head. Every
            hidden layer is followed by normalization and dropout so
            the extra depth is regularized, the same lesson
            NeuralIntentClassifier's _ResidualBlock design already
            demonstrated (though this one uses plain stacking rather
            than skip connections, since a 5-layer plain stack is
            still well within what these dataset sizes can support -
            skip connections start earning their complexity cost at
            greater depths than five layers)."""

            def __init__(self):
                super().__init__()
                self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
                layers = []
                prev_dim = embed_dim
                for h in hidden_dims:
                    layers.append(nn.Linear(prev_dim, h))
                    layers.append(nn.BatchNorm1d(h))
                    layers.append(nn.GELU())
                    layers.append(nn.Dropout(0.3))
                    prev_dim = h
                self.stack = nn.Sequential(*layers)
                self.head = nn.Linear(prev_dim, num_classes)

            @staticmethod
            def _mean_pool(embedded, token_ids):
                mask = (token_ids != 0).unsqueeze(-1).float()
                summed = (embedded * mask).sum(dim=1)
                counts = mask.sum(dim=1).clamp(min=1.0)
                return summed / counts

            def forward(self, token_ids):
                pooled = self._mean_pool(self.embedding(token_ids), token_ids)
                h = self.stack(pooled)
                return self.head(h)

        torch.manual_seed(42)
        return _DeepDenseNet()

    def _fit_torch(self, texts, labels):
        self.vocab = _TextVocab(texts, max_len=16)
        y = [self.label_to_idx[l] for l in labels]
        X_ids = [self.vocab.encode(t) for t in texts]

        X_train, X_val, y_train, y_val = self._split(X_ids, y)
        model = self._build_torch_model(len(self.vocab), len(self.label_list))
        optimizer = torch.optim.Adam(model.parameters(), lr=0.005, weight_decay=1e-4)
        criterion = nn.CrossEntropyLoss()

        X_train_t = torch.tensor(X_train, dtype=torch.long)
        y_train_t = torch.tensor(y_train, dtype=torch.long)
        X_val_t = torch.tensor(X_val, dtype=torch.long)
        y_val_t = torch.tensor(y_val, dtype=torch.long)

        best_val_acc, best_state, patience_left = -1.0, None, self.EARLY_STOP_PATIENCE
        for epoch in range(self.MAX_EPOCHS):
            model.train()
            optimizer.zero_grad()
            logits = model(X_train_t)
            loss = criterion(logits, y_train_t)
            loss.backward()
            optimizer.step()

            model.eval()
            with torch.no_grad():
                val_logits = model(X_val_t)
                val_preds = val_logits.argmax(dim=1)
                val_acc = (val_preds == y_val_t).float().mean().item()

            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_state = {k: v.clone() for k, v in model.state_dict().items()}
                patience_left = self.EARLY_STOP_PATIENCE
            else:
                patience_left -= 1
                if patience_left <= 0:
                    break

        if best_state is not None:
            model.load_state_dict(best_state)
        model.eval()
        self.model = model
        self.last_val_accuracy = best_val_acc
        self.last_training_info = {
            "backend": "torch", "architecture": f"embedding -> {len(self.HIDDEN_DIMS)} dense layers -> softmax",
            "val_accuracy": round(best_val_acc, 3), "train_examples": len(X_train), "val_examples": len(X_val),
        }

    def _fit_sklearn(self, texts, labels):
        cache_key = model_cache_key(
            type(self).__name__ + "_sklearn_v1", texts, labels, self.HIDDEN_DIMS,
        )
        cached = load_cached_model(cache_key)
        if cached is not None:
            self.vectorizer = cached["vectorizer"]
            self.model = cached["model"]
            self.last_val_accuracy = cached["last_val_accuracy"]
            self.last_training_info = cached["last_training_info"]
            return

        # min_df=2 + max_features=200 (rather than the unbounded
        # min_df=1 first used here): measured against these datasets,
        # unbounded TF-IDF gave ~620 features for ~100 examples - more
        # input dimensions than training rows, which was very likely
        # the dominant cause of the poor validation accuracy (worse
        # than the layer-width/depth choice). Dropping singleton terms
        # and capping vocabulary shrinks that to a far saner ratio.
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200)
        X = self.vectorizer.fit_transform(texts).toarray()
        y = [self.label_to_idx[l] for l in labels]

        X_train, X_val, y_train, y_val = self._split(X, y)
        # Same 5-layer depth as the torch side, translated to sklearn's
        # hidden_layer_sizes tuple - no skip connections available here,
        # so this is more overfitting-prone on small data (same caveat
        # documented for the intent/sentiment sklearn fallbacks).
        model = MLPClassifier(
            hidden_layer_sizes=self.HIDDEN_DIMS, activation="relu", alpha=0.03,
            max_iter=2000, random_state=42, early_stopping=False, n_iter_no_change=50,
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=ConvergenceWarning)
            model.fit(X_train, y_train)

        val_acc = accuracy_score(y_val, model.predict(X_val)) if len(y_val) else None
        self.model = model
        self.last_val_accuracy = val_acc
        self.last_training_info = {
            "backend": "sklearn", "architecture": f"TF-IDF -> MLPClassifier{self.HIDDEN_DIMS}",
            "val_accuracy": round(val_acc, 3) if val_acc is not None else None,
            "train_examples": len(X_train), "val_examples": len(X_val),
        }
        save_cached_model(cache_key, {
            "vectorizer": self.vectorizer, "model": self.model,
            "last_val_accuracy": self.last_val_accuracy, "last_training_info": self.last_training_info,
        })

    def predict(self, text: str):
        """Returns (label, confidence)."""
        if self.backend == "torch":
            ids = torch.tensor([self.vocab.encode(text)], dtype=torch.long)
            self.model.eval()
            with torch.no_grad():
                probs = torch.softmax(self.model(ids), dim=1)[0]
            idx = int(torch.argmax(probs))
            return self.label_list[idx], float(probs[idx])
        else:
            X = self.vectorizer.transform([text]).toarray()
            probs = self.model.predict_proba(X)[0]
            idx = int(np.argmax(probs))
            return self.label_list[idx], float(probs[idx])


class _DeepDenseTextRegressor:
    """
    Regression counterpart to _DeepDenseTextClassifier: same 5-layer
    deep dense stack over mean-pooled word embeddings, but a single
    linear (sigmoid-bounded) output unit trained with MSE loss instead
    of a softmax head trained with cross-entropy - a genuinely
    different training objective/task TYPE, not just a differently
    labeled classifier. Used by TextComplexityRegressor.
    """

    EMBED_DIM = 32
    HIDDEN_DIMS = (64, 64, 48, 32, 16)
    MAX_EPOCHS = 150
    EARLY_STOP_PATIENCE = 20
    VAL_FRACTION = 0.2

    def __init__(self, examples):
        self.examples = list(examples)  # (text, float_target_in_0_1)
        self.backend = "torch" if TORCH_AVAILABLE else "sklearn"
        self.vocab = None
        self.vectorizer = None
        self.model = None
        self.last_val_mae = None
        self.last_training_info = None
        self._fit()

    def _fit(self):
        texts = [t for t, _s in self.examples]
        scores = [s for _t, s in self.examples]
        if self.backend == "torch":
            self._fit_torch(texts, scores)
        else:
            self._fit_sklearn(texts, scores)

    def _build_torch_model(self, vocab_size):
        embed_dim, hidden_dims = self.EMBED_DIM, self.HIDDEN_DIMS

        class _DeepDenseRegressionNet(nn.Module):
            def __init__(self):
                super().__init__()
                self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
                layers = []
                prev_dim = embed_dim
                for h in hidden_dims:
                    layers.append(nn.Linear(prev_dim, h))
                    layers.append(nn.BatchNorm1d(h))
                    layers.append(nn.GELU())
                    layers.append(nn.Dropout(0.3))
                    prev_dim = h
                self.stack = nn.Sequential(*layers)
                self.head = nn.Linear(prev_dim, 1)

            @staticmethod
            def _mean_pool(embedded, token_ids):
                mask = (token_ids != 0).unsqueeze(-1).float()
                summed = (embedded * mask).sum(dim=1)
                counts = mask.sum(dim=1).clamp(min=1.0)
                return summed / counts

            def forward(self, token_ids):
                pooled = self._mean_pool(self.embedding(token_ids), token_ids)
                h = self.stack(pooled)
                return torch.sigmoid(self.head(h)).squeeze(-1)  # bounded to (0, 1)

        torch.manual_seed(42)
        return _DeepDenseRegressionNet()

    def _fit_torch(self, texts, scores):
        self.vocab = _TextVocab(texts, max_len=20)
        X_ids = [self.vocab.encode(t) for t in texts]
        X_train, X_val, y_train, y_val = train_test_split(
            X_ids, scores, test_size=self.VAL_FRACTION, random_state=42
        )

        model = self._build_torch_model(len(self.vocab))
        optimizer = torch.optim.Adam(model.parameters(), lr=0.005, weight_decay=1e-4)
        criterion = nn.MSELoss()

        X_train_t = torch.tensor(X_train, dtype=torch.long)
        y_train_t = torch.tensor(y_train, dtype=torch.float32)
        X_val_t = torch.tensor(X_val, dtype=torch.long)
        y_val_t = torch.tensor(y_val, dtype=torch.float32)

        best_val_mae, best_state, patience_left = float("inf"), None, self.EARLY_STOP_PATIENCE
        for epoch in range(self.MAX_EPOCHS):
            model.train()
            optimizer.zero_grad()
            preds = model(X_train_t)
            loss = criterion(preds, y_train_t)
            loss.backward()
            optimizer.step()

            model.eval()
            with torch.no_grad():
                val_preds = model(X_val_t)
                val_mae = (val_preds - y_val_t).abs().mean().item()

            if val_mae < best_val_mae:
                best_val_mae = val_mae
                best_state = {k: v.clone() for k, v in model.state_dict().items()}
                patience_left = self.EARLY_STOP_PATIENCE
            else:
                patience_left -= 1
                if patience_left <= 0:
                    break

        if best_state is not None:
            model.load_state_dict(best_state)
        model.eval()
        self.model = model
        self.last_val_mae = best_val_mae
        self.last_training_info = {
            "backend": "torch", "architecture": f"embedding -> {len(self.HIDDEN_DIMS)} dense layers -> sigmoid",
            "val_mae": round(best_val_mae, 4), "train_examples": len(X_train), "val_examples": len(X_val),
        }

    def _fit_sklearn(self, texts, scores):
        cache_key = model_cache_key(type(self).__name__ + "_sklearn_v1", texts, scores, self.HIDDEN_DIMS)
        cached = load_cached_model(cache_key)
        if cached is not None:
            self.vectorizer = cached["vectorizer"]
            self.model = cached["model"]
            self.last_val_mae = cached["last_val_mae"]
            self.last_training_info = cached["last_training_info"]
            return

        # Same dimensionality fix as _DeepDenseTextClassifier - see the
        # comment there.
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200)
        X = self.vectorizer.fit_transform(texts).toarray()
        X_train, X_val, y_train, y_val = train_test_split(X, scores, test_size=self.VAL_FRACTION, random_state=42)

        model = MLPRegressor(
            hidden_layer_sizes=self.HIDDEN_DIMS, activation="relu", alpha=0.03,
            max_iter=2000, random_state=42, early_stopping=False, n_iter_no_change=50,
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=ConvergenceWarning)
            model.fit(X_train, y_train)

        val_preds = np.clip(model.predict(X_val), 0.0, 1.0)
        val_mae = float(np.mean(np.abs(val_preds - np.array(y_val)))) if len(y_val) else None
        self.model = model
        self.last_val_mae = val_mae
        self.last_training_info = {
            "backend": "sklearn", "architecture": f"TF-IDF -> MLPRegressor{self.HIDDEN_DIMS}",
            "val_mae": round(val_mae, 4) if val_mae is not None else None,
            "train_examples": len(X_train), "val_examples": len(X_val),
        }
        save_cached_model(cache_key, {
            "vectorizer": self.vectorizer, "model": self.model,
            "last_val_mae": self.last_val_mae, "last_training_info": self.last_training_info,
        })

    def predict(self, text: str) -> float:
        if self.backend == "torch":
            ids = torch.tensor([self.vocab.encode(text)], dtype=torch.long)
            self.model.eval()
            with torch.no_grad():
                score = float(self.model(ids)[0])
            return max(0.0, min(1.0, score))
        else:
            X = self.vectorizer.transform([text]).toarray()
            return float(np.clip(self.model.predict(X)[0], 0.0, 1.0))


# ==============================================================================
# Network 6: URGENCY CLASSIFIER (low / medium / high)
# ==============================================================================
URGENCY_EXAMPLES = [
    ("call an ambulance right now", "high"),
    ("the building is on fire, get out", "high"),
    ("i need help immediately, this can't wait", "high"),
    ("this is a genuine emergency", "high"),
    ("please respond right away, it's extremely urgent", "high"),
    ("drop everything, we have a crisis on our hands", "high"),
    ("asap, the production server just went down", "high"),
    ("act now before it's too late", "high"),
    ("emergency, someone is missing", "high"),
    ("hurry, we're rapidly running out of time", "high"),
    ("this needs to happen this second, no delays", "high"),
    ("critical failure, everything is down right now", "high"),
    ("i'm panicking, please help me right now", "high"),
    ("the deadline is in ten minutes and nothing is ready", "high"),
    ("mayday, we need immediate assistance", "high"),
    ("can you get back to me sometime today", "medium"),
    ("i'd like this wrapped up by tomorrow", "medium"),
    ("this needs some attention pretty soon", "medium"),
    ("let's resolve this by the end of the week", "medium"),
    ("please follow up when you can, maybe this week", "medium"),
    ("it's not an emergency but it should be handled soon", "medium"),
    ("this is somewhat time sensitive", "medium"),
    ("i'd appreciate a reply in the next day or two", "medium"),
    ("we should probably sort this out before friday", "medium"),
    ("no huge rush, but don't let it sit too long", "medium"),
    ("this is a moderate priority item", "medium"),
    ("try to get to this within the next couple days", "medium"),
    ("whenever you get a chance is fine", "low"),
    ("no rush at all, take your time", "low"),
    ("this can wait as long as it needs to", "low"),
    ("just a casual question, absolutely no hurry", "low"),
    ("not time sensitive, just curious about it", "low"),
    ("someday it'd be nice to look into this", "low"),
    ("low priority, feel free to set it aside", "low"),
    ("purely for fun, no deadline whatsoever", "low"),
    ("whenever is convenient for you works", "low"),
    ("this has been sitting for months, no urgency", "low"),
]

URGENCY_EXAMPLES_EXTRA = [
    ("someone is having chest pains, call 911", "high"),
    ("we are flooding, need help this instant", "high"),
    ("the deadline is in five minutes", "high"),
    ("server outage affecting all customers right now", "high"),
    ("i smell gas, evacuate the building now", "high"),
    ("she's not breathing, send help immediately", "high"),
    ("the data breach is happening as we speak", "high"),
    ("time critical, the flight leaves in twenty minutes", "high"),
    ("respond this instant, lives are at stake", "high"),
    ("the dam is about to burst, act now", "high"),
    ("urgent, the payment failed and the client is furious", "high"),
    ("we need this fixed before the demo in ten minutes", "high"),
    ("please review this contract sometime this week", "medium"),
    ("get back to me within the next couple of days", "medium"),
    ("this should be handled before the sprint ends", "medium"),
    ("let's aim to finish this by wednesday", "medium"),
    ("i'd like an answer sometime soon, not urgent though", "medium"),
    ("this needs to be scheduled for later this month", "medium"),
    ("please look into this before our next meeting", "medium"),
    ("it would help to have this by end of week", "medium"),
    ("this is a fairly important task but not on fire", "medium"),
    ("try to squeeze this in sometime this sprint", "medium"),
    ("whenever works for you, honestly no timeline", "low"),
    ("this is just a nice-to-have, no pressure", "low"),
    ("feel free to get to it next month or so", "low"),
    ("purely optional, do it if you feel like it", "low"),
    ("i'm in no hurry whatsoever about this", "low"),
    ("this has been on the backlog forever, still fine", "low"),
    ("take all the time you need, genuinely", "low"),
    ("this is the lowest priority thing on my list", "low"),
    ("someday, maybe, no specific timeline at all", "low"),
    ("this can sit indefinitely, not a concern", "low"),
]
URGENCY_EXAMPLES.extend(URGENCY_EXAMPLES_EXTRA)

URGENCY_EXAMPLES_EXTRA_2 = [
    ("he collapsed, we need paramedics now", "high"),
    ("the store is being robbed right now", "high"),
    ("water is pouring through the ceiling as we speak", "high"),
    ("the client is threatening to cancel unless we respond this hour", "high"),
    ("i locked myself out and my baby is inside alone", "high"),
    ("the reactor temperature is spiking past safe limits", "high"),
    ("we lost contact with the climbing team, send rescue now", "high"),
    ("checkout is broken and we're losing sales every second", "high"),
    ("please reply before the board meeting starts in five minutes", "medium"),
    ("i'd like the draft back sometime tomorrow morning", "medium"),
    ("this needs sign-off before we can move to the next phase", "medium"),
    ("could you review this ahead of thursday's call", "medium"),
    ("we should settle on a vendor sometime this quarter", "medium"),
    ("please confirm your attendance by end of day", "medium"),
    ("this is worth addressing before it becomes a bigger issue", "medium"),
    ("i'd like your notes before we finalize things next week", "medium"),
    ("no timeline on this one, just brainstorming out loud", "low"),
    ("this is purely hypothetical for now", "low"),
    ("feel free to revisit this whenever it crosses your mind", "low"),
    ("i'm in absolutely no rush on this one", "low"),
    ("this has been on my someday list for a while", "low"),
    ("no deadline attached, just thought i'd mention it", "low"),
    ("whenever suits your schedule is totally fine", "low"),
    ("this is low stakes, don't stress about timing", "low"),
]
URGENCY_EXAMPLES.extend(URGENCY_EXAMPLES_EXTRA_2)

URGENCY_EXAMPLES_EXTRA_3 = [
    ("the surgeon needs the chart right this second", "high"),
    ("evacuate now, the alarm isn't a drill", "high"),
    ("we're losing the signal, respond immediately", "high"),
    ("send backup, the situation is escalating fast", "high"),
    ("the invoice is due today or we lose the discount", "medium"),
    ("let's wrap this up sometime before the quarter closes", "medium"),
    ("please weigh in before we lock the design", "medium"),
    ("aim to have feedback back within a few days", "medium"),
    ("this can wait until next season honestly", "low"),
    ("zero urgency, just an idle thought", "low"),
    ("read it whenever, no expectations", "low"),
    ("this has been fine sitting untouched for a year", "low"),
]
URGENCY_EXAMPLES.extend(URGENCY_EXAMPLES_EXTRA_3)

URGENCY_EXAMPLES_EXTRA_4 = [
    ("power just went out across the whole hospital wing", "high"),
    ("the brakes feel like they're failing right now", "high"),
    ("please advise before the wire transfer window closes in minutes", "high"),
    ("let's circle back on this sometime next sprint", "medium"),
    ("i'd like your sign-off before the end of the week", "medium"),
    ("this could use a fresh look sometime soon", "medium"),
    ("no timeline pressure, just something to think about eventually", "low"),
    ("this is purely for curiosity's sake, no rush", "low"),
]
URGENCY_EXAMPLES.extend(URGENCY_EXAMPLES_EXTRA_4)


class UrgencyClassifier(_DeepDenseTextClassifier):
    """How time-sensitive a message seems (low/medium/high) - could be
    used to prioritize to-do items or flag messages worth a faster
    reply, though it's currently exposed mainly via 'how urgent is
    this' for direct use."""

    def __init__(self):
        super().__init__(URGENCY_EXAMPLES)

    def format_predict(self, text: str) -> str:
        label, confidence = self.predict(text)
        return f"That reads as **{label}** urgency ({confidence:.0%} confidence)."


# ==============================================================================
# Network 7: POLITENESS CLASSIFIER (polite / neutral / rude)
# ==============================================================================
POLITENESS_EXAMPLES = [
    ("would you mind helping me with this, please", "polite"),
    ("i'd really appreciate your assistance if possible", "polite"),
    ("thank you so much for your time and patience", "polite"),
    ("excuse me, could you possibly help me out", "polite"),
    ("i'm sorry to bother you, but could i ask something", "polite"),
    ("please let me know whenever is convenient for you", "polite"),
    ("many thanks in advance for your help", "polite"),
    ("i hope this isn't too much trouble to ask", "polite"),
    ("would it be alright if i asked a favor", "polite"),
    ("i truly appreciate you taking the time", "polite"),
    ("if it's not too much bother, could you check this", "polite"),
    ("thanks a ton, you've been wonderfully helpful", "polite"),
    ("i'd be grateful for any guidance you can offer", "polite"),
    ("pardon the interruption, may i ask a quick question", "polite"),
    ("send me the file when you have a moment", "neutral"),
    ("what time is the meeting scheduled for", "neutral"),
    ("here's the report you asked about", "neutral"),
    ("i need the updated numbers", "neutral"),
    ("list the steps for this process", "neutral"),
    ("give me an update on the project", "neutral"),
    ("the document is attached below", "neutral"),
    ("confirm the appointment for tuesday", "neutral"),
    ("forward this message to the team", "neutral"),
    ("check the inventory count please", "neutral"),
    ("update the spreadsheet with today's totals", "neutral"),
    ("schedule the call for next week", "neutral"),
    ("just do it already, i don't have time for this", "rude"),
    ("why is this so slow, fix it right now", "rude"),
    ("stop wasting my time with excuses", "rude"),
    ("this is useless, do better next time", "rude"),
    ("quit stalling and just answer me", "rude"),
    ("you clearly have no idea what you're doing", "rude"),
    ("hurry up, i don't have all day for this", "rude"),
    ("this is a joke, get your act together", "rude"),
    ("i'm sick of your incompetence honestly", "rude"),
    ("just shut up and fix the problem", "rude"),
    ("are you even listening to me at all", "rude"),
    ("this is pathetic, try harder", "rude"),
]

POLITENESS_EXAMPLES_EXTRA = [
    ("i was wondering if you could possibly assist me", "polite"),
    ("it would mean a lot if you could take a look", "polite"),
    ("thank you kindly for considering my request", "polite"),
    ("i really don't want to impose, but could you help", "polite"),
    ("would you be so kind as to review this", "polite"),
    ("i sincerely appreciate whatever you can do", "polite"),
    ("no worries if you can't, but i'd love your input", "polite"),
    ("thank you ever so much for your patience", "polite"),
    ("i hope you're doing well, could i ask a small favor", "polite"),
    ("your help would be so appreciated, thank you", "polite"),
    ("if you have a spare moment, i'd value your thoughts", "polite"),
    ("i'm grateful for any time you can spare", "polite"),
    ("attach the invoice to the email", "neutral"),
    ("the numbers are in column c", "neutral"),
    ("move the call to three pm", "neutral"),
    ("upload the slides before the presentation", "neutral"),
    ("the password reset link expires in an hour", "neutral"),
    ("print two copies of the agreement", "neutral"),
    ("the shipment tracking number is below", "neutral"),
    ("set the thermostat to seventy degrees", "neutral"),
    ("the survey closes on friday", "neutral"),
    ("update the client's contact information", "neutral"),
    ("cut the nonsense and get this done", "rude"),
    ("i'm tired of your lame excuses", "rude"),
    ("you always mess everything up", "rude"),
    ("do i have to spell it out for you", "rude"),
    ("this is embarrassing, fix it now", "rude"),
    ("i don't care about your reasons, just fix it", "rude"),
    ("how hard can this possibly be for you", "rude"),
    ("you're useless at this, honestly", "rude"),
    ("enough talk, just get it done already", "rude"),
    ("i'm done waiting around for your excuses", "rude"),
]
POLITENESS_EXAMPLES.extend(POLITENESS_EXAMPLES_EXTRA)

POLITENESS_EXAMPLES_EXTRA_2 = [
    ("i'd be so thankful if you could spare a minute", "polite"),
    ("please don't go out of your way, but if you could", "polite"),
    ("it would be wonderful if you had time to help", "polite"),
    ("i really don't mean to impose on your schedule", "polite"),
    ("would you kindly let me know your thoughts", "polite"),
    ("i appreciate you more than you know for this", "polite"),
    ("thank you for even considering my request", "polite"),
    ("no pressure at all, just wondering if you're able to help", "polite"),
    ("i'm grateful for your patience with all my questions", "polite"),
    ("might i trouble you for a quick favor", "polite"),
    ("the invoice number is at the top of the page", "neutral"),
    ("submit the form before the end of business", "neutral"),
    ("the results are posted on the shared drive", "neutral"),
    ("check the calendar for open slots", "neutral"),
    ("the update rolls out next tuesday", "neutral"),
    ("bring your badge for building access", "neutral"),
    ("the training session runs for two hours", "neutral"),
    ("confirm receipt of this message", "neutral"),
    ("the vendor list is attached as a pdf", "neutral"),
    ("replace the batteries in the smoke detector", "neutral"),
    ("figure it out yourself, i'm not doing this for you", "rude"),
    ("you never listen, why do i even bother", "rude"),
    ("this is a total waste of my time", "rude"),
    ("i shouldn't have to explain this twice", "rude"),
    ("get it together already, seriously", "rude"),
    ("your work here is honestly subpar", "rude"),
    ("i don't want to hear another excuse", "rude"),
    ("this is ridiculous, just get on with it", "rude"),
    ("stop dragging your feet and finish it", "rude"),
    ("i'm done being patient with your mistakes", "rude"),
]
POLITENESS_EXAMPLES.extend(POLITENESS_EXAMPLES_EXTRA_2)

POLITENESS_EXAMPLES_EXTRA_3 = [
    ("i would be delighted if you had a moment to help", "polite"),
    ("thanks so much, i really owe you one", "polite"),
    ("whenever you have a chance, no pressure at all, thank you", "polite"),
    ("the shipment tracking updates every few hours", "neutral"),
    ("please label the boxes before the movers arrive", "neutral"),
    ("the survey results will be shared next week", "neutral"),
    ("i'm not asking again, just fix it", "rude"),
    ("save the excuses, i've heard them all", "rude"),
    ("act like you know what you're doing for once", "rude"),
]
POLITENESS_EXAMPLES.extend(POLITENESS_EXAMPLES_EXTRA_3)

POLITENESS_EXAMPLES_EXTRA_4 = [
    ("i'd be ever so grateful if you found the time", "polite"),
    ("please only if convenient, thank you kindly", "polite"),
    ("the badge readers are being serviced this week", "neutral"),
    ("submit expense reports by the fifth of the month", "neutral"),
    ("i'm not repeating myself again, sort it out", "rude"),
    ("this is beneath basic competence, honestly", "rude"),
]
POLITENESS_EXAMPLES.extend(POLITENESS_EXAMPLES_EXTRA_4)


class PolitenessClassifier(_DeepDenseTextClassifier):
    """How something is being asked (polite/neutral/rude) - distinct
    from SentimentClassifier's mood reading: a message can be negative
    in sentiment ('I'm having a rough day') while still being polite,
    or neutral in sentiment while being rude in register ('just do it
    already'). Register and mood are genuinely separate signals."""

    def __init__(self):
        super().__init__(POLITENESS_EXAMPLES)

    def format_predict(self, text: str) -> str:
        label, confidence = self.predict(text)
        return f"That reads as **{label}** in tone ({confidence:.0%} confidence)."


# ==============================================================================
# Network 8: QUESTION-TYPE CLASSIFIER
# (yes_no / what / why / how / who / when / where / other)
# ==============================================================================
QUESTION_TYPE_EXAMPLES = [
    ("is this correct", "yes_no"),
    ("did you finish the report", "yes_no"),
    ("can you help me with this", "yes_no"),
    ("will it rain tomorrow", "yes_no"),
    ("do you like coffee", "yes_no"),
    ("are we meeting today", "yes_no"),
    ("have you seen this movie", "yes_no"),
    ("is the store still open", "yes_no"),
    ("was the meeting rescheduled", "yes_no"),
    ("does this make sense to you", "yes_no"),
    ("what is the capital of france", "what"),
    ("what time is it right now", "what"),
    ("what should i cook tonight", "what"),
    ("what does this word actually mean", "what"),
    ("what's the plan for tomorrow", "what"),
    ("what happened at the meeting", "what"),
    ("what is your favorite book", "what"),
    ("why is the sky blue", "why"),
    ("why did you do that", "why"),
    ("why is the server down", "why"),
    ("why can't i log into my account", "why"),
    ("why does this keep happening", "why"),
    ("why would anyone choose that option", "why"),
    ("how do i reset my password", "how"),
    ("how does this feature work", "how"),
    ("how far is the airport from here", "how"),
    ("how many people showed up", "how"),
    ("how do you make this recipe", "how"),
    ("how did you fix that bug", "how"),
    ("who wrote this book", "who"),
    ("who is the current president", "who"),
    ("who called earlier today", "who"),
    ("who's coming to the party tonight", "who"),
    ("who's responsible for this decision", "who"),
    ("when does the store open", "when"),
    ("when is the project deadline", "when"),
    ("when did this whole thing start", "when"),
    ("when will you arrive at the office", "when"),
    ("when is the next holiday", "when"),
    ("where is the nearest train station", "where"),
    ("where did i leave my keys", "where"),
    ("where should we meet for lunch", "where"),
    ("where is the nearest exit", "where"),
    ("where do you live these days", "where"),
    ("close the door on your way out", "other"),
    ("that's absolutely amazing news", "other"),
    ("i really love this song", "other"),
    ("stop right there immediately", "other"),
    ("please send over the file", "other"),
    ("what a beautiful sunset tonight", "other"),
]

QUESTION_TYPE_EXAMPLES_EXTRA = [
    ("is the report finished yet", "yes_no"),
    ("can we reschedule the call", "yes_no"),
    ("do you have the file handy", "yes_no"),
    ("is everyone accounted for", "yes_no"),
    ("did the package arrive today", "yes_no"),
    ("will you be attending the event", "yes_no"),
    ("what's the title of that song", "what"),
    ("what ingredients do i need", "what"),
    ("what's the wifi password here", "what"),
    ("what's on the agenda today", "what"),
    ("why does my phone keep freezing", "why"),
    ("why did the flight get delayed", "why"),
    ("why is everyone so quiet today", "why"),
    ("how do i unsubscribe from this list", "how"),
    ("how does the elevator work in this building", "how"),
    ("how long does shipping usually take", "how"),
    ("who approved this budget", "who"),
    ("who's leading the project now", "who"),
    ("who left this note on my desk", "who"),
    ("when does the semester start", "when"),
    ("when was the last update released", "when"),
    ("when should i expect a reply", "when"),
    ("where can i park around here", "where"),
    ("where is the conference room located", "where"),
    ("where do these boxes go", "where"),
    ("turn off the lights before leaving", "other"),
    ("i can't believe how good this tastes", "other"),
    ("send that email whenever you're ready", "other"),
    ("this place looks completely different now", "other"),
]
QUESTION_TYPE_EXAMPLES.extend(QUESTION_TYPE_EXAMPLES_EXTRA)

QUESTION_TYPE_EXAMPLES_EXTRA_2 = [
    ("is dinner ready yet", "yes_no"),
    ("does the warranty cover this", "yes_no"),
    ("has the invoice been paid", "yes_no"),
    ("can i borrow your charger", "yes_no"),
    ("what's for breakfast tomorrow", "what"),
    ("what's the return policy here", "what"),
    ("what did the email say exactly", "what"),
    ("why won't the app open anymore", "why"),
    ("why did the price go up so much", "why"),
    ("why is nobody answering the phone", "why"),
    ("how do you pronounce this name", "how"),
    ("how much does shipping cost", "how"),
    ("how do i cancel my subscription", "how"),
    ("who's in charge of hiring here", "who"),
    ("who fixed the printer earlier", "who"),
    ("when do applications close", "when"),
    ("when did you move to this city", "when"),
    ("where does this cable plug in", "where"),
    ("where can i return this item", "where"),
    ("hand me the remote please", "other"),
    ("that concert was absolutely incredible", "other"),
    ("i think we should leave now", "other"),
]
QUESTION_TYPE_EXAMPLES.extend(QUESTION_TYPE_EXAMPLES_EXTRA_2)

QUESTION_TYPE_EXAMPLES_EXTRA_3 = [
    ("is the invoice paid in full", "yes_no"),
    ("can i get a refund on this", "yes_no"),
    ("does the plan include international calls", "yes_no"),
    ("is parking included with the ticket", "yes_no"),
    ("what's the fastest way to the station", "what"),
    ("what's included in the subscription", "what"),
    ("what's causing this error message", "what"),
    ("why does the app crash on startup", "why"),
    ("why are prices higher this season", "why"),
    ("how do i merge these two files", "how"),
    ("how do you say this word properly", "how"),
    ("who designed this logo", "who"),
    ("who's on call this weekend", "who"),
    ("when does boarding begin", "when"),
    ("when was this policy last updated", "when"),
    ("where do i submit the paperwork", "where"),
    ("where does this road lead", "where"),
    ("wow that's a huge improvement", "other"),
    ("grab your coat, we're leaving", "other"),
    ("i really appreciate your help today", "other"),
]
QUESTION_TYPE_EXAMPLES.extend(QUESTION_TYPE_EXAMPLES_EXTRA_3)

QUESTION_TYPE_EXAMPLES_EXTRA_4 = [
    ("is the elevator working today", "yes_no"),
    ("did the shipment leave the warehouse yet", "yes_no"),
    ("can we push the call to friday", "yes_no"),
    ("does this come with a warranty card", "yes_no"),
    ("are the tickets refundable", "yes_no"),
    ("will the discount still apply next week", "yes_no"),
    ("what's the boarding gate number", "what"),
    ("what's the difference between these two plans", "what"),
    ("what's playing at the theater tonight", "what"),
    ("what caused the delay this time", "what"),
    ("why is my order still processing", "why"),
    ("why did the meeting get cancelled", "why"),
    ("why does this keep timing out", "why"),
    ("how do i update my billing info", "how"),
    ("how long is the warranty valid for", "how"),
    ("how do you reset the router", "how"),
    ("who manages this account now", "who"),
    ("who signed off on the budget", "who"),
    ("when does the offer expire", "when"),
    ("when can i pick up my order", "when"),
    ("where is the customer service desk", "where"),
    ("where did you find that recipe", "where"),
    ("that was an unforgettable performance", "other"),
    ("lock the door behind you", "other"),
    ("i can't thank you enough for this", "other"),
    ("this view is absolutely stunning", "other"),
]
QUESTION_TYPE_EXAMPLES.extend(QUESTION_TYPE_EXAMPLES_EXTRA_4)

QUESTION_TYPE_EXAMPLES_EXTRA_5 = [
    ("is the venue wheelchair accessible", "yes_no"),
    ("did the update fix the login bug", "yes_no"),
    ("can you send this over by email instead", "yes_no"),
    ("what's the story behind this tradition", "what"),
    ("what's the fine print on this offer", "what"),
    ("why is the queue moving so slowly", "why"),
    ("why did they change the packaging", "why"),
    ("how do i join the waitlist", "how"),
    ("how many seats are left in the class", "how"),
    ("who's catering the event this year", "who"),
    ("when do the results get posted", "when"),
    ("where should i drop off the donation", "where"),
    ("congratulations, you really earned this", "other"),
    ("don't forget to lock up tonight", "other"),
]
QUESTION_TYPE_EXAMPLES.extend(QUESTION_TYPE_EXAMPLES_EXTRA_5)


class QuestionTypeClassifier(_DeepDenseTextClassifier):
    """Classifies a question's TYPE (yes/no vs what/why/how/who/when/
    where, or 'other' for non-questions) - useful for tailoring how a
    fallback response is phrased even when the specific intent isn't
    recognized (a 'why' question warrants a different fallback tone
    than a 'when' question)."""

    def __init__(self):
        super().__init__(QUESTION_TYPE_EXAMPLES)

    def format_predict(self, text: str) -> str:
        label, confidence = self.predict(text)
        return f"That looks like a **{label}**-type question ({confidence:.0%} confidence)."


# ==============================================================================
# Network 9: TEXT-COMPLEXITY REGRESSOR (continuous 0-1 score, NOT a classifier)
# ==============================================================================
# Hand-scored examples spanning simple to complex prose, used to train
# a REGRESSION network - this is the one network in this section (and
# one of only two regression-style tasks in the whole file, alongside
# nothing else here) whose training objective is "predict a continuous
# number" rather than "pick a label", so it needs its own base class
# (_DeepDenseTextRegressor above) with an MSE loss and a sigmoid output
# instead of softmax.
TEXT_COMPLEXITY_EXAMPLES = [
    ("i like cats", 0.03),
    ("the sun is hot", 0.04),
    ("we ate lunch", 0.03),
    ("he ran fast", 0.03),
    ("it is cold today", 0.05),
    ("she likes tea", 0.04),
    ("the dog barked loudly", 0.08),
    ("we went to the park", 0.07),
    ("i am very tired", 0.05),
    ("the car is red", 0.04),
    ("please close the door", 0.06),
    ("this is a good book", 0.07),
    ("my friend called me today", 0.09),
    ("the store closes at six", 0.10),
    ("we should leave soon", 0.08),
    ("the committee reviewed the quarterly budget report before the meeting", 0.45),
    ("she decided to pursue a career in mechanical engineering after graduation", 0.48),
    ("the software update introduced several performance improvements and minor bug fixes", 0.50),
    ("researchers observed a noticeable increase in rainfall across the region this year", 0.47),
    ("the negotiations between the two companies concluded without a final agreement", 0.52),
    ("investors remained cautious despite the unexpectedly positive earnings report", 0.55),
    ("the museum's new exhibit explores the intersection of art and technology", 0.46),
    ("local authorities announced updated guidelines for construction permits", 0.49),
    ("the novel explores themes of identity and belonging through its protagonist", 0.53),
    ("economists debated whether the policy change would affect long-term growth", 0.56),
    ("the epistemological ramifications of quantum indeterminacy continue to provoke substantial disagreement among contemporary philosophers of science", 0.92),
    ("notwithstanding the aforementioned stipulations, the plaintiff's counsel maintained that the contractual obligations remained enforceable despite the ostensible ambiguity therein", 0.95),
    ("the juxtaposition of postmodern architectural elements against the neoclassical facade exemplifies a deliberate subversion of stylistic orthodoxy", 0.90),
    ("the committee's deliberations were characterized by an ostensibly irreconcilable divergence of epistemic priors regarding fiscal sustainability", 0.93),
    ("her dissertation interrogates the phenomenological underpinnings of intersubjective consciousness within a post-structuralist framework", 0.94),
    ("the arbitration tribunal's jurisdiction was contested on the grounds of an alleged procedural irregularity in the antecedent proceedings", 0.91),
    ("the algorithm's asymptotic complexity renders it computationally intractable for sufficiently large input cardinalities", 0.89),
    ("the paper's central thesis hinges on a nuanced reinterpretation of hermeneutical tradition vis-a-vis contemporary critical theory", 0.93),
]

TEXT_COMPLEXITY_EXAMPLES_EXTRA = [
    ("my sister has a new puppy", 0.06),
    ("we watched a movie last night", 0.08),
    ("the coffee shop opens early", 0.09),
    ("i finished my homework quickly", 0.10),
    ("the garden needs some water", 0.07),
    ("she plays the guitar on weekends", 0.12),
    ("the train was a bit late this morning", 0.14),
    ("he ordered a sandwich and some fries", 0.13),
    ("the weather changed suddenly this afternoon", 0.18),
    ("they moved into a new apartment downtown", 0.20),
    ("the quarterly sales figures showed modest improvement over last year", 0.38),
    ("the city council approved funding for the new library branch", 0.40),
    ("employees were asked to complete the training module by friday", 0.36),
    ("the airline announced changes to its baggage policy this week", 0.42),
    ("the study examined how sleep patterns affect memory retention", 0.60),
    ("the report highlighted several inconsistencies in the audit process", 0.62),
    ("the panel discussed the ethical implications of automated decision-making", 0.68),
    ("critics argued that the film's pacing undermined its narrative ambitions", 0.65),
    ("the treaty's provisions regarding maritime boundaries remained contentious", 0.72),
    ("the manuscript's argument relies heavily on contested archival interpretations", 0.75),
    ("the symposium addressed competing theories of macroeconomic stagnation", 0.78),
    ("the ruling clarified the scope of statutory interpretation in administrative law", 0.80),
]
TEXT_COMPLEXITY_EXAMPLES.extend(TEXT_COMPLEXITY_EXAMPLES_EXTRA)

# Second expansion pass (targeting +65% total dataset size).
TEXT_COMPLEXITY_EXAMPLES_EXTRA_2 = [
    ("the cat sat by the window", 0.05),
    ("she waved and said hello", 0.06),
    ("we packed our bags for the trip", 0.09),
    ("the kettle whistled on the stove", 0.08),
    ("he tied his shoes and left", 0.07),
    ("the baby giggled at the puppy", 0.09),
    ("rain tapped gently on the roof", 0.10),
    ("they shared a pizza after the game", 0.11),
    ("the candle flickered in the dark", 0.09),
    ("she hummed a tune while cooking", 0.10),
    ("the marketing team revised the campaign timeline after client feedback", 0.44),
    ("volunteers organized the food drive over the holiday weekend", 0.39),
    ("the app's new interface confused several longtime users initially", 0.41),
    ("regulators proposed stricter guidelines for data storage practices", 0.51),
    ("the orchestra rehearsed the symphony's final movement twice", 0.37),
    ("analysts questioned whether the merger would pass antitrust review", 0.58),
    ("the documentary examines the decline of a once-thriving fishing town", 0.54),
    ("the startup pivoted its business model after losing its main investor", 0.50),
    ("the professor's lecture wove together history and economic theory", 0.63),
    ("critics praised the exhibit's unconventional use of negative space", 0.59),
    ("the algorithm's convergence guarantees depend on strict convexity assumptions", 0.83),
    ("the treatise interrogates the ontological status of fictional entities within modal realism", 0.94),
    ("the court's opinion parses the statute's legislative history with unusual granularity", 0.86),
    ("her argument presupposes a contestable distinction between constitutive and regulative norms", 0.90),
    ("the derivation invokes a nontrivial application of the dominated convergence theorem", 0.88),
    ("the committee's finding rests on an equivocal reading of the underlying empirical data", 0.71),
    ("the essay's rhetorical strategy relies on strategic ambiguity rather than direct argumentation", 0.76),
]
TEXT_COMPLEXITY_EXAMPLES.extend(TEXT_COMPLEXITY_EXAMPLES_EXTRA_2)

TEXT_COMPLEXITY_EXAMPLES_EXTRA_3 = [
    ("the kids played outside until dinner", 0.08),
    ("he forgot his umbrella at the office", 0.10),
    ("the printer jammed again this morning", 0.11),
    ("the panel's recommendations sparked immediate pushback from industry groups", 0.57),
    ("the thesis synthesizes competing frameworks without fully reconciling their assumptions", 0.85),
    ("the audit revealed discrepancies attributable to inconsistent reporting standards", 0.66),
    ("her closing argument reframed the jury's understanding of intent", 0.64),
]
TEXT_COMPLEXITY_EXAMPLES.extend(TEXT_COMPLEXITY_EXAMPLES_EXTRA_3)


class TextComplexityRegressor(_DeepDenseTextRegressor):
    """Predicts a continuous 0 (very simple) to 1 (very complex)
    reading-complexity score for a piece of text - a REGRESSION task,
    not classification, trained on hand-scored examples spanning
    simple sentences to dense academic/legal prose."""

    def __init__(self):
        super().__init__(TEXT_COMPLEXITY_EXAMPLES)

    def format_predict(self, text: str) -> str:
        score = self.predict(text)
        if score < 0.25:
            band = "simple"
        elif score < 0.6:
            band = "moderate"
        else:
            band = "complex"
        return f"Estimated reading complexity: {score:.2f} ({band})."


# ==============================================================================
# Network 10: EMOJI PREDICTOR (happy / sad / love / laugh / angry / surprised / neutral)
# ==============================================================================
EMOJI_EXAMPLES = [
    ("i got the job, i'm thrilled", "happy"),
    ("what a wonderful day this has been", "happy"),
    ("feeling great today, everything's going well", "happy"),
    ("i'm so pleased with how this turned out", "happy"),
    ("this made me really happy", "happy"),
    ("i miss my old friends so much", "sad"),
    ("today was really rough, i feel down", "sad"),
    ("i feel so low right now", "sad"),
    ("this news made me quite sad", "sad"),
    ("i've been feeling blue all week", "sad"),
    ("i adore my family more than anything", "love"),
    ("you mean the whole world to me", "love"),
    ("sending you all my love today", "love"),
    ("i love spending time with you", "love"),
    ("my heart is so full of love right now", "love"),
    ("that joke was absolutely hilarious", "laugh"),
    ("i can't stop laughing at this", "laugh"),
    ("lol that's so funny, i'm dying", "laugh"),
    ("this is the funniest thing i've seen all week", "laugh"),
    ("i burst out laughing at that", "laugh"),
    ("this is absolutely infuriating", "angry"),
    ("i'm so mad about this right now", "angry"),
    ("that really ticked me off", "angry"),
    ("i'm furious about how this was handled", "angry"),
    ("this makes my blood boil", "angry"),
    ("wow, i did not see that coming at all", "surprised"),
    ("no way, seriously? that's shocking", "surprised"),
    ("that's such surprising news", "surprised"),
    ("i'm stunned, i didn't expect that", "surprised"),
    ("whoa, that caught me completely off guard", "surprised"),
    ("the meeting starts at noon today", "neutral"),
    ("here is the document you requested", "neutral"),
    ("please review the attached file", "neutral"),
    ("the report is due next friday", "neutral"),
    ("the office is on the third floor", "neutral"),
]

EMOJI_EXAMPLES_EXTRA = [
    ("i just got accepted into my dream school", "happy"),
    ("this is the best news i've heard all year", "happy"),
    ("i'm walking on air right now", "happy"),
    ("everything is finally falling into place", "happy"),
    ("i can't wipe this smile off my face", "happy"),
    ("i feel so alone lately", "sad"),
    ("this loss has been really hard on me", "sad"),
    ("i just want to cry right now", "sad"),
    ("nothing feels the same anymore", "sad"),
    ("i've been in a slump for weeks", "sad"),
    ("i cherish every moment we spend together", "love"),
    ("my heart melts every time i see you", "love"),
    ("i'm so thankful to have you in my life", "love"),
    ("you make everything better just by being here", "love"),
    ("i love you more than words can say", "love"),
    ("i haven't laughed this hard in ages", "laugh"),
    ("that meme had me in tears laughing", "laugh"),
    ("i'm crying from laughing so much", "laugh"),
    ("this comedian is absolutely killing it", "laugh"),
    ("haha that's way too funny", "laugh"),
    ("i am beyond furious about this decision", "angry"),
    ("this whole situation makes me livid", "angry"),
    ("i want to scream i'm so angry", "angry"),
    ("how dare they treat us like this", "angry"),
    ("i'm seething over what just happened", "angry"),
    ("i literally jumped when that happened", "surprised"),
    ("i never expected to see you here", "surprised"),
    ("that plot twist completely blindsided me", "surprised"),
    ("i'm speechless, that's incredible news", "surprised"),
    ("who would have guessed that outcome", "surprised"),
    ("the invoice total is listed below", "neutral"),
    ("the elevator is out of service today", "neutral"),
    ("please bring your id to the appointment", "neutral"),
    ("the conference call link is in the email", "neutral"),
    ("the printer is out of paper again", "neutral"),
]
EMOJI_EXAMPLES.extend(EMOJI_EXAMPLES_EXTRA)

EMOJI_EXAMPLES_EXTRA_2 = [
    ("today turned out better than expected, i'm delighted", "happy"),
    ("i feel light and joyful this morning", "happy"),
    ("everything is coming together so nicely", "happy"),
    ("i'm heartbroken over this loss", "sad"),
    ("i feel empty after hearing that", "sad"),
    ("this has been a really gloomy stretch", "sad"),
    ("i treasure every second with you", "love"),
    ("being with you feels like home", "love"),
    ("my affection for you keeps growing", "love"),
    ("that stand-up bit was comedy gold", "laugh"),
    ("i snorted from laughing so hard", "laugh"),
    ("this gif is sending me, too funny", "laugh"),
    ("i am beyond irritated with this outcome", "angry"),
    ("this decision makes my blood boil", "angry"),
    ("i'm outraged by how this was handled", "angry"),
    ("i gasped out loud when i saw that", "surprised"),
    ("that twist completely caught me off guard", "surprised"),
    ("i genuinely did not expect that at all", "surprised"),
    ("the invoice number is printed at the top", "neutral"),
    ("the parking garage closes at midnight", "neutral"),
    ("please silence your phone during the talk", "neutral"),
]
EMOJI_EXAMPLES.extend(EMOJI_EXAMPLES_EXTRA_2)

EMOJI_EXAMPLES_EXTRA_3 = [
    ("we just hit our fundraising goal, amazing", "happy"),
    ("i woke up in such a good mood today", "happy"),
    ("this cozy weather makes me so content", "happy"),
    ("i've been crying on and off all day", "sad"),
    ("i feel invisible lately, like nobody notices", "sad"),
    ("this anniversary is hard without them here", "sad"),
    ("i want to hold you close forever", "love"),
    ("you're my favorite person in the whole world", "love"),
    ("every little thing you do makes me love you more", "love"),
    ("that impression had the whole room cracking up", "laugh"),
    ("i'm wheezing, this is too good", "laugh"),
    ("this cat video is comedy perfection", "laugh"),
    ("i am not okay with how this was handled, furious", "angry"),
    ("this rude comment really set me off", "angry"),
    ("i slammed the door i was so angry", "angry"),
    ("i literally froze, did not expect that reveal", "surprised"),
    ("out of nowhere, totally caught me off guard", "surprised"),
    ("i had no idea that was even possible", "surprised"),
    ("the badge scanner is by the front entrance", "neutral"),
    ("the newsletter goes out every other friday", "neutral"),
    ("the thermostat is set to auto mode", "neutral"),
]
EMOJI_EXAMPLES.extend(EMOJI_EXAMPLES_EXTRA_3)

EMOJI_EXAMPLES_EXTRA_4 = [
    ("i'm bursting with pride right now", "happy"),
    ("this playlist has me in the best mood", "happy"),
    ("i finally feel at peace with everything", "happy"),
    ("i keep replaying that goodbye in my head", "sad"),
    ("this quiet apartment feels too empty now", "sad"),
    ("i miss how things used to be", "sad"),
    ("you're the first thing i think of every morning", "love"),
    ("i'd choose you in every lifetime", "love"),
    ("being near you feels like coming home", "love"),
    ("i almost fell off my chair laughing", "laugh"),
    ("this caption is sending me into orbit", "laugh"),
    ("i can't even type i'm laughing so hard", "laugh"),
    ("i am boiling with rage over this", "angry"),
    ("this is an absolute disgrace and i'm livid", "angry"),
    ("i slammed my laptop shut, so frustrated", "angry"),
    ("i actually gasped out loud reading that", "surprised"),
    ("did that really just happen, i'm stunned", "surprised"),
    ("the meeting minutes are in the shared folder", "neutral"),
    ("the elevator inspection is scheduled for monday", "neutral"),
]
EMOJI_EXAMPLES.extend(EMOJI_EXAMPLES_EXTRA_4)

EMOJI_EXAMPLES_EXTRA_5 = [
    ("i feel unstoppable after that win", "happy"),
    ("this little win made my whole week", "happy"),
    ("i've been staring at old photos, feeling nostalgic and sad", "sad"),
    ("this silence in the house is heavy today", "sad"),
    ("i fall for you more every single day", "love"),
    ("you make ordinary days feel special", "love"),
    ("this blooper reel is pure chaos and i love it", "laugh"),
    ("i'm wheezing at how accurate this meme is", "laugh"),
    ("i am done being calm about this, i'm furious", "angry"),
    ("that comment crossed a serious line", "angry"),
    ("i did not expect that ending at all", "surprised"),
    ("the parking permit renews automatically each year", "neutral"),
]
EMOJI_EXAMPLES.extend(EMOJI_EXAMPLES_EXTRA_5)


class EmojiPredictor(_DeepDenseTextClassifier):
    """Predicts which single emoji best fits the emotional content of
    a message - complements SentimentClassifier's coarser 3-way mood
    reading with a finer-grained, 7-way emotional category."""

    _EMOJI_MAP = {
        "happy": "😊", "sad": "😢", "love": "❤️", "laugh": "😂",
        "angry": "😠", "surprised": "😲", "neutral": "🙂",
    }

    def __init__(self):
        super().__init__(EMOJI_EXAMPLES)

    def predict_emoji(self, text: str):
        """Returns (emoji_char, label, confidence)."""
        label, confidence = self.predict(text)
        return self._EMOJI_MAP.get(label, ""), label, confidence

    def format_predict(self, text: str) -> str:
        emoji, label, confidence = self.predict_emoji(text)
        return f"That feels {label} to me {emoji} ({confidence:.0%} confidence)."
