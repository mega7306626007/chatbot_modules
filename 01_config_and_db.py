"""Header, imports, global config (Section 1), SQLite database layer (Section 1B)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
 RULE-BASED CHATBOT WITH THREE REAL NEURAL NETWORKS
================================================================================
A mostly offline, mostly rule-based conversational chatbot, with three
genuinely trained neural networks doing distinct jobs: guessing intent,
reading mood, and predicting what you'll probably ask next.

Design notes:
- ALL persistence (remembered facts, the to-do list, the full
  conversation log, both neural classifiers' user-verified corrections,
  their training history) lives in ONE real SQLite database
  (chatbot.db, Section 1B) - sqlite3 is part of the Python standard
  library, so no extra install is needed. Upgrading from an older,
  pre-database version of this file triggers a one-time, automatic
  import from the old JSON/CSV files into chatbot.db, so nothing is
  lost. Say "db stats" to see real row counts.
- The CORE conversation logic (regex intents, memory, dates, stories,
  poems, arithmetic, hangman, stats) is still 100% rigid pattern
  matching and hand-written logic - no learning involved.
- THREE real neural networks live in Sections 6G-6H:
    1. NeuralIntentClassifier - classifies free-form text into an
       intent (greetings, feelings, bot commands, ...). PyTorch
       backend (if installed): a hand-built nn.Embedding -> mean-pool
       -> BatchNorm1d -> GELU -> Dropout -> Linear stack, trained with
       Adam + a StepLR scheduler, an explicit train/validation split,
       and early stopping on validation accuracy. Sklearn fallback (if
       PyTorch isn't installed): MLPClassifier over TF-IDF features -
       still a real backprop network, so nothing crashes either way.
    2. SentimentClassifier - a SEPARATE, smaller network reading mood
       (positive/negative/neutral) to color response TONE, not to pick
       a handler. Same dual-backend strategy as above.
    3. SmartSuggestionEngine - a DIFFERENT kind of task: given the
       CURRENT intent, predicts a likely NEXT one, powering the
       "(you might also want to ask ...)" suggestions after replies.
       Backend: a small keras.Sequential model (Embedding -> Flatten
       -> Dense(relu) -> Dropout -> Dense(softmax)) trained with
       model.fit() if TensorFlow is installed; a frequency-table
       lookup over the same transition data otherwise.
  All three report REAL held-out validation accuracy after fitting
  (see 'nn stats') rather than just claiming to work. All learn ONLY
  from user-VERIFIED corrections (see 'no, i meant ...' / 'retrain'),
  never from their own unverified predictions, since that would let
  confidently-wrong guesses compound with no ground truth correcting
  them. 'compare models' shows what the intent and sentiment networks
  each independently think about the same message, side by side.
- scikit-learn is ALSO used in two older, simpler, clearly-labeled
  places that predate the above and aren't "learning" systems:
    - A TF-IDF + cosine-similarity FALLBACK MATCHER (SimilarityMatcher):
      a fixed lookup table, fit once at startup and never updated.
      Kept as a final safety net behind the neural classifier.
    - An explicitly-labeled "cluster my notes" DEMO TOOL that runs
      KMeans over the user's to-do list text purely to show how
      clustering works, refit from scratch every call.
- No externally-fetched data or network calls are needed for the CORE
  bot to work - only the Python standard library, plus pandas, numpy,
  scikit-learn, and (optionally, if installed) PyTorch, TensorFlow, and
  OpenCV. Section 13 adds a SEPARATE, fully OPT-IN layer of real
  external API connectors (current weather, currency conversion, fresh
  trivia, news headlines, machine translation) - these do make live
  HTTP calls when used, but every single one fails closed (a plain-
  language message, never a crash or a hang) if there's no network,
  the service is down, or the response doesn't parse. Nothing in
  Sections 1-12 depends on any of them being reachable.
- Two MORE real trained models live in Sections 6H2/6H3, beyond the
  three neural networks already described above:
    4. MoodTrendForecaster - a genuinely different kind of network
       from the three above: an LSTM (Keras) that reads a SEQUENCE of
       the last few sentiment readings this session and forecasts
       which mood is coming next, rather than classifying one input in
       isolation. Falls back to a recency-weighted frequency heuristic
       without TensorFlow.
    5. SemanticMemoryIndex - a PyTorch sentence encoder trained with a
       margin-based CONTRASTIVE loss (metric learning, not ordinary
       classification) on NN_INTENT_EXAMPLES paraphrase pairs, used to
       search the user's remembered facts by MEANING rather than exact
       keyword. Falls back to a fresh per-query TF-IDF/cosine search
       without PyTorch.
  Say "ml backends status" to see, in one place, which real backend
  (vs. offline fallback) is currently active for every one of these
  five models plus OpenCV/Pillow/LLM/API availability.
- OpenCV (Section 12/12-extended) does real, classic computer-vision
  work beyond the original face/edge detection: k-means color-palette
  extraction, contour-based object counting, RMS-contrast + histogram-
  equalization analysis, a bilateral-filter "cartoon effect" pipeline,
  and thumbnail/edge-map export - all standard, well-established
  OpenCV techniques, no bundled pretrained detection model.
- The LLM hybrid (Section 6I) goes beyond a single generate-and-return
  call: retry-with-backoff for transient failures, a offline token/
  cost estimator, a chunked "streaming-style" generator for progressive
  display, a small hand-written PROMPT_TEMPLATES library (personas for
  summarization, tutoring, debate, code help, translation polishing,
  and more), a PromptBuilder for assembling few-shot prompts, and a
  JSON tool-calling parser/dispatcher (Section 13B) that can route a
  structured LLM response to real chatbot methods (weather, currency,
  trivia, memory search). ExtractiveSummarizer (offline, TF-IDF
  sentence ranking) backs conversation summarization whenever the LLM
  isn't configured or a call fails.
- TypoCorrector (Section 7) also fixes a different kind of input issue
  from ordinary misspellings: French elisions typed without the
  apostrophe ("jai" for "j'ai", "cest" for "c'est", "quest-ce" for
  "qu'est-ce"). These are restored via a dedicated FRENCH_ELISION_FIXES
  dictionary, checked separately from the English typo dictionary,
  since nothing about the word is actually MISSPELLED - the apostrophe
  was just dropped, which is common when typing fast.
- The Swahili response banks (Section 8) also carry a hand-written
  Sheng supplement (Section 8-EXT4) - Sheng being the real, living
  Nairobi urban vernacular (a fluid Swahili/English slang mix, not a
  separate standardized language), so it's merged into "sw" rather
  than added as a fourth top-level language.
- StoryTeller (Section 5) got richer in two ways: two brand-new
  categories (horror, slice_of_life) alongside more stories in every
  existing category, and - more importantly - every telling now wraps
  the (fixed) story text in a randomly chosen atmosphere opener/closer
  line (ATMOSPHERE_OPENERS/NARRATOR_CLOSERS), so re-reading the same
  story doesn't feel identical each time, the same "phrase bank"
  variety idea used throughout this file applied to narration.
- Section 14 adds a genuine, classic word-prediction model - a
  trigram-with-backoff Markov chain, the same foundational technique
  behind early predictive-text keyboards - trained OFFLINE on a real
  casual conversational corpus and embedded as PRUNED, AGGREGATED
  word-transition counts (any sequence appearing fewer than twice was
  dropped, so recurring style survives but the raw source text does
  not).
- Section 14B layers a genuine (if tiny) TRANSFORMER on top of Section
  14's trigram model: token + positional embeddings, causally-masked
  multi-head self-attention, a feedforward block, and a linear output
  head - the same core recipe real transformer LLMs use, just at toy
  scale. Called "transformer-like" rather than "an LLM" on purpose:
  the architecture is real, the scale/capability is not comparable.
  "Online mode" here means "torch is installed, so a real learned
  model runs" (nothing calls the network) - trained via self-
  distillation on synthetic sentences SAMPLED from Section 14's own
  trigram model, never on stored text. Without torch, prediction/
  continuation falls straight back to Section 14's rule-based trigram
  backoff - both paths share one interface (TransformerLanguageModel),
  so "predict next word after: X" / "continue this: X" automatically
  use whichever is available.
- LLM support infrastructure (Section 6I-EXT..EXT4) sits between
  LLMConnector and any handler that calls it: a response cache keyed
  on (system_prompt, user_text) so an identical repeated request
  doesn't cost a second network round-trip; a soft usage/cost budget
  tracker using LLMConnector's own token estimator, which can refuse a
  call BEFORE it's made rather than after; a PII pre-check (email/
  phone/card/SSN-shaped patterns) that warns, but never blocks, before
  text would leave the machine for a third-party API; and a bounded
  conversation-context window that folds recent turns into the prompt
  while staying under a token budget, dropping the oldest turns first.
  ChatBot._call_llm_safely() is the single recommended entry point
  that wires all four together.
- Several genuinely new OFFLINE (no ML, no network) capabilities were
  added alongside those LLM improvements, on the theory that the
  rule-based half of this bot deserved the same round of attention as
  the LLM-backed half: a scientific calculator (sqrt/power/log/trig/
  percentages, still no eval() of arbitrary expressions - one rigid
  pattern per operation, same philosophy as the original arithmetic
  handler), a text case converter (snake/kebab/camel/Pascal/Title/
  upper/lower, normalizing through a common "list of words"
  representation so any case converts to any other), a cryptographically
  secure password/passphrase generator (Python's `secrets` module, not
  `random`), a much wider unit converter (area, volume, digital
  storage, speed, energy, pressure, and time, on top of the original
  distance/weight/temperature), a topic-continuity tracker (rolling
  history of what's been discussed, answering "go back to what we were
  talking about"), and a Leitner-system flashcard scheduler over the
  trivia bank (the same box-based spaced-repetition idea behind
  real flashcard software, predating any ML approach to the problem).
- Building the case-converter and topic-tracker features surfaced two
  more instances of a known TypoCorrector failure mode (a legitimate
  word sitting at edit-distance 1 from an unrelated common word and
  getting silently "corrected" into it): "world" -> "would" and
  "back" -> "black". Both are now in COMMON_WORDS, alongside the
  earlier "old" -> "gold" and "teal" -> "tell" fixes - this class of
  bug is inherent to the edit-distance approach and likely still has
  undiscovered instances.
- The bot can:
    * Hold a normal conversation (greetings, small talk, farewells)
    * Remember facts about the user (name, favorite color, birthday, etc.)
      and recall them later in the same session and across sessions
      (saved to a local JSON file).
    * Tell you the current date and time, day of week, and do simple
      date math ("how many days until Christmas").
    * Tell stories from a built-in story library, optionally personalized
      with the user's remembered name.
    * Write poems using template-based, rule-driven poem generation
      (acrostic, haiku-style, rhyming couplets).
    * Do simple arithmetic.
    * Keep a log of the conversation and show simple statistics about
      the chat session using pandas/numpy.
    * Fall back on a trained neural network to guess intent when
      nothing else matches, adapt tone based on a second network's
      read on your mood, and proactively suggest a next thing to try
      via a third - and learn from your corrections to any of it.
    * Forecast where the conversation's mood is trending, search
      remembered facts by meaning, and summarize a session - offline
      by default, upgraded automatically when torch/TensorFlow/an LLM
      are available.
    * Look up real current weather, convert currencies, fetch fresh
      trivia and news headlines, and (optionally) machine-translate
      text - each via a small, no-crash REST connector.

Run it with:
    python chatbot.py            (plain-text chat in the terminal)
    python chatbot.py --gui      (graphical chat window - needs Kivy)
    python chatbot.py --test     (offline self-test, no input needed)

Type 'help' inside the chatbot to see what it can do.
================================================================================
"""

import os
import re
import io
import csv
import sys
import json
import time
import pickle
import hashlib

# ==============================================================================
# MODEL CACHING (efficiency): every sklearn-backed network in this file
# was being retrained from scratch on EVERY startup - measured via
# cProfile at ~14-20 seconds total, almost entirely inside
# MLPClassifier.fit(). None of that work changes between runs unless
# the training data or hyperparameters actually change, so this caches
# the fitted model + vectorizer to disk, keyed by a hash of exactly
# the things that SHOULD invalidate it (training examples,
# hyperparameters) - change the data or architecture and the hash
# changes too, so a stale cache is never silently reused; change
# nothing, and startup skips training entirely.
MODEL_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_cache")


def model_cache_key(*parts) -> str:
    hasher = hashlib.sha256()
    for part in parts:
        hasher.update(repr(part).encode("utf-8"))
    return hasher.hexdigest()[:20]


def load_cached_model(cache_key: str):
    """Returns the cached dict of fitted attributes, or None if no
    cache exists yet, or it can't be read for any reason - fails
    closed to retraining rather than ever crashing startup."""
    path = os.path.join(MODEL_CACHE_DIR, f"{cache_key}.pkl")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception:
        return None


def save_cached_model(cache_key: str, data: dict):
    """Saves the dict of fitted attributes to the cache - best-effort
    and silent on failure (e.g. read-only filesystem), since a caching
    failure should never break training that already succeeded."""
    try:
        os.makedirs(MODEL_CACHE_DIR, exist_ok=True)
        path = os.path.join(MODEL_CACHE_DIR, f"{cache_key}.pkl")
        with open(path, "wb") as f:
            pickle.dump(data, f)
    except Exception:
        pass
import math
import random
import string
import base64
import secrets
import hashlib
import binascii
import textwrap
import datetime as dt
from collections import Counter, defaultdict

import warnings

# Used only by LLMConnector (Section 6I) to call the Anthropic API
# directly over HTTPS with zero extra dependencies - no SDK install
# needed beyond what's already required for this file.
import urllib.request
import urllib.error
import urllib.parse

# Used by Database (Section 2) - a single SQLite file backing ALL of
# the chatbot's persistence (facts, todos, conversation log, both
# classifiers' corrections, training history, LLM config), replacing
# five separate hand-rolled JSON/CSV files. sqlite3 is part of the
# Python standard library, so no extra pip install is needed.
import sqlite3
import contextlib

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# PyTorch is OPTIONAL. If it's installed, the neural intent classifier
# (Section 6G) builds and trains a real torch.nn neural network. If not,
# it automatically falls back to scikit-learn's MLPClassifier, which is
# also a genuine backprop-trained multi-layer perceptron - so the feature
# works either way, with no crash if torch isn't present.
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

# TensorFlow/Keras is ALSO OPTIONAL, and powers a genuinely different
# feature from the two PyTorch networks: SmartSuggestionEngine (Section
# 6H) predicts a likely NEXT intent given the current one (a sequence/
# transition problem), rather than classifying the current message's
# text. If TensorFlow isn't installed, it falls back to a simple
# frequency-table lookup built from the same transition data, so the
# "smart suggestions" feature still works, just without the Keras model.
try:
    import tensorflow as tf
    from tensorflow import keras
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

# psutil is OPTIONAL and powers the 'system status' command (Section
# 12) - live CPU/RAM/battery info read straight from the device. If
# it's not installed, that command says so plainly instead of crashing.
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Pillow and OpenCV are OPTIONAL and power the image-analysis feature
# (Section 12) - letting the user point the bot at an image file and
# get back real, computed information about it (dimensions, dominant
# colors, brightness, detected faces/edges) rather than a canned
# "I can't see images" response. Pillow handles basic loading/
# metadata/color analysis; OpenCV handles the heavier computer-vision
# parts (face detection, edge detection). Each is checked separately so
# the feature degrades gracefully (Pillow-only analysis still works
# even if OpenCV isn't installed, and vice versa for the parts that
# don't need OpenCV).
try:
    from PIL import Image, ImageDraw, ImageFilter
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False


# ==============================================================================
# SECTION 1: GLOBAL CONFIGURATION
# ==============================================================================

APP_NAME = "PyChat"
APP_VERSION = "1.0.0"

# Single SQLite database backing ALL persistence (Section 1B's Database
# class) - facts, todos, conversation log, both classifiers'
# corrections, training history, and LLM config all live here now.
DATABASE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot.db")

# The paths below are KEPT only so a one-time migration can import data
# from anyone upgrading from a pre-database version of this file. Once
# migrated, these old files are not written to again - all reads/writes
# go through Database from here on.
MEMORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_memory.json")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_log.csv")
NN_TRAINING_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_nn_training.json")
SENTIMENT_TRAINING_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_sentiment_training.json")
LLM_CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_llm_config.json")
TRANSLATION_CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_translation_config.json")

# Maximum number of turns to keep in short-term (in-session) memory buffer.
SHORT_TERM_MEMORY_LIMIT = 50

# Bot "personality" name - can be changed by the user with 'call yourself X'
DEFAULT_BOT_NAME = "PyChat"

# Random seed is intentionally NOT fixed - we want varied responses each run.
# (No learning happens; randomness here is only for picking among
# pre-written rigid templates/phrases, not for adapting behavior.)


# ==============================================================================
# SECTION 1B: DATABASE (single SQLite store for all persistence)
# ==============================================================================
#
# Everything the chatbot used to persist as separate hand-rolled JSON
# and CSV files - remembered facts, the to-do list, the conversation
# log, both neural classifiers' user-verified corrections, their
# training history, and the LLM hybrid's config - now lives in ONE
# real, queryable, transactional SQLite database (chatbot.db).
#
# Uses sqlite3 from the Python standard library only - no extra pip
# install needed, works on Pydroid 3 out of the box.
#
# MIGRATION: on first run after upgrading from a pre-database version
# of this file, if chatbot.db is empty, a one-time import pulls in
# everything from the old JSON/CSV files (see migrate_from_* methods
# and main()'s startup sequence) so nobody loses their remembered
# facts, to-do list, corrections, or training history. After that,
# the old files are left untouched and unused.

DATABASE_SCHEMA = """
CREATE TABLE IF NOT EXISTS facts (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bot_meta (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS important_dates (
    label TEXT PRIMARY KEY,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    year INTEGER,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS conversation_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    speaker TEXT NOT NULL,
    message TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS corrections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classifier TEXT NOT NULL,
    text TEXT NOT NULL,
    label TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS training_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classifier TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    backend TEXT,
    num_base_examples INTEGER,
    num_corrections INTEGER,
    val_accuracy REAL,
    training_loss REAL
);

CREATE TABLE IF NOT EXISTS llm_config (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE INDEX IF NOT EXISTS idx_log_timestamp ON conversation_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_corrections_classifier ON corrections(classifier);
CREATE INDEX IF NOT EXISTS idx_history_classifier ON training_history(classifier);
"""


class Database:
    """
    Single SQLite-backed store for everything the chatbot persists
    across sessions. See the Section 1B module docstring above for the
    full rationale. Every other persistence-touching class in this file
    (MemoryStore, ConversationLogger, both neural classifiers,
    LLMConnector) holds a reference to one shared Database instance and
    routes its reads/writes through it, while keeping each class's own
    PUBLIC interface unchanged from before - callers elsewhere in the
    file don't need to know storage moved from JSON/CSV to SQLite.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def _init_schema(self):
        with self._conn:
            self._conn.executescript(DATABASE_SCHEMA)

    def close(self):
        self._conn.close()

    @contextlib.contextmanager
    def _cursor(self):
        """Every write happens inside an explicit transaction (commit on
        success, rollback on any exception) rather than relying on
        sqlite3's sometimes-surprising implicit transaction behavior."""
        cur = self._conn.cursor()
        try:
            yield cur
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise

    # ---- facts ----------------------------------------------------------

    def get_fact(self, key: str):
        row = self._conn.execute("SELECT value FROM facts WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else None

    def get_all_facts(self) -> dict:
        rows = self._conn.execute("SELECT key, value FROM facts").fetchall()
        return {row["key"]: row["value"] for row in rows}

    def set_fact(self, key: str, value: str):
        now = dt.datetime.now().isoformat()
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO facts (key, value, updated_at) VALUES (?, ?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
                (key, value, now),
            )

    def delete_fact(self, key: str) -> bool:
        with self._cursor() as cur:
            cur.execute("DELETE FROM facts WHERE key = ?", (key,))
            return cur.rowcount > 0

    def clear_facts(self):
        with self._cursor() as cur:
            cur.execute("DELETE FROM facts")

    # ---- bot metadata -----------------------------------------------------

    def get_meta(self, key: str, default=None):
        row = self._conn.execute("SELECT value FROM bot_meta WHERE key = ?", (key,)).fetchone()
        return row["value"] if row else default

    def set_meta(self, key: str, value):
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO bot_meta (key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, str(value)),
            )

    # ---- to-do list -------------------------------------------------------
    #
    # NOTE: the rest of the codebase (MemoryStore, _handle_todo_*)
    # addresses to-dos by 1-based POSITION in a list, not by database
    # row id. MemoryStore's wrapper methods translate between the two -
    # see MemoryStore.add_todo/complete_todo/remove_todo below - so this
    # class stays a thin, position-agnostic SQL layer.

    def add_todo_row(self, text: str) -> int:
        now = dt.datetime.now().isoformat(timespec="seconds")
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO todos (text, done, created_at) VALUES (?, 0, ?)", (text, now)
            )
            return cur.lastrowid

    def list_todo_rows(self):
        rows = self._conn.execute(
            "SELECT id, text, done, created_at FROM todos ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]

    def mark_todo_row_done(self, row_id: int) -> bool:
        with self._cursor() as cur:
            cur.execute("UPDATE todos SET done = 1 WHERE id = ?", (row_id,))
            return cur.rowcount > 0

    def remove_todo_row(self, row_id: int) -> bool:
        with self._cursor() as cur:
            cur.execute("DELETE FROM todos WHERE id = ?", (row_id,))
            return cur.rowcount > 0

    def clear_todo_rows(self):
        with self._cursor() as cur:
            cur.execute("DELETE FROM todos")

    # ---- important dates (birthdays, anniversaries, etc.) ----------------
    #
    # Distinct from the generic key-value `facts` table: dates need
    # structured month/day/year fields so other features (the age
    # calculator, a future "days until X" lookup) can do real date
    # arithmetic on them, rather than re-parsing a free-text fact value
    # every time. `label` is the primary key (e.g. "birthday",
    # "anniversary") so re-stating a date naturally UPDATES the
    # existing entry instead of creating duplicates.

    def set_important_date(self, label: str, month: int, day: int, year: int = None):
        now = dt.datetime.now().isoformat(timespec="seconds")
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO important_dates (label, month, day, year, created_at) "
                "VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(label) DO UPDATE SET month = excluded.month, "
                "day = excluded.day, year = excluded.year, created_at = excluded.created_at",
                (label, month, day, year, now),
            )

    def get_important_date(self, label: str):
        row = self._conn.execute(
            "SELECT label, month, day, year FROM important_dates WHERE label = ?", (label,)
        ).fetchone()
        return dict(row) if row else None

    def list_important_dates(self):
        rows = self._conn.execute(
            "SELECT label, month, day, year FROM important_dates ORDER BY label"
        ).fetchall()
        return [dict(row) for row in rows]

    def delete_important_date(self, label: str) -> bool:
        with self._cursor() as cur:
            cur.execute("DELETE FROM important_dates WHERE label = ?", (label,))
            return cur.rowcount > 0

    # ---- conversation log ---------------------------------------------

    def log_message(self, speaker: str, message: str):
        now = dt.datetime.now().isoformat(timespec="seconds")
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO conversation_log (timestamp, speaker, message) VALUES (?, ?, ?)",
                (now, speaker, message),
            )

    def full_log_rows(self):
        rows = self._conn.execute(
            "SELECT timestamp, speaker, message FROM conversation_log ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]

    # ---- classifier corrections --------------------------------------

    def add_correction(self, classifier: str, text: str, label: str):
        now = dt.datetime.now().isoformat()
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO corrections (classifier, text, label, created_at) VALUES (?, ?, ?, ?)",
                (classifier, text, label, now),
            )

    def get_corrections(self, classifier: str):
        rows = self._conn.execute(
            "SELECT text, label FROM corrections WHERE classifier = ? ORDER BY id",
            (classifier,),
        ).fetchall()
        return [(row["text"], row["label"]) for row in rows]

    # ---- training history -----------------------------------------------

    def add_training_snapshot(self, classifier: str, backend: str, num_base_examples: int,
                                num_corrections: int, val_accuracy, training_loss):
        now = dt.datetime.now().isoformat(timespec="seconds")
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO training_history "
                "(classifier, timestamp, backend, num_base_examples, num_corrections, val_accuracy, training_loss) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (classifier, now, backend, num_base_examples, num_corrections, val_accuracy, training_loss),
            )

    def get_training_history(self, classifier: str, limit: int = 50):
        rows = self._conn.execute(
            "SELECT timestamp, backend, num_base_examples, num_corrections, val_accuracy, training_loss "
            "FROM training_history WHERE classifier = ? ORDER BY id DESC LIMIT ?",
            (classifier, limit),
        ).fetchall()
        return [dict(row) for row in reversed(rows)]

    # ---- LLM config -----------------------------------------------------

    def get_llm_config(self) -> dict:
        rows = self._conn.execute("SELECT key, value FROM llm_config").fetchall()
        result = {}
        for row in rows:
            try:
                result[row["key"]] = json.loads(row["value"])
            except (json.JSONDecodeError, TypeError):
                result[row["key"]] = row["value"]
        return result

    def set_llm_config(self, config: dict):
        with self._cursor() as cur:
            for key, value in config.items():
                cur.execute(
                    "INSERT INTO llm_config (key, value) VALUES (?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                    (key, json.dumps(value)),
                )

    # ---- one-time migration from the old JSON/CSV files ------------------

    def is_empty(self) -> bool:
        """True if this looks like a brand-new database with nothing in
        it yet - used to decide whether a one-time migration from old
        files should run."""
        counts = self._conn.execute(
            "SELECT "
            "(SELECT COUNT(*) FROM facts) + "
            "(SELECT COUNT(*) FROM todos) + "
            "(SELECT COUNT(*) FROM conversation_log) + "
            "(SELECT COUNT(*) FROM corrections) AS total"
        ).fetchone()
        return counts["total"] == 0

    def migrate_from_memory_json(self, filepath: str) -> bool:
        """One-time import of an old chatbot_memory.json into facts/
        bot_meta/todos. Returns True if anything was imported."""
        if not os.path.exists(filepath):
            return False
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return False

        imported = False
        for key, value in data.get("facts", {}).items():
            self.set_fact(key, value)
            imported = True
        for meta_key in ("bot_name", "created_at", "last_seen", "visit_count"):
            if meta_key in data and data[meta_key] is not None:
                self.set_meta(meta_key, data[meta_key])
                imported = True
        for item in data.get("todos", []):
            with self._cursor() as cur:
                cur.execute(
                    "INSERT INTO todos (text, done, created_at) VALUES (?, ?, ?)",
                    (item.get("description", ""), int(bool(item.get("done", False))),
                     item.get("created_at", dt.datetime.now().isoformat())),
                )
            imported = True
        return imported

    def migrate_from_log_csv(self, filepath: str) -> bool:
        """One-time import of an old chatbot_log.csv into conversation_log."""
        if not os.path.exists(filepath):
            return False
        try:
            import csv
            with open(filepath, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except (OSError, csv.Error):
            return False
        if not rows:
            return False
        with self._cursor() as cur:
            for row in rows:
                cur.execute(
                    "INSERT INTO conversation_log (timestamp, speaker, message) VALUES (?, ?, ?)",
                    (row.get("timestamp", ""), row.get("speaker", ""), row.get("message", "")),
                )
        return True

    def migrate_from_corrections_json(self, filepath: str, classifier: str) -> bool:
        """One-time import of an old corrections JSON file (used by both
        the intent and sentiment classifiers, distinguished by the
        classifier label) into corrections/training_history."""
        if not os.path.exists(filepath):
            return False
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return False

        imported = False
        for text, label in data.get("corrections", []):
            self.add_correction(classifier, text, label)
            imported = True
        for snap in data.get("training_history", []):
            self.add_training_snapshot(
                classifier,
                snap.get("backend"),
                snap.get("num_base_examples"),
                snap.get("num_corrections"),
                snap.get("val_accuracy"),
                snap.get("training_loss"),
            )
            imported = True
        return imported

    def migrate_from_llm_config_json(self, filepath: str) -> bool:
        """One-time import of an old chatbot_llm_config.json file."""
        if not os.path.exists(filepath):
            return False
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return False
        if not data:
            return False
        self.set_llm_config(data)
        return True

    def run_one_time_migration(self):
        """Runs all four migrations if (and only if) this database is
        still empty - safe to call every startup, since it's a no-op
        once data exists."""
        if not self.is_empty():
            return False
        migrated_anything = False
        migrated_anything |= self.migrate_from_memory_json(MEMORY_FILE)
        migrated_anything |= self.migrate_from_log_csv(LOG_FILE)
        migrated_anything |= self.migrate_from_corrections_json(NN_TRAINING_FILE, "intent")
        migrated_anything |= self.migrate_from_corrections_json(SENTIMENT_TRAINING_FILE, "sentiment")
        migrated_anything |= self.migrate_from_llm_config_json(LLM_CONFIG_FILE)
        return migrated_anything

    # ---- whole-database introspection -----------------------------------

    def table_counts(self) -> dict:
        """Real row counts for every table - used by the 'db stats'
        command so the answer is a live query, not a guess."""
        tables = ["facts", "bot_meta", "todos", "conversation_log",
                  "corrections", "training_history", "llm_config"]
        counts = {}
        for table in tables:
            row = self._conn.execute(f"SELECT COUNT(*) AS c FROM {table}").fetchone()
            counts[table] = row["c"]
        return counts

    def file_size_bytes(self) -> int:
        try:
            return os.path.getsize(self.db_path)
        except OSError:
            return 0


# ==============================================================================
