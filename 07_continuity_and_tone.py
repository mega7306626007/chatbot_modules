"""Topic continuity, flashcards, tone tracker (Sections 6D2-6D4)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 6D2: TOPIC CONTINUITY TRACKER (rule-based, no ML)
# ==============================================================================
#
# Keeps a small rolling history of which topics/intents have come up
# this session, so the bot can answer "go back to what we were talking
# about" or "what were we discussing before that" - simple stack-based
# bookkeeping, not a learned dialogue model. This is a genuinely
# missing piece of "conversation memory" that's easy to overlook: the
# bot already remembers FACTS (MemoryStore, Section 2) but had no
# memory of the SHAPE of the conversation itself (what topics came up,
# in what order) until now.
class TopicContinuityTracker:
    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self._history = []  # list of (topic_label, timestamp)
        # Light per-turn conversation memory: the last raw user message,
        # its typo-corrected form, and the label that ended up resolving
        # this turn. Kept alongside the rolling topic stack so follow-up
        # logic ("why?", bare "advice", "yes"/"no" to a bot offer) can
        # read the most recent context without threading it through every
        # handler signature.
        self.last_user_text = None
        self.last_corrected_text = None
        self.last_label = None
        # Rolling short-term conversation turn memory (most recent first)
        # for multi-turn continuity: the last few raw/corrected/label
        # triples, so follow-up logic can look back more than one turn.
        # Capped at 4 turns - this is contextual glue, not a topic log
        # (that's `_history`).
        self.turn_history = []

    # Follow-up cues that mean "keep talking about whatever we were just
    # talking about" even though the message itself carries no topic.
    FOLLOW_UP_CUES = re.compile(
        r"^(and(?: then)?|what about it|tell me more|say more|go on|continue|"
        r"what happened next|what else|i see(?: you)?|really|interesting|"
        r"makes sense|that makes sense|how so|why is that|you said|is that so|"
        r"no way|oh really|meanwhile|also|so what now|hmm[, ]?$|right[,]?$)",
        re.IGNORECASE,
    )
    # Words that, in a SHORT otherwise-unrouted message, read as
    # referring back to the last thing the bot said.
    BACK_REFERENCE_PRONOUNS = ("it", "that", "this", "them", "they", "its",
                               "so", "really", "one")

    def remember_turn(self, raw, corrected, label):
        self.last_user_text = raw
        self.last_corrected_text = corrected
        self.last_label = label
        self.turn_history.insert(0, {
            "raw": raw, "corrected": corrected, "label": label})
        if len(self.turn_history) > 4:
            self.turn_history.pop()

    def recent_labels(self, limit: int = 3) -> list:
        """Most-recent non-None labels, newest first, de-duplicated."""
        seen = set()
        out = []
        for lbl in [self.last_label] + [t["label"] for t in self.turn_history]:
            if lbl and lbl not in seen:
                seen.add(lbl)
                out.append(lbl)
            if len(out) >= limit:
                break
        return out

    def resolve_follow_up(self, text):
        """If an unrouted message is clearly a continuation cue or a
        short back-reference, return the label of the topic we were last
        on, so the core can re-engage that topic's bank. Returns None
        when the message reads as genuinely new - callers then fall
        through to their normal unrouted handling."""
        labels = self.recent_labels(2)
        if not labels:
            return None
        text_l = (text or "").strip().lower()
        if not text_l:
            return None
        if self.FOLLOW_UP_CUES.match(text_l):
            return labels[0]
        words = re.findall(r"[a-z']+", text_l)
        if 1 <= len(words) <= 8 and any(w in self.BACK_REFERENCE_PRONOUNS for w in words):
            return labels[0]
        return None

    def record(self, topic_label: str):
        if not topic_label:
            return
        self.last_label = topic_label
        # Collapse immediate repeats (asking two jokes in a row
        # shouldn't count as "changing topic and changing back").
        if self._history and self._history[-1][0] == topic_label:
            return
        self._history.append((topic_label, dt.datetime.now()))
        if len(self._history) > self.max_history:
            self._history.pop(0)

    def previous_topic(self):
        """Returns the topic label BEFORE the current one, or None if
        there isn't one yet."""
        if len(self._history) < 2:
            return None
        return self._history[-2][0]

    def current_topic(self):
        if not self._history:
            return None
        return self._history[-1][0]

    def recent_topics(self, limit: int = 5) -> list:
        return [label for label, _ts in self._history[-limit:]]

    def format_recent_topics(self, limit: int = 5) -> str:
        topics = self.recent_topics(limit)
        if not topics:
            return "We haven't really settled on any particular topics yet this session."
        readable = [t.replace("_", " ") for t in topics]
        return "We've touched on: " + ", ".join(readable) + "."


# ==============================================================================
# SECTION 6D3: FLASHCARD / SPACED-REPETITION QUIZ (rule-based scheduling)
# ==============================================================================
#
# Builds a tiny spaced-repetition scheduler on top of FunExtras' TRIVIA
# bank (Section 6B): each question gets a "box" (1-5, the classic
# Leitner system - a real, well-established, non-ML spaced-repetition
# technique predating computerized flashcard apps by decades). A
# correct answer promotes a question to the next box (reviewed less
# often); a wrong answer demotes it back to box 1 (reviewed again
# soon). This is deterministic bookkeeping, not a learned model of the
# user's memory - the same scheduling algorithm real flashcard software
# like Anki is loosely based on.
# ==============================================================================
# SECTION 6D4: ADAPTIVE TONE TRACKER (rule-based register detection)
# ==============================================================================
#
# Scores each user message for FORMALITY using plain heuristics - word-
# list membership, contraction detection, repeated-letter/punctuation
# patterns ("heyyy", "sooo") - no ML, same "rigid, hand-written rules"
# philosophy as the rest of this file's non-learned components. A
# rolling average (exponential smoothing) means one unusually formal or
# casual message doesn't instantly flip the detected register; it has
# to be a genuine pattern across several turns.
#
# What this actually changes: response banks in Section 8 already
# contain BOTH the original, more composed phrasings AND two later
# supplements written in a looser register (_CASUAL_TONE_PHRASES,
# _SHENG_PHRASES) - all merged into one pool per bank at import time.
# ChatBot._pick_toned_response() (see the ChatBot class) uses this
# tracker to bias WHICH part of that merged pool gets sampled: leaning
# into the casual/Sheng supplement for a user who's clearly texting
# casually, or filtering it OUT (falling back to the original,
# non-supplement phrasings) for a user who's writing formally -
# without needing to duplicate or re-tag every bank from scratch.
class AdaptiveToneTracker:
    CASUAL_MARKERS = {
        "lol", "lmao", "haha", "hehe", "yo", "hey", "hii", "heyy", "ayy",
        "gonna", "wanna", "kinda", "sorta", "yeah", "yep", "nah", "sup",
        "niaje", "sasa", "poa", "buda", "msee", "fiti", "omg", "btw",
    }
    FORMAL_MARKERS = {
        "furthermore", "therefore", "however", "regarding", "shall",
        "would", "could", "please", "kindly", "greetings", "sincerely",
        "appreciate", "assist", "inquire", "request", "accordingly",
    }
    _CONTRACTION_RE = re.compile(r"\b\w+'(t|re|ve|ll|d|s|m)\b")
    _REPEATED_LETTERS_RE = re.compile(r"(.)\1{2,}")

    def __init__(self, smoothing: float = 0.25):
        self.smoothing = smoothing
        self.score = 0.5  # 0.0 = very casual, 1.0 = very formal; start neutral

    def score_message(self, text: str) -> float:
        if not text:
            return self.score
        lower = text.lower()
        words = re.findall(r"[a-z']+", lower)
        if not words:
            return self.score

        casual_hits = sum(1 for w in words if w in self.CASUAL_MARKERS)
        formal_hits = sum(1 for w in words if w in self.FORMAL_MARKERS)
        has_contraction = bool(self._CONTRACTION_RE.search(lower))
        has_repeated_letters = bool(self._REPEATED_LETTERS_RE.search(lower))
        starts_lowercase = text[:1].islower()
        avg_word_len = sum(len(w) for w in words) / len(words)
        ends_properly_punctuated = text.rstrip().endswith((".", ":", ";"))

        casual_signal = casual_hits * 2 + has_contraction + has_repeated_letters + starts_lowercase
        formal_signal = formal_hits * 2 + (avg_word_len > 5.5) + (text[:1].isupper() and ends_properly_punctuated)

        raw = (formal_signal / (casual_signal + formal_signal)) if (casual_signal or formal_signal) else 0.5
        self.score = self.score * (1 - self.smoothing) + raw * self.smoothing
        return self.score

    def is_casual(self) -> bool:
        return self.score < 0.4

    def is_formal(self) -> bool:
        return self.score > 0.6

    def describe(self) -> str:
        if self.is_casual():
            return "casual"
        if self.is_formal():
            return "formal"
        return "neutral"

    def format_status(self) -> str:
        return f"Detected conversational register: {self.describe()} (score {self.score:.2f}, 0=casual, 1=formal)."


class LeitnerFlashcards:
    NUM_BOXES = 5
    # Box N is reviewed every BOX_INTERVALS[N-1] "sessions" - a
    # simplified, session-count-based interval rather than real
    # calendar time, appropriate for a chatbot with no persistent
    # background scheduler.
    BOX_INTERVALS = [1, 2, 4, 8, 16]

    def __init__(self):
        self.cards = {}  # question_text -> {"box": int, "sessions_since_review": int, "item": dict}
        self.session_count = 0
        self._active_card = None  # question_text currently awaiting an answer

    def load_from_trivia(self, trivia_items: list):
        for item in trivia_items:
            question = item["question"]
            if question not in self.cards:
                self.cards[question] = {"box": 1, "sessions_since_review": 0, "item": item}

    def advance_session(self):
        self.session_count += 1
        for card in self.cards.values():
            card["sessions_since_review"] += 1

    def _due_cards(self) -> list:
        due = []
        for question, card in self.cards.items():
            interval = self.BOX_INTERVALS[min(card["box"], self.NUM_BOXES) - 1]
            if card["sessions_since_review"] >= interval:
                due.append(question)
        return due

    def next_card(self):
        """Returns the next due flashcard's trivia item, preferring
        lower boxes (things the user knows less well) - or None if
        nothing is due right now."""
        due = self._due_cards()
        if not due:
            return None
        due.sort(key=lambda q: self.cards[q]["box"])
        question = due[0]
        self._active_card = question
        return self.cards[question]["item"]

    def answer(self, guess: str):
        """Grades the active card, updates its box, and returns
        (is_correct, correct_answer) - or None if no card is active."""
        if self._active_card is None:
            return None
        card = self.cards[self._active_card]
        correct_answer = card["item"]["answer"].lower().strip()
        is_correct = guess.lower().strip() == correct_answer or guess.lower().strip() in correct_answer

        if is_correct:
            card["box"] = min(card["box"] + 1, self.NUM_BOXES)
        else:
            card["box"] = 1
        card["sessions_since_review"] = 0
        self._active_card = None
        return is_correct, card["item"]["answer"]

    def format_progress(self) -> str:
        if not self.cards:
            return "No flashcards loaded yet."
        by_box = Counter(card["box"] for card in self.cards.values())
        lines = [f"Flashcard progress ({len(self.cards)} cards, session {self.session_count}):"]
        for box in range(1, self.NUM_BOXES + 1):
            lines.append(f"  Box {box}: {by_box.get(box, 0)} card(s)")
        return "\n".join(lines)


# ==============================================================================
