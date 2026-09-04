"""Pattern/intent matching, typo correction, language detection, keyword topic matcher (Section 7 family)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 7: PATTERN / INTENT MATCHING ENGINE
# ==============================================================================

class Intent:
    """
    Represents a single recognizable intent: a name, a list of regex
    patterns that trigger it, and a handler function that produces a
    response. Purely declarative - no statistical matching, no scoring
    beyond "first pattern that matches wins" (with patterns ordered from
    most specific to most general by the engine that registers them).
    """

    def __init__(self, name: str, patterns, handler):
        self.name = name
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        self.handler = handler

    def match(self, text: str):
        for pattern in self.compiled_patterns:
            m = pattern.search(text)
            if m:
                return m
        return None


class IntentEngine:
    """
    Holds an ordered list of Intents and finds the first one whose pattern
    matches the user's input. Order matters: more specific intents should
    be registered before more general "catch-all" ones.
    """

    def __init__(self):
        self.intents = []
        # Tracks the name of the last intent whose pattern matched and
        # whose handler returned a non-None response, WITHOUT changing
        # handle()'s return type - used by ChatBot.respond() to power
        # the smart-suggestions "you might also want to..." chips.
        self.last_matched_intent = None

    def register(self, name: str, patterns, handler):
        self.intents.append(Intent(name, patterns, handler))

    def handle(self, text: str, bot):
        """Try every intent in order; return the first non-None response.

        Note: handler is already a bound method (e.g. self._handle_greeting),
        so it only needs (text, match) - bot is implicit via the binding.
        """
        for intent in self.intents:
            m = intent.match(text)
            if m:
                response = intent.handler(text, m)
                if response is not None:
                    self.last_matched_intent = intent.name
                    return response
        return None


# ==============================================================================
# SECTION 7A2: TYPO CORRECTION (rigid dictionary + edit-distance, no ML)
# ==============================================================================

class TypoCorrector:
    """
    Corrects common fast-typing mistakes BEFORE the text reaches the
    intent engine or keyword matcher, so a typo like "tge" instead of
    "the" doesn't cause an otherwise-recognizable message to fall
    through to "I don't understand."

    Two layers, both fully rigid/deterministic - no machine learning:

      1. A hand-written dictionary of extremely common fast-typing
         mistakes (adjacent-key slips, transposed letters, doubled
         letters, dropped letters) mapped directly to their intended
         word. This is checked first because it's instant and covers
         the overwhelming majority of real-world typos for common
         words like "the", "you", "and", "what", etc.
      2. A small Levenshtein (edit-distance) fallback that compares
         any remaining unrecognized word against a fixed list of
         common English words used throughout this bot's intents and
         keyword banks. If a word is within edit-distance 1 of exactly
         one known common word, it's corrected; ties or distance-2+
         are left alone to avoid corrupting real words or names.

    This only touches words that aren't already recognized (i.e. don't
    already appear in the bot's known-word list), so correctly spelled
    text, names, and non-English/non-French/non-Swahili words are left
    completely untouched.
    """

    # Extremely common fast-typing slips, mapped to their intended word.
    # This list focuses on high-frequency words that appear constantly
    # in casual typing: "the", "you", "and", "what", "is", "to", etc.,
    # since correcting these has the highest payoff for unblocking an
    # otherwise-recognizable sentence.
    COMMON_TYPOS = {
        # "the"
        "tge": "the", "teh": "the", "hte": "the", "th3": "the", "thw": "the",
        "rhe": "the", "tje": "the", "thd": "the", "tne": "the",
        # "you"
        "yoy": "you", "yu": "you", "yopu": "you", "yoi": "you", "uou": "you",
        "youu": "you", "ypu": "you", "yoou": "you",
        # "and"
        "adn": "and", "nad": "and", "anf": "and", "amd": "and", "an d": "and",
        # "what"
        "waht": "what", "whta": "what", "wat": "what", "qhat": "what",
        "whay": "what", "whst": "what", "wht": "what",
        # "that"
        "taht": "that", "taht": "that", "thta": "that", "htat": "that",
        # "with"
        "wiht": "with", "wtih": "with", "wit": "with", "wih": "with",
        # "have"
        "ahve": "have", "hve": "have", "haev": "have", "hav": "have",
        # "this"
        "tihs": "this", "thsi": "this", "htis": "this", "dis": "this",
        # "your"
        "yuor": "your", "youe": "your", "yor": "your", "ypur": "your",
        # "are"
        "aer": "are", "rae": "are", "arr": "are",
        # "is"
        "si": "is", "iss": "is",
        # "for"
        "fro": "for", "fpr": "for", "ofr": "for", "foer": "for",
        # "can"
        "cna": "can", "acn": "can", "czn": "can",
        # "want"
        "wnat": "want", "wnt": "want", "watn": "want",
        # "know"
        "kno": "know", "knwo": "know", "konw": "know",
        # "time"
        "tiem": "time", "tmie": "time", "tim": "time",
        # "tell"
        "tel": "tell", "tlel": "tell", "telll": "tell",
        # "today"
        "todya": "today", "tody": "today", "toady": "today",
        # "tomorrow"
        "tommorow": "tomorrow", "tommorrow": "tomorrow", "tomorow": "tomorrow",
        "tomarow": "tomorrow", "tomorrw": "tomorrow",
        # "favorite"
        "favroite": "favorite", "favorit": "favorite", "favourtie": "favorite",
        # "because"
        "becuase": "because", "becasue": "because", "becuse": "because",
        "cuz": "because", "bcuz": "because",
        # "definitely"
        "definately": "definitely", "definitly": "definitely", "defintely": "definitely",
        # "really"
        "realy": "really", "realllly": "really", "reallly": "really",
        # "actually"
        "actualy": "actually", "actully": "actually",
        # "remember"
        "remeber": "remember", "remmeber": "remember", "rember": "remember",
        # "people"
        "poeple": "people", "ppl": "people", "peopel": "people",
        # "thanks"/"thank"
        "thnaks": "thanks", "thx": "thanks", "thanx": "thanks", "tnx": "thanks",
        "thakn": "thank", "thnk": "thank",
        # "please"
        "pls": "please", "plz": "please", "plez": "please", "pleas": "please",
        # "because"
        "becaus": "because",
        # "would"
        "owuld": "would", "woudl": "would", "wuold": "would",
        # "could"
        "coudl": "could", "cuold": "could",
        # "should"
        "shoudl": "should", "shuold": "should",
        # "from"
        "form": "from", "fomr": "from", "frmo": "from",
        # "when"
        "wehn": "when", "whne": "when",
        # "where"
        "wher": "where", "wheer": "where", "wherer": "where",
        # "which"
        "whihc": "which", "whcih": "which",
        # "right"
        "rigth": "right", "irght": "right", "rght": "right",
        # "great"
        "graet": "great", "grerat": "great", "gret": "great",
        # "happy"
        "happpy": "happy", "hapy": "happy", "hapyy": "happy",
        # "going"
        "goign": "going", "gonig": "going",
        # "doing"
        "doign": "doing", "diong": "doing",
        # "something"
        "smoething": "something", "soemthing": "something", "somthing": "something",
        # "nothing"
        "nothign": "nothing", "nothnig": "nothing",
        # "everything"
        "everythign": "everything", "everythnig": "everything",
        # "story"
        "stroy": "story", "stry": "story",
        # "poem"
        "pome": "poem", "pome": "poem",
        # "joke"
        "jkoe": "joke", "joek": "joke",
        # "weather"
        "waether": "weather", "wether": "weather", "wheather": "weather",
        # "friend"
        "freind": "friend", "frend": "friend", "frined": "friend",
        # "family"
        "familly": "family", "famly": "family",
        # "birthday"
        "bday": "birthday", "birtday": "birthday", "brithday": "birthday",
        # "tired" (NOT mapping "tried" here - that's a common valid word
        # on its own, e.g. "I tried my best", so correcting it would do
        # more harm than good)
        "tiered": "tired", "tird": "tired",
        # "hungry"
        "hugnry": "hungry", "hungy": "hungry",
        # "sorry"
        "sory": "sorry", "srry": "sorry", "soryy": "sorry",
        # "story" / "poem" / "joke" / "riddle" / "trivia" - heavily used
        # across this bot's intents, so typos here have an outsized
        # impact on whether a request gets recognized at all.
        "stroy": "story", "stry": "story", "stoy": "story",
        "poeam": "poem", "pome": "poem",
        "jkoe": "joke", "joek": "joke", "jole": "joke",
        "riddel": "riddle", "ridle": "riddle", "ridel": "riddle",
        "trvia": "trivia", "trivai": "trivia",
        "qoute": "quote", "qutoe": "quote",
        # "hangman" / "play"
        "hagnman": "hangman", "hangmna": "hangman", "hnagman": "hangman",
        "paly": "play", "plya": "play",
        # "remember" / "forget"
        "remeber": "remember", "rmember": "remember",
        "forgte": "forget", "fogret": "forget", "frget": "forget",
        # "calculate" / "convert"
        "calcualte": "calculate", "calculat": "calculate", "calclate": "calculate",
        "convrt": "convert", "convet": "convert", "convertt": "convert",
        # "number" / "prime" / "factorial"
        "numebr": "number", "nubmer": "number", "numbr": "number",
        "prmie": "prime", "priem": "prime",
        "factoial": "factorial", "factorail": "factorial",
        # "date" / "day" / "month" / "year"
        "daet": "date", "dtae": "date",
        "dya": "day", "dayy": "day",
        "moth": "month", "monht": "month",
        "yera": "year", "yaer": "year",
        # "list" / "add" / "remove" / "complete" / "delete"
        "lsit": "list", "ilst": "list",
        "remvoe": "remove", "rmeove": "remove",
        "compelte": "complete", "complet": "complete", "compete": "complete",
        "delet": "delete", "deltee": "delete",
        # "yourself" / "myself"
        "yourslef": "yourself", "yoursefl": "yourself",
        "myslef": "myself", "myseld": "myself",
        # "help" itself, surprisingly often mistyped under stress
        "hlep": "help", "hepl": "help", "jelp": "help",
        # generic doubled-letter slip examples are handled by the
        # edit-distance fallback below rather than hardcoded here.
    }

    # Common French words people type without the apostrophe when typing
    # fast/casually - "jai" for "j'ai", "cest" for "c'est", etc. These are
    # ELISIONS (je+ai -> j'ai, ce+est -> c'est), a completely different
    # kind of "typo" than the English slips above (nothing is misspelled
    # here, the apostrophe was just dropped), so they get their own
    # dictionary and their own check in _correct_word, rather than being
    # mixed into COMMON_TYPOS. Keys are the glued, no-apostrophe form;
    # values are the properly elided form.
    FRENCH_ELISION_FIXES = {
        # je + vowel-starting verb -> j'
        "jai": "j'ai", "jaime": "j'aime", "jadore": "j'adore",
        "jespere": "j'espère", "jespère": "j'espère", "jetais": "j'étais",
        "jétais": "j'étais", "jirai": "j'irai", "jarrive": "j'arrive",
        "jecoute": "j'écoute", "jécoute": "j'écoute", "jhabite": "j'habite",
        "jeviens": "j'arrive", "jappelle": "j'appelle", "jaimerais": "j'aimerais",
        "jutilise": "j'utilise", "jimagine": "j'imagine", "joublie": "j'oublie",
        "jespérais": "j'espérais", "jai pas": "j'ai pas", "jétudie": "j'étudie",
        "jetudie": "j'étudie", "jaurais": "j'aurais", "jaurai": "j'aurai",
        # ce + est/était/etc -> c'
        "cest": "c'est", "cetait": "c'était", "cétait": "c'était",
        "cestbon": "c'est bon", "cestca": "c'est ça", "cestca": "c'est ça",
        "cestvrai": "c'est vrai", "cestpas": "c'est pas", "cestqui": "c'est qui",
        "ceserait": "ce serait", "csa": "ça",
        # que + vowel -> qu'
        "quest": "qu'est", "questce": "qu'est-ce", "quil": "qu'il",
        "quils": "qu'ils", "quon": "qu'on", "quun": "qu'un", "quune": "qu'une",
        "quelle": "quelle", "quelles": "quelles",  # already fine, no elision
        "quimporte": "qu'importe", "quand meme": "quand même",
        # ne + vowel -> n'
        "nai": "n'ai", "nest": "n'est", "narrive": "n'arrive",
        "noublie": "n'oublie", "nimporte": "n'importe", "naime": "n'aime",
        "nas": "n'as", "navais": "n'avais", "nallait": "n'allait",
        "nira": "n'ira", "nexiste": "n'existe",
        # se + vowel -> s'
        "sappelle": "s'appelle", "sappellent": "s'appellent", "sil": "s'il",
        "sils": "s'ils", "savere": "s'avère", "sagit": "s'agit",
        "sennuie": "s'ennuie", "sinquiete": "s'inquiète", "sinquiète": "s'inquiète",
        # de + vowel -> d'
        "dacc": "d'accord", "daccord": "d'accord", "dailleurs": "d'ailleurs",
        "dabord": "d'abord", "dune": "d'une", "dun": "d'un",
        "dautres": "d'autres", "dhabitude": "d'habitude", "dou": "d'où",
        "doù": "d'où", "denfer": "d'enfer",
        # le/la + vowel -> l'
        "lheure": "l'heure", "lecole": "l'école", "lécole": "l'école",
        "lami": "l'ami", "lamie": "l'amie", "lamour": "l'amour",
        "lautre": "l'autre", "lidee": "l'idée", "lidée": "l'idée",
        "lannee": "l'année", "lannée": "l'année", "largent": "l'argent",
        "lecran": "l'écran", "lécran": "l'écran",
        # me/te + vowel -> m'/t'
        "mappelle": "m'appelle", "mennuie": "m'ennuie", "mexcuse": "m'excuse",
        "tappelles": "t'appelles", "tinquiete": "t'inquiète", "tinquiète": "t'inquiète",
        "texplique": "t'explique", "taime": "t'aime",
    }


    # used as the reference dictionary for the edit-distance fallback.
    # Deliberately limited to high-value, high-frequency words rather than
    # a full dictionary, to keep correction fast and avoid false positives.
    COMMON_WORDS = {
        "the", "you", "your", "and", "what", "that", "with", "have", "this",
        "are", "is", "for", "can", "want", "know", "time", "tell", "today",
        "tomorrow", "yesterday", "favorite", "because", "definitely",
        "really", "actually", "remember", "people", "thanks", "thank",
        "please", "would", "could", "should", "from", "when", "where",
        "which", "right", "great", "happy", "sad", "tired", "hungry",
        "going", "doing", "something", "nothing", "everything", "story",
        "poem", "joke", "weather", "friend", "friends", "family",
        "birthday", "sorry", "hello", "hi", "hey", "bye", "goodbye",
        "name", "love", "like", "feel", "feeling", "good", "bad", "okay",
        "yes", "no", "maybe", "help", "play", "game", "song", "music",
        "work", "school", "money", "food", "water", "sleep", "dream",
        "think", "thought", "believe", "understand", "explain", "again",
        # New feature-module trigger words (Section 22-31) - without
        # these, typo correction mangled them into the nearest already-
        # known word (e.g. "tac"->"tan", "toe"->"the", "size"->"side")
        # before the new intents' regexes ever saw the text.
        "tic", "tac", "toe", "size", "scramble", "morse", "caesar",
        "rot13", "ascii", "banner", "countdown", "countdowns", "anagram",
        "anagrams", "dice", "roll", "coin", "flip", "rps", "tip",
        "vigenere", "cipher", "phrase", "recurring", "advantage",
        "disadvantage", "adv", "disadv", "itemized", "auto", "smart",
        "easy", "medium", "hard", "starting", "every", "key", "real", "photo", "best",
        "always", "never", "sometimes", "often", "now", "later", "soon",
        "riddle", "trivia", "quote", "hangman", "forget", "calculate",
        "convert", "number", "prime", "factorial", "date", "day", "month",
        "year", "list", "add", "remove", "complete", "delete", "yourself",
        "myself", "stats", "status", "memory", "todo",
        # Age/birth-date vocabulary - "old" was missing here, which let
        # the edit-distance fallback "correct" it to "gold" (one
        # substitution away, and "gold" was already a recognized color
        # name) - this silently broke every age-calculator phrasing
        # containing "how old...". Same root cause as the teal->tell
        # bug: a real, common word absent from this list gets quietly
        # replaced by an unrelated word that happens to be closer in
        # edit distance than nothing.
        "old", "age", "aged", "young", "born", "birth", "anniversary",
        "ago", "fear",
        # Common color names - without these, short/uncommon-looking but
        # perfectly valid words like "teal" or "navy" can get mistakenly
        # "corrected" to an unrelated word at edit-distance 1 (e.g. "teal"
        # is one substitution away from "tell"). Better to recognize them
        # outright than rely on the edit-distance fallback to leave them
        # alone.
        "red", "blue", "green", "yellow", "purple", "orange", "pink",
        "black", "white", "brown", "gray", "grey", "teal", "navy",
        "maroon", "gold", "silver", "violet", "indigo", "cyan", "lime",
        "beige", "tan", "coral", "turquoise", "magenta", "crimson",
        # More everyday words that were absent here and sat exactly
        # edit-distance-1 from an unrelated common word, causing the
        # same silent-miscorrection bug as "old"->"gold" and
        # "teal"->"tell" above (found via "convert hello world to
        # snake case" -> "hello_would", i.e. "world" being "corrected"
        # to "would").
        "world", "case", "text", "camel", "snake", "kebab", "pascal",
        "title", "upper", "lower", "password", "passphrase", "generate",
        "back", "front", "side", "topic", "topics", "flashcard", "flashcards",
        "test", "tests", "testing", "tested",
        "base", "base64", "hash", "json", "csv", "entities", "entity",
        "extract", "validate", "decode", "encode",
        # Everyday conversational vocabulary that was absent here, each
        # sitting at edit-distance 1 from an unrelated COMMON_WORDS entry
        # and therefore getting silently rewritten on real messages
        # (measured: "our national team won last night" -> "your national
        # teal won list night"). Adding them makes the edit-distance
        # fallback leave legitimate words alone, exactly like the older
        # world->would and old->gold fixes.
        "our", "ours", "you", "we", "they", "us", "them", "he", "she",
        "one", "now", "how", "own", "team", "teams", "last", "won",
        "night", "tonight", "morning", "afternoon", "evening", "week",
        "weeks", "month", "months", "year", "years", "before", "about",
        "after", "again", "together", "around", "between", "during",
        "behind", "below", "above", "since", "until", "while", "make",
        "made", "making", "take", "took", "taking", "give", "gives",
        "given", "gave", "come", "came", "coming", "went", "goes",
        "going", "gone", "cook", "cooked", "cooking", "recipe",
        "recipes", "baking", "camera", "cameras", "lens", "lenses",
        "guitar", "piano", "jazz", "concert", "concerts", "album",
        "albums", "song", "songs", "artist", "artists", "stress",
        "stressful", "stressed", "overwhelmed", "worried", "worry",
        "worrying", "anxiety", "anxious", "panic", "nervous",
        "national", "international", "friend", "friends",
        "meeting", "meetings", "call", "called", "calling", "phone",
        "talk", "talking", "chatted", "chatting", "message", "messages",
        "text", "think", "thinking", "thought", "feel", "feels",
        "feeling", "felt", "happy", "sad", "glad", "better", "worse",
        "bad", "good", "great", "nice", "cool", "fine", "busy", "free",
        "last", "next", "first", "every", "each", "both", "either",
        "another", "other", "others", "some", "many", "much", "few",
        "lot", "lots", "bit", "little", "big", "small", "large",
        "start", "started", "starting", "stop", "stopped", "stopping",
        "keep", "kept", "keeping", "get", "got", "gotten", "getting",
        "put", "puts", "putting", "set", "buy", "bought", "buying",
        "sell", "sold", "paid", "pay", "spend", "spent", "spending",
        "money", "cost", "costs", "expensive", "cheap", "game", "games",
        "match", "matches", "score", "goal", "goals", "win", "wins",
        "winning", "lose", "lost", "losing", "coach", "player", "players",
        "football", "soccer", "basketball", "tennis", "rugby", "cricket",
        "meet", "met", "meeting", "travel", "traveled", "travelling",
        "trip", "trips", "place", "places", "house", "home", "town",
        "city", "village", "school", "class", "classes", "teacher",
        "students", "student", "exam", "exams", "test", "passed",
        "failing", "fail", "failed", "study", "studied", "studying",
        "learn", "learned", "learning", "understand", "understood",
        "question", "questions", "answer", "answers", "believe",
        "believed", "happen", "happened", "happens", "happening",
        "wonder", "wondering", "wanted", "wants", "wait", "waited",
        "waiting", "hope", "hoping", "hoped", "wish", "wished", "wishing",
        "want", "need", "needs", "needed", "needing", "nice", "kind",
        "sweet", "awesome", "amazing", "wonderful", "fantastic", "terrible",
        "awful", "horrible", "interesting", "boring", "exciting",
        "worried", "special", "important", "serious", "honest", "honest",
        "really", "actually", "literally", "basically", "probably",
        "maybe", "perhaps", "anyway", "anyways", "though", "although",
        "still", "yet", "already", "always", "never", "sometimes",
        "often", "usually", "rarely", "almost", "even", "only", "just",
        "quite", "very", "too", "also", "either", "neither", "either",
        "instead", "anyway", "aside", "okay", "alright", "sure", "yeah",
        "yep", "nah", "hmm", "gosh", "wow", "here", "there", "these",
        "those", "this", "that", "them", "their", "there", "theyre",
        "ours", "yours", "its", "it's", "we're", "we've", "they've",
        "they're", "you've", "you're", "i'm", "i've", "i'd", "he's", "she's",
    }

    def __init__(self):
        # Pre-compute a quick lookup set for the "is this word already
        # fine" check, combining common words with all the vocabulary
        # already used across the bot's language marker dictionaries,
        # so we don't accidentally "correct" a word that's already
        # perfectly valid (e.g. a Swahili or French word).
        self._known_words = set(self.COMMON_WORDS)
        self._known_words |= LanguageDetector.ENGLISH_MARKERS
        self._known_words |= LanguageDetector.SWAHILI_MARKERS
        self._known_words |= LanguageDetector.FRENCH_MARKERS
        # Unit-conversion vocabulary (Section 3, NumberTools) - short,
        # legitimate abbreviations/words that would otherwise sit at
        # edit-distance 1 from an unrelated common word (bar -> bad,
        # psi has no close match but atm/tsp/tbsp are short enough to
        # risk false corrections too) and get "corrected" into
        # something completely unintended.
        self._known_words |= {
            "bar", "psi", "atm", "kb", "mb", "gb", "tb", "ml", "tsp", "tbsp",
            "mph", "kmh", "kph", "kcal", "cal", "hectares", "acres", "knots",
        }

        # Efficiency: _correct_word() used to loop over ALL of
        # COMMON_WORDS (several hundred entries) for every single
        # unrecognized word, checking each one's length before ever
        # computing an edit distance. That length check is real work
        # too at this scale (called for every non-dictionary word in
        # every message), and almost all of it is wasted, since only
        # words within length +/-1 can ever match anyway. Precomputing
        # one bucket per word length here means _correct_word only
        # ever looks at the (typically tiny) handful of same-length-ish
        # words, not the whole dictionary.
        self._common_words_by_length = {}
        for known in self.COMMON_WORDS:
            self._common_words_by_length.setdefault(len(known), []).append(known)

    @staticmethod
    def _levenshtein(a: str, b: str) -> int:
        """Standard edit-distance computation (insertions, deletions,
        substitutions). Small, rigid dynamic-programming implementation -
        no external library, no learning."""
        if a == b:
            return 0
        if not a:
            return len(b)
        if not b:
            return len(a)

        previous_row = list(range(len(b) + 1))
        for i, char_a in enumerate(a, start=1):
            current_row = [i]
            for j, char_b in enumerate(b, start=1):
                insert_cost = current_row[j - 1] + 1
                delete_cost = previous_row[j] + 1
                substitute_cost = previous_row[j - 1] + (0 if char_a == char_b else 1)
                current_row.append(min(insert_cost, delete_cost, substitute_cost))
            previous_row = current_row
        return previous_row[-1]

    def _correct_word(self, word: str) -> str:
        """Correct a single word, or return it unchanged if no confident
        correction is found."""
        lower = word.lower()

        # Already a recognized word - leave it alone.
        if lower in self._known_words:
            return word

        # Simple plural/singular of an already-known word - also leave
        # alone. Without this, a plural like "years" (not itself listed)
        # could get "corrected" down to the singular "year" purely
        # because it's distance-1 in Levenshtein terms - technically
        # not wrong-looking, but it silently changes the user's actual
        # words and can break exact-phrase matching elsewhere (this is
        # exactly what broke "how many years old..." matching the age
        # calculator's regex, which expects the literal word "years").
        # This one check covers that entire class of bug generically,
        # rather than requiring every plural to be added to
        # COMMON_WORDS by hand one at a time.
        if lower.endswith("s") and lower[:-1] in self._known_words:
            return word
        if (lower + "s") in self._known_words:
            return word

        # Layer 1: exact match in the hand-written common-typo dictionary.
        if lower in self.COMMON_TYPOS:
            corrected = self.COMMON_TYPOS[lower]
            return corrected.capitalize() if word[:1].isupper() else corrected

        # Layer 1.5: French elisions typed without the apostrophe (see
        # FRENCH_ELISION_FIXES above) - checked separately from the
        # English typo dictionary since this isn't correcting a
        # misspelling, it's restoring a dropped apostrophe so the
        # French intent patterns/keyword matcher (which expect the
        # properly elided form, e.g. "j'ai") can recognize the word.
        if lower in self.FRENCH_ELISION_FIXES:
            corrected = self.FRENCH_ELISION_FIXES[lower]
            return corrected[0].upper() + corrected[1:] if word[:1].isupper() else corrected

        # Layer 2: edit-distance fallback against the common-words list.
        # Only correct if exactly one common word is at distance 1 - if
        # there's a tie (e.g. equally close to two different words) or
        # the closest match is distance 2+, leave the word alone rather
        # than risk a wrong "correction".
        if len(lower) < 3:
            return word  # too short to safely correct (e.g. "hi", "ok")

        candidates = []
        for length in (len(lower) - 1, len(lower), len(lower) + 1):
            for known in self._common_words_by_length.get(length, []):
                dist = self._levenshtein(lower, known)
                if dist == 1:
                    candidates.append(known)

        if len(candidates) == 1:
            corrected = candidates[0]
            return corrected.capitalize() if word[:1].isupper() else corrected

        return word

    def correct_text(self, text: str) -> str:
        """
        Correct likely typos in a full message. Punctuation and spacing
        are preserved; only word tokens are checked/corrected.
        """
        def replace(match):
            return self._correct_word(match.group(0))

        return re.sub(r"[A-Za-z']+", replace, text)


# ==============================================================================
# SECTION 7B: LANGUAGE DETECTION (rigid keyword dictionary, no translation)
# ==============================================================================

class LanguageDetector:
    """
    Detects whether a message is most likely English, Swahili, or French,
    purely by counting how many words in the message appear in a fixed,
    hand-written keyword dictionary for each language.

    This is NOT a trained language-identification model and does NOT
    translate anything. It's a deterministic word-overlap count against
    three fixed word lists written in advance. If no language's word
    list scores above zero, English is used as the default.

    Why this approach: it keeps every behavior fully explainable ("the
    message contained 3 Swahili marker-words and 0 French/English
    marker-words, so we treat it as Swahili") without any statistical
    model, embedding, or learned weights.
    """

    # Common function words / high-frequency markers per language.
    # These lists are deliberately broad (articles, pronouns, common
    # verbs, question words) since those words appear in almost every
    # sentence in a given language, making them strong rigid signals.
    ENGLISH_MARKERS = {
        "the", "is", "are", "what", "how", "when", "where", "why", "who",
        "you", "your", "i", "my", "me", "we", "us", "do", "does", "did",
        "can", "could", "would", "will", "shall", "have", "has", "had",
        "and", "or", "but", "not", "this", "that", "these", "those",
        "hello", "hi", "hey", "thanks", "thank", "please", "yes", "no",
        "good", "bad", "today", "tomorrow", "yesterday", "time", "date",
        "name", "story", "poem", "joke", "tell", "give", "want", "like",
        "love", "feel", "feeling", "okay", "ok", "sure", "maybe", "am",
        "was", "were", "be", "been", "being", "to", "of", "in", "on", "at",
        "for", "with", "about", "from", "as", "it", "he", "she", "they",
        "going", "gonna", "gotta", "need", "needs", "think", "thought",
        "know", "knew", "see", "saw", "look", "looking", "make", "made",
        "get", "got", "take", "took", "come", "came", "go", "went",
        "work", "working", "play", "playing", "eat", "eating", "drink",
        "happy", "sad", "tired", "hungry", "thirsty", "angry", "nervous",
        "lonely", "proud", "jealous", "relieved", "excited", "bored",
        "weather", "rain", "snow", "wind", "sun", "sunny", "cold", "hot",
        "morning", "evening", "night", "afternoon", "week", "month", "year",
        "family", "mom", "dad", "mother", "father", "brother", "sister",
        "friend", "friends", "school", "work", "job", "boss", "teacher",
        "money", "save", "spend", "buy", "bought", "shopping", "food",
        "music", "song", "movie", "show", "game", "games", "book", "read",
        "phone", "computer", "internet", "technology", "app", "dog", "cat",
        "pet", "animal", "travel", "trip", "vacation", "holiday", "party",
        "birthday", "celebrate", "congratulations", "sorry", "apologize",
        "help", "advice", "opinion", "agree", "disagree", "right", "wrong",
        "true", "false", "maybe", "perhaps", "really", "very", "so", "too",
        "also", "again", "still", "already", "just", "only", "even",
    }

    SWAHILI_MARKERS = {
        "habari", "jambo", "mambo", "salama", "nzuri", "asubuhi", "mchana",
        "jioni", "usiku", "asante", "tafadhali", "ndiyo", "hapana", "ndio",
        "wewe", "wako", "mimi", "yangu", "sisi", "wetu", "wao", "yeye",
        "nini", "vipi", "lini", "wapi", "kwa nini", "nani", "je",
        "naitwa", "jina", "leo", "kesho", "jana", "saa", "tarehe",
        "ninataka", "napenda", "ninapenda", "unataka", "unapenda",
        "habari yako", "freshi", "poa", "sawa", "karibu", "kwaheri",
        "lala", "salama", "nzuri", "mbaya", "vizuri", "hadithi", "shairi",
        "utani", "soma", "andika", "samahani", "pole", "haya", "sawa",
        "na", "ya", "wa", "la", "kwa", "ni", "si", "kama", "lakini",
        "hii", "hiyo", "huyu", "yule", "mzuri", "mbovu", "kucheza",
        "nahitaji", "nataka", "nafikiri", "ninafikiri", "najua", "ninajua",
        "ninaona", "naona", "tafuta", "natafuta", "fanya", "ninafanya",
        "kazi", "shule", "mwalimu", "bosi", "familia", "mama", "baba",
        "kaka", "dada", "rafiki", "marafiki", "pesa", "kununua", "duka",
        "chakula", "muziki", "wimbo", "filamu", "kipindi", "mchezo",
        "kitabu", "simu", "kompyuta", "mtandao", "mbwa", "paka", "mnyama",
        "safari", "likizo", "sherehe", "siku ya kuzaliwa", "hongera",
        "msaada", "ushauri", "mtazamo", "nakubaliana", "sikubaliani",
        "kweli", "uongo", "sana", "tena", "bado", "tayari", "tu", "pia",
        "njaa", "kiu", "hasira", "wasiwasi", "upweke", "fahari", "wivu",
        "furaha", "huzuni", "uchovu", "hewa", "mvua", "theluji", "upepo",
        "jua", "baridi", "joto", "wiki", "mwezi", "mwaka",
    }

    FRENCH_MARKERS = {
        "bonjour", "salut", "bonsoir", "merci", "svp", "oui", "non",
        "comment", "quoi", "pourquoi", "quand", "où", "qui", "combien",
        "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "moi",
        "toi", "mon", "ma", "mes", "ton", "ta", "tes", "votre", "vos",
        "le", "la", "les", "un", "une", "des", "de", "du", "et", "ou",
        "mais", "pas", "ne", "est", "sont", "suis", "es", "sommes",
        "êtes", "avoir", "ai", "as", "avons", "avez", "ont", "être",
        "aujourd'hui", "demain", "hier", "heure", "date", "nom",
        "histoire", "poème", "blague", "raconte", "dis", "veux", "aime",
        "s'il", "vous plaît", "au revoir", "comment allez", "ça va",
        "très", "bien", "mal", "content", "triste", "pourriez",
        "vais", "va", "vas", "allons", "allez", "vont", "aller",
        "veux", "veut", "voulons", "voulez", "veulent", "vouloir",
        "sais", "sait", "savons", "savez", "savent", "savoir",
        "fais", "fait", "faisons", "faites", "font", "faire",
        "travail", "école", "professeur", "patron", "famille", "mère",
        "père", "frère", "sœur", "ami", "amis", "argent", "acheter",
        "magasin", "nourriture", "musique", "chanson", "film", "série",
        "jeu", "jeux", "livre", "lire", "téléphone", "ordinateur",
        "internet", "chien", "chat", "animal", "voyage", "vacances",
        "fête", "anniversaire", "félicitations", "pardon", "excuse",
        "aide", "conseil", "avis", "accord", "vrai", "faux", "encore",
        "déjà", "juste", "seulement", "même", "aussi", "beaucoup",
        "faim", "soif", "colère", "anxieux", "seul", "fier", "jaloux",
        "heureux", "triste", "fatigué", "météo", "pluie", "neige",
        "vent", "soleil", "froid", "chaud", "semaine", "mois", "année",
    }

    @staticmethod
    def _tokenize(text: str):
        return re.findall(r"[a-zàâäéèêëïîôöùûüÿçñ']+", text.lower())

    def detect(self, text: str) -> str:
        """Returns 'en', 'sw', or 'fr'. Defaults to 'en' on a tie or
        if nothing matches (since English is this bot's primary
        language and most ambiguous short inputs are English)."""
        tokens = set(self._tokenize(text))
        if not tokens:
            return "en"

        en_score = len(tokens & self.ENGLISH_MARKERS)
        sw_score = len(tokens & self.SWAHILI_MARKERS)
        fr_score = len(tokens & self.FRENCH_MARKERS)

        scores = {"en": en_score, "sw": sw_score, "fr": fr_score}
        best_lang = max(scores, key=scores.get)

        if scores[best_lang] == 0:
            return "en"
        return best_lang


# ==============================================================================
# SECTION 7C: KEYWORD TOPIC MATCHER (flexible, anywhere-in-sentence matching)
# ==============================================================================

class KeywordTopicMatcher:
    """
    A flexible companion to the strict IntentEngine. Instead of requiring
    a whole sentence to match a specific regex shape, this matcher looks
    for the PRESENCE of topic keywords anywhere in the message - in any
    of English, Swahili, or French - and maps them to the same topic
    label the rest of the bot already understands (e.g. 'joke',
    'weather_smalltalk', 'feelings_sad').

    This intentionally trades precision for flexibility: a message like
    "lol I could really use a joke right now man" won't match any of the
    IntentEngine's strict regexes, but it DOES contain the keyword
    "joke", so this matcher recognizes the topic anyway.

    Design: each topic maps to a set of keywords/phrases per language.
    A topic "fires" if ANY of its keywords appears as a whole word (or
    exact phrase, for multi-word keywords) anywhere in the message. This
    is still 100% rigid dictionary lookup - no fuzzy scoring, no
    statistics, no learning.

    This matcher is consulted as a FALLBACK after the strict IntentEngine
    finds no match, so precise commands still behave exactly as before;
    this only broadens what counts as "good enough" once strict matching
    has already failed.
    """

    # Each topic: {"en": [...], "sw": [...], "fr": [...]}
    # Keywords are matched as whole words/phrases (word-boundary aware),
    # case-insensitively, with the LanguageDetector also using a copy of
    # this same vocabulary indirectly (related, but a separate concern).
    TOPICS = {
        "joke": {
            "en": ["joke", "jokes", "funny", "make me laugh", "something funny"],
            "sw": ["utani", "kuchekesha", "nichekeshe", "mzaha"],
            "fr": ["blague", "blagues", "drôle", "fais-moi rire", "rigoler"],
        },
        "quote": {
            "en": ["quote", "quotes", "inspire me", "inspirational", "wisdom"],
            "sw": ["nukuu", "maneno ya hekima", "nitie moyo", "hekima"],
            "fr": ["citation", "citations", "inspire-moi", "sagesse"],
        },
        "riddle": {
            "en": ["riddle", "riddles", "puzzle me", "brain teaser"],
            "sw": ["kitendawili", "vitendawili"],
            "fr": ["devinette", "devinettes", "énigme"],
        },
        "trivia": {
            "en": ["trivia", "quiz", "quiz me", "test my knowledge"],
            "sw": ["maswali", "jaribu maarifa yangu"],
            "fr": ["quiz", "questions", "teste mes connaissances"],
        },
        "story": {
            "en": ["story", "stories", "tale", "narrate", "story time"],
            "sw": ["hadithi", "hadithi za", "niambie hadithi"],
            "fr": ["histoire", "histoires", "conte", "raconte-moi une histoire", "raconte une histoire"],
        },
        "poem": {
            "en": ["poem", "poetry", "haiku", "acrostic", "verse"],
            "sw": ["shairi", "mashairi", "tungo"],
            "fr": ["poème", "poèmes", "poésie", "vers"],
        },
        "time_query": {
            "en": ["what time", "current time", "clock"],
            "sw": ["saa ngapi", "muda gani", "saa sasa"],
            "fr": ["quelle heure", "heure actuelle"],
        },
        "date_query": {
            "en": ["what date", "today's date", "what day is it"],
            "sw": ["tarehe gani", "leo ni tarehe"],
            "fr": ["quelle date", "quel jour"],
        },
        "weather_smalltalk": {
            "en": ["weather", "sunny", "nice out", "weather like"],
            "sw": ["hali ya hewa", "jua"],
            "fr": ["météo", "il fait beau"],
        },
        "feelings_happy": {
            "en": ["i'm happy", "i am happy", "feeling great", "i'm so glad", "excited",
                   "feeling happy", "really happy", "so happy", "feeling good",
                   "i am very happy", "i'm very happy", "very happy", "quite happy", "extremely happy"],
            "sw": ["nina furaha", "nimefurahi", "ninafuraha", "nina shangwe", "furaha sana"],
            "fr": ["je suis content", "je suis heureux", "je suis ravi", "content", "très content", "si heureux"],
        },
        "feelings_sad": {
            "en": ["i'm sad", "i am sad", "feeling down", "unhappy", "depressed", "feeling sad", "so sad", "really sad"],
            "sw": ["nina huzuni", "nimehuzunika", "sina furaha"],
            "fr": ["je suis triste", "je ne suis pas bien", "je suis déprimé", "très triste", "si triste"],
        },
        "feelings_tired": {
            "en": ["i'm tired", "i am tired", "exhausted", "sleepy", "need sleep", "feeling tired", "so tired", "really tired"],
            "sw": ["nimechoka", "nina usingizi", "nahisi uchovu", "uchovu sana"],
            "fr": ["je suis fatigué", "épuisé", "j'ai sommeil", "très fatigué", "si fatigué"],
        },
        "compliment_topic": {
            "en": ["you're great", "you're awesome", "good job", "well done", "i like you"],
            "sw": ["wewe ni mzuri", "umefanya vizuri", "ninakupenda"],
            "fr": ["tu es génial", "bien joué", "je t'aime bien"],
        },
        "gratitude": {
            "en": ["thank you", "thanks", "appreciate it", "much appreciated"],
            "sw": ["asante", "nashukuru", "ahsante"],
            "fr": ["merci", "je te remercie", "merci beaucoup"],
        },
        "farewell_topic": {
            "en": ["bye", "goodbye", "see you", "talk later", "gotta go"],
            "sw": ["kwaheri", "tutaonana", "nakwenda"],
            "fr": ["au revoir", "à bientôt", "salut", "je dois partir"],
        },
        "greeting_topic": {
            "en": ["hello", "hi there", "hey"],
            "sw": ["habari", "jambo", "mambo"],
            "fr": ["bonjour", "salut", "bonsoir", "coucou"],
        },
        "how_are_you_topic": {
            "en": ["how are you", "how's it going", "how have you been"],
            "sw": ["habari yako", "hujambo", "mambo vipi", "u hali gani"],
            "fr": ["comment vas-tu", "comment ça va", "ça va"],
        },
        "todo_topic": {
            "en": ["to-do list", "todo list", "my tasks", "things to do", "reminder"],
            "sw": ["orodha ya kazi", "kazi zangu", "nikumbushe"],
            "fr": ["liste de tâches", "mes tâches", "rappelle-moi"],
        },
        "hangman_topic": {
            "en": ["hangman", "word game", "guessing game"],
            "sw": ["mchezo wa maneno", "mchezo wa kubahatisha"],
            "fr": ["jeu du pendu", "jeu de devinette"],
        },
        "help_topic": {
            "en": ["help", "what can you do", "commands", "options"],
            "sw": ["msaada", "unaweza kufanya nini", "amri"],
            "fr": ["aide", "que peux-tu faire", "commandes"],
        },
        "math_topic": {
            "en": ["calculate", "math", "arithmetic", "what is", "plus", "minus", "times"],
            "sw": ["hesabu", "jumlisha", "toa", "zidisha"],
            "fr": ["calculer", "mathématiques", "addition", "soustraction"],
        },
        "age_topic": {
            "en": ["how old", "my age", "calculate my age"],
            "sw": ["umri gani", "umri wangu"],
            "fr": ["quel âge", "mon âge", "calculer mon âge"],
        },

        # --- Additional smalltalk topics (added for broader, more
        # flexible everyday conversation coverage) ---

        "food_hungry": {
            "en": ["i'm hungry", "i am hungry", "feeling hungry", "want to eat", "what should i eat", "favorite food", "love food", "starving"],
            "sw": ["nina njaa", "ninataka kula", "nile nini", "chakula ninachopenda", "ninakufa kwa njaa"],
            "fr": ["j'ai faim", "je veux manger", "que devrais-je manger", "plat préféré", "j'adore la nourriture", "je meurs de faim"],
        },
        "food_thirsty": {
            "en": ["i'm thirsty", "i am thirsty", "need water", "want a drink"],
            "sw": ["nina kiu", "nahitaji maji", "nataka kinywaji"],
            "fr": ["j'ai soif", "j'ai besoin d'eau", "je veux boire"],
        },
        "hobbies_topic": {
            "en": ["my hobby", "my hobbies", "what i like to do", "free time", "spare time"],
            "sw": ["hobby yangu", "ninavyofurahia", "muda wa mapumziko"],
            "fr": ["mon passe-temps", "mes loisirs", "ce que j'aime faire", "temps libre"],
        },
        "family_topic": {
            "en": ["my family", "my mom", "my dad", "my mother", "my father", "my brother", "my sister", "my parents"],
            "sw": ["familia yangu", "mama yangu", "baba yangu", "kaka yangu", "dada yangu", "wazazi wangu"],
            "fr": ["ma famille", "ma mère", "mon père", "mon frère", "ma sœur", "mes parents"],
        },
        "work_school_topic": {
            "en": ["my job", "my work", "my boss", "my school", "my class", "my teacher", "homework", "exam", "studying"],
            "sw": ["kazi yangu", "bosi wangu", "shule yangu", "darasa langu", "mwalimu wangu", "kazi ya nyumbani", "mtihani", "kusoma"],
            "fr": ["mon travail", "mon patron", "mon école", "ma classe", "mon professeur", "devoirs", "examen", "étudier"],
        },
        "agreement_topic": {
            "en": ["i agree", "you're right", "exactly", "totally agree"],
            "sw": ["nakubaliana", "una haki", "hasa", "kabisa"],
            "fr": ["je suis d'accord", "tu as raison", "exactement"],
        },
        "disagreement_topic": {
            "en": ["i disagree", "that's not true", "you're wrong", "i don't think so", "not really"],
            "sw": ["sikubaliani", "si kweli", "umekosea", "sidhani hivyo", "siyo kweli"],
            "fr": ["je ne suis pas d'accord", "ce n'est pas vrai", "tu as tort", "je ne pense pas"],
        },
        "apology_topic": {
            "en": ["i'm sorry", "i apologize", "my bad", "my mistake", "sorry about that"],
            "sw": ["pole", "samahani", "nimekosea", "ni kosa langu"],
            "fr": ["je suis désolé", "je m'excuse", "ma faute", "pardon"],
        },
        "boredom_topic": {
            "en": ["i'm bored", "i am bored", "so boring", "nothing to do", "bored out of my mind", "so bored", "really bored", "extremely bored"],
            "sw": ["nimechoshwa", "inachosha", "sina la kufanya"],
            "fr": ["je m'ennuie", "c'est ennuyeux", "rien à faire"],
        },
        "love_relationships_topic": {
            "en": ["my girlfriend", "my boyfriend", "my partner", "my spouse", "my husband", "my wife", "in love", "relationship advice"],
            "sw": ["mpenzi wangu", "mke wangu", "mume wangu", "nipo kwenye mapenzi", "ushauri wa mahusiano"],
            "fr": ["ma copine", "mon copain", "mon partenaire", "mon mari", "ma femme", "amoureux", "conseils relationnels"],
        },
        "music_topic": {
            "en": ["favorite song", "favorite music", "favorite artist", "listening to music", "love music",
                   "jazz", "guitar", "piano", "drums", "concert", "album", "play an instrument", "making music"],
            "sw": ["wimbo ninaopenda", "muziki ninaopenda", "msanii ninaopenda", "ninasikiliza muziki"],
            "fr": ["chanson préférée", "musique préférée", "artiste préféré", "j'écoute de la musique"],
        },
        "sports_topic": {
            "en": ["favorite sport", "favorite team", "watching the game", "football", "basketball", "soccer",
                   "rugby", "cricket", "tennis", "volleyball", "the match", "national team", "sports"],
            "sw": ["mchezo ninaopenda", "timu ninayopenda", "kutazama mechi", "mpira wa miguu", "mpira wa kikapu"],
            "fr": ["sport préféré", "équipe préférée", "regarder le match", "football", "basket-ball"],
        },
        "books_topic": {
            "en": ["favorite book", "reading a book", "love reading", "good book to read"],
            "sw": ["kitabu ninachopenda", "kusoma kitabu", "ninapenda kusoma", "kitabu kizuri cha kusoma"],
            "fr": ["livre préféré", "lire un livre", "j'adore lire", "bon livre à lire"],
        },
        "technology_topic": {
            "en": ["my phone", "my computer", "new technology", "favorite app", "love coding", "learning to code"],
            "sw": ["simu yangu", "kompyuta yangu", "teknolojia mpya", "programu ninayopenda", "ninapenda kuandika programu"],
            "fr": ["mon téléphone", "mon ordinateur", "nouvelle technologie", "application préférée", "j'aime coder"],
        },
        "pets_animals_topic": {
            "en": ["my dog", "my cat", "my pet", "favorite animal", "love animals"],
            "sw": ["mbwa wangu", "paka wangu", "mnyama wangu", "mnyama ninaopenda", "ninapenda wanyama"],
            "fr": ["mon chien", "mon chat", "mon animal", "animal préféré", "j'aime les animaux"],
        },
        "travel_topic": {
            "en": ["want to travel", "favorite place", "been to", "planning a trip", "love traveling"],
            "sw": ["nataka kusafiri", "mahali ninayopenda", "nimefika", "kupanga safari", "ninapenda kusafiri"],
            "fr": ["je veux voyager", "endroit préféré", "déjà allé", "planifier un voyage", "j'aime voyager"],
        },
        "health_topic": {
            "en": ["i'm sick", "i feel ill", "not feeling well", "have a headache", "feeling under the weather"],
            "sw": ["mimi ni mgonjwa", "sijisikii vizuri", "nina maumivu ya kichwa"],
            "fr": ["je suis malade", "je ne me sens pas bien", "j'ai mal à la tête"],
        },
        "money_topic": {
            "en": ["need money", "save money", "spending too much", "financial advice", "budgeting"],
            "sw": ["nahitaji pesa", "kuokoa pesa", "kutumia pesa nyingi", "ushauri wa kifedha", "bajeti"],
            "fr": ["besoin d'argent", "économiser de l'argent", "dépenser trop", "conseils financiers", "budget"],
        },
        "birthday_topic": {
            "en": ["my birthday", "it's my birthday", "birthday today", "happy birthday to me"],
            "sw": ["siku yangu ya kuzaliwa", "leo ni siku yangu ya kuzaliwa", "heri ya kuzaliwa kwangu"],
            "fr": ["mon anniversaire", "c'est mon anniversaire", "joyeux anniversaire à moi"],
        },
        "confusion_topic": {
            "en": ["i'm confused", "i don't understand", "this is confusing", "i'm lost", "what do you mean", "so confused", "really confused"],
            "sw": ["nimechanganyikiwa", "sielewi", "hii inachanganya", "nimepotea"],
            "fr": ["je suis confus", "je ne comprends pas", "c'est confus", "je suis perdu"],
        },
        "encouragement_topic": {
            "en": ["i can't do this", "i'm not good enough", "i give up", "i'm a failure", "i'm struggling"],
            "sw": ["siwezi kufanya hili", "sina uwezo wa kutosha", "nakata tamaa", "ninapambana"],
            "fr": ["je n'y arrive pas", "je ne suis pas assez bien", "j'abandonne", "je galère"],
        },
        "congratulations_topic": {
            "en": ["i got the job", "i passed", "i won", "i succeeded", "great news", "good news"],
            "sw": ["nimepata kazi", "nimefaulu", "nimeshinda", "habari njema"],
            "fr": ["j'ai eu le poste", "j'ai réussi", "j'ai gagné", "bonne nouvelle"],
        },
        "surprise_topic": {
            "en": ["wow really", "i can't believe it", "no way", "that's surprising", "are you serious"],
            "sw": ["loo kweli", "siwezi kuamini", "haiwezekani", "hiyo inashangaza"],
            "fr": ["wow vraiment", "je n'arrive pas à le croire", "pas possible", "c'est surprenant"],
        },
        "small_request_topic": {
            "en": ["can you help me", "could you help", "i need help", "i need your help"],
            "sw": ["unaweza kunisaidia", "nahitaji msaada", "nahitaji msaada wako"],
            "fr": ["peux-tu m'aider", "pourrais-tu aider", "j'ai besoin d'aide", "j'ai besoin de ton aide"],
        },
        "bot_identity_curiosity": {
            "en": ["are you real", "are you a robot", "are you human", "do you have feelings", "are you alive"],
            "sw": ["wewe ni wa kweli", "wewe ni roboti", "wewe ni binadamu", "una hisia", "uko hai"],
            "fr": ["es-tu réel", "es-tu un robot", "es-tu humain", "as-tu des sentiments", "es-tu vivant"],
        },
        "goodnight_topic": {
            "en": ["good night", "going to bed", "time for bed", "sleep well"],
            "sw": ["lala salama", "ninakwenda kulala", "ni wakati wa kulala"],
            "fr": ["bonne nuit", "je vais me coucher", "il est temps de dormir"],
        },
        "good_morning_topic": {
            "en": ["good morning", "morning everyone", "just woke up", "rise and shine"],
            "sw": ["habari za asubuhi", "asubuhi njema", "nimeamka tu"],
            "fr": ["bonjour à tous", "je viens de me réveiller", "bonne matinée"],
        },
        "good_evening_topic": {
            "en": ["good evening", "evening everyone"],
            "sw": ["habari za jioni", "jioni njema"],
            "fr": ["bonsoir à tous", "bonne soirée"],
        },
        "weekend_topic": {
            "en": ["happy weekend", "weekend plans", "it's the weekend", "thank god it's friday"],
            "sw": ["furaha ya wikendi", "mipango ya wikendi", "leo ni wikendi"],
            "fr": ["bon week-end", "plans pour le week-end", "c'est le week-end"],
        },
        "weather_cold_topic": {
            "en": ["it's cold", "freezing outside", "so cold today"],
            "sw": ["ni baridi", "baridi sana nje", "leo ni baridi"],
            "fr": ["il fait froid", "il gèle dehors", "il fait si froid aujourd'hui"],
        },
        "weather_hot_topic": {
            "en": ["it's hot", "so hot today", "boiling outside"],
            "sw": ["ni joto", "leo ni joto sana", "joto sana nje"],
            "fr": ["il fait chaud", "il fait si chaud aujourd'hui"],
        },

        # --- Third wave of additional smalltalk topics ---

        "weather_rain_topic": {
            "en": ["it's raining", "pouring outside", "rainy day"],
            "sw": ["mvua inanyesha", "mvua nyingi nje", "siku ya mvua"],
            "fr": ["il pleut", "il pleut des cordes", "journée pluvieuse"],
        },
        "weather_snow_topic": {
            "en": ["it's snowing", "snow outside", "snowy day"],
            "sw": ["theluji inanyesha", "theluji nje"],
            "fr": ["il neige", "neige dehors", "journée neigeuse"],
        },
        "weather_windy_topic": {
            "en": ["it's windy", "so windy today", "strong wind outside"],
            "sw": ["upepo mkali", "upepo mkali leo"],
            "fr": ["il y a du vent", "il fait très venteux"],
        },
        "holiday_smalltalk": {
            "en": ["happy holidays", "merry christmas", "happy new year", "happy easter", "festive season"],
            "sw": ["sikukuu njema", "krismasi njema", "mwaka mpya mwema", "pasaka njema"],
            "fr": ["joyeuses fêtes", "joyeux noël", "bonne année", "joyeuses pâques"],
        },
        "learning_topic": {
            "en": ["learning something new", "trying to learn", "want to learn", "picking up a new skill"],
            "sw": ["kujifunza kitu kipya", "ninajaribu kujifunza", "nataka kujifunza", "kujifunza ujuzi mpya"],
            "fr": ["apprendre quelque chose de nouveau", "j'essaie d'apprendre", "je veux apprendre", "acquérir une nouvelle compétence"],
        },
        "motivation_goals_topic": {
            "en": ["my goals", "working towards", "trying to achieve", "my dream", "my ambition"],
            "sw": ["malengo yangu", "ninajitahidi kufikia", "ninajaribu kufanikisha", "ndoto yangu"],
            "fr": ["mes objectifs", "je travaille vers", "j'essaie d'atteindre", "mon rêve", "mon ambition"],
        },
        "nostalgia_topic": {
            "en": ["i miss the old days", "back in the day", "i remember when", "those were good times"],
            "sw": ["ninakumbuka siku za zamani", "zamani", "nakumbuka wakati"],
            "fr": ["je regrette le passé", "à l'époque", "je me souviens quand"],
        },
        "future_plans_topic": {
            "en": ["my plans for", "looking forward to", "can't wait for", "planning to"],
            "sw": ["mipango yangu ya", "ninatazamia", "siwezi kusubiri", "ninapanga"],
            "fr": ["mes plans pour", "j'ai hâte de", "je ne peux pas attendre", "je prévois de"],
        },
        "gaming_topic": {
            "en": ["playing video games", "favorite game", "love gaming", "video games"],
            "sw": ["kucheza michezo ya video", "mchezo ninaopenda", "ninapenda michezo ya video"],
            "fr": ["jouer aux jeux vidéo", "jeu préféré", "j'adore les jeux vidéo"],
        },
        "cooking_topic": {
            "en": ["cooking dinner", "trying a recipe", "love cooking", "what should i cook",
                   "cooking", "to cook", "recipe", "recipes", "baking"],
            "sw": ["kupika chakula cha jioni", "kujaribu mlo", "ninapenda kupika", "nipike nini"],
            "fr": ["je cuisine le dîner", "j'essaie une recette", "j'adore cuisiner", "que devrais-je cuisiner"],
        },
        "nature_outdoors_topic": {
            "en": ["going for a walk", "love nature", "outdoor activities", "hiking"],
            "sw": ["kutembea nje", "ninapenda asili", "shughuli za nje", "kutembea milimani"],
            "fr": ["je vais faire une promenade", "j'adore la nature", "activités de plein air", "randonnée"],
        },
        "sleep_dreams_topic": {
            "en": ["had a weird dream", "couldn't sleep", "trouble sleeping", "strange dream"],
            "sw": ["nimeota ndoto ya ajabu", "sikulala", "tatizo la kulala"],
            "fr": ["j'ai fait un rêve bizarre", "je n'ai pas pu dormir", "difficulté à dormir"],
        },
        "humor_appreciation_topic": {
            "en": ["that's funny", "haha that's good", "lol", "you made me laugh", "that's hilarious"],
            "sw": ["hiyo ni ya kuchekesha", "haha nzuri", "umenichekesha"],
            "fr": ["c'est drôle", "haha c'est bon", "tu m'as fait rire", "c'est hilarant"],
        },
        "skepticism_topic": {
            "en": ["i doubt it", "not sure i believe that", "sounds fake", "is that even true"],
            "sw": ["ninatilia shaka", "sina hakika naamini hilo", "inasikika si ya kweli"],
            "fr": ["j'en doute", "pas sûr d'y croire", "ça sonne faux"],
        },
        "filler_acknowledgement_topic": {
            "en": ["okay cool", "alright then", "yeah sure", "got it thanks", "that makes sense", "ah i see"],
            "sw": ["sawa basi", "vizuri basi", "ndiyo sawa", "nimeelewa"],
            "fr": ["d'accord cool", "très bien alors", "oui d'accord", "compris merci"],
        },
        "opinion_request_topic": {
            "en": ["what do you think about", "your opinion on", "what's your take on"],
            "sw": ["unafikiri nini kuhusu", "mtazamo wako kuhusu", "una mtazamo gani kuhusu"],
            "fr": ["qu'en penses-tu", "ton avis sur", "quel est ton avis sur"],
        },
        "advice_request_topic": {
            "en": ["what should i do", "any advice", "what would you do", "need some advice"],
            "sw": ["nifanye nini", "una ushauri", "ungefanya nini", "nahitaji ushauri"],
            "fr": ["que devrais-je faire", "des conseils", "que ferais-tu", "j'ai besoin de conseils"],
        },
        "comparison_topic": {
            "en": ["which is better", "compare", "versus", "difference between"],
            "sw": ["ni kipi bora", "linganisha", "tofauti kati ya"],
            "fr": ["lequel est mieux", "comparer", "différence entre"],
        },
        "feelings_angry_topic": {
            "en": ["i'm angry", "i am angry", "so frustrated", "this is annoying", "makes me mad", "so angry", "really angry"],
            "sw": ["nimekasirika", "nina hasira", "inasumbua"],
            "fr": ["je suis en colère", "tellement frustré", "ça m'énerve"],
        },
        "feelings_nervous_topic": {
            "en": ["i'm nervous", "i am nervous", "feeling anxious", "so nervous about", "so nervous", "really nervous"],
            "sw": ["nina wasiwasi", "ninahisi wasiwasi", "nina hofu kuhusu"],
            "fr": ["je suis nerveux", "je suis anxieux", "j'ai le trac pour"],
        },
        "anxiety_topic": {
            "en": ["anxiety", "anxious thoughts", "panic attack", "panicking",
                   "overthinking", "racing thoughts", "can't stop worrying",
                   "constant worry", "on edge", "stressful", "stressed out",
                   "overwhelmed", "worried", "so anxious", "i'm anxious",
                   "i am anxious", "worrying", "i feel anxious",
                   "my heart races", "heart racing", "racing heart",
                   "my heart pounds", "pounding heart", "heart is racing",
                   "i'm so nervous", "i am so nervous", "anxiety attack"],
            "sw": ["wasiwasi mkubwa", "hofu ya ghafla", "mawazo mengi",
                   "siwezi kuacha kuwa na wasiwasi"],
            "fr": ["anxiété", "crise d'angoisse", "pensées qui tournent en boucle",
                   "je n'arrive pas à arrêter de m'inquiéter", "sur les nerfs"],
        },
        "feelings_lonely_topic": {
            "en": ["i feel lonely", "i'm lonely", "feeling alone", "nobody to talk to", "so lonely", "really lonely"],
            "sw": ["ninahisi upweke", "nina upweke", "sina mtu wa kuongea naye"],
            "fr": ["je me sens seul", "je suis seul", "personne à qui parler"],
        },
        "feelings_proud_topic": {
            "en": ["i'm proud of myself", "feeling proud", "i'm proud that", "proud of my", "so proud", "really proud"],
            "sw": ["ninajivunia mwenyewe", "ninahisi fahari", "ninajivunia"],
            "fr": ["je suis fier de moi", "je me sens fier", "fier de mon"],
        },
        "feelings_jealous_topic": {
            "en": ["i'm jealous", "i am jealous", "feeling jealous", "feel jealous",
                   "so jealous", "envious of", "i'm envious", "i am envious"],
            "sw": ["nina wivu", "ninahisi wivu", "wivu mwingi"],
            "fr": ["je suis jaloux", "je me sens jaloux", "envieux de", "tellement jaloux"],
        },
        "feelings_relieved_topic": {
            "en": ["what a relief", "feeling relieved", "so relieved", "glad that's over"],
            "sw": ["nafuu kiasi gani", "ninahisi nafuu", "nafurahi imeshapita"],
            "fr": ["quel soulagement", "je me sens soulagé", "content que ce soit fini"],
        },
        "bot_capability_curiosity_topic": {
            "en": ["what languages do you speak", "can you speak swahili", "can you speak french", "do you understand other languages"],
            "sw": ["unaongea lugha gani", "unaweza kuongea kiswahili", "unaweza kuongea kifaransa"],
            "fr": ["quelles langues parles-tu", "peux-tu parler swahili", "peux-tu parler français"],
        },
        "small_talk_weather_check_topic": {
            "en": ["nice weather today", "lovely day", "beautiful day outside"],
            "sw": ["hali ya hewa nzuri leo", "siku nzuri", "siku nzuri nje"],
            "fr": ["belle météo aujourd'hui", "belle journée", "belle journée dehors"],
        },
        "introduction_request_topic": {
            "en": ["introduce yourself", "tell me about yourself", "who made you"],
            "sw": ["jitambulishe", "niambie kuhusu wewe", "nani alikutengeneza"],
            "fr": ["présente-toi", "parle-moi de toi", "qui t'a créé"],
        },
        "small_talk_busy_topic": {
            "en": ["so busy lately", "been really busy", "a lot going on"],
            "sw": ["nina shughuli nyingi siku hizi", "nimekuwa na shughuli nyingi"],
            "fr": ["tellement occupé dernièrement", "j'ai été vraiment occupé"],
        },

        # --- Fourth wave of additional smalltalk topics ---

        "politeness_please_topic": {
            "en": ["please", "if you don't mind", "if you could"],
            "sw": ["tafadhali", "ikiwa hauna shida"],
            "fr": ["s'il te plaît", "si ça ne te dérange pas"],
        },
        "exercise_fitness_topic": {
            "en": ["going to the gym", "working out", "exercise routine", "trying to get fit", "went for a run"],
            "sw": ["kwenda gym", "kufanya mazoezi", "ratiba ya mazoezi", "kukimbia"],
            "fr": ["aller à la salle de sport", "faire de l'exercice", "routine d'exercice", "je suis allé courir"],
        },
        "mental_health_checkin_topic": {
            "en": ["taking care of my mental health", "feeling overwhelmed", "need a mental break", "my mental health"],
            "sw": ["kujali afya yangu ya akili", "ninahisi nimezidiwa", "nahitaji mapumziko ya akili"],
            "fr": ["prendre soin de ma santé mentale", "je me sens dépassé", "j'ai besoin d'une pause mentale"],
        },
        "gratitude_for_bot_topic": {
            "en": ["thanks for listening", "thanks for being here", "glad i can talk to you", "appreciate you listening"],
            "sw": ["asante kwa kusikiliza", "asante kwa kuwa hapa", "nafurahi naweza kuongea na wewe"],
            "fr": ["merci de m'écouter", "merci d'être là", "content de pouvoir te parler"],
        },
        "repeat_clarify_topic": {
            "en": ["can you repeat that", "say that again", "what did you say", "come again"],
            "sw": ["unaweza kurudia hilo", "sema tena", "ulisema nini"],
            "fr": ["peux-tu répéter ça", "dis-le encore", "qu'as-tu dit"],
        },
        "small_celebration_topic": {
            "en": ["we did it", "let's celebrate", "this calls for celebration", "cheers to that"],
            "sw": ["tumefanya", "tusherehekee", "hii inahitaji sherehe"],
            "fr": ["on l'a fait", "célébrons", "ça appelle une célébration"],
        },
        "forecast_question_topic": {
            "en": ["will it rain tomorrow", "what's the forecast", "weather forecast"],
            "sw": ["mvua itanyesha kesho", "utabiri wa hewa ukoje"],
            "fr": ["va-t-il pleuvoir demain", "quelles sont les prévisions"],
        },
        "language_practice_topic": {
            "en": ["practicing my french", "practicing my swahili", "learning a new language", "trying to speak"],
            "sw": ["ninajizoeza kifaransa", "ninajizoeza kiingereza", "kujifunza lugha mpya"],
            "fr": ["je pratique mon anglais", "je pratique mon swahili", "apprendre une nouvelle langue"],
        },
        "bot_age_location_topic": {
            "en": ["how old are you", "where do you live", "where are you from", "where are you located"],
            "sw": ["una umri gani", "unaishi wapi", "unatoka wapi"],
            "fr": ["quel âge as-tu", "où habites-tu", "d'où viens-tu"],
        },
        "bot_name_opinion_topic": {
            "en": ["i like your name", "your name is cool", "nice name"],
            "sw": ["ninapenda jina lako", "jina lako ni zuri"],
            "fr": ["j'aime ton nom", "ton nom est cool", "joli nom"],
        },
        "slow_down_topic": {
            "en": ["slow down", "wait a second", "hold on", "one moment"],
            "sw": ["punguza mwendo", "subiri kidogo", "ngoja"],
            "fr": ["ralentis", "attends une seconde", "un instant"],
        },
        "awkward_pause_topic": {
            "en": ["um", "uh", "hmm", "well then", "anyway"],
            "sw": ["mh", "hivyo basi", "kwa hiyo"],
            "fr": ["euh", "hum", "bon alors", "bref"],
        },
        "compliment_response_topic": {
            "en": ["good answer", "that was helpful", "nice response", "well explained"],
            "sw": ["jibu zuri", "hiyo ilikuwa msaada", "jibu nzuri"],
            "fr": ["bonne réponse", "c'était utile", "bien expliqué"],
        },
        "remember_specific_topic": {
            "en": ["remember this for later", "don't forget this", "keep this in mind"],
            "sw": ["kumbuka hili kwa baadaye", "usisahau hili", "weka hili akilini"],
            "fr": ["souviens-toi de ça pour plus tard", "n'oublie pas ça", "garde ça en tête"],
        },
        "today_plans_topic": {
            "en": ["my plans for today", "today i'm going to", "today i have to"],
            "sw": ["mipango yangu ya leo", "leo nitafanya", "leo ninahitaji"],
            "fr": ["mes plans pour aujourd'hui", "aujourd'hui je vais", "aujourd'hui je dois"],
        },
        "technology_complaint_topic": {
            "en": ["my phone is so slow", "internet is down", "computer crashed", "technology is frustrating"],
            "sw": ["simu yangu ni ya polepole", "intaneti imekatika", "kompyuta imeharibika"],
            "fr": ["mon téléphone est si lent", "internet est en panne", "l'ordinateur a planté"],
        },
        "aspirations_dreams_topic": {
            "en": ["my dream is to", "i've always wanted to", "someday i want to", "my biggest dream"],
            "sw": ["ndoto yangu ni", "nimekuwa nikitaka", "siku moja nataka"],
            "fr": ["mon rêve est de", "j'ai toujours voulu", "un jour je veux"],
        },
        "missing_someone_topic": {
            "en": ["i miss her", "i miss him", "i miss them", "miss my friend", "miss my family"],
            "sw": ["ninamkosa", "ninawakosa", "ninamkosa rafiki yangu", "ninaikosa familia yangu"],
            "fr": ["elle me manque", "il me manque", "ils me manquent", "mon ami me manque"],
        },
        "excitement_event_topic": {
            "en": ["so excited for", "can't wait for", "really looking forward to", "counting down to"],
            "sw": ["nimevutiwa sana na", "siwezi kusubiri", "ninatazamia sana"],
            "fr": ["tellement excité pour", "je ne peux pas attendre", "j'attends avec impatience"],
        },
        "disappointment_topic": {
            "en": ["i'm disappointed", "that's disappointing", "didn't go as planned", "expected better"],
            "sw": ["nimekata tamaa", "hiyo inakatisha tamaa", "haikuwenda kama ilivyopangwa"],
            "fr": ["je suis déçu", "c'est décevant", "ça ne s'est pas passé comme prévu"],
        },
        "chat_meta_topic": {
            "en": ["this is a fun conversation", "i like talking to you", "this chat is nice", "enjoying this chat", "really like talking to you", "love talking to you"],
            "sw": ["huu ni mazungumzo ya kufurahisha", "ninapenda kuongea na wewe", "mazungumzo haya ni mazuri"],
            "fr": ["c'est une conversation amusante", "j'aime te parler", "cette discussion est sympa"],
        },
        "season_spring_topic": {
            "en": ["spring is here", "love springtime", "flowers blooming"],
            "sw": ["majira ya kuchipua yamefika", "ninapenda majira ya kuchipua"],
            "fr": ["le printemps est arrivé", "j'adore le printemps", "les fleurs fleurissent"],
        },
        "season_summer_topic": {
            "en": ["summer vibes", "love summer", "summer is here"],
            "sw": ["majira ya joto yamefika", "ninapenda majira ya joto"],
            "fr": ["ambiance d'été", "j'adore l'été", "l'été est arrivé"],
        },
        "season_autumn_topic": {
            "en": ["love autumn", "fall is here", "leaves are changing"],
            "sw": ["ninapenda majira ya vuli", "majani yanabadilika"],
            "fr": ["j'adore l'automne", "l'automne est arrivé", "les feuilles changent"],
        },
        "season_winter_topic": {
            "en": ["love winter", "winter is here", "winter vibes"],
            "sw": ["ninapenda majira ya baridi", "majira ya baridi yamefika"],
            "fr": ["j'adore l'hiver", "l'hiver est arrivé"],
        },

        # --- Fifth wave of additional smalltalk topics ---

        "nightmare_topic": {
            "en": ["had a nightmare", "bad dream", "scary dream", "nightmares"],
            "sw": ["nimeota ndoto mbaya", "ndoto ya kutisha"],
            "fr": ["j'ai fait un cauchemar", "mauvais rêve", "rêve effrayant"],
        },
        "traffic_topic": {
            "en": ["stuck in traffic", "traffic is terrible", "long commute"],
            "sw": ["nimekwama kwenye msongamano", "msongamano wa magari ni mbaya"],
            "fr": ["coincé dans les embouteillages", "circulation terrible"],
        },
        "news_topic": {
            "en": ["did you see the news", "heard about the news", "in the news today"],
            "sw": ["umesikia habari", "habari za leo"],
            "fr": ["as-tu vu les nouvelles", "entendu parler des nouvelles"],
        },
        "color_preference_topic": {
            "en": ["my favorite color is", "i love the color", "favorite colour"],
            "sw": ["rangi ninayopenda ni", "ninapenda rangi"],
            "fr": ["ma couleur préférée est", "j'adore la couleur"],
        },
        "studying_exam_topic": {
            "en": ["studying for an exam", "exam is coming up", "preparing for a test", "exam tomorrow"],
            "sw": ["ninasoma kwa mtihani", "mtihani unakuja", "kujiandaa kwa mtihani"],
            "fr": ["j'étudie pour un examen", "l'examen approche", "je me prépare pour un test"],
        },
        "gardening_plants_topic": {
            "en": ["my garden", "growing plants", "love gardening", "planting flowers"],
            "sw": ["bustani yangu", "kukua mimea", "ninapenda kilimo cha bustani"],
            "fr": ["mon jardin", "faire pousser des plantes", "j'adore le jardinage"],
        },
        "shopping_topic": {
            "en": ["going shopping", "love shopping", "bought something new"],
            "sw": ["kwenda kununua", "ninapenda kununua", "nimenunua kitu kipya"],
            "fr": ["je vais faire du shopping", "j'adore le shopping", "j'ai acheté quelque chose"],
        },
        "movies_tv_topic": {
            "en": ["favorite movie", "watching a show", "favorite tv show", "binge watching"],
            "sw": ["filamu ninayopenda", "kutazama kipindi", "kipindi cha tv ninachopenda"],
            "fr": ["film préféré", "je regarde une série", "émission préférée"],
        },
        "coffee_tea_topic": {
            "en": ["love coffee", "love tea", "need my coffee", "morning coffee"],
            "sw": ["ninapenda kahawa", "ninapenda chai", "nahitaji kahawa yangu"],
            "fr": ["j'adore le café", "j'adore le thé", "j'ai besoin de mon café"],
        },
        "exam_results_topic": {
            "en": ["got my results", "exam results", "passed my exam", "failed my exam"],
            "sw": ["nimepata matokeo yangu", "matokeo ya mtihani", "nimefaulu mtihani"],
            "fr": ["j'ai eu mes résultats", "résultats d'examen", "j'ai réussi mon examen"],
        },
        "party_event_topic": {
            "en": ["going to a party", "hosting a party", "big event coming up"],
            "sw": ["kwenda kwenye sherehe", "kuandaa sherehe", "tukio kubwa linakuja"],
            "fr": ["je vais à une fête", "j'organise une fête", "grand événement à venir"],
        },
        "siblings_topic": {
            "en": ["my brother", "my sister", "my siblings"],
            "sw": ["kaka yangu", "dada yangu", "ndugu zangu"],
            "fr": ["mon frère", "ma sœur", "mes frères et sœurs"],
        },
        "career_change_topic": {
            "en": ["changing careers", "new job", "switching jobs", "career change"],
            "sw": ["kubadilisha kazi", "kazi mpya", "kubadilisha taaluma"],
            "fr": ["changer de carrière", "nouveau travail", "changement de carrière"],
        },
        "volunteer_work_topic": {
            "en": ["volunteering", "volunteer work", "giving back to the community"],
            "sw": ["kujitolea", "kazi ya kujitolea", "kurudisha kwa jamii"],
            "fr": ["faire du bénévolat", "travail bénévole", "redonner à la communauté"],
        },
        "spirituality_topic": {
            "en": ["my faith", "my religion", "praying", "spiritual journey"],
            "sw": ["imani yangu", "dini yangu", "kusali", "safari ya kiroho"],
            "fr": ["ma foi", "ma religion", "prier", "voyage spirituel"],
        },
        "politics_deflect_topic": {
            "en": ["what do you think about politics", "political opinion", "who should i vote for"],
            "sw": ["unafikiri nini kuhusu siasa", "mtazamo wa kisiasa", "nipigie kura nani"],
            "fr": ["que penses-tu de la politique", "opinion politique", "pour qui devrais-je voter"],
        },
        "silence_filler_topic": {
            "en": ["...", "no comment", "nothing to say", "i don't know what to say"],
            "sw": ["sina la kusema", "sijui nieleze nini"],
            "fr": ["rien à dire", "je ne sais pas quoi dire"],
        },
        "directions_recommendation_topic": {
            "en": ["can you recommend", "any recommendations", "what would you suggest"],
            "sw": ["unaweza kupendekeza", "una mapendekezo", "ungesemaje"],
            "fr": ["peux-tu recommander", "des recommandations", "que suggérerais-tu"],
        },
        "name_recognition_topic": {
            "en": ["do you remember my name", "you remembered my name", "you know my name"],
            "sw": ["unakumbuka jina langu", "umekumbuka jina langu"],
            "fr": ["te souviens-tu de mon nom", "tu as retenu mon nom"],
        },
        "general_curiosity_topic": {
            "en": ["i'm curious about", "wondering about", "just curious"],
            "sw": ["nina hamu ya kujua", "ninajiuliza kuhusu"],
            "fr": ["je suis curieux de", "je me demande à propos de"],
        },

        # --- Sixth wave of additional smalltalk topics ---

        "laughter_topic": {
            "en": ["i can't stop laughing", "laughing so hard", "giggling"],
            "sw": ["siwezi kuacha kucheka", "ninacheka sana"],
            "fr": ["je n'arrête pas de rire", "je ris tellement"],
        },
        "crying_topic": {
            "en": ["i'm crying", "started crying", "tearing up", "fighting back tears"],
            "sw": ["ninalia", "nimeanza kulia", "machozi yananijaa"],
            "fr": ["je pleure", "j'ai commencé à pleurer", "les larmes me montent"],
        },
        "mild_frustration_topic": {
            "en": ["ugh", "so annoying", "this is ridiculous", "come on"],
            "sw": ["aisee", "inasumbua sana", "hii haiwezekani"],
            "fr": ["ugh", "tellement énervant", "c'est ridicule"],
        },
        "bot_favorite_things_topic": {
            "en": ["what's your favorite", "do you have a favorite", "what do you like"],
            "sw": ["unaopenda zaidi ni nini", "una kipendwa", "unapenda nini"],
            "fr": ["quel est ton préféré", "as-tu un préféré", "qu'est-ce que tu aimes"],
        },
        "birds_fish_topic": {
            "en": ["my bird", "my fish", "pet bird", "pet fish", "aquarium"],
            "sw": ["ndege wangu", "samaki wangu", "bwawa la samaki"],
            "fr": ["mon oiseau", "mon poisson", "aquarium"],
        },
        "commute_transport_topic": {
            "en": ["taking the bus", "driving to work", "riding my bike", "taking the train"],
            "sw": ["kupanda basi", "kuendesha gari kwenda kazini", "kuendesha baiskeli"],
            "fr": ["prendre le bus", "conduire au travail", "faire du vélo"],
        },
        "allergies_topic": {
            "en": ["my allergies", "allergic to", "allergy season"],
            "sw": ["mzio wangu", "nina mzio wa", "msimu wa mzio"],
            "fr": ["mes allergies", "allergique à", "saison des allergies"],
        },
        "diet_nutrition_topic": {
            "en": ["eating healthy", "on a diet", "watching what i eat", "trying to eat better"],
            "sw": ["kula afya", "niko kwenye lishe", "ninajaribu kula vizuri zaidi"],
            "fr": ["manger sainement", "au régime", "j'essaie de mieux manger"],
        },
        "sleep_schedule_topic": {
            "en": ["my sleep schedule", "going to bed early", "staying up late", "night owl"],
            "sw": ["ratiba yangu ya kulala", "kulala mapema", "kukesha usiku"],
            "fr": ["mon horaire de sommeil", "se coucher tôt", "veiller tard"],
        },
        "photography_art_topic": {
            "en": ["taking photos", "love photography", "painting a picture", "drawing",
                   "photography", "photograph", "camera", "camera lens", "photos", "picture taking"],
            "sw": ["kupiga picha", "ninapenda upigaji picha", "kuchora picha"],
            "fr": ["prendre des photos", "j'adore la photographie", "dessiner"],
        },
        "grammar_question_topic": {
            "en": ["is this grammatically correct", "grammar question", "which is correct"],
            "sw": ["hii ni sahihi kisarufi", "swali la sarufi"],
            "fr": ["est-ce grammaticalement correct", "question de grammaire"],
        },
        "naming_things_topic": {
            "en": ["naming my baby", "baby names", "what should i name", "naming my pet"],
            "sw": ["kumtafutia mtoto jina", "majina ya watoto", "nimwite nani"],
            "fr": ["nommer mon bébé", "noms de bébé", "comment devrais-je nommer"],
        },
        "weather_extreme_topic": {
            "en": ["there's a storm", "hurricane warning", "severe weather", "thunderstorm"],
            "sw": ["kuna dhoruba", "tahadhari ya kimbunga", "hali mbaya ya hewa"],
            "fr": ["il y a une tempête", "alerte ouragan", "intempéries"],
        },
        "home_house_topic": {
            "en": ["my house", "my apartment", "moving house", "redecorating"],
            "sw": ["nyumba yangu", "ghorofa yangu", "kuhamia nyumba mpya"],
            "fr": ["ma maison", "mon appartement", "déménager"],
        },
        "neighbors_topic": {
            "en": ["my neighbor", "my neighbors", "noisy neighbor"],
            "sw": ["jirani yangu", "majirani wangu", "jirani mwenye kelele"],
            "fr": ["mon voisin", "mes voisins", "voisin bruyant"],
        },
        "pet_loss_topic": {
            "en": ["my pet passed away", "lost my dog", "lost my cat", "my pet died"],
            "sw": ["mnyama wangu amefariki", "nimepoteza mbwa wangu", "nimepoteza paka wangu"],
            "fr": ["mon animal est décédé", "j'ai perdu mon chien", "j'ai perdu mon chat"],
        },
        "achievement_milestone_topic": {
            "en": ["reached a milestone", "hit a milestone", "big achievement", "proud milestone"],
            "sw": ["nimefikia hatua muhimu", "mafanikio makubwa"],
            "fr": ["j'ai atteint une étape importante", "grande réalisation"],
        },
        "waiting_patience_topic": {
            "en": ["waiting for", "still waiting", "patience is hard", "can't wait any longer"],
            "sw": ["ninasubiri", "bado ninasubiri", "uvumilivu ni mgumu"],
            "fr": ["j'attends", "j'attends toujours", "la patience est difficile"],
        },
        "positive_surprise_topic": {
            "en": ["pleasantly surprised", "what a nice surprise", "didn't expect that"],
            "sw": ["nimeshangaa kwa furaha", "mshangao mzuri"],
            "fr": ["agréablement surpris", "quelle belle surprise"],
        },
        "compliment_back_request_topic": {
            "en": ["say something nice", "compliment me", "give me a compliment"],
            "sw": ["niambie kitu kizuri", "nisifie", "nipe pongezi"],
            "fr": ["dis-moi quelque chose de gentil", "fais-moi un compliment"],
        },

        # --- Seventh and final wave of additional smalltalk topics ---

        "deadline_topic": {
            "en": ["deadline is coming up", "have a deadline", "due tomorrow", "due date for"],
            "sw": ["muda wa mwisho unakaribia", "nina muda wa mwisho", "inahitajika kesho"],
            "fr": ["la date limite approche", "j'ai une échéance", "à rendre demain"],
        },
        "pregnancy_baby_topic": {
            "en": ["i'm pregnant", "we're expecting", "having a baby", "new baby"],
            "sw": ["nina mimba", "tunatarajia", "tutapata mtoto"],
            "fr": ["je suis enceinte", "nous attendons un bébé", "nouveau bébé"],
        },
        "wedding_engagement_topic": {
            "en": ["i'm getting married", "just got engaged", "wedding planning", "my wedding"],
            "sw": ["ninaolewa", "ninafunga ndoa", "nimeposwa hivi karibuni", "kupanga harusi"],
            "fr": ["je me marie", "je viens de me fiancer", "planification du mariage"],
        },
        "graduation_topic": {
            "en": ["i'm graduating", "just graduated", "graduation day", "finishing school"],
            "sw": ["ninahitimu", "nimehitimu hivi karibuni", "siku ya kuhitimu"],
            "fr": ["je vais obtenir mon diplôme", "je viens de terminer mes études"],
        },
        "moving_city_topic": {
            "en": ["moving to a new city", "relocating", "moving away", "new city"],
            "sw": ["kuhamia mji mpya", "kuhama", "mji mpya"],
            "fr": ["déménager dans une nouvelle ville", "je déménage", "nouvelle ville"],
        },
        "new_pet_topic": {
            "en": ["got a new pet", "adopted a dog", "adopted a cat", "new puppy", "new kitten"],
            "sw": ["nimepata mnyama mpya", "nimeasili mbwa", "nimeasili paka"],
            "fr": ["j'ai un nouvel animal", "j'ai adopté un chien", "j'ai adopté un chat"],
        },
        "first_day_topic": {
            "en": ["first day at", "first day of", "starting a new", "nervous about my first day"],
            "sw": ["siku ya kwanza katika", "kuanza mpya", "wasiwasi kuhusu siku yangu ya kwanza"],
            "fr": ["premier jour à", "premier jour de", "je commence un nouveau"],
        },
        "reunion_topic": {
            "en": ["seeing an old friend", "reunion with", "haven't seen in years", "catching up with"],
            "sw": ["kuona rafiki wa zamani", "mkutano na", "sijaona kwa miaka"],
            "fr": ["voir un vieil ami", "retrouvailles avec", "je n'ai pas vu depuis des années"],
        },
        "fluency_goals_topic": {
            "en": ["want to be fluent", "fluency goal", "trying to speak fluently"],
            "sw": ["nataka kuwa fasaha", "lengo la ufasaha"],
            "fr": ["je veux être bilingue courant", "objectif de fluidité"],
        },
        "cultural_traditions_topic": {
            "en": ["my culture", "our traditions", "cultural celebration", "traditional food"],
            "sw": ["utamaduni wangu", "mila zetu", "sherehe za kitamaduni", "chakula cha kitamaduni"],
            "fr": ["ma culture", "nos traditions", "célébration culturelle"],
        },
        "sustainability_topic": {
            "en": ["going green", "reducing waste", "sustainability", "recycling"],
            "sw": ["kuwa rafiki wa mazingira", "kupunguza taka", "uendelevu", "kuchakata tena"],
            "fr": ["devenir écolo", "réduire les déchets", "durabilité", "recyclage"],
        },
        "fun_fact_topic": {
            "en": ["tell me a fun fact", "did you know", "random fact", "interesting fact"],
            "sw": ["niambie jambo la kufurahisha", "je ulijua", "ukweli wa ajabu"],
            "fr": ["dis-moi un fait amusant", "savais-tu que", "fait intéressant"],
        },

        # --- Eighth wave of additional smalltalk topics ---

        "gift_thanks_topic": {
            "en": ["got a gift", "received a present", "thank you for the gift", "loved the present"],
            "sw": ["nimepata zawadi", "asante kwa zawadi", "nimependa zawadi"],
            "fr": ["j'ai reçu un cadeau", "merci pour le cadeau", "j'ai adoré le cadeau"],
        },
        "running_late_topic": {
            "en": ["running late", "i'm late", "going to be late", "late again"],
            "sw": ["nimechelewa", "nitachelewa", "nimechelewa tena"],
            "fr": ["je suis en retard", "je vais être en retard", "encore en retard"],
        },
        "time_management_topic": {
            "en": ["managing my time", "time management", "so much to do", "never enough time"],
            "sw": ["kusimamia muda wangu", "usimamizi wa muda", "mengi ya kufanya"],
            "fr": ["gérer mon temps", "gestion du temps", "tellement de choses à faire"],
        },
        "sports_victory_topic": {
            "en": ["my team won", "we won the game", "victory today"],
            "sw": ["timu yangu imeshinda", "tumeshinda mchezo"],
            "fr": ["mon équipe a gagné", "on a gagné le match"],
        },
        "sports_loss_topic": {
            "en": ["my team lost", "we lost the game", "tough loss"],
            "sw": ["timu yangu imeshindwa", "tumeshindwa mchezo"],
            "fr": ["mon équipe a perdu", "on a perdu le match"],
        },
        "unpredictable_weather_topic": {
            "en": ["weather keeps changing", "unpredictable weather", "weather is so weird"],
            "sw": ["hali ya hewa inabadilika", "hali ya hewa isiyotabirika"],
            "fr": ["la météo change tout le temps", "météo imprévisible"],
        },
        "new_year_resolution_topic": {
            "en": ["new year's resolution", "my resolution this year", "resolutions for the year"],
            "sw": ["azimio la mwaka mpya", "azimio langu mwaka huu"],
            "fr": ["résolution du nouvel an", "ma résolution cette année"],
        },
        "childhood_memory_topic": {
            "en": ["when i was a kid", "childhood memory", "growing up", "as a child"],
            "sw": ["nilipokuwa mtoto", "kumbukumbu za utotoni", "nilipokuwa nikikua"],
            "fr": ["quand j'étais enfant", "souvenir d'enfance", "en grandissant"],
        },
        "role_model_topic": {
            "en": ["my role model", "who inspires me", "look up to", "my inspiration"],
            "sw": ["kielelezo changu", "ananitia moyo", "ninamheshimu"],
            "fr": ["mon modèle", "qui m'inspire", "j'admire"],
        },
        "fear_phobia_topic": {
            "en": ["i'm afraid of", "scared of", "my biggest fear", "phobia of"],
            "sw": ["ninaogopa", "hofu yangu kubwa", "ninaogopa sana"],
            "fr": ["j'ai peur de", "ma plus grande peur", "phobie de"],
        },
        "dream_interpretation_topic": {
            "en": ["what does it mean when i dream", "dream interpretation", "interpret my dream"],
            "sw": ["inamaanisha nini ninapoota", "tafsiri ya ndoto"],
            "fr": ["qu'est-ce que ça signifie quand je rêve", "interprétation de rêve"],
        },
        "self_improvement_topic": {
            "en": ["working on myself", "self improvement", "becoming a better person", "personal growth"],
            "sw": ["ninajifanyia kazi", "kujiboresha", "kuwa mtu bora", "ukuaji wa kibinafsi"],
            "fr": ["je travaille sur moi-même", "amélioration personnelle", "devenir une meilleure personne"],
        },
        "social_media_topic": {
            "en": ["posted on social media", "social media break", "too much screen time", "instagram", "twitter"],
            "sw": ["nimeweka kwenye mitandao ya kijamii", "mapumziko ya mitandao", "muda mwingi wa skrini"],
            "fr": ["j'ai posté sur les réseaux sociaux", "pause des réseaux sociaux", "trop de temps d'écran"],
        },
        "remote_work_topic": {
            "en": ["working from home", "remote work", "working remotely"],
            "sw": ["kufanya kazi nyumbani", "kazi ya mbali"],
            "fr": ["travailler à domicile", "travail à distance"],
        },
        "job_interview_topic": {
            "en": ["job interview", "interview tomorrow", "preparing for an interview", "nervous about my interview"],
            "sw": ["mahojiano ya kazi", "mahojiano kesho", "kujiandaa kwa mahojiano"],
            "fr": ["entretien d'embauche", "entretien demain", "se préparer pour un entretien"],
        },
        "recipe_dish_topic": {
            "en": ["favorite recipe", "favorite dish", "homemade meal", "trying a new recipe"],
            "sw": ["mlo ninaopenda", "chakula ninachopenda", "mlo wa nyumbani"],
            "fr": ["recette préférée", "plat préféré", "repas fait maison"],
        },

        # --- Ninth wave of additional smalltalk topics ---

        "insomnia_topic": {
            "en": ["can't sleep", "insomnia", "lying awake", "tossing and turning"],
            "sw": ["siwezi kulala", "kukosa usingizi", "kugeuka geuka kitandani"],
            "fr": ["je ne peux pas dormir", "insomnie", "je me retourne dans mon lit"],
        },
        "quitting_habit_topic": {
            "en": ["trying to quit", "breaking a habit", "quitting smoking", "cutting back on"],
            "sw": ["ninajaribu kuacha", "kuvunja tabia", "kuacha kuvuta sigara"],
            "fr": ["j'essaie d'arrêter", "casser une habitude", "arrêter de fumer"],
        },
        "meditation_mindfulness_topic": {
            "en": ["meditating", "practicing mindfulness", "breathing exercises", "trying yoga"],
            "sw": ["kutafakari", "kufanya mazoezi ya akili tulivu", "mazoezi ya kupumua"],
            "fr": ["je médite", "pratiquer la pleine conscience", "exercices de respiration"],
        },
        "sibling_rivalry_topic": {
            "en": ["my sibling rivalry", "always compared to my sibling", "fighting with my brother", "fighting with my sister"],
            "sw": ["ushindani na ndugu yangu", "kupigana na kaka yangu", "kupigana na dada yangu"],
            "fr": ["rivalité avec mon frère", "rivalité avec ma sœur", "je me bats avec mon frère"],
        },
        "long_distance_relationship_topic": {
            "en": ["long distance relationship", "missing my partner", "video call with my partner"],
            "sw": ["uhusiano wa mbali", "ninamkosa mpenzi wangu"],
            "fr": ["relation à distance", "mon partenaire me manque"],
        },
        "pet_peeve_topic": {
            "en": ["my pet peeve", "really bothers me when", "can't stand it when", "drives me crazy when"],
            "sw": ["kinachonisumbua zaidi", "kinachoniudhi ni", "siwezi kustahimili wakati"],
            "fr": ["ce qui m'énerve vraiment", "ce qui me dérange quand", "je ne supporte pas quand"],
        },
        "kindness_topic": {
            "en": ["did something kind", "random act of kindness", "someone was so kind to me", "paying it forward"],
            "sw": ["nimefanya jambo la huruma", "kitendo cha huruma cha bahati", "mtu alikuwa mpole kwangu"],
            "fr": ["j'ai fait quelque chose de gentil", "acte de bonté gratuit", "quelqu'un a été si gentil avec moi"],
        },
        "procrastination_topic": {
            "en": ["i keep procrastinating", "putting it off", "procrastinating again", "should be doing"],
            "sw": ["ninaendelea kuchelewesha", "ninaliweka kando", "ninachelewesha tena"],
            "fr": ["je n'arrête pas de procrastiner", "je le repousse", "je procrastine encore"],
        },
        "decluttering_topic": {
            "en": ["decluttering my room", "minimalism", "getting rid of stuff", "cleaning out my closet"],
            "sw": ["kupanga chumba changu", "kuondoa vitu visivyo vya muhimu", "kusafisha kabati langu"],
            "fr": ["je désencombre ma chambre", "minimalisme", "me débarrasser de mes affaires"],
        },
        "public_speaking_topic": {
            "en": ["public speaking", "giving a presentation", "scared to speak in public", "presentation tomorrow"],
            "sw": ["kuongea hadharani", "kutoa uwasilishaji", "kuogopa kuongea hadharani"],
            "fr": ["prendre la parole en public", "faire une présentation", "peur de parler en public"],
        },
        "learning_to_drive_topic": {
            "en": ["learning to drive", "driving lessons", "got my license", "nervous about driving"],
            "sw": ["kujifunza kuendesha gari", "masomo ya kuendesha", "nimepata leseni"],
            "fr": ["apprendre à conduire", "leçons de conduite", "j'ai eu mon permis"],
        },
        "retirement_planning_topic": {
            "en": ["planning for retirement", "retirement savings", "retiring soon"],
            "sw": ["kupanga kwa kustaafu", "akiba ya kustaafu", "kustaafu hivi karibuni"],
            "fr": ["planifier la retraite", "épargne retraite", "je prends ma retraite bientôt"],
        },
        "programming_coding_topic": {
            "en": ["writing code", "debugging", "my code won't work", "learning to program"],
            "sw": ["kuandika programu", "kutafuta hitilafu", "msimbo wangu haufanyi kazi"],
            "fr": ["écrire du code", "déboguer", "mon code ne fonctionne pas"],
        },
        "gym_intimidation_topic": {
            "en": ["intimidated at the gym", "nervous to go to the gym", "gym anxiety"],
            "sw": ["ninaogopa kwenye gym", "wasiwasi wa gym"],
            "fr": ["intimidé à la salle de sport", "anxiété de la salle de sport"],
        },
        "comfort_food_topic": {
            "en": ["comfort food", "craving something", "need comfort food", "comfort food right now"],
            "sw": ["chakula cha faraja", "ninahitaji chakula cha faraja", "ninatamani kitu"],
            "fr": ["nourriture réconfortante", "j'ai envie de quelque chose", "besoin de réconfort"],
        },

        # --- Tenth wave of additional smalltalk topics ---

        "singing_voice_topic": {
            "en": ["love singing", "singing in the shower", "learning to sing", "my singing voice"],
            "sw": ["ninapenda kuimba", "kuimba bafuni", "kujifunza kuimba"],
            "fr": ["j'adore chanter", "chanter sous la douche", "apprendre à chanter"],
        },
        "journaling_topic": {
            "en": ["keeping a journal", "journaling helps", "writing in my diary", "love journaling"],
            "sw": ["kuandika jarida", "kuandika kwenye diari yangu", "ninapenda kuandika jarida"],
            "fr": ["tenir un journal", "écrire dans mon journal intime", "j'adore tenir un journal"],
        },
        "board_games_puzzles_topic": {
            "en": ["playing board games", "love puzzles", "doing a jigsaw puzzle", "board game night"],
            "sw": ["kucheza michezo ya bodi", "ninapenda fumbo", "usiku wa michezo ya bodi"],
            "fr": ["jouer à des jeux de société", "j'adore les puzzles", "soirée jeux de société"],
        },
        "camping_outdoor_trip_topic": {
            "en": ["going camping", "camping trip", "sleeping under the stars", "pitching a tent"],
            "sw": ["kwenda kupiga kambi", "safari ya kambi", "kulala chini ya nyota"],
            "fr": ["aller camper", "voyage de camping", "dormir sous les étoiles"],
        },
        "car_trouble_topic": {
            "en": ["car broke down", "car trouble", "flat tire", "car won't start"],
            "sw": ["gari limeharibika", "tatizo la gari", "tairi limepasuka"],
            "fr": ["la voiture est en panne", "problème de voiture", "pneu crevé"],
        },
        "roommates_topic": {
            "en": ["my roommate", "living with roommates", "roommate drama"],
            "sw": ["mwenzangu wa nyumba", "kuishi na wenzangu wa nyumba"],
            "fr": ["mon colocataire", "vivre avec des colocataires"],
        },
        "online_dating_topic": {
            "en": ["online dating", "matched with someone", "dating app", "first date"],
            "sw": ["uchumba mtandaoni", "nimepatana na mtu", "programu ya uchumba"],
            "fr": ["rencontres en ligne", "j'ai matché avec quelqu'un", "application de rencontre"],
        },
        "tattoos_piercings_topic": {
            "en": ["getting a tattoo", "new piercing", "thinking about a tattoo"],
            "sw": ["kupata tatoo", "kutoboa kipya", "ninafikiria tatoo"],
            "fr": ["se faire tatouer", "nouveau piercing", "je pense à un tatouage"],
        },
        "fashion_style_topic": {
            "en": ["my style", "fashion sense", "outfit of the day", "what to wear"],
            "sw": ["mtindo wangu", "hisia ya mitindo", "nguo za leo", "nivae nini"],
            "fr": ["mon style", "sens de la mode", "tenue du jour", "que porter"],
        },
        "language_barrier_topic": {
            "en": ["language barrier", "don't understand the language", "hard to communicate"],
            "sw": ["kizuizi cha lugha", "sielewi lugha", "ngumu kuwasiliana"],
            "fr": ["barrière linguistique", "je ne comprends pas la langue", "difficile de communiquer"],
        },
        "school_volunteering_topic": {
            "en": ["volunteering at school", "helping at my kid's school", "school event"],
            "sw": ["kujitolea shuleni", "kusaidia shule ya mtoto wangu"],
            "fr": ["faire du bénévolat à l'école", "aider à l'école de mon enfant"],
        },
        "charity_donation_topic": {
            "en": ["donated to charity", "giving to charity", "fundraiser"],
            "sw": ["nimechangia hisani", "kutoa kwa hisani", "ukusanyaji wa fedha"],
            "fr": ["j'ai fait un don à une association", "faire un don", "collecte de fonds"],
        },
        "hosting_guests_topic": {
            "en": ["hosting guests", "having people over", "guests are coming"],
            "sw": ["kupokea wageni", "wageni wanakuja"],
            "fr": ["recevoir des invités", "j'ai du monde qui vient", "les invités arrivent"],
        },
        "time_zones_topic": {
            "en": ["different time zones", "time zone difference", "what time is it there"],
            "sw": ["maeneo tofauti ya muda", "tofauti ya saa"],
            "fr": ["fuseaux horaires différents", "différence de fuseau horaire"],
        },
        "productivity_tools_topic": {
            "en": ["productivity app", "using a planner", "trying to stay organized", "productivity hacks"],
            "sw": ["programu ya uzalishaji", "kutumia kalenda", "kujaribu kuwa na mpangilio"],
            "fr": ["application de productivité", "utiliser un agenda", "essayer de rester organisé"],
        },

        # --- Eleventh wave of additional smalltalk topics ---

        "parenting_topic": {
            "en": ["being a parent", "raising my kids", "parenting is hard", "my kids"],
            "sw": ["kuwa mzazi", "kulea watoto wangu", "uzazi ni mgumu", "watoto wangu"],
            "fr": ["être parent", "élever mes enfants", "être parent c'est dur", "mes enfants"],
        },
        "teenager_struggle_topic": {
            "en": ["my teenager", "parenting a teen", "teenage years are hard"],
            "sw": ["kijana wangu wa balehe", "kulea kijana", "miaka ya balehe ni migumu"],
            "fr": ["mon adolescent", "élever un ado", "l'adolescence est difficile"],
        },
        "elderly_parent_care_topic": {
            "en": ["caring for my elderly parent", "taking care of my aging parents", "caregiver for my mom", "caregiver for my dad"],
            "sw": ["kumtunza mzazi wangu mzee", "kuwatunza wazazi wangu wanaozeeka"],
            "fr": ["prendre soin de mon parent âgé", "m'occuper de mes parents vieillissants"],
        },
        "grief_loss_topic": {
            "en": ["lost a loved one", "grieving", "my loved one passed away", "dealing with grief"],
            "sw": ["nimepoteza mpendwa", "ninaomboleza", "mpendwa wangu amefariki"],
            "fr": ["j'ai perdu un être cher", "je fais mon deuil", "mon proche est décédé"],
        },
        "therapy_counseling_topic": {
            "en": ["going to therapy", "seeing a therapist", "started counseling", "my therapist said"],
            "sw": ["kwenda kwa tiba", "kumwona mtaalamu wa saikolojia", "nimeanza ushauri"],
            "fr": ["aller en thérapie", "voir un thérapeute", "j'ai commencé une thérapie"],
        },
        "addiction_recovery_topic": {
            "en": ["in recovery", "sober", "recovering from addiction", "staying clean"],
            "sw": ["katika kupona", "sina ulevi", "kupona kutoka uraibu"],
            "fr": ["en rétablissement", "sobre", "en convalescence d'une addiction"],
        },
        "identity_coming_out_topic": {
            "en": ["coming out", "discovering my identity", "figuring out who i am"],
            "sw": ["kujitokeza", "kugundua utambulisho wangu", "kujua mimi ni nani"],
            "fr": ["faire son coming out", "découvrir mon identité", "comprendre qui je suis"],
        },
        "immigration_topic": {
            "en": ["moving to a new country", "immigrating", "adjusting to a new country", "homesick"],
            "sw": ["kuhamia nchi mpya", "kuhama nchi", "kuzoea nchi mpya", "kukosa nyumbani"],
            "fr": ["déménager dans un nouveau pays", "immigrer", "s'adapter à un nouveau pays", "mal du pays"],
        },
        "disability_accessibility_topic": {
            "en": ["my disability", "accessibility issues", "living with a disability"],
            "sw": ["ulemavu wangu", "matatizo ya ufikiaji", "kuishi na ulemavu"],
            "fr": ["mon handicap", "problèmes d'accessibilité", "vivre avec un handicap"],
        },
        "menstrual_health_topic": {
            "en": ["my period", "menstrual cramps", "that time of the month"],
            "sw": ["hedhi yangu", "maumivu ya hedhi"],
            "fr": ["mes règles", "crampes menstruelles"],
        },
        "checkup_vaccine_topic": {
            "en": ["doctor's appointment", "getting a checkup", "vaccine appointment", "annual physical"],
            "sw": ["miadi ya daktari", "uchunguzi wa afya", "miadi ya chanjo"],
            "fr": ["rendez-vous chez le médecin", "bilan de santé", "rendez-vous de vaccination"],
        },
        "climate_anxiety_topic": {
            "en": ["worried about climate change", "climate anxiety", "the planet is warming"],
            "sw": ["wasiwasi kuhusu mabadiliko ya tabianchi", "sayari inaongezeka joto"],
            "fr": ["inquiet du changement climatique", "anxiété climatique", "la planète se réchauffe"],
        },
        "ai_technology_fear_topic": {
            "en": ["worried about ai", "scared of artificial intelligence", "will ai take my job"],
            "sw": ["wasiwasi kuhusu ai", "ninaogopa akili bandia", "ai itanichukua kazi"],
            "fr": ["inquiet de l'ia", "peur de l'intelligence artificielle", "l'ia va-t-elle prendre mon travail"],
        },
        "remote_learning_topic": {
            "en": ["online school", "remote learning", "virtual classes", "studying from home"],
            "sw": ["shule mtandaoni", "kujifunza kwa mbali", "madarasa ya mtandaoni"],
            "fr": ["école en ligne", "apprentissage à distance", "cours virtuels"],
        },
        "hobby_club_topic": {
            "en": ["joined a club", "hobby group", "found a community of", "meetup group"],
            "sw": ["nimejiunga na klabu", "kikundi cha hobby", "nimepata jamii ya"],
            "fr": ["j'ai rejoint un club", "groupe de loisir", "j'ai trouvé une communauté de"],
        },

        # --- Twelfth wave of additional smalltalk topics ---

        "sneeze_hiccup_topic": {
            "en": ["i just sneezed", "i have the hiccups", "can't stop sneezing"],
            "sw": ["nimepiga chafya", "nina kwikwi"],
            "fr": ["je viens d'éternuer", "j'ai le hoquet"],
        },
        "handedness_topic": {
            "en": ["i'm left handed", "i'm right handed", "being left handed"],
            "sw": ["mimi ni mkono wa kushoto", "mimi ni mkono wa kulia"],
            "fr": ["je suis gaucher", "je suis droitier"],
        },
        "astrology_zodiac_topic": {
            "en": ["my zodiac sign", "what's your sign", "astrology", "horoscope"],
            "sw": ["alama yangu ya nyota", "unyota", "horoscope"],
            "fr": ["mon signe du zodiaque", "astrologie", "horoscope"],
        },
        "personality_type_topic": {
            "en": ["my personality type", "i'm an introvert", "i'm an extrovert", "mbti"],
            "sw": ["aina yangu ya utu", "mimi ni mtu wa kujifungia", "mimi ni mchangamfu"],
            "fr": ["mon type de personnalité", "je suis introverti", "je suis extraverti"],
        },
        "lucky_superstition_topic": {
            "en": ["my lucky number", "superstitious about", "good luck charm"],
            "sw": ["namba yangu ya bahati", "imani za kishirikina kuhusu", "hirizi ya bahati"],
            "fr": ["mon chiffre porte-bonheur", "superstitieux à propos de", "porte-bonheur"],
        },
        "favorite_season_topic": {
            "en": ["my favorite season", "best season of the year"],
            "sw": ["msimu ninaopenda", "msimu bora wa mwaka"],
            "fr": ["ma saison préférée", "meilleure saison de l'année"],
        },
        "ideal_vacation_topic": {
            "en": ["dream vacation", "ideal vacation", "bucket list trip"],
            "sw": ["likizo ya ndoto", "likizo bora", "safari ya orodha ya matamanio"],
            "fr": ["vacances de rêve", "vacances idéales", "voyage de la liste de souhaits"],
        },
        "first_impression_topic": {
            "en": ["first impression of", "what was your first impression", "made a good impression"],
            "sw": ["mtazamo wa kwanza wa", "umetoa mtazamo mzuri"],
            "fr": ["première impression de", "fait bonne impression"],
        },
        "bucket_list_topic": {
            "en": ["on my bucket list", "bucket list item", "before i die i want to"],
            "sw": ["kwenye orodha yangu ya matamanio", "kabla sijafa nataka"],
            "fr": ["sur ma liste de choses à faire avant de mourir", "avant de mourir je veux"],
        },
        "give_compliment_to_bot_topic": {
            "en": ["you're doing a good job", "you're helpful", "you're a good listener"],
            "sw": ["unafanya kazi nzuri", "una msaada", "unasikiliza vizuri"],
            "fr": ["tu fais du bon travail", "tu es utile", "tu écoutes bien"],
        },

        # --- Conversation starters: extremely common casual openers that
        # should almost never fall through to "I don't understand",
        # since they're some of the most frequent first messages people
        # actually send a chatbot. ---

        "conversation_starter_topic": {
            "en": [
                "what's up", "whats up", "what's new", "whats new", "sup",
                "what's good", "whats good", "what's happening", "whats happening",
                "you up", "u up", "you there", "u there", "anyone there",
                "talk to me", "let's chat", "lets chat", "let's talk", "lets talk",
                "i'm bored let's talk", "tell me something", "entertain me",
                "say something", "talk to me please", "keep me company",
                "what's going on", "whats going on", "how's life", "hows life",
                "how's everything", "hows everything", "what's on your mind",
                "anything new", "what have you been up to", "long time no talk",
                "i'm back", "im back", "miss me", "guess what",
            ],
            "sw": [
                "mambo gani", "kuna nini", "kuna jipya", "mambo vipi",
                "uko hapo", "uko pale", "kuna mtu", "niongelee", "tuongee",
                "nimechoka niongee na mtu", "niambie kitu", "nifurahishe",
                "sema kitu", "nikupe ushirika", "mambo yanaendaje", "maisha yakoje",
                "kuna nini akilini mwako", "kuna jipya", "umekuwa wapi",
                "muda mrefu hatuongei", "nimerudi", "nikose",
            ],
            "fr": [
                "quoi de neuf", "ça va", "comment ça va", "t'es là", "tu es là",
                "il y a quelqu'un", "parle-moi", "discutons", "papotons",
                "je m'ennuie parlons", "dis-moi quelque chose", "divertis-moi",
                "dis quelque chose", "tiens-moi compagnie", "qu'est-ce qui se passe",
                "comment va la vie", "comment va tout", "à quoi tu penses",
                "quoi de nouveau", "qu'est-ce que tu as fait", "ça fait longtemps",
                "je suis de retour", "je suis revenu", "devine quoi",
            ],
        },

        # --- A second, even broader catch-all for short filler openers
        # and conversational connectors that often start a message but
        # don't carry topic content on their own (e.g. "so,", "anyway,",
        # "by the way"). These route to a gentle "go on" style prompt
        # rather than failing to match anything at all. ---

        "conversational_filler_starter_topic": {
            "en": [
                "by the way", "btw", "speaking of which", "anyway so",
                "so anyway", "random question", "quick question",
                "can i ask you something", "can i tell you something",
                "i have a question", "i need to tell you something",
                "guess what happened", "you won't believe this",
                "not gonna lie", "ngl", "honestly though", "real talk",
                "no joke", "i swear", "okay so", "so basically",
            ],
            "sw": [
                "kwa njia", "kuhusiana na hilo", "hata hivyo basi",
                "swali la ghafla", "swali la haraka", "naweza kukuuliza kitu",
                "naweza kukuambia kitu", "nina swali", "nahitaji kukuambia kitu",
                "kisha nini kilitokea", "hutaamini hili", "kwa uhakika",
                "kwa kweli", "naapa", "sawa basi", "kwa msingi",
            ],
            "fr": [
                "au fait", "à propos", "en parlant de ça", "bref donc",
                "question random", "question rapide", "je peux te demander quelque chose",
                "je peux te dire quelque chose", "j'ai une question",
                "je dois te dire quelque chose", "devine ce qui s'est passé",
                "tu ne vas pas croire ça", "honnêtement", "sans mentir",
                "je te jure", "bon donc", "en gros",
            ],
        },

        # --- Thirteenth wave of additional smalltalk topics ---

        "luck_fortune_topic": {
            "en": ["had good luck", "feeling lucky", "what bad luck", "such bad luck"],
            "sw": ["nimepata bahati nzuri", "ninahisi bahati", "bahati mbaya kiasi gani"],
            "fr": ["j'ai eu de la chance", "je me sens chanceux", "quelle malchance"],
        },
        "relaxing_weekend_topic": {
            "en": ["relaxing weekend", "doing nothing this weekend", "lazy weekend"],
            "sw": ["wikendi ya kupumzika", "sitafanya chochote wikendi hii"],
            "fr": ["week-end relaxant", "ne rien faire ce week-end"],
        },
        "proud_of_someone_topic": {
            "en": ["so proud of my", "proud of my friend", "proud of my kid", "proud of my partner"],
            "sw": ["ninajivunia", "ninamjivunia rafiki yangu", "ninamjivunia mtoto wangu"],
            "fr": ["si fier de mon", "fier de mon ami", "fier de mon enfant"],
        },
        "forgiveness_topic": {
            "en": ["learning to forgive", "forgiving someone", "hard to forgive", "i forgave"],
            "sw": ["kujifunza kusamehe", "kumsamehe mtu", "vigumu kusamehe"],
            "fr": ["apprendre à pardonner", "pardonner à quelqu'un", "difficile de pardonner"],
        },
        "mistake_learning_topic": {
            "en": ["made a mistake", "learned from my mistake", "i messed up"],
            "sw": ["nimefanya kosa", "nimejifunza kutoka kosa langu", "nimeharibu"],
            "fr": ["j'ai fait une erreur", "j'ai appris de mon erreur", "j'ai tout gâché"],
        },
        "trust_issues_topic": {
            "en": ["hard to trust", "trust issues", "i don't trust easily"],
            "sw": ["vigumu kuamini", "matatizo ya kuamini", "siamini kwa urahisi"],
            "fr": ["difficile de faire confiance", "problèmes de confiance", "je ne fais pas facilement confiance"],
        },
        "setting_boundaries_topic": {
            "en": ["setting boundaries", "learning to say no", "boundaries are important"],
            "sw": ["kuweka mipaka", "kujifunza kukataa", "mipaka ni muhimu"],
            "fr": ["fixer des limites", "apprendre à dire non", "les limites sont importantes"],
        },
        "self_care_routine_topic": {
            "en": ["my self care routine", "taking care of myself", "self care day"],
            "sw": ["ratiba yangu ya kujitunza", "kujitunza mwenyewe", "siku ya kujitunza"],
            "fr": ["ma routine de soins personnels", "prendre soin de moi", "journée de bien-être"],
        },
        "feeling_stuck_topic": {
            "en": ["feeling stuck", "i feel stuck", "stuck in a rut", "not moving forward"],
            "sw": ["ninahisi nimekwama", "nimekwama", "sisogei mbele"],
            "fr": ["je me sens coincé", "coincé dans une routine", "je n'avance pas"],
        },
        "life_transition_topic": {
            "en": ["going through a transition", "big life change", "everything is changing"],
            "sw": ["ninapitia mabadiliko", "mabadiliko makubwa ya maisha", "kila kitu kinabadilika"],
            "fr": ["je traverse une transition", "grand changement de vie", "tout change"],
        },
        "hope_future_topic": {
            "en": ["hopeful about the future", "things will get better", "looking forward to better days"],
            "sw": ["nina matumaini kuhusu siku zijazo", "mambo yatakuwa bora"],
            "fr": ["plein d'espoir pour l'avenir", "les choses vont s'améliorer"],
        },
        "gratitude_practice_topic": {
            "en": ["grateful for", "thankful for", "practicing gratitude", "counting my blessings"],
            "sw": ["nashukuru kwa", "ninafanya mazoezi ya shukrani", "ninahesabu baraka zangu"],
            "fr": ["reconnaissant pour", "je pratique la gratitude", "je compte mes bénédictions"],
        },
    }

    def __init__(self):
        self.language_detector = LanguageDetector()
        # BUGFIX/efficiency: this used to only build a flat list of RAW
        # (topic, lang, keyword) tuples and recompile a regex from the
        # keyword string on every single _contains_phrase() call.
        # Measured via cProfile: for one incoming message, find_topic()
        # was calling re.search() on a freshly-built pattern string
        # roughly 1,000+ times (once per keyword across all topics/
        # languages) - Python's internal re cache couldn't keep that
        # many distinct patterns warm, so most of those calls were
        # full regex COMPILATIONS, not just matches, accounting for the
        # large majority of this whole method's cost. Precompiling
        # every pattern ONCE here, and grouping by language so
        # find_topic only has to scan the relevant list, cuts that to
        # zero recompilation and roughly a third of the comparisons
        # per call (only the detected language's entries, not all
        # three, for the common case where the first language checked
        # already matches).
        self._entries_by_lang = {"en": [], "sw": [], "fr": []}
        for topic, lang_map in self.TOPICS.items():
            for lang, keywords in lang_map.items():
                for kw in keywords:
                    pattern = re.compile(r"\b" + re.escape(kw) + r"\b", re.IGNORECASE)
                    self._entries_by_lang.setdefault(lang, []).append((topic, kw, pattern))

    def find_topic(self, text: str):
        """
        Returns (topic_name, detected_language) for the BEST matching
        topic keyword found anywhere in the text, searching the detected
        language's keyword list first (for relevance) and then the other
        two languages (in case of code-switching). Returns (None, lang)
        if nothing matches.

        "Best" means the LONGEST matching keyword (by character count),
        not just the first one encountered in dict insertion order. This
        matters because several topics intentionally share short, generic
        keywords with more specific ones - e.g. "thanks" (generic
        gratitude) vs "thanks for listening" (gratitude aimed at the bot
        specifically). Without preferring the longer/more specific match,
        the generic topic would always win simply by being defined
        earlier in the TOPICS dict, regardless of which phrase is the
        better description of what the user actually said. This is still
        a fully deterministic, rigid rule (longest keyword wins) - no
        scoring model, no learning.
        """
        detected_lang = self.language_detector.detect(text)
        lang_priority = [detected_lang] + [l for l in ("en", "sw", "fr") if l != detected_lang]

        for lang in lang_priority:
            best_topic = None
            best_length = -1
            for topic, kw, pattern in self._entries_by_lang.get(lang, []):
                if len(kw) > best_length and pattern.search(text):
                    best_topic = topic
                    best_length = len(kw)
            if best_topic is not None:
                return best_topic, lang
        return None, detected_lang


# ==============================================================================
