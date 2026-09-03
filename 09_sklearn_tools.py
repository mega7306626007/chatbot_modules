"""scikit-learn assisted tools (Section 6F)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 6F: SCIKIT-LEARN ASSISTED TOOLS
# ==============================================================================

class SimilarityMatcher:
    """
    A TF-IDF + cosine-similarity FALLBACK MATCHER, used only when the
    rigid regex intent engine finds no match at all.

    How it works:
      1. At startup, we fit a TfidfVectorizer on a FIXED list of example
         phrases that Claude wrote in advance (one or more per known
         command/intent). This fit happens once and is never updated -
         there is no online learning, no adaptation to what the user
         says, and no model state persisted between runs.
      2. When given a new piece of user text, we vectorize it with that
         same fixed vectorizer and compute cosine similarity against
         every example phrase, then return the best-matching example's
         associated intent label (e.g. 'tell_story') plus a similarity
         score, IF the score clears a confidence threshold.
      3. The chatbot then offers this as a suggestion ("did you mean...")
         rather than silently acting on it, so behavior stays predictable.

    This is a static lookup table with fuzzy matching, not a trained
    classifier in the conventional sense - it is included to fulfil a
    specific request to make use of scikit-learn, in a way that keeps
    the bot's core behavior fully rigid and explainable.
    """

    # Each example phrase maps to the label of the intent that handles it,
    # and to a short human-readable suggestion shown to the user.
    EXAMPLES = [
        ("what is my name", "ask_my_name", "ask what your name is"),
        ("remember my favorite food", "remember_fact", "tell me a fact to remember, like 'my favorite food is pizza'"),
        ("what time is it right now", "current_time", "ask for the current time"),
        ("what is today's date", "current_date", "ask for today's date"),
        ("how many days until a holiday", "days_until_holiday", "ask how many days until a holiday"),
        ("how many days between two dates", "days_between_dates", "ask how many days are between two dates"),
        ("how old am i if i was born on a date", "age_calculator", "ask me to calculate an age from a birth date"),
        ("tell me an adventure story", "tell_story", "ask for a story"),
        ("give me a story to read", "tell_story", "ask for a story"),
        ("write a haiku poem", "write_haiku", "ask me to write a haiku"),
        ("write an acrostic poem", "write_acrostic", "ask me to write an acrostic poem"),
        ("write a rhyming poem", "write_poem_general", "ask me to write a poem"),
        ("calculate a math expression", "simple_math", "ask a simple arithmetic question like 'what is 4 + 5'"),
        ("tell me a funny joke", "tell_joke", "ask for a joke"),
        ("tell me an inspirational quote", "tell_quote", "ask for a quote"),
        ("give me a riddle to solve", "tell_riddle", "ask for a riddle"),
        ("ask me a trivia question", "tell_trivia", "ask for a trivia question"),
        ("count the words in this text", "word_count_tool", "ask me to count words in some text"),
        ("check if this word is a palindrome", "palindrome_check", "ask if a word is a palindrome"),
        ("convert miles to kilometers", "unit_convert", "ask me to convert between units"),
        ("check if a number is prime", "prime_check", "ask if a number is prime"),
        ("spell out a number in words", "number_to_words_tool", "ask me to spell a number in words"),
        ("add an item to my to-do list", "todo_add", "ask me to add something to your to-do list"),
        ("show my to-do list", "todo_list", "ask to see your to-do list"),
        ("play a game of hangman", "hangman_start", "ask to play hangman"),
        ("show me the help menu", "help", "type 'help' to see everything I can do"),
    ]

    def __init__(self):
        self.phrases = [ex[0] for ex in self.EXAMPLES]
        self.labels = [ex[1] for ex in self.EXAMPLES]
        self.suggestions = [ex[2] for ex in self.EXAMPLES]

        # Fit once on the fixed example phrases - never re-fit later.
        self.vectorizer = TfidfVectorizer()
        self.example_vectors = self.vectorizer.fit_transform(self.phrases)

    def best_match(self, user_text: str, threshold: float = 0.35):
        """
        Returns (suggestion_text, label, score) for the closest known
        example phrase, or None if nothing clears the similarity
        threshold. This never executes an intent itself - it only
        suggests one for the chatbot to mention to the user.
        """
        if not user_text.strip():
            return None

        user_vector = self.vectorizer.transform([user_text])
        similarities = cosine_similarity(user_vector, self.example_vectors)[0]

        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        if best_score < threshold:
            return None

        return self.suggestions[best_idx], self.labels[best_idx], best_score


class NotesClusterer:
    """
    An explicitly-labeled DEMO TOOL: runs scikit-learn's KMeans over the
    text of the user's to-do list to group similar-sounding items
    together. This is presented to the user as a demonstration of
    clustering, not a feature the bot depends on, and it does not
    persist any model state between calls - every invocation fits a
    brand-new KMeans model from scratch on whatever to-do items exist
    at that moment.
    """

    def cluster_notes(self, notes: list, num_clusters: int = None):
        """
        notes: list of plain text strings (e.g. to-do descriptions).
        Returns a human-readable summary string, or an explanation if
        there isn't enough data to cluster meaningfully.
        """
        if len(notes) < 2:
            return ("I need at least 2 to-do items to demonstrate clustering. "
                     "Add a few more with 'add to my to-do list: ...' first.")

        if num_clusters is None:
            num_clusters = max(2, min(3, len(notes) // 2))
        num_clusters = min(num_clusters, len(notes))

        vectorizer = TfidfVectorizer(stop_words="english")
        try:
            X = vectorizer.fit_transform(notes)
        except ValueError:
            return "I couldn't extract enough meaningful words from those notes to cluster them."

        if X.shape[1] == 0:
            return "I couldn't extract enough meaningful words from those notes to cluster them."

        model = KMeans(n_clusters=num_clusters, n_init=10, random_state=None)
        labels = model.fit_predict(X)

        clusters = defaultdict(list)
        for note, label in zip(notes, labels):
            clusters[int(label)].append(note)

        lines = [f"(Demo) KMeans grouped your {len(notes)} to-do items into {len(clusters)} clusters:"]
        for cluster_id in sorted(clusters.keys()):
            lines.append(f"\nCluster {cluster_id + 1}:")
            for note in clusters[cluster_id]:
                lines.append(f"  - {note}")
        lines.append(
            "\n(Note: this clustering is recomputed fresh every time you ask - "
            "nothing here is learned or remembered between requests.)"
        )
        return "\n".join(lines)



# ==============================================================================
