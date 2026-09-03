"""Persistent memory manager (Section 2) + conversation logger (Section 3)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 2: PERSISTENT MEMORY MANAGER
# ==============================================================================

class MemoryStore:
    """
    Handles all long-term memory: facts the user tells the bot to
    remember (name, favorite things, birthday, etc.), bot identity, and
    the to-do list.

    Backed by Database (Section 1B) - a single SQLite file - rather
    than a hand-rolled JSON file. The public interface here is
    UNCHANGED from the pre-database version: callers elsewhere in this
    file still address to-dos by 1-based position in a list, exactly as
    before. This class translates that positional interface into row-id
    based SQL operations internally, so nothing else in the codebase
    needed to change.
    """

    def __init__(self, db: "Database"):
        self.db = db
        created_at = self.db.get_meta("created_at")
        if created_at is None:
            created_at = dt.datetime.now().isoformat()
            self.db.set_meta("created_at", created_at)
        self._created_at = created_at

        visit_count = int(self.db.get_meta("visit_count", 0)) + 1
        self.db.set_meta("visit_count", visit_count)
        self.db.set_meta("last_seen", dt.datetime.now().isoformat())

        if self.db.get_meta("bot_name") is None:
            self.db.set_meta("bot_name", DEFAULT_BOT_NAME)

    def save(self):
        """
        Kept for backward compatibility with existing call sites
        (main()/self-test call memory.save() at the end of a session).
        Database writes happen immediately on each call now (every
        set_fact/add_todo/etc. commits its own transaction), so there's
        nothing left to flush here - this is a deliberate no-op.
        """
        pass

    # ---- fact management -----------------------------------------------------

    def remember(self, key: str, value: str):
        """Store a fact under a normalized key."""
        norm_key = self._normalize_key(key)
        self.db.set_fact(norm_key, value)

    def recall(self, key: str):
        """Retrieve a fact, or None if unknown."""
        norm_key = self._normalize_key(key)
        return self.db.get_fact(norm_key)

    def forget(self, key: str) -> bool:
        """Delete a fact. Returns True if something was actually deleted."""
        norm_key = self._normalize_key(key)
        return self.db.delete_fact(norm_key)

    def forget_all(self):
        """Wipe all remembered facts (but keep visit counters etc.)."""
        self.db.clear_facts()

    def all_facts(self) -> dict:
        return self.db.get_all_facts()

    @staticmethod
    def _normalize_key(key: str) -> str:
        key = key.strip().lower()
        key = re.sub(r"\s+", "_", key)
        key = re.sub(r"[^a-z0-9_]", "", key)
        return key

    # ---- bot identity -----------------------------------------------------

    def set_bot_name(self, name: str):
        self.db.set_meta("bot_name", name.strip())

    def get_bot_name(self) -> str:
        return self.db.get_meta("bot_name", DEFAULT_BOT_NAME)

    # ---- misc ---------------------------------------------------------------

    def get_visit_count(self) -> int:
        return int(self.db.get_meta("visit_count", 1))

    def get_created_at(self) -> dt.datetime:
        try:
            return dt.datetime.fromisoformat(self._created_at)
        except (ValueError, TypeError):
            return dt.datetime.now()

    # ---- to-do list management -----------------------------------------
    #
    # The rest of the codebase addresses to-dos by 1-based POSITION
    # (matching what a user sees in a numbered list), not by database
    # row id. These methods translate between the two on every call -
    # list_todo_rows() is already ordered by id, so position N
    # corresponds to the Nth row in that ordering.

    def add_todo(self, description: str) -> int:
        """Add a new to-do item. Returns its 1-based index."""
        self.db.add_todo_row(description.strip())
        return len(self.db.list_todo_rows())

    def list_todos(self, include_done: bool = True) -> list:
        rows = self.db.list_todo_rows()
        todos = [
            {"description": row["text"], "done": bool(row["done"]), "created_at": row["created_at"]}
            for row in rows
        ]
        if include_done:
            return todos
        return [t for t in todos if not t["done"]]

    def complete_todo(self, index: int) -> bool:
        """Mark a 1-based to-do index as done. Returns True on success."""
        rows = self.db.list_todo_rows()
        if 1 <= index <= len(rows):
            return self.db.mark_todo_row_done(rows[index - 1]["id"])
        return False

    def remove_todo(self, index: int) -> bool:
        """Delete a 1-based to-do index entirely. Returns True on success."""
        rows = self.db.list_todo_rows()
        if 1 <= index <= len(rows):
            return self.db.remove_todo_row(rows[index - 1]["id"])
        return False

    def clear_todos(self):
        self.db.clear_todo_rows()

    def find_todo_by_text(self, text: str):
        """Find the 1-based index of a to-do whose description contains
        the given text (case-insensitive). Returns None if not found."""
        text_lower = text.strip().lower()
        rows = self.db.list_todo_rows()
        for i, row in enumerate(rows, start=1):
            if text_lower in row["text"].lower():
                return i
        return None

    # ---- important dates (birthdays, anniversaries, etc.) ----------------

    def remember_important_date(self, label: str, date: dt.date):
        """Store a structured important date (e.g. a birthday) under a
        normalized label. Re-stating the same label updates it rather
        than creating a duplicate."""
        norm_label = self._normalize_key(label)
        self.db.set_important_date(norm_label, date.month, date.day, date.year)

    def recall_important_date(self, label: str):
        """Returns a datetime.date for a stored important date, using
        the CURRENT year if no year was originally given (so 'when's my
        birthday' always resolves to something usable), or None if
        nothing is stored under that label."""
        norm_label = self._normalize_key(label)
        row = self.db.get_important_date(norm_label)
        if row is None:
            return None
        year = row["year"] if row["year"] else dt.datetime.now().year
        try:
            return dt.date(year, row["month"], row["day"])
        except ValueError:
            return None

    def recall_important_date_with_year(self, label: str):
        """Like recall_important_date, but returns the ORIGINAL stored
        year (possibly None) rather than substituting the current year -
        useful when the actual birth year matters, e.g. for the age
        calculator. Returns None if nothing is stored under that label."""
        norm_label = self._normalize_key(label)
        row = self.db.get_important_date(norm_label)
        if row is None or row["year"] is None:
            return None
        try:
            return dt.date(row["year"], row["month"], row["day"])
        except ValueError:
            return None

    def list_important_dates(self):
        return self.db.list_important_dates()

    def forget_important_date(self, label: str) -> bool:
        norm_label = self._normalize_key(label)
        return self.db.delete_important_date(norm_label)


# ==============================================================================
# SECTION 3: CONVERSATION LOGGER (uses pandas)
# ==============================================================================

class ConversationLogger:
    """
    Keeps a running record of every (speaker, message, timestamp) triple
    for the current session, and persists it to the shared Database
    (Section 1B) rather than a hand-rolled CSV file.

    Provides simple statistics (via pandas/numpy) about the conversation:
    word counts, message counts, most common words, session duration, etc.
    This is descriptive statistics only - not learning or model fitting.
    """

    COLUMNS = ["timestamp", "speaker", "message"]

    def __init__(self, db: "Database"):
        self.db = db
        self.session_rows = []  # list of dicts, accumulated this run

    def log(self, speaker: str, message: str):
        row = {
            "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
            "speaker": speaker,
            "message": message,
        }
        self.session_rows.append(row)

    def flush_to_disk(self):
        """
        Persist this session's rows to the database. Kept the same
        method name as the old CSV-based version for backward
        compatibility with existing call sites (main()/self-test call
        this at the end of a session).
        """
        for row in self.session_rows:
            self.db.log_message(row["speaker"], row["message"])

    def session_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.session_rows, columns=self.COLUMNS)

    def recent_transcript_lines(self, limit: int = 40) -> list:
        """Returns the last `limit` turns of this session as plain
        "speaker: message" strings - the format LLMConnector.
        summarize_conversation() and ExtractiveSummarizer both expect.
        Session-only (not the full historical log across all runs),
        since summarizing "this conversation" should mean this session."""
        recent = self.session_rows[-limit:]
        return [f"{row['speaker']}: {row['message']}" for row in recent]

    def full_history_dataframe(self) -> pd.DataFrame:
        """Load the entire historical log (all sessions ever, including
        this one once flushed) from the database."""
        rows = self.db.full_log_rows()
        if not rows:
            return pd.DataFrame(columns=self.COLUMNS)
        return pd.DataFrame(rows, columns=self.COLUMNS)

    def session_stats(self) -> str:
        """Build a human-readable statistics summary using pandas/numpy."""
        df = self.session_dataframe()
        if df.empty:
            return "No conversation has happened yet this session."

        user_df = df[df["speaker"] == "user"]
        bot_df = df[df["speaker"] == "bot"]

        user_word_counts = user_df["message"].str.split().apply(len)
        bot_word_counts = bot_df["message"].str.split().apply(len)

        total_user_words = int(user_word_counts.sum()) if not user_df.empty else 0
        total_bot_words = int(bot_word_counts.sum()) if not bot_df.empty else 0

        avg_user_words = float(np.mean(user_word_counts)) if not user_df.empty else 0.0

        # Most common words the user typed (very simple frequency count,
        # ignoring punctuation and very short "stop" words).
        stopwords = {
            "the", "a", "an", "is", "it", "to", "of", "and", "in", "you",
            "i", "my", "me", "do", "are", "for", "on", "that", "this",
        }
        all_words = []
        for msg in user_df["message"]:
            cleaned = re.sub(r"[^\w\s]", "", str(msg).lower())
            all_words.extend(w for w in cleaned.split() if w not in stopwords and len(w) > 2)
        common = Counter(all_words).most_common(5)

        if len(df) >= 2:
            start = dt.datetime.fromisoformat(df.iloc[0]["timestamp"])
            end = dt.datetime.fromisoformat(df.iloc[-1]["timestamp"])
            duration = end - start
            duration_str = str(duration).split(".")[0]
        else:
            duration_str = "0:00:00"

        lines = [
            "Session statistics:",
            f"  Messages from you:   {len(user_df)}",
            f"  Messages from me:    {len(bot_df)}",
            f"  Your total words:    {total_user_words}",
            f"  My total words:      {total_bot_words}",
            f"  Your avg words/msg:  {avg_user_words:.1f}",
            f"  Session duration:    {duration_str}",
        ]
        if common:
            common_str = ", ".join(f"'{w}' ({c}x)" for w, c in common)
            lines.append(f"  Your top words:      {common_str}")
        return "\n".join(lines)


# ==============================================================================
