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

    def __init__(self, normalizer=None):
        self.intents = []
        self.normalizer = normalizer
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

        When a FlexiblePhraseNormalizer is attached, loose natural phrasing
        is rewritten to canonical triggers here FIRST, so users can type
        flexibly without each intent needing a dozen pattern variants.
        """
        if self.normalizer is not None:
            text = self.normalizer.normalize(text)
        for intent in self.intents:
            m = intent.match(text)
            if m:
                response = intent.handler(text, m)
                if response is not None:
                    self.last_matched_intent = intent.name
                    return response
        return None


# ==============================================================================
# SECTION 7A1A: FLEXIBLE PHRASE NORMALIZER (offline, no ML, adds typing freedom)
# ==============================================================================
#
# The intent engine above is deliberately rigid (explicit regex triggers
# per tool). This normalizer is the "make the regex better" layer: it runs
# on every message right before matching and rewrites loose, natural
# phrasing into canonical forms the existing intents already understand -
# fully offline and deterministic, exactly like the typo corrector next to
# it, and completely orthogonal to the optional LLM hybrid.
#
# It does four things, each conservative and fail-open (if nothing applies,
# the text passes through untouched and matching behaves exactly as before):
#
#   1. Strips leading conversational filler ("please", "can you",
#      "okay", "so", ...) that carries no intent meaning.
#   2. Converts English number words to digits ("sixteen" -> 16,
#      "twenty one" -> 21, "three point five" -> 3.5) and common math
#      words to symbols ("times" -> *, "divided by" -> /, "squared" -> ^2)
#      - ONLY when the message actually looks like math, so normal chat
#      is never mangled.
#   3. Maps loose tool-request phrasings onto the exact triggers the
#      rigid handlers already match ("make me a story" -> "tell me a
#      story", "crack a joke" -> "tell me a joke", ...).
#   4. Normalizes a few very common casual descriptors ("how is the
#      weather in X", "i want to know the time").
#
# Handlers that extract payload text VERBATIM (ciphers, markdown tables,
# ASCII banners) already re-read the untouched original from
# ChatBot._current_raw_text rather than the matched text, so rewriting
# here can never corrupt user payloads.
class FlexiblePhraseNormalizer:
    """Rewrites flexible natural phrasing into canonical forms the rigid
    regex intents already understand. Deterministic, offline, fail-open."""

    # --- Leading filler prefixes (never trigger words themselves) ---
    FILLER_RE = re.compile(
        r"^\s*(?:please\s+)?(?:can you|could you|would you|will you|do you think you can)"
        r"(?:\s+please)?\s+"
        r"|^\s*please\s+"
        r"|^\s*(?:okay|ok|ok then|so|um|hmm|hmm,|uh|uhh|umm|right|alright),?\s+"
        r"|^\s*(?:well,\s+|look,\s+)"
        r"|^\s*(?:hey(?: there)?,\s+|yo,?\s+|aight,?\s+)"
        r"|^\s*(?:i want (?:you )?to|i'?d like (?:you )?to|i need you to|i would like (?:you )?to)\s+",
        re.IGNORECASE,
    )

    # --- Math-signal words: if absent, math-rewrites are skipped entirely ---
    MATH_SIGNAL_RE = re.compile(
        r"\d|times|multiplied|multiply|plus|minus|subtract|divided|divide|"
        r"squared|cubed|power|percent|square root|sqrt|log|ln|"
        r"calculate|compute|equation|solve|integrate|derive|derivative|over\b",
        re.IGNORECASE,
    )

    _ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven",
             "eight", "nine"]
    _TEENS = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
              "sixteen", "seventeen", "eighteen", "nineteen"]
    _TENS = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy",
             "eighty", "ninety"]
    _NUMBER_WORDS = set(_ONES) | set(_TEENS) | set(_TENS) | {"hundred", "thousand"}

    # --- Math word -> symbol (applied only when a math signal fired) ---
    MATH_WORD_SYMBOLS = [
        (r"\bmultiplied by\b", "*"),
        (r"\btimes\b", "*"),
        (r"\bdivided by\b", "/"),
        (r"\bto the power of\b", "^"),
        (r"\bpower\b", "^"),
        (r"\bplus\b", "+"),
        (r"\bminus\b", "-"),
        (r"\bminus\b", "-"),
        (r"\bsubtract\b", "-"),
        (r"\btake away\b", "-"),
        (r"\bsquared\b", "^2"),
        (r"\bcubed\b", "^3"),
    ]

    # --- Loose tool phrasing -> canonical trigger (word-boundary safe) ---
    PHRASE_SWAPS = [
        # stories
        (r"\bmake (?:me )?(?:a |an? )?story\b", "tell me a story"),
        (r"\bwrite (?:me )?(?:a |an? )?story\b", "tell me a story"),
        (r"\bcreate (?:me )?(?:a |an? )?story\b", "tell me a story"),
        (r"\bmake up (?:a |an? )?story\b", "tell me a story"),
        (r"\btell me a tale\b", "tell me a story"),
        (r"\bwrite me a tale\b", "tell me a story"),
        (r"\bmake (?:me )?(?:a |an? )?poem\b", "write me a poem"),
        (r"\bwrite (?:me )?some poetry\b", "write me a poem"),
        # jokes / quotes / riddles
        (r"\bcrack (?:me )?(?:a |an? )?joke\b", "tell me a joke"),
        (r"\btell (?:me )?something funny\b", "tell me a joke"),
        (r"\bsay a quote\b", "tell me a quote"),
        (r"\bshare (?:a |an? )?quote\b", "tell me a quote"),
        (r"\bgive me some wisdom\b", "tell me a quote"),
        (r"\briddle me this\b", "tell me a riddle"),
        (r"\btell me a funny joke\b", "tell me a joke"),
        (r"\btell me (?:a|an)other joke\b", "tell me a joke"),
        (r"\bgive me a joke\b", "tell me a joke"),
        (r"\bgive me an? (?:inspirational|inspiring) quote\b", "tell me a quote"),
        (r"\bgive me an? riddle\b", "tell me a riddle"),
        (r"\bgive me (?:a |some )?fun facts?\b", "tell me a fun fact"),
        (r"\bshare (?:a |an? )?fun fact\b", "tell me a fun fact"),
        (r"\bpick my brain\b", "ask me a trivia question"),
        (r"\bquiz me\b", "ask me a trivia question"),
        # images
        (r"\bgenerate (?:a |an? )?picture of\b", "generate image of"),
        (r"\bgenerate (?:a |an? )?photo of\b", "generate image of"),
        (r"\bmake (?:me )?(?:a |an? )?(?:picture|photo|image) of\b", "generate image of"),
        (r"\bcreate (?:a |an? )?(?:picture|photo) of\b", "generate image of"),
        # weather
        (r"\bhow is the weather (in|at|for)\b(.+)", r"weather in\2"),
        (r"\bhow('?s| is) the weather like (in|at|for)\b(.+)", r"weather in\3"),
        (r"\bwhat('?s| is) the weather like (in|at|for)\b(.+)", r"weather in\3"),
        (r"\bwhat'?s the weather (in|at|for)\b(.+)", r"weather in\2"),
        (r"\bwhat is the weather in\b(.+)", r"weather in\1"),
        (r"\bweather report for\b", "weather in"),
        (r"\bis it (?:sunny|raining|hot|cold|windy|snowing|cloudy|foggy) (?:in|at)\b(.+)", r"weather in\1"),
        (r"\ba hundred\b", "one hundred"),
        (r"\ba thousand\b", "one thousand"),
        # casual time/date/name knowledge asks
        (r"\b(?:i want to know|i'?d like to know|can you tell me|could you tell me) (?:the )?time\b",
         "what time is it"),
        (r"\b(?:i want to know|i'?d like to know|can you tell me|could you tell me) (?:today'?s |the )?date\b",
         "what's today's date"),
        (r"\b(?:i want to know|i'?d like to know|can you tell me|could you tell me) my name\b",
         "what is my name"),
    ]

    # --- Verb-object pairs that reset the normalizer's question until the
    #     filler strip above runs - placeholder for future expansion ---

    def _number_word_value(self, word):
        if word in self._ONES:
            return self._ONES.index(word)
        if word in self._TEENS:
            return 10 + self._TEENS.index(word)
        if word in self._TENS:
            return (self._TENS.index(word) + 2) * 10
        return None

    def _number_run_to_digits(self, tokens):
        """Converts a maximal run of number-word tokens (possibly with
        'and' connectors and 'point' decimals) to a digit string, or
        returns None if the run isn't a clean number phrase."""
        total = 0
        current = 0
        i = 0
        while i < len(tokens):
            w = tokens[i]
            if w == "point":
                frac = ""
                j = i + 1
                while j < len(tokens) and tokens[j] in self._ONES:
                    frac += str(self._ONES.index(tokens[j]))
                    j += 1
                integer = total + current
                return f"{integer}.{frac}" if frac else str(integer)
            if w == "and":
                i += 1
                continue
            if w == "hundred":
                current = (current or 1) * 100
            elif w == "thousand":
                total = (total + current) * 1000
                current = 0
            elif w in ("a", "an"):
                current += 1
            else:
                v = self._number_word_value(w)
                if v is None:
                    return None
                current += v
            i += 1
        return str(total + current)

    def _has_math_signal(self, text: str) -> bool:
        return bool(self.MATH_SIGNAL_RE.search(text))

    def _convert_number_words(self, text: str) -> str:
        words = text.split(" ")
        result = []
        i = 0
        n = len(words)
        while i < n:
            bare = words[i].strip(".,;:!?()").lower()
            next_bare = ""
            if i + 1 < n:
                next_bare = words[i + 1].strip(".,;:!?()").lower()
            starts_run = (
                bare in self._NUMBER_WORDS
                or bare == "point"
                or (bare in ("a", "an") and next_bare in ("hundred", "thousand"))
            )
            if starts_run:
                run = []
                j = i
                while j < n:
                    bj = words[j].strip(".,;:!?()").lower()
                    follow = ""
                    if j + 1 < n:
                        follow = words[j + 1].strip(".,;:!?()").lower()
                    in_run = (
                        bj in self._NUMBER_WORDS
                        or bj in ("point", "and")
                        or (bj in ("a", "an") and follow in ("hundred", "thousand"))
                    )
                    if in_run:
                        run.append(words[j])
                        j += 1
                    else:
                        break
                digits = self._number_run_to_digits(
                    [t.strip(".,;:!?()") for t in run])
                if digits is not None and digits != run[0].strip(".,;:!?()").lower():
                    trailing_punct = re.search(r"[.,;:!?]+$", words[j - 1])
                    result.append(digits + (trailing_punct.group(0) if trailing_punct else ""))
                    i = j
                    continue
            result.append(words[i])
            i += 1
        return " ".join(result)

    def _convert_math_words(self, text: str) -> str:
        lowered = text
        for pattern, symbol in self.MATH_WORD_SYMBOLS:
            lowered = re.sub(pattern, symbol, lowered, flags=re.IGNORECASE)
        return lowered

    def _rewrite_verb_operators(self, text: str) -> str:
        """Turns verb-first math phrasings ('multiply 6 by 5',
        'divide 20 by 4') into the operand-first form the math-symbol
        pass understands. Only ever runs inside the math-signal gate."""
        text = re.sub(
            r"\bmultiply\s+(\S+)\s+by\s+(\S+)",
            r"\1 multiplied by \2",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(
            r"\bdivide\s+(\S+)\s+by\s+(\S+)",
            r"\1 divided by \2",
            text,
            flags=re.IGNORECASE,
        )
        return text

    def _apply_phrase_swaps(self, text: str) -> str:
        lowered = text
        for pattern, replacement in self.PHRASE_SWAPS:
            lowered = re.sub(pattern, replacement, lowered, flags=re.IGNORECASE)
        return lowered

    def normalize(self, text: str) -> str:
        """Rewrites flexible phrasing toward canonical forms. Fail-open:
        anything not recognized passes through byte-identical."""
        if not text:
            return text

        # 1. Math rewrites - gated on a math signal so everyday prose is
        #    never touched, and done FIRST so "six times four" becomes
        #    "6 * 4" before filler/other passes.
        if self._has_math_signal(text):
            text = self._convert_number_words(text)
            text = self._rewrite_verb_operators(text)
            text = self._convert_math_words(text)

        # 2. Loose tool phrasings -> canonical triggers.
        text = self._apply_phrase_swaps(text)

        # 3. Leading conversational filler (after swaps, so canonical
        #    triggers like "give me a riddle" are never stripped).
        text = self.FILLER_RE.sub("", text, count=1).strip()

        # 4. Trailing politeness ("tell me a joke please" -> "tell me a joke"),
        #    so intent patterns with anchored ends still fire.
        text = re.sub(r"\s+please\b[.!?]*\s*$", "", text, flags=re.IGNORECASE)

        return text


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
        # No-apostrophe English contractions (fast casual typing): restore
        # the apostrophe so intent patterns like r"i'?d like to" or the
        # keyword matcher's possessive forms see the canonical spelling.
        "dont": "don't", "cant": "can't", "wont": "won't",
        "didnt": "didn't", "couldnt": "couldn't", "shouldnt": "shouldn't",
        "wouldnt": "wouldn't", "isnt": "isn't", "arent": "aren't",
        "wasnt": "wasn't", "werent": "weren't", "havent": "haven't",
        "hasnt": "hasn't", "doesnt": "doesn't",
        "im": "i'm", "ive": "i've", "youre": "you're",
        "youve": "you've", "youd": "you'd", "theyre": "they're",
        "theyve": "they've", "theyd": "they'd", "weve": "we've",
        "whats": "what's", "thats": "that's", "theres": "there's",
        # Casual collapsed phrases (informal but universally understood)
        "wanna": "want to", "gonna": "going to", "gotta": "got to",
        "gimme": "give me", "lemme": "let me", "kinda": "kind of",
        "coz": "because", "dunno": "don't know",
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
        "extract", "validate", "decode", "encode", "code", "qr",
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
        "niaje", "sasa", "fiti", "buda", "msee", "aman",
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
            "en": [ "i'm sad", 'i am sad', 'feeling down', 'unhappy', 'depressed', 'feeling sad', 'so sad',
                'really sad', 'i got left', 'i was left', 'she left me', 'he left me',
                'left me', 'broke up with me', 'my heart is broken', "i'm heartbroken",
                'heartbroken', 'i got dumped', 'i feel betrayed', 'betrayed by',
                'my partner left me', "it's over between us", 'i feel terrible', 'i am so down',
                "i'm so down today", "i'm really down", 'i feel horrible', 'i feel like crying',
                "i can't stop crying", "i've been crying", 'i feel empty',
                'feeling empty inside', 'i feel so alone inside', 'so heartbroken',
                'completely heartbroken', 'my heart is shattered', 'my heart is breaking',
                "i'm devastated", 'i am devastated', 'totally devastated', 'i feel crushed',
                'i feel so low', 'feeling really low', "i've hit rock bottom",
                'i hit rock bottom', 'crying my eyes out', 'in tears all the time',
                'i keep crying', "tears won't stop", "i'm so unhappy", 'this is so depressing',
                'i feel so down', 'feeling so down', 'i feel worthless',
                'i feel like a failure today', 'nothing makes me happy anymore',
                'i lost the will', "i don't feel like myself", "i'm not myself lately",
                'she broke up with me', 'he broke up with me', 'we broke up',
                'it ended with us', 'she dumped me', 'he dumped me', 'she walked away',
                'he walked away', 'she found someone else', 'he found someone else',
                'my heart aches', 'it hurts so bad'],
            "sw": [ 'nina huzuni', 'nimehuzunika', 'sina furaha', 'najisikia vibaya', 'nina furaha kidogo',
                'sina moyo wa kufanya lolote', 'nimevunjika moyo', 'moyo wangu umeumia',
                'nina huzuni kubwa', 'nimeishia chini', 'silala vizuri kwa huzuni',
                'ninalia kila siku', 'nahisi utupu ndani', 'najisikia peke yangu na huzuni',
                'nimepoteza furaha', 'kilichonitokea hakipendezi', 'nimekata tamaa',
                'sina mwelekeo'],
            "fr": [ 'je suis triste', 'je ne suis pas bien', 'je suis déprimé', 'très triste', 'si triste',
                'je me sens mal', 'je me sens vraiment mal', "j'ai envie de pleurer",
                "je n'arrête pas de pleurer", 'je me sens vide',
                "je me sens vide à l'intérieur", "j'ai le moral à zéro",
                'je suis complètement déprimé', 'je suis devasté', 'mon coeur est brisé',
                "j'ai le coeur brisé", 'ça me fait trop mal', 'je suis au plus bas',
                'je touche le fond', 'je ne suis plus moi-même', "elle m'a quitté",
                "il m'a quitté", 'on a rompu', "j'ai perdu goût à tout",
                'plus rien ne me rend heureux'],
        },
                "feelings_tired": {
            "en": [ "i'm tired", 'i am tired', 'exhausted', 'sleepy', 'need sleep', 'feeling tired', 'so tired',
                'really tired', "i'm exhausted", 'i am exhausted', 'totally exhausted',
                'completely exhausted', 'worn out', "i'm worn out", 'drained', 'i feel drained',
                'completely drained', 'running on empty', "i'm running on empty",
                'out of energy', 'i have no energy', 'no energy at all', "i'm so sleepy",
                "i'm really sleepy", 'feeling so tired', "i'm beat", "i'm so beat",
                'dead tired', 'doggone tired', 'i need to rest', 'i need some rest',
                "i'm burning out", 'i feel burnt out', 'can barely keep my eyes open',
                'my eyes are closing', 'too tired to think', 'too tired to do anything',
                "i'm falling asleep", 'i could sleep for days', 'need a nap', "i'm wiped",
                'totally wiped', "i'm wiped out", 'sleep deprived', "i haven't slept well"],
            "sw": [ 'nimechoka', 'nina usingizi', 'nahisi uchovu', 'uchovu sana', 'nimechoka sana',
                'nimechoka kabisa', 'sina nguvu kabisa', 'nimepoteza nishati',
                'najuanga usingizi', 'nina usingizi mkubwa', 'nahitaji kupumzika',
                'nimechoka kufa', 'siwezi kuamka', 'nimechoshwa na kila kitu',
                'lazima nipumzike', 'nimechoka mno'],
            "fr": [ 'je suis fatigué', 'épuisé', "j'ai sommeil", 'très fatigué', 'si fatigué', 'je suis épuisé',
                'je suis complètement épuisé', 'je suis à plat', "je n'ai plus d'énergie",
                "je n'ai aucune énergie", 'je suis mort de fatigue', 'je tombe de sommeil',
                "j'ai besoin de repos", 'je suis vidé', 'je suis crevé',
                'je suis au bout du rouleau', "je n'arrive plus à garder les yeux ouverts",
                'je suis sur les rotules'],
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
            "sw": ["habari", "jambo", "mambo", "niaje", "sasa", "vipi", "fiti", "freshi"],
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
            "en": [ "i can't do this", "i'm not good enough", 'i give up', "i'm a failure", "i'm struggling",
                "i can't do it", "i can't handle it", "i can't do anything right",
                'i always mess everything up', 'i always fail', 'i never succeed',
                "i'm not good at anything", "i'm useless", 'i feel useless',
                'i feel like a burden', "i'm a burden to everyone",
                'everyone is better than me', "i'll never make it", "i'll never get there",
                "it's hopeless", "there's no point", "what's the point anymore",
                'i want to quit', 'i feel like giving up', "i'm ready to give up",
                "i don't have the strength", "i'm at the end of my rope",
                "i've run out of options", "i'm running out of hope", 'i lost hope',
                "i'm losing hope", 'nothing i do matters', "i'm not making any progress",
                'i keep hitting walls', "i'm stuck and can't do it", "i'm too weak",
                "i'm not strong enough", "i don't have what it takes",
                "i can't go on like this", "i don't see a way out",
                "there's no light at the end of the tunnel"],
            "sw": [ 'siwezi kufanya hili', 'sina uwezo wa kutosha', 'nakata tamaa', 'ninapambana',
                'siwezi kufanya', 'siwezi kuendelea', 'sijafaulu chochote', 'daima nashindwa',
                'sina uwezo', 'ninajisikia bure', 'ninalemewa', 'nimechoka kupambana',
                'nimepoteza matumaini', 'hakuna tumaini', 'sina nguvu tena',
                'niishia kwenye ukuta', 'siwezi kuendelea hivi', 'sioni njia ya kutoka',
                'niko mwisho wa nguvu zangu', 'ninajisikia kuwa mizigo'],
            "fr": [ "je n'y arrive pas", 'je ne suis pas assez bien', "j'abandonne", 'je galère',
                "je n'y arriverai jamais", 'je ne peux pas le faire', "je n'arrive à rien",
                'je rate tout', 'je suis nul', 'je suis inutile', 'je suis un fardeau',
                'je ne suis pas assez fort', "je n'ai pas la force", 'je veux abandonner',
                'je suis prêt à abandonner', "c'est sans espoir", "j'ai perdu espoir",
                'je perds espoir', 'je suis au bout du rouleau', 'tout ce que je fais échoue',
                "je n'ai plus d'options", "je ne vois pas d'issue",
                "je n'ai plus la force de continuer"],
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
            "en": ["what should i do", "any advice", "what would you do", "need some advice",
                   "advice", "some advice", "need advice", "give me advice", "i need advice"],
            "sw": ["nifanye nini", "una ushauri", "ungefanya nini", "nahitaji ushauri"],
            "fr": ["que devrais-je faire", "des conseils", "que ferais-tu", "j'ai besoin de conseils", "conseille-moi"],
        },
        "comparison_topic": {
            "en": ["which is better", "compare", "versus", "difference between"],
            "sw": ["ni kipi bora", "linganisha", "tofauti kati ya"],
            "fr": ["lequel est mieux", "comparer", "différence entre"],
        },
                "feelings_angry_topic": {
            "en": [ "i'm angry", 'i am angry', 'so frustrated', 'this is annoying', 'makes me mad', 'so angry',
                'really angry', "i'm furious", 'i am furious', "i can't stand this",
                'this drives me crazy', "i'm really upset", 'i got so mad', 'making me angry',
                'i hate this', "i'm irritated", "i'm mad", 'i am mad', "i'm so mad",
                'really mad', 'so mad right now', "i'm so furious", "i'm livid", 'i am livid',
                'so livid', "i'm angry about", 'i am angry at', 'so angry at',
                'really angry at', 'mad at', "i'm annoyed", 'so annoyed', 'really annoyed',
                'i am irritated', 'so irritated', 'this is infuriating',
                'this is infuriating me', "i'm fuming", "i'm seeing red", 'it makes me see red',
                "i'm boiling with anger", "i'm seething", "i'm furious about it", "i'm pissed",
                "i'm so pissed", 'pissed off', "i'm so pissed off", 'this is so unfair',
                "it's so unfair", 'this makes my blood boil', "i'm losing my temper",
                "i'm about to lose it", "i'm about to snap", 'i want to scream',
                "i'm so frustrated", 'so frustrated with', 'frustrated at', 'grinds my gears',
                'drives me up the wall', "i can't believe this", 'unbelievable',
                'this is ridiculous'],
            "sw": [ 'nimekasirika', 'nina hasira', 'inasumbua', 'nina kinyongo', 'nimeshangaa vibaya',
                'nimekasirika sana', 'nina hasira kali', 'ninaandamtumbuka', 'nina mifo',
                'hii inanikasirisha', 'sina subira tena', 'nimechoka kuudhika',
                'maumivu ya moyo na hasira', 'najisikia kujitenga kwa hasira',
                'nimekasirika kupita kiasi', 'hili ni jambo la kutia hasira',
                'sipendi hata kidogo', 'nimechafuka'],
            "fr": [ 'je suis en colère', 'tellement frustré', "ça m'énerve", 'je suis furieux',
                'je ne supporte plus ça', 'ça me rend fou', 'je suis vraiment en colère',
                'je suis hors de moi', 'je suis fou de rage', 'je bouille',
                'je suis très énervé', 'ça me met en colère', 'ça me rend dingue',
                "j'en ai marre", "j'en ai ras-le-bol", 'je vais exploser',
                'je perds mon sang-froid', "c'est tellement injuste", "c'est vraiment injuste",
                'ça me révolte', 'je suis exaspéré', "c'est insupportable", 'je suis en rogne'],
        },
                "feelings_nervous_topic": {
            "en": [ "i'm nervous", 'i am nervous', 'feeling anxious', 'so nervous about', 'so nervous',
                'really nervous', "i'm so nervous", 'quite nervous', 'so nervous right now',
                "i'm anxious about", 'i am anxious about', "i'm worried about",
                'i am worried about', "i'm worried", "i'm so worried", "i'm stressed about",
                "i'm on edge", "i'm getting nervous", 'i have butterflies',
                'butterflies in my stomach', 'my stomach is in knots', "i'm worked up",
                "i'm shaking", 'my hands are shaking', "i'm shaking with nerves",
                'i feel jittery', "i can't calm down", "i'm panicking", "i'm starting to panic",
                "i'm uneasy", 'i feel uneasy about', "i'm dreading it", "i'm dreading tomorrow",
                "i'm trembling", "i'm on pins and needles", "i'm freaking out",
                "i'm so freaked out", 'nervous wreck', "i'm a nervous wreck",
                "i'm scared to go", "i'm scared for the interview", 'nerves are getting to me',
                'the nerves are bad today', 'i feel sick with worry', "i've got the jitters"],
            "sw": [ 'nina wasiwasi', 'ninahisi wasiwasi', 'nina hofu kuhusu', 'nina wasiwasi sana',
                'nina hofu kubwa', 'nina mashaka', 'najisikia wasiwasi',
                'moyo wangu unaruka kwa wasiwasi', 'mikono yangu inatetemeka',
                'nina hofu ya kesho', 'siwezi kujituliza', 'ninaogopa kuhusu',
                'nina tabu kuhusu', 'nina wasiwasi kuhusu', 'nimeshangazwa kwa shida',
                'nakabiliwa na hofu'],
            "fr": [ 'je suis nerveux', 'je suis anxieux', "j'ai le trac pour", 'je suis très nerveux',
                'je suis stressé', 'je suis inquiet', 'je suis très inquiet',
                "je m'inquiète pour", "j'ai peur de", "j'ai l'estomac noué",
                "j'ai des papillons dans le ventre", 'je tremble', 'mes mains tremblent',
                'je suis sur les nerfs', "je n'arrive pas à me calmer", 'je panique',
                'je commence à paniquer', 'je redoute ça', 'je suis angoissé', "j'appréhende",
                "j'appréhende demain", 'je suis tétanisé'],
        },
                "anxiety_topic": {
            "en": [ 'anxiety', 'anxious thoughts', 'panic attack', 'panicking', 'overthinking', 'racing thoughts',
                "can't stop worrying", 'constant worry', 'on edge', 'stressful', 'stressed out',
                'overwhelmed', 'worried', 'so anxious', "i'm anxious", 'i am anxious',
                'worrying', 'i feel anxious', 'my heart races', 'heart racing', 'racing heart',
                'my heart pounds', 'pounding heart', 'heart is racing', "i'm so nervous",
                'i am so nervous', 'anxiety attack', "can't stop thinking about it",
                'worried sick', 'anxious right now', 'i feel anxious right now',
                "i'm feeling anxious", 'i get anxious', 'anxiety is hitting me',
                'my anxiety is bad today', 'anxiety got me', "i'm having a panic attack",
                'having a panic attack', "i'm panicking right now", "i can't breathe",
                'it feels like my chest is tight', 'my chest feels tight',
                'tightness in my chest', "i can't catch my breath", 'my breathing is shallow',
                "i feel like i'm suffocating", 'everything feels out of control',
                'i feel out of control', "my mind won't stop racing",
                'my brain is going a mile a minute', "i can't switch off my brain",
                'i keep worrying about everything', 'i worry about everything', "i'm a worrier",
                'i feel on edge', "i've been on edge all day", 'everything makes me jumpy',
                "i'm jumpy", 'i feel tense', 'my muscles are tense', "i'm constantly tense",
                'i feel wound up', "i'm wound up", "i can't relax", 'i feel restless',
                'my thoughts are spinning', "my thoughts won't settle",
                'i keep going over worst case scenarios', 'i imagine the worst',
                'my mind always goes to the worst', 'what if everything goes wrong',
                "i'm dreading something", 'i feel dread', 'a sense of dread',
                'i have this dread feeling', 'anxiety is taking over',
                'the anxiety is overwhelming', "i'm overwhelmed by worry",
                "i can't function, i'm so anxious", 'anxious and twitchy',
                'feel like crying from nerves'],
            "sw": [ 'wasiwasi mkubwa', 'hofu ya ghafla', 'mawazo mengi', 'siwezi kuacha kuwa na wasiwasi',
                'nina wasiwasi mwingi', 'wasiwasi unanimeza', 'ninahisi mashaka',
                'ninategemea mabaya', 'siwezi kupumua vizuri', 'kifua changu kinabanana',
                'nikiliwaza yote inaonekana mbaya', 'mawazo yangu hayasemi',
                'akili yangu inazunguka zunguka', 'sijisikii salama',
                'nina wasiwasi kuhusu kila kitu', 'naogopa mabaya yatetendeka',
                'inakuwaje mabaya kila mara', 'naweza kukosa usingizi kwa mawazo',
                'moyo wangu unapigapiga', 'nina hisia ya hatari'],
            "fr": [ 'anxiété', "crise d'angoisse", 'pensées qui tournent en boucle',
                "je n'arrive pas à arrêter de m'inquiéter", 'sur les nerfs',
                "j'ai une crise d'angoisse", 'je fais une crise de panique',
                "j'ai une crise de panique", 'je panique', "je n'arrive pas à respirer",
                "j'ai l'impression d'étouffer", 'ma poitrine est serrée',
                "j'ai une boule dans la gorge", 'mon coeur bat la chamade',
                "mon coeur s'emballe", 'je ne peux pas arrêter de penser au pire',
                'je pense toujours au pire scénario', 'je me sens sur les nerfs',
                "j'ai le trac", 'je suis tendu', 'je suis crispé',
                'je suis stressé en permanence', 'mes pensées tournent en boucle',
                "mes pensées ne s'arrêtent pas", "je n'arrive pas à m'arrêter de m'inquiéter",
                "je m'inquiète pour tout", "j'ai un sentiment de malheur imminent",
                "je suis submergé par l'anxiété", "l'anxiété me submerge",
                "je me sens submergé d'inquiétude"],
        },
                "feelings_lonely_topic": {
            "en": [ 'i feel lonely', "i'm lonely", 'feeling alone', 'nobody to talk to', 'so lonely',
                'really lonely', 'all alone', 'no one understands', 'i feel invisible',
                'left out', 'isolated', 'all by myself', 'i feel alone', 'i am alone',
                "i'm all alone today", "i'm so alone", 'i feel so alone',
                'i feel totally alone', "i'm by myself too much", "i'm always by myself",
                'i spend my days alone', 'i have nobody', "i've got no one",
                'no one to spend time with', 'nobody to hang out with', 'i have no friends',
                "i don't have friends", 'nobody texts me', 'no one calls me',
                'no one reaches out to me', "it's just me and my thoughts",
                "i'm surrounded by people but feel alone", 'lonely even in a crowd',
                'i feel disconnected from everyone', 'i feel distant from people',
                'no one really knows me', 'nobody understands me', 'i feel like nobody cares',
                'it feels like no one cares', "i'm going through it alone", 'i feel abandoned',
                'i feel forgotten', 'like everyone forgot about me', "i'm invisible to people",
                "i feel like i don't belong", "i don't fit in anywhere", "i'm always left out",
                'always the third wheel', 'i feel so isolated', 'isolating myself',
                "i've been isolating", 'i shut everyone out', 'i have no one to talk to',
                'there is no one to talk to', 'i miss having people around',
                'i miss companionship'],
            "sw": [ 'ninahisi upweke', 'nina upweke', 'sina mtu wa kuongea naye', 'mimi peke yangu',
                'nimeachwa peke', 'najisikia mpweke', 'niko peke yangu', 'nimebaki peke yangu',
                'sina rafiki', 'hakuna mtu aniyefikiria', 'hakuna mtu ananijali',
                'najisikia kutengwa', 'nahisi nimeachwa', 'najisikia nisiyefahamika',
                'sijafaa popote', 'najisikia mbali na wengine',
                'ninaishi siku zangu peke yangu', 'nimekunja uso peke yangu',
                'hakuna mtu anayenizingatia', 'nimezoea upweke', 'upweke unaniumiza'],
            "fr": [ 'je me sens seul', 'je suis seul', 'personne à qui parler', 'tout seul',
                'je me sens invisible', 'je suis seul si souvent', 'je suis tout seul',
                'je me sens complètement seul', "je n'ai personne", "je n'ai pas d'amis",
                "personne ne m'appelle", 'personne ne me contacte', 'personne ne pense à moi',
                'je suis toujours seul', 'je passe mes journées seul', 'je me sens isolé',
                'je me sens abandonné', 'je me sens oublié', 'je me sens à part',
                "je n'ai personne à qui parler", 'personne ne me comprend',
                'je me sens étranger partout', 'la solitude me pèse', 'je me sens exclu',
                'je suis seul au milieu des autres'],
        },
                "stress_overwhelm_topic": {
            "en": [ "i'm stressed", 'i am stressed', 'so stressed', "i'm so stressed", 'burned out', 'burnt out',
                'so much pressure', 'pressure at work', 'ruining my sleep',
                'pressure is getting to me', 'too much on my plate', "i can't handle it all",
                'everything is too much', "i'm cracking under pressure",
                "i don't know how to cope", "i'm overwhelmed", 'i am overwhelmed',
                'so overwhelmed', 'totally overwhelmed', 'i feel overwhelmed',
                "i'm feeling overwhelmed", 'overwhelmed by everything', "it's all too much",
                'this is too much', 'too much on my shoulders', 'carrying too much',
                'i have too much to do', 'my to-do list is crazy', 'deadlines are piling up',
                "i'm drowning in work", 'buried in work', "i'm drowning",
                'sinking under pressure', 'i feel swamped', "i'm swamped",
                "i've got too much to handle", "i can't keep up", 'everything is piling up',
                'one thing after another', "i'm juggling too many things",
                "i'm stretched too thin", "i'm spread too thin", 'under a lot of pressure',
                'under so much pressure', "i'm under stress", 'work is stressing me',
                'work stress is killing me', 'school is stressing me out',
                'family is stressing me', "i'm stressed about money", 'money is stressing me',
                "i'm stressed about my exams", 'the pressure is too much', "i'm cracking",
                "i'm about to crack", "i'm at my breaking point", "i've hit my limit",
                "i can't take it anymore", "i can't handle this anymore",
                'i feel like everything is closing in', 'the walls are closing in',
                'i desperately need a break', 'i need a break from everything'],
            "sw": [ 'nina msongo', 'nimechoka sana', 'mzigo mwingi kwangu', 'shinikizo kubwa',
                'siwezi kuvumilia tena', 'nimelemewa na kazi', 'nimezidiwa',
                'nimezidiwa na kila kitu', 'nina mzigo mwingi', 'mzigo ni mwingi sana',
                'sina muda wa kutosha', 'kazi imenijaa', 'ninajitosa chini ya shinikizo',
                'shinikizo linanimeza', 'siwezi kuvumilia', 'nimefika ukingoni',
                'nimechoka kabisa na shida', 'nilisahau kupumzika', 'naumia kwa shinikizo',
                'kila kitu kiko juu yangu', 'sina tena nguvu ya kuvumilia'],
            "fr": [ 'je suis stressé', 'je suis tellement stressé', 'surmené', 'épuisé mentalement',
                'trop de pression', "je n'arrive plus à gérer", 'je craque sous la pression',
                "c'est trop pour moi", 'je suis débordé', 'je suis submergé',
                'je suis complètement débordé', 'tout est trop', "j'en ai trop sur les épaules",
                "j'ai trop de choses à faire", 'je me noie dans le travail',
                'je suis débordé de travail', 'je ne suis plus capable de suivre',
                'je suis à bout', 'je suis au bord du gouffre', 'je vais craquer',
                "j'étais à ma limite", "je n'en peux plus", 'je ne supporte plus',
                "j'ai trop de pression", 'je travaille sous pression', 'le travail me stresse',
                "je suis stressé par l'argent", 'je suis stressé par mes examens',
                "l'école me stresse", 'la pression devient insupportable'],
        },
                "decision_making_topic": {
            "en": [ "i can't decide", "can't decide", 'torn between', 'choose between', 'make a decision',
                "it's a tough choice", 'hard decision', "i don't know what to pick", 'dilemma',
                'what should i choose', 'weighing my options', "i'm going back and forth",
                "can't make up my mind", 'i have to choose', 'i need to choose',
                'i must decide', 'i need to decide', 'i have to make a decision',
                'i need to make a choice', 'torn', "i'm torn", "i'm torn between two",
                "i'm conflicted", 'i feel conflicted', "i'm arguing with myself",
                'you think i should', 'what do i do', 'what should i do', 'what would you do',
                'which one do i pick', 'which is better', 'pros and cons',
                'weigh the pros and cons', "i'm weighing my options", 'i listed the options',
                'i can see both sides', 'i like both', "i'm stuck between", "i'm split",
                "i'm on the fence", 'on the fence about', 'iffy about',
                'not sure which way to go', 'i keep changing my mind', 'i flip flop',
                "i'm flip flopping", 'hard choice', 'tough choice', 'difficult choice',
                'major decision', 'big decision', 'life changing decision',
                'a big life decision', 'i have two offers', 'both options look good',
                'either way i lose', "damned if i do, damned if i don't", "i can't decide if"],
            "sw": [ 'siwezi kuamua', 'nimegawanyika kati', 'chagua kati ya', 'uamuzi mgumu',
                'sijui nichague nini', 'nina tabu ya kuchagua', 'naendelea kubadilisha nia',
                'nahitaji kuchagua', 'lazima nichague', 'lazima niamue', 'nimegawanyika',
                'ninasita', 'najisikia kuchanganyikiwa', 'unafikiri nifanye nini',
                'nifanye nini', 'wingapi ni bora', 'faida na hasara', 'nauelekea pande zote',
                'sijui niende wapi', 'nina mashaka ya kuchagua', 'sijaamua bado',
                'ninabadilisha nia kila mara', 'uamuzi mkubwa'],
            "fr": [ "je n'arrive pas à décider", 'je suis partagé entre', 'choisir entre',
                'une décision difficile', 'je ne sais pas quoi choisir', "j'hésite",
                'je ne peux pas me décider', 'je dois choisir', "j'ai besoin de choisir",
                'je dois décider', 'je dois prendre une décision', 'je suis partagé',
                'je suis indécis', 'je suis déchiré', 'je suis tiraillé',
                'tu penses que je devrais faire quoi', 'je fais quoi',
                'que ferais-tu à ma place', 'lequel choisir', 'le pour et le contre',
                "j'hésite entre", 'je balance', 'je suis sur la corde raide',
                'je ne sais pas quelle direction prendre', "je n'arrive pas à me décider",
                "je change sans cesse d'avis", 'choix difficile', 'décision importante',
                'une décision qui change la vie'],
        },
                "curiosity_topic": {
            "en": [ "i'm curious", 'i wonder', 'curious about', 'how does it work', "i've been wondering",
                'it makes me wonder', "i'd like to understand", "what's the science behind",
                'how do they make', 'tell me about how', "i've been wondering about that",
                'how does', 'how do', 'why is', 'why do', 'why are', 'why does', 'why would',
                'what happens when', 'what happens if', "what's the difference between",
                'what is the meaning of', 'explain this to me', 'can you explain',
                'explain it to me', 'i need to understand', 'i want to understand',
                "i'd love to know", 'i wanna know', 'i want to know more',
                'tell me more about that', 'go deeper on that', "i'm curious how",
                'curious about the world', 'been curious about', 'always wondered',
                "i've always wondered", 'i sometimes wonder', 'i wonder why', 'i wonder how',
                'that makes me curious', 'this is so interesting', 'i find that fascinating',
                'i find it fascinating', 'interesting question', 'that got me thinking',
                'it got me wondering', 'let me think about', 'how is that possible',
                'is that possible', 'how does that work', 'can you teach me',
                'teach me something', 'i want to learn', 'i love learning'],
            "sw": [ 'nina hamu ya kujua', 'nashangaa', 'ninajiuliza', 'inafanya kazi aje',
                'nimekuwa nikijiuliza kuhusu', 'kama vipi', 'vipi',
                'je kazi yake inavyofanya kazi', 'kwa nini', 'inaukurkasi',
                'nini kitatokea ikiwa', 'nini tofauti kati ya', 'unaelekeza nini',
                'naomba unieleze', 'naelewa kidogo', 'nataka kujua zaidi',
                'nina shauku ya kujua', 'nimekuwa nikijiuliza', 'daima nilijiuliza',
                'hilo linanifanya nijiulize', 'inavutia sana', 'inanishangaza',
                'unawelweza kunifundisha', 'nataka kujifunza'],
            "fr": [ 'je suis curieux', 'je me demande', 'curieux de savoir', 'comment ça marche',
                'je me posais la question', "j'aimerais comprendre", 'comment est-ce que',
                'comment ça', 'pourquoi est-ce que', 'pourquoi', "qu'est-ce qui se passe si",
                'quelle est la différence entre', 'quelle est la signification de',
                'explique-moi ça', "tu peux m'expliquer", "j'ai besoin de comprendre",
                'je veux comprendre', "j'aimerais savoir", 'je veux en savoir plus',
                "dis-m'en plus", 'je suis curieux de savoir', "j'ai toujours voulu savoir",
                'je me demande pourquoi', 'ça me rend curieux', "c'est fascinant",
                'je trouve ça passionnant', "tu peux m'apprendre", "j'aime apprendre",
                'je cherche à comprendre'],
        },
                "rumination_topic": {
            "en": [ 'i keep thinking about', "thoughts won't stop", 'keep replaying',
                "can't get it out of my head", 'intrusive thoughts', 'it keeps coming back',
                "my mind won't stop", 'i keep replaying it', "the thought won't leave",
                'i keep going over it', "my brain won't shut up about it",
                'i keep thinking about it', "i can't stop thinking about",
                "can't stop thinking", 'i keep replaying it in my head',
                'it plays in my head on repeat', 'i keep reliving it', 'i keep remembering',
                'i keep thinking back', 'the memory keeps coming back', 'it haunts me',
                "i'm haunted by it", "it's eating at me", "it's gnawing at me",
                "i can't let it go", "i can't move on", 'my mind is stuck on it',
                "my head won't drop it", "brain won't drop it", 'i obsess over',
                'i keep obsessing', "it's all i think about", 'it occupies my mind',
                'consuming my thoughts', 'constantly on my mind', 'always on my mind',
                'i think about it nonstop', 'thoughts are looping', 'looping thoughts',
                'same thought over and over', 'recurring thought', 'i ruminate',
                "i'm ruminating", 'i dwell on it', 'i keep dwelling', 'spiraling thoughts',
                'my thoughts are spiraling', 'down the rabbit hole of worry',
                'i beat myself up over it', 'i keep punishing myself with the memory'],
            "sw": [ 'naendelea kufikiria', 'mawazo hayaachi', 'siwezi kuisahau', 'mawazo yanaingia bila hiari',
                'akili yangu haiketi', 'naendelea kuifikiria', 'siwezi kuacha kufikiria',
                'inarudi nakumbuka kila mara', 'inaniuma kila mara nakumbuka',
                'akili yangu imefungwa kwake', 'inaniumiza moyoni',
                'inakuja mara kwa mara akilini', 'ninafikiria juu yake usiku na mchana',
                'mawazo yanarudi rudi', 'sinaweza kujiondoa nayo', 'ni kama inanifuata',
                'najiambia mwenyewe kila mara', 'ninajidharau juu yake'],
            "fr": [ "je ne peux pas m'empêcher d'y penser", 'je repense sans cesse', 'je ressasse',
                "je n'arrive pas à l'empêcher de revenir", 'pensées intrusives',
                "mon esprit n'arrête pas d'y revenir", "je n'arrête pas d'y penser",
                "je ne peux pas arrêter d'y penser", 'je repense sans cesse à',
                'je ressasse encore', 'je ressasse et ressasse', 'ça revient sans cesse',
                'ça me hante', 'je suis hanté par ça', 'ça me ronge',
                "je n'arrive pas à passer à autre chose", 'mon esprit est fixé dessus',
                'je ne peux pas lâcher prise', "c'est tout ce que je pense",
                'ça occupe mes pensées', 'je pense à ça sans arrêt', 'pensées en boucle',
                'je rumine', "je m'attarde sur ça", 'mes pensées tournent en spirale',
                'je me culpabilise avec ces souvenirs'],
        },
                "feelings_proud_topic": {
            "en": [ "i'm proud of myself", 'feeling proud', "i'm proud that", 'proud of my', 'so proud',
                'really proud', 'i passed', 'i got the job', 'i did it', 'i finally did it',
                'i got accepted', 'i won', 'i got promoted', "i'm so proud of myself",
                'proud of what i did', 'i did something brave', 'i stood up for myself',
                "i'm proud", 'i am proud', 'i feel proud', 'so proud of myself',
                'i am proud of myself', 'i made myself proud', "i'm proud of what i did",
                'proud of my progress', 'proud of my growth', "i'm proud of how far i've come",
                "i'm proud of myself today", "i'm proud of my work", "i'm proud of my result",
                'i impressed myself', 'i surprised myself', 'i outdid myself',
                'i exceeded my own expectations', 'i came through', 'i pulled through',
                'i made it happen', 'i got it done', 'i nailed it', 'i crushed it', 'i aced it',
                'i knocked it out of the park', 'i stood my ground', 'i was brave',
                'i faced my fear', 'i overcame my fear', 'i did something hard',
                'i did something i was scared of', 'i finally passed', 'i passed the test',
                'i passed the exam', 'i got the grade i wanted', 'i got into the program',
                'i got the scholarship', 'i got the job offer', 'i landed the job',
                'i was selected', 'i won the award', 'i got first place',
                'i won the competition', 'my hard work paid off', 'it all paid off',
                "i'm glowing with pride"],
            "sw": [ 'ninajivunia mwenyewe', 'ninahisi fahari', 'ninajivunia', 'nimefanya vizuri', 'nimeshinda',
                'najisikia fahari', 'nimejishangaza mwenyewe',
                'nimezidi matarajio na upande mwenyewe', 'nilifanya vizuri sana',
                'nimepita mtihani', 'nimepata kazi', 'nimechukua hatua za ujasiri',
                'nilichokimaliza kimenishinda', 'nimefanya jambo gumu',
                'nimekabiliana na hofu yangu', 'kazi yangu imelipa', 'nilishinda tuzo',
                'nilipata nafasi ya kwanza'],
            "fr": [ 'je suis fier de moi', 'je me sens fier', 'fier de mon', "j'ai réussi", "j'ai gagné",
                "je suis fier de ce que j'ai fait", 'je suis fier', 'je suis fière de moi',
                'fier de ma progression', 'fier de mon évolution',
                'je suis fier du chemin parcouru', 'je me suis impressionné',
                'je me suis surpassé', "j'ai dépassé mes attentes", "je l'ai fait",
                "je m'en suis sorti", "j'ai excellé", "j'ai fait face à ma peur",
                "j'ai surmonté ma peur", "j'ai fait quelque chose de difficile",
                "j'ai enfin réussi l'examen", "j'ai eu le poste", "j'ai été embauché",
                "j'ai gagné le prix", "j'ai eu la première place",
                'mes efforts ont porté leurs fruits', "j'ai tenu bon", "j'ai été courageux"],
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
            "en": [ 'taking care of my mental health', 'feeling overwhelmed', 'need a mental break',
                'my mental health', 'checking in on my mental health',
                "i'm working on my mental health", 'my mental health matters',
                'my mental well being', 'mental health', 'i need a mental health day',
                'i need to focus on my mental health', "i'm taking a mental health break",
                'my head is not in a good place', "i'm not in a good headspace",
                'my headspace is bad right now', "i'm struggling mentally",
                "i'm not okay mentally", "mentally i'm burned out", 'i need therapy',
                'i should see a therapist', 'i want to talk to a counselor',
                'i keep it all inside', 'i bottle everything up', "i don't process my feelings",
                'i need to rest my mind', 'my brain needs a break', 'i feel mentally drained',
                "i'm emotionally drained", 'my emotions are all over the place',
                "i can't manage my emotions", 'i want to work on myself', "i'm trying to heal",
                "i'm on my healing journey", 'working on my wellbeing',
                'taking care of my mind'],
            "sw": [ 'kujali afya yangu ya akili', 'ninahisi nimezidiwa', 'nahitaji mapumziko ya akili',
                'nafuatilia afya yangu ya akili', 'ninafanyia kazi afya yangu ya akili',
                'ninahitaji siku ya kupumzika akili', 'kichwa changu hakiko sawa',
                'sijisikii vizuri kiakili', 'ninahitaji msaada wa kisaikolojia',
                'nihitaji mjazo', 'ninafinywa hisia zangu', 'nahisi nimechoka kiakili',
                'nyoyo yangu inatatizika', 'nataka kuboresha maisha yangu ya ndani',
                'ninafanyia kazi kujipanga'],
            "fr": [ 'prendre soin de ma santé mentale', 'je me sens dépassé', "j'ai besoin d'une pause mentale",
                'je prends soin de ma santé mentale', 'ma santé mentale compte',
                "j'ai besoin d'une journée de repos mental",
                "ma tête n'est pas dans un bon état", 'je ne vais pas bien mentalement',
                'je suis épuisé mentalement', 'je suis vidé émotionnellement',
                'je refoule tout', "j'ai besoin de parler à quelqu'un",
                'je dois voir un médecin', 'je dois consulter', 'je veux aller mieux',
                'je suis sur mon chemin de guérison', 'je travaille sur moi-même',
                "j'ai besoin de faire une pause mentale"],
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
            "en": [ 'we did it', "let's celebrate", 'this calls for celebration', 'cheers to that', 'great news',
                'good news', "i've got some great news", 'big news', 'guess what',
                'i did something great', 'i got something to celebrate', 'we made it', 'we won',
                'we passed', 'time to celebrate', 'something to celebrate',
                'i have news to celebrate', 'big win today', 'small win today',
                'little victory', "i'm celebrating", 'cheers', "here's to us",
                'we deserve a treat', "let's pop some champagne", 'good tidings',
                'fantastic news', 'wonderful news', 'amazing news', 'great day today',
                'things are looking up', 'good things are happening', 'finally some good luck',
                'i pulled it off', 'it worked out', 'everything worked out',
                'it finally happened', 'guess what happened', 'wanna know what happened',
                'i have something fun to share', 'good things today',
                'i got a pleasant surprise', 'the plan worked', 'we crushed it', 'we aced it',
                'snagged a win'],
            "sw": [ 'tumefanya', 'tusherehekee', 'hii inahitaji sherehe', 'habari njema', 'nina habari njema',
                'tumefanikiwa', 'tumeshinda', 'tumepita', 'ni wakati wa sherehe',
                'kuna kitu cha kusherehekea', 'habari njema sana', 'ushindi mdogo leo',
                'ninasherehekea', 'mambo yanaenda vizuri', 'mambo yamekamilika',
                'nimepata baraka leo', 'tumefanya vizuri', 'nilipata mshangao mzuri'],
            "fr": [ "on l'a fait", 'célébrons', 'ça appelle une célébration', 'bonne nouvelle',
                "j'ai de bonnes nouvelles", "j'ai fait quelque chose de super", 'on a réussi',
                'nous avons réussi', 'on a gagné', "on a réussi l'examen",
                "c'est l'heure de célébrer", "j'ai de quoi célébrer",
                "une petite victoire aujourd'hui", 'je célèbre', 'excellente nouvelle',
                'merveilleuse nouvelle', "belle journée aujourd'hui", "les choses s'améliorent",
                'ça a marché', "c'est enfin arrivé", "j'ai eu une bonne surprise"],
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
            "en": [ 'i miss her', 'i miss him', 'i miss them', 'miss my friend', 'miss my family', 'i miss you',
                'i miss so much', 'missing her', 'missing him', 'missing my friend',
                'missing my family', 'i really miss her', 'i really miss him',
                'i miss being with them', 'i miss home', "i'm homesick", 'homesick for',
                'i miss my mom', 'i miss my dad', 'i miss my sister', 'i miss my brother',
                'i miss my grandma', 'i miss my grandpa', 'i miss my old friends',
                'i miss the good old days', 'i miss school', 'i miss my classmates',
                'i miss my childhood', 'i miss those times', 'i wish they were here',
                'i wish she was here', 'i wish he was here', 'i wish you were here',
                'it feels empty without them', 'life feels empty without',
                "i can't wait to see them", 'i long to see them', 'i yearn for',
                'missing that person', 'i miss everyone', 'wish my friend was around',
                'i think about them constantly'],
            "sw": [ 'ninamkosa', 'ninawakosa', 'ninamkosa rafiki yangu', 'ninaikosa familia yangu', 'nakumiss',
                'ninaumiza kukosa', 'ninamkosa sana', 'ninamkosa mama yangu',
                'ninamkosa baba yangu', 'ninamkosa dada yangu', 'ninamkosa kaka yangu',
                'ninawakosa wandugu', 'nina hamu ya kuwaona', 'natamani wangekuwa hapa',
                'nina nyumba nzima ninayoikosa', 'sijawaona muda mrefu', 'nahimaji muda nao',
                'ninakosa nyumbani', 'nimechoka kuwa mbali nao'],
            "fr": [ 'elle me manque', 'il me manque', 'ils me manquent', 'mon ami me manque', 'tu me manques',
                'elle me manque tellement', 'il me manque tellement', 'ça me manque',
                'ma famille me manque', 'ma mère me manque', 'mon père me manque',
                "j'ai le mal du pays", 'je pense constamment à eux',
                "j'aimerais qu'ils soient là", "j'aimerais qu'elle soit là",
                "j'aimerais qu'il soit là", 'la vie est vide sans eux',
                "j'ai hâte de les revoir", "je m'ennuie d'eux", 'il me manque énormément'],
        },
        "excitement_event_topic": {
            "en": ["so excited for", "can't wait for", "really looking forward to", "counting down to"],
            "sw": ["nimevutiwa sana na", "siwezi kusubiri", "ninatazamia sana"],
            "fr": ["tellement excité pour", "je ne peux pas attendre", "j'attends avec impatience"],
        },
                "disappointment_topic": {
            "en": [ "i'm disappointed", "that's disappointing", "didn't go as planned", 'expected better',
                'i feel disappointed', 'i am let down', 'this is disappointing',
                'that was disappointing', 'so disappointing', 'really disappointing',
                "i'm let down", 'feeling let down', 'that let me down', 'you let me down',
                'i expected more', 'i expected better of', 'that was a letdown',
                'what a letdown', 'that fell flat', 'that was a flop', 'this was a letdown',
                'i got my hopes up', 'i had high hopes for', 'my hopes got crushed',
                "i'm underwhelmed", 'that disappointed me', "it didn't match expectations",
                "it didn't live up to the hype", "i'm not happy with how it went",
                "that didn't go the way i wanted", "it didn't turn out as i hoped",
                "that wasn't what i hoped for"],
            "sw": [ 'nimekata tamaa', 'hiyo inakatisha tamaa', 'haikuwenda kama ilivyopangwa', 'nimesikitishwa',
                'nimehu mishka', 'nimekatazwa', 'hii inakatisha tamaa',
                'nimeweka matumaini makubwa', 'matumaini yangu yamevunjika', 'sikutarajia hivi',
                'umekatisha tamaa', 'nilitegemea zaidi', 'hayajakwenda kama nilitaka',
                'sijafurahishwa na hilo', 'niliyotarajia hayakutokea'],
            "fr": [ 'je suis déçu', "c'est décevant", "ça ne s'est pas passé comme prévu",
                'je suis vraiment déçu', 'je suis déçu par', "que c'est décevant",
                'je me sens déçu', "j'attendais mieux", "j'espérais mieux de sa part",
                "c'était une déception", 'quelle déception',
                "je suis déçu de la façon dont ça s'est passé",
                "ça ne s'est pas passé comme je voulais", "c'est pas ce que j'espérais",
                "je m'attendais à mieux"],
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
            "en": [ 'reached a milestone', 'hit a milestone', 'big achievement', 'proud milestone', 'i achieved',
                'i accomplished', 'i finally reached', 'i hit a goal', 'i completed it',
                'i finished the project', 'i graduated', 'i reached a goal',
                'i achieved a goal', 'i met a goal', 'i hit my goal', 'i reached my target',
                'i reached a milestone', 'i crossed a milestone', 'major milestone',
                'huge milestone', 'personal milestone', 'major achievement',
                'great achievement', 'i achieved something', 'i finally achieved',
                'i accomplished something', 'i finally accomplished', 'i completed a big task',
                'i finished a big project', 'i concluded a goal', 'i landed it', 'i earned it',
                'i earned it myself', 'i was recognized for', 'got recognized at work',
                'got a promotion', 'i graduated college', 'i finished school',
                'i completed my degree', 'i got my degree', 'i finished my training',
                'i completed the marathon', 'i ran a marathon', 'i saved up enough',
                'i paid off my debt', 'i bought my first car', 'first year sober',
                'i hit one year', 'i marked an important day', 'i achieved a life goal'],
            "sw": [ 'nimefikia hatua muhimu', 'mafanikio makubwa', 'nimefikisha lengo', 'nimehitimu',
                'nimefikia lengo la maisha', 'nimekamilisha kazi kubwa', 'nimepata promotion',
                'nilitambuliwa kazini', 'nimefanya vizuri sana', 'nimeweza kufanikiwa',
                'nimeweza kusudi', 'nimebeba jina la mafanikio', 'mbele ya wengi nimetunukiwa',
                'nimekamilisha mradi wangu'],
            "fr": [ "j'ai atteint une étape importante", 'grande réalisation', "j'ai accompli",
                'je suis enfin arrivé au bout', "j'ai fini le projet",
                "j'ai obtenu mon diplôme", "j'ai atteint mon objectif", "j'ai atteint un but",
                "j'ai franchi une étape", 'une étape importante', 'une grande étape',
                'une grande réussite', "j'ai accompli quelque chose", "j'ai enfin accompli",
                "j'ai terminé un grand projet", "j'ai terminé un gros travail",
                'je me suis fait reconnaître', "j'ai été reconnu au travail",
                "j'ai eu une promotion", "j'ai terminé mes études", "j'ai réussi ma formation",
                "j'ai bouclé mon premier mois"],
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
            "en": [ "i'm afraid of", 'scared of', 'my biggest fear', 'phobia of', 'i am afraid of', 'i fear',
                'i fear that', "i'm scared of", 'i am scared of', "i'm terrified of",
                "i'm terrified that", "i'm deathly afraid of", 'scared to death',
                'i have a phobia', 'my phobia is', "i'm scared to do it", "i'm scared to try",
                "i'm afraid to speak up", 'i have stage fright', "i'm afraid of heights",
                "i'm scared of spiders", 'scared of the dark', 'afraid of failing',
                'scared to fail', 'i fear rejection', 'afraid of being judged',
                'fear of judgment', "i'm scared of what people think", 'i fear the unknown',
                'scared to take the risk', "i'm scared to move forward",
                'nothing scares me more than', 'my biggest fear is', 'my worst fear is',
                "that's my worst nightmare"],
            "sw": [ 'ninaogopa', 'hofu yangu kubwa', 'ninaogopa sana', 'nina hofu', 'nina uhofu', 'nina hofu ya',
                'ninaogopa kufeli', 'nina hofu ya kuanguka', 'hofu yangu kuu ni',
                'ninatetemeka kwa hofu', 'naogopa kukataliwa', 'ninaogopa kuhukumiwa',
                'nikizingatia jambo hicho naogopa', 'hiyo ndio ndoto yangu mbaya',
                'sina ujasiri kwa sababu ya hofu'],
            "fr": [ "j'ai peur de", 'ma plus grande peur', 'phobie de', "j'ai peur que", "j'ai très peur de",
                'je suis terrifié par', 'je crains', 'je crains que', "j'ai une phobie",
                'ma phobie est', "j'ai peur de l'échec", "j'ai peur du jugement",
                "j'ai peur de l'inconnu", "j'ai peur de prendre le risque",
                "j'ai peur d'avancer", "j'ai le traque", 'ma plus grande peur est',
                "c'est mon pire cauchemar", "je panique à l'idée de",
                "j'ai peur qu'on me rejette"],
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
            "en": [ 'lost a loved one', 'grieving', 'my loved one passed away', 'dealing with grief',
                'my dad passed away', 'my mom passed away', 'my mother passed away',
                'my father passed away', 'my brother passed away', 'my sister passed away',
                'my grandpa died', 'my grandma died', 'i lost my dad', 'i lost my mom',
                'i lost my brother', 'i lost my sister', 'i lost my best friend',
                'i lost someone close', 'someone close to me died', 'a family member died',
                'my family member passed', 'they passed away recently', "i'm grieving",
                "i'm in mourning", "i'm mourning my loss", 'in the middle of grief',
                "it's been hard since they died", "i still can't believe they're gone",
                "i can't accept the loss", 'the loss is too much', 'my grief is overwhelming',
                'i visited their grave', 'i remember them every day',
                "i'm heartbroken over the loss", 'dealing with the death of',
                'coping with loss', 'i attend the funeral'],
            "sw": [ 'nimepoteza mpendwa', 'ninaomboleza', 'mpendwa wangu amefariki', 'baba yangu amefariki',
                'mama yangu amefariki', 'nimepoteza mzazi wangu', 'kaka yangu amekufa',
                'dada yangu amekufa', 'nimepoteza mtu wa karibu',
                'nimepoteza rafiki yangu bora', 'naomboleza kifo', 'nina huzuni ya kifo',
                'bado siamini wameondoka', 'maumivu ya kupoteza yamaniweza',
                'huzuni yangu ni kubwa', 'niko kwenye mazishi', 'inaniumiza kutembelea kaburi',
                'nimezama kwenye maombolezo'],
            "fr": [ "j'ai perdu un être cher", 'je fais mon deuil', 'mon proche est décédé',
                'mon père est décédé', 'ma mère est décédée', "j'ai perdu mon père",
                "j'ai perdu ma mère", "j'ai perdu mon frère", "j'ai perdu ma sœur",
                "j'ai perdu quelqu'un de proche", 'un proche est décédé', 'je suis en deuil',
                'je suis dans le deuil', 'je pleure mon proche',
                "je ne peux pas croire qu'il est parti",
                "je ne peux pas croire qu'elle est partie", "c'est dur depuis son départ",
                'la perte est trop dure', 'mon chagrin est immense',
                'je pense à lui chaque jour', 'je pense à elle chaque jour'],
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
            "en": [ 'feeling stuck', 'i feel stuck', 'stuck in a rut', 'not moving forward', "i'm at a dead end",
                "i don't know where to go next", "i'm going in circles",
                "can't seem to move forward", 'feeling directionless', 'i feel stuck in life',
                "i'm stuck in life", 'my life is stuck', "i'm going nowhere",
                "i feel like i'm going nowhere", 'going in circles', 'i keep going in circles',
                "i'm stuck in a loop", "i'm on a treadmill", 'running but not moving',
                'no progress at all', "i'm not progressing", "i can't move forward",
                "i can't make progress", 'stuck in the same place', 'same problems every day',
                'nothing ever changes', 'i feel trapped', "i'm trapped in this situation",
                'trapped in my job', 'stuck in this job', "can't find a way out",
                'see no way forward', "i'm at a crossroads", "i don't know which way to go",
                'undecided about my future', 'my life feels on hold', "i'm treading water",
                'just treading water', 'i feel paralyzed', 'paralyzed by choices',
                "can't make anything happen", "i'm waiting for something to change",
                'waiting for my big break', 'i feel stagnated', 'my career is stuck',
                'my life is stagnant', "i'm stuck and can't see ahead"],
            "sw": [ 'ninahisi nimekwama', 'nimekwama', 'sisogei mbele', 'sijui niende wapi', 'nimekwama maishani',
                'maisha yangu yamekwama', 'sisongi mbele', 'nazunguka tu',
                'nimekwama kwenye kazi', 'sina mwelekeo wa maisha',
                'sijui nitafanya nini baadaye', 'nimefungwa kwenye hali hii',
                'hali inanizuia kusonga', 'siongei mbele kamwe', 'nasubiri kitu kibadilike',
                'nimejaa bila kusonga', 'sina njia ya kutoka', 'nimekubali kuwa mwili huu huo'],
            "fr": [ 'je me sens coincé', 'coincé dans une routine', "je n'avance pas",
                'je ne sais pas quoi faire ensuite', 'je tourne en rond',
                'je me sens coincé dans la vie', 'ma vie est au point mort',
                'je suis dans une impasse', 'je ne progresse pas', "je n'arrive pas à avancer",
                'je suis bloqué', 'je suis bloqué dans cette situation',
                'piégé dans mon travail', 'je ne peux pas sortir de là',
                'je ne vois pas de sortie', 'je suis à un carrefour', 'ma vie est en suspens',
                'je patauge', 'je me sens paralysé', 'mon travail stagne',
                'je stagne depuis des années', 'rien ne change jamais pour moi'],
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
