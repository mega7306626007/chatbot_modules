"""N-gram Markov model + tiny self-attention transformer (Sections 14, 14B)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 14: CONVERSATIONAL N-GRAM LANGUAGE MODEL (real "predict next word")
# ==============================================================================
#
# A genuine, classic word-prediction model - the same foundational
# technique behind early predictive-text keyboards and the first
# generation of chatbots/autocomplete systems, well before neural
# language models existed: count how often each word follows each
# 1-2 word context in a real training corpus, then sample from those
# learned frequency distributions to predict/continue text.
#
# Trained OFFLINE (not at runtime) on a real personal conversation
# corpus, specifically to capture a genuinely casual, human
# conversational register (contractions, code-switched English/
# Swahili/French, short reactive turns) rather than a generic or
# formal one. IMPORTANT PRIVACY NOTE: what's embedded below is NOT
# the raw conversation - it's PRUNED, AGGREGATED word-transition
# counts (any word sequence that appeared fewer than twice was
# dropped entirely). That deliberately keeps recurring STYLE/PATTERNS
# (how sentences tend to start, common short reactions, typical word
# transitions) while dropping one-off idiosyncratic personal details
# that only appeared once - the raw source text itself was never
# included and isn't reconstructable from these counts.
#
# Backoff strategy (a simplified version of classic Katz backoff):
# try the trigram table first (most specific, best prediction when
# available), fall back to bigram, then unigram, so the model can
# always produce SOME prediction rather than failing on an unseen
# context.
_NGRAM_UNIGRAMS = {
    "<end>": 655,
    "how's": 7,
    "you": 128,
    "doing": 8,
    "hello": 6,
    "sleeping": 5,
    "beauty": 6,
    "has": 8,
    "finally": 6,
    "who": 14,
    "the": 158,
    "true": 4,
    "love": 6,
    "kiss": 3,
    "this": 39,
    "is": 53,
    "st": 2,
    "century": 2,
    "i": 185,
    "just": 16,
    "set": 4,
    "an": 11,
    "alarm": 3,
    "can't": 10,
    "on": 30,
    "prince": 3,
    "charming": 3,
    "he": 11,
    "might": 3,
    "be": 33,
    "running": 2,
    "late": 7,
    "from": 21,
    "where": 5,
    "a": 98,
    "suit": 2,
    "didn't": 7,
    "ask": 2,
    "for": 35,
    "would": 11,
    "have": 28,
    "been": 18,
    "okay": 41,
    "with": 20,
    "and": 88,
    "i'm": 37,
    "exact": 2,
    "my": 48,
    "phone": 3,
    "can": 18,
    "silent": 2,
    "at": 28,
    "possible": 3,
    "i'll": 15,
    "still": 17,
    "wake": 3,
    "up": 20,
    "that's": 21,
    "crazy": 9,
    "......": 5,
    "are": 22,
    "wow": 11,
    "....": 6,
    "thought": 5,
    "said": 9,
    "slippers": 4,
    "no": 18,
    "used": 3,
    "to": 128,
    "waking": 2,
    "early": 2,
    "pants": 3,
    "?": 26,
    "how": 27,
    "about": 20,
    "maybe": 10,
    "mean": 4,
    "live": 4,
    "but": 51,
    "you're": 13,
    "one": 21,
    "don't": 8,
    "mind": 7,
    "oh": 15,
    "were": 18,
    "those": 3,
    "must": 2,
    "nice": 14,
    "limits": 2,
    "since": 17,
    "when": 16,
    "did": 11,
    "her": 4,
    "was": 51,
    "or": 18,
    "we": 12,
    "decided": 4,
    "in": 50,
    "wah": 4,
    "agree": 2,
    "disagree": 2,
    "your": 18,
    "mine": 5,
    "simple": 2,
    "why": 17,
    "cause": 2,
    "all": 20,
    "that": 64,
    "ama": 8,
    "fir": 2,
    "...": 20,
    "convenience": 3,
    "super": 2,
    "of": 74,
    "more": 10,
    "like": 24,
    "princess": 5,
    "so": 27,
    "course": 6,
    "there": 12,
    "problem": 3,
    "being": 8,
    "not": 45,
    "repunzel": 2,
    "cinderella": 2,
    "least": 3,
    "they": 17,
    "had": 16,
    "good": 32,
    "foundation": 2,
    ".": 114,
    "want": 6,
    "knight": 2,
    "shining": 3,
    "armor": 4,
    "damsel": 2,
    "distress": 4,
    "without": 4,
    "will": 22,
    "shoes": 2,
    "wouldn't": 5,
    "wish": 2,
    "anyone": 3,
    "enough": 5,
    "as": 23,
    "it": 95,
    "long": 9,
    "main": 2,
    "over": 4,
    "then": 14,
    "even": 7,
    "new": 6,
    "what": 22,
    "it's": 37,
    "cut": 3,
    "hair": 4,
    "couldn't": 3,
    "y": 3,
    "afterwards": 2,
    "jelous": 2,
    "do": 14,
    "taking": 3,
    "care": 4,
    "lot": 2,
    "work": 7,
    "world": 3,
    "made": 2,
    "people": 9,
    "validation": 2,
    "yours": 3,
    "should": 9,
    "seek": 2,
    "yeah": 12,
    "year": 3,
    "kind": 2,
    "different": 2,
    "lazy": 3,
    "right": 6,
    "now": 14,
    "im": 4,
    "too": 10,
    "any": 4,
    "out": 13,
    "salut": 2,
    "!": 2,
    "see": 10,
    "je": 5,
    "we're": 3,
    "each": 3,
    "other": 3,
    "go": 6,
    "going": 2,
    "btw": 2,
    "campus": 2,
    "meant": 2,
    "night": 5,
    "yes": 2,
    "mmhm": 2,
    "communication": 2,
    "bon": 8,
    "chance": 2,
    "merci": 2,
    "better": 9,
    "his": 8,
    "before": 8,
    "here": 5,
    "wanna": 4,
    "yourself": 2,
    "de": 3,
    "sure": 7,
    "if": 12,
    "there's": 3,
    "some": 7,
    "something": 12,
    "me": 43,
    "run": 2,
    "off": 4,
    "oooh": 6,
    "bytha": 4,
    "check": 2,
    "am": 12,
    "supposed": 3,
    "mirror": 13,
    "way": 4,
    "years": 2,
    "never": 13,
    "known": 2,
    "its": 12,
    "know": 14,
    "mother": 3,
    "knew": 7,
    "princesses": 3,
    "than": 6,
    "i've": 10,
    "fine": 9,
    "happy": 3,
    "embarrassed": 2,
    "say": 9,
    "nothing": 6,
    ".....": 8,
    "gentleman": 2,
    "else": 2,
    "ok": 7,
    "won't": 2,
    "close": 2,
    "call": 6,
    "hola": 2,
    "dora": 2,
    "en": 2,
    "comment": 2,
    "tu": 5,
    "vais": 3,
    "bien": 4,
    "et": 4,
    "toi": 4,
    "aussi": 2,
    "c'est": 8,
    "idée": 2,
    "dis": 2,
    "moi": 2,
    "un": 2,
    "superbe": 2,
    "ou": 2,
    "occupé": 2,
    "moment": 4,
    "pendant": 2,
    "les": 2,
    "week": 5,
    "avec": 2,
    "dimanche": 2,
    "house": 3,
    "haven't": 2,
    "written": 2,
    "story": 7,
    "form": 3,
    "try": 2,
    "hi": 5,
    "yet": 7,
    "time": 16,
    "write": 3,
    "thank": 4,
    "looking": 3,
    "believe": 6,
    "tell": 5,
    "poems": 2,
    "thanks": 7,
    "give": 3,
    "due": 3,
    "besides": 2,
    "happens": 3,
    "memory": 2,
    "times": 2,
    "most": 2,
    "hows": 2,
    "sleep": 10,
    "stay": 5,
    "class": 4,
    "na": 3,
    "either": 4,
    "two": 2,
    "cool": 5,
    "eventually": 2,
    "both": 2,
    "actually": 6,
    "eish": 3,
    "sawa": 2,
    "came": 4,
    "fall": 3,
    "another": 3,
    "simply": 3,
    "always": 4,
    "part": 4,
    "ever": 4,
    "day": 10,
    "wanted": 5,
    "change": 3,
    "accept": 5,
    "only": 13,
    "able": 2,
    "myself": 4,
    "everyone": 2,
    "after": 6,
    "these": 4,
    "same": 2,
    "away": 5,
    "took": 2,
    "trap": 2,
    "salvation": 2,
    "hope": 5,
    "freedom": 2,
    "under": 2,
    "edge": 2,
    "wall": 6,
    "their": 2,
    "shadow": 7,
    "light": 3,
    "safe": 2,
    "accustomed": 2,
    "darkness": 5,
    "shadows": 4,
    "refused": 2,
    "though": 8,
    "own": 3,
    "far": 6,
    "act": 2,
    "against": 2,
    "fate": 2,
    "void": 2,
    "chill": 2,
    "end": 3,
    "could": 5,
    "into": 5,
    "held": 2,
    "little": 2,
    "influence": 2,
    "asked": 4,
    "last": 2,
    "wrote": 3,
    "down": 4,
    "amazing": 4,
    "firm": 2,
    "found": 2,
    "fell": 2,
    "asleep": 2,
    "brain": 2,
    "life": 7,
    "trying": 2,
    "went": 6,
    "tried": 3,
    "alive": 2,
    "thoughts": 2,
    "future": 3,
    "barely": 2,
    "today": 4,
    "commit": 2,
    "once": 4,
    "again": 5,
    "pray": 2,
    "breath": 3,
    "anymore": 2,
    "them": 9,
    "song": 8,
    "please": 2,
    "ooh": 2,
    "interesting": 2,
    "thing": 2,
    "intro": 2,
    "poem": 3,
    "great": 3,
    "ringtone": 2,
    "really": 9,
    "morning": 14,
    "itself": 2,
    "got": 4,
    "bored": 2,
    "between": 4,
    "seconds": 3,
    "tuesday": 2,
    "because": 10,
    "already": 3,
    "accidentally": 3,
    "forward": 2,
    "backward": 2,
    "sideways": 2,
    "s": 3,
    "everything": 4,
    "small": 2,
    "didn": 3,
    "t": 7,
    "quietly": 2,
    "stepped": 2,
    "lemanuel": 6,
    "woke": 3,
    "find": 3,
    "school": 3,
    "teacher": 2,
    "finished": 2,
    "asking": 2,
    "anything": 3,
    "birds": 2,
    "reverse": 4,
    "preferred": 3,
    "yesterday": 3,
    "told": 2,
    "heard": 5,
    "somewhere": 3,
    "also": 7,
    "somehow": 2,
    "him": 3,
    "hummed": 2,
    "almost": 4,
    "laugh": 3,
    "name": 2,
    "called": 4,
    "by": 11,
    "which": 7,
    "arrived": 2,
    "through": 2,
    "while": 4,
    "lunch": 2,
    "break": 2,
    "slightly": 2,
    "someone": 5,
    "tree": 2,
    "half": 2,
    "beneath": 2,
    "chaos": 2,
    "mistakes": 4,
    "voice": 2,
    "happen": 2,
    "curious": 2,
    "every": 2,
    "well": 12,
    "get": 7,
    "choose": 2,
    "started": 2,
    "understand": 2,
    "back": 7,
    "things": 3,
    "normal": 5,
    "listen": 7,
    "second": 3,
    "next": 4,
    "hear": 6,
    "playing": 2,
    "first": 8,
    "forget": 2,
    "anime": 3,
    "opinion": 3,
    "sound": 3,
    "dreams": 4,
    "watched": 2,
    "hard": 4,
    "paying": 2,
    "failure": 4,
    "reject": 3,
    "statistics": 2,
    "successful": 4,
    "speak": 2,
    "working": 2,
    "toiling": 2,
    "strong": 2,
    "ll": 2,
    "sacrifice": 2,
    "attitude": 2,
    "take": 3,
    "luck": 4,
    "matters": 2,
    "heart": 2,
    "become": 3,
    "lie": 4,
    "truth": 3,
    "won": 2,
    "make": 7,
    "silence": 2,
    "whispers": 2,
    "fight": 3,
    "sits": 2,
    "throne": 2,
    "says": 3,
    "stand": 2,
    "seriously": 2,
    "watch": 2,
    "such": 3,
    "until": 2,
    "i'd": 2,
    "hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii": 2,
    "kama": 2,
    "nah": 3,
    "whats": 2,
    "computer": 4,
    "pm": 3,
    "hey": 7,
    "sister": 2,
    "our": 2,
    "talk": 4,
    "fun": 3,
    "enjoyed": 3,
    "rise": 2,
    "shine": 2,
    "sorry": 12,
    "talking": 2,
    "songs": 2,
    "around": 3,
    "high": 2,
    "what's": 2,
    "done": 6,
    "having": 2,
    "much": 7,
    "gooood": 2,
    "afternoon": 3,
    "brethren": 4,
    "fare": 2,
    "very": 5,
    "guests": 3,
    "hiiiiiiiiiiiiiii": 2,
    "fairing": 3,
    "aaahhh": 2,
    "fairest": 2,
    "deleted": 2,
    "message": 2,
    "words": 2,
    "curse": 2,
    "gone": 2,
    "music": 6,
    "tired": 3,
    "anyway": 2,
    "help": 5,
    "finish": 2,
    "general": 2,
    "tomorrow": 3,
    "packages": 2,
    "need": 3,
    "fair": 2,
    "best": 3,
    "hiiiiii": 3,
    "share": 2,
    "full": 2,
    "nuit": 3,
    "nooooooooooooh": 3,
    "bed": 3,
    "guess": 5,
    "evening": 3,
    "maiden": 2,
    "missed": 3,
    "mass": 2,
    "health": 3,
    "food": 2,
    "kid": 2,
    "rooftop": 2,
    "philosophy": 3,
    "sessions": 2,
    "midnight": 2,
    "waited": 2,
    "forgiven": 2,
    "many": 4,
    "starry": 3,
    "session": 4,
    "matin": 3,
    "dreamt": 2,
    "à": 2,
    "broke": 3,
    "discuss": 2,
    "ideas": 3,
    "sleepy": 5,
    "head": 3,
    "awake": 2,
    "church": 2,
    "home": 2,
    "bonjour": 2,
    "reading": 2,
    "novel": 2,
    "soon": 2,
    "wait": 2,
    "interest": 3,
    "famous": 2,
    "think": 3,
    "yaaaaaaaaaayyyyyyy": 2,
    "relatively": 2,
    "strenuous": 2,
    "bit": 3,
    "elsieeeeeeeeeeeeeeeeee": 2,
    "m'y": 2,
    "hiiiiiiiiiiiiiiiiiiiiiii": 2,
    "complain": 2,
    "seem": 2,
    "usually": 3,
    "seems": 2,
    "movie": 2,
    "series": 2,
    "artists": 2,
    "walker": 2,
    "ed": 2,
    "sheeran": 2,
    "imagine": 2,
    "dragons": 2,
    "john": 2,
    "howell": 2,
    "us": 2,
    "saying": 3,
    "return": 2,
    "inner": 2,
    "greetings": 2,
    "comme": 2
}

_NGRAM_STARTERS = {
    "how's": 7,
    "hello": 6,
    "who": 4,
    "this": 3,
    "can't": 2,
    "i": 49,
    "i'm": 18,
    "my": 8,
    "that's": 13,
    "wow": 9,
    "no": 7,
    "but": 14,
    "oh": 13,
    "okay": 13,
    "since": 5,
    "wah": 4,
    "mine": 2,
    "it": 11,
    "what": 9,
    "it's": 15,
    "are": 3,
    "why": 4,
    "the": 12,
    "you": 13,
    "yeah": 10,
    "we": 2,
    "im": 2,
    "still": 2,
    "can": 6,
    "salut": 2,
    "i'll": 4,
    "for": 2,
    "yes": 2,
    "mmhm": 2,
    "merci": 2,
    "just": 2,
    "oooh": 6,
    "so": 4,
    "am": 2,
    "you're": 3,
    "not": 7,
    "how": 19,
    "they": 2,
    "i've": 6,
    "nothing": 2,
    "that": 6,
    "hola": 2,
    "je": 3,
    "et": 3,
    "c'est": 3,
    "its": 6,
    "hi": 5,
    "thank": 2,
    "thanks": 6,
    "hows": 2,
    "eish": 3,
    "is": 2,
    "of": 2,
    "ooh": 2,
    "really": 3,
    "good": 17,
    "actually": 2,
    "also": 4,
    "well": 3,
    "hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii": 2,
    "which": 4,
    "whats": 2,
    "and": 4,
    "hey": 7,
    "rise": 2,
    "sorry": 6,
    "what's": 2,
    "much": 2,
    "gooood": 2,
    "nah": 2,
    "hiiiiiiiiiiiiiii": 2,
    "aaahhh": 2,
    "mirror": 5,
    "from": 2,
    "general": 2,
    "hiiiiii": 3,
    "did": 3,
    "something": 2,
    "bon": 6,
    "nooooooooooooh": 3,
    "a": 2,
    "bonjour": 2,
    "yaaaaaaaaaayyyyyyy": 2,
    "elsieeeeeeeeeeeeeeeeee": 2,
    "hiiiiiiiiiiiiiiiiiiiiiii": 2
}

_NGRAM_BIGRAMS = {
    "how's": {
        "you": 4
    },
    "you": {
        "doing": 2,
        "would": 2,
        "don't": 3,
        "<end>": 22,
        "know": 3,
        "do": 2,
        "sure": 2,
        "have": 3,
        "were": 5,
        "should": 3,
        "had": 2,
        "get": 2,
        "listen": 3,
        "far": 2,
        "are": 2,
        "can": 3,
        "as": 3,
        "deleted": 2,
        "say": 2,
        "too": 2,
        "not": 2,
        "been": 2,
        "laugh": 2
    },
    "doing": {
        "<end>": 3
    },
    "hello": {
        "<end>": 4
    },
    "sleeping": {
        "beauty": 4
    },
    "beauty": {
        "is": 2
    },
    "has": {
        "to": 2
    },
    "who": {
        "said": 2
    },
    "the": {
        "st": 2,
        "pants": 2,
        "one": 3,
        "damsel": 2,
        "main": 2,
        "world": 3,
        "year": 2,
        "time": 2,
        "wall": 6,
        "light": 2,
        "darkness": 3,
        "void": 2,
        "chill": 2,
        "shadows": 2,
        "last": 2,
        "intro": 2,
        "chaos": 2,
        "first": 6,
        "statistics": 2,
        "future": 2,
        "lie": 4,
        "throne": 2,
        "truth": 2,
        "second": 2,
        "fairest": 2,
        "moment": 2,
        "best": 2,
        "only": 2,
        "interest": 2,
        "story": 2
    },
    "true": {
        "love": 2,
        "<end>": 2
    },
    "love": {
        "it": 2
    },
    "this": {
        "is": 6,
        "<end>": 2,
        "fine": 2,
        "message": 2
    },
    "is": {
        "the": 3,
        "a": 3,
        "<end>": 3,
        "over": 2,
        "to": 2,
        "that": 2,
        "all": 3
    },
    "st": {
        "century": 2
    },
    "i": {
        "just": 3,
        "didn't": 4,
        "would": 4,
        "thought": 3,
        "mean": 3,
        "have": 7,
        "wouldn't": 2,
        "be": 2,
        "see": 3,
        "wanna": 3,
        "supposed": 2,
        "know": 5,
        "<end>": 2,
        "should": 2,
        "am": 7,
        "won't": 2,
        "haven't": 2,
        "knew": 4,
        "never": 2,
        "wrote": 2,
        "fell": 2,
        "commit": 2,
        "love": 2,
        "like": 2,
        "tried": 2,
        "will": 13,
        "reject": 3,
        "accept": 2,
        "silence": 2,
        "can't": 5,
        "really": 2,
        "was": 12,
        "did": 2,
        "can": 3,
        "still": 2,
        "waited": 2,
        "dreamt": 2,
        "help": 2,
        "think": 3,
        "guess": 2,
        "could": 2
    },
    "on": {
        "my": 2,
        "the": 11,
        "you": 2,
        "<end>": 2
    },
    "prince": {
        "charming": 3
    },
    "he": {
        "might": 2,
        "said": 2,
        "sits": 2
    },
    "be": {
        "able": 2,
        "more": 2,
        "a": 3,
        "successful": 2,
        "done": 4
    },
    "running": {
        "late": 2
    },
    "late": {
        "<end>": 2
    },
    "from": {
        "the": 5,
        "one": 2
    },
    "a": {
        "suit": 2,
        "good": 5,
        "lot": 2,
        "mirror": 2,
        "gentleman": 2,
        "part": 2,
        "little": 2,
        "song": 2,
        "while": 2,
        "failure": 4,
        "kid": 2,
        "starry": 2,
        "bit": 3
    },
    "didn't": {
        "get": 2
    },
    "for": {
        "a": 5,
        "me": 4,
        "the": 5,
        "you": 4
    },
    "would": {
        "have": 3,
        "i": 2
    },
    "have": {
        "been": 3,
        "i": 2,
        "a": 3,
        "you": 3
    },
    "been": {
        "okay": 2,
        "<end>": 3
    },
    "okay": {
        "with": 2,
        "that's": 2,
        "<end>": 18,
        "if": 2,
        "so": 3
    },
    "with": {
        "me": 3,
        "a": 4,
        "that": 2
    },
    "and": {
        "a": 2,
        "i'll": 4,
        "it's": 3,
        "accidentally": 2,
        "toiling": 2,
        "attitude": 2,
        "i": 3,
        "shine": 2,
        "woke": 2,
        "you": 2,
        "it": 2
    },
    "i'm": {
        "the": 2,
        "just": 2,
        "too": 2,
        "not": 3,
        "doing": 2,
        "sorry": 5,
        "okay": 3
    },
    "my": {
        "phone": 3,
        "brain": 2,
        "heart": 2,
        "sister": 2,
        "brethren": 2,
        "mother": 2,
        "day": 3
    },
    "can": {
        "you": 4,
        "i": 5
    },
    "at": {
        "least": 3,
        "the": 8,
        "midnight": 2,
        "all": 2,
        "<end>": 2
    },
    "i'll": {
        "be": 5
    },
    "wake": {
        "up": 3
    },
    "up": {
        "<end>": 4,
        "to": 3,
        "and": 2,
        "for": 2
    },
    "that's": {
        "crazy": 2,
        "a": 2,
        "the": 3,
        "why": 3,
        "nice": 8
    },
    "crazy": {
        "<end>": 5
    },
    "are": {
        "you": 10,
        "a": 2
    },
    "wow": {
        "you": 2
    },
    "thought": {
        "you": 3
    },
    "no": {
        "i": 2,
        "they": 2,
        "it": 2,
        "no": 3
    },
    "used": {
        "to": 2
    },
    "to": {
        "live": 2,
        "the": 6,
        "be": 10,
        "disagree": 2,
        "do": 4,
        "stay": 3,
        "believe": 2,
        "change": 2,
        "accept": 2,
        "see": 3,
        "find": 2,
        "this": 6,
        "speak": 2,
        "sleep": 3,
        "go": 3,
        "hear": 2,
        "you": 6,
        "my": 2
    },
    "waking": {
        "up": 2
    },
    "?": {
        "<end>": 11,
        "the": 2
    },
    "how": {
        "about": 2,
        "it": 2,
        "has": 2,
        "can": 3,
        "was": 4,
        "are": 2,
        "did": 2,
        "have": 2
    },
    "about": {
        "princesses": 3,
        "that": 2,
        "me": 3,
        "<end>": 2,
        "the": 2
    },
    "maybe": {
        "not": 2,
        "<end>": 2
    },
    "but": {
        "you're": 2,
        "at": 2,
        "i'm": 2,
        "it's": 5,
        "it": 3,
        "from": 2,
        "this": 2,
        "i": 2,
        "of": 2,
        "not": 2,
        "i'll": 2
    },
    "you're": {
        "ok": 2
    },
    "one": {
        "who": 2,
        "to": 2,
        "of": 3
    },
    "mind": {
        "<end>": 2
    },
    "oh": {
        "okay": 7,
        "and": 2
    },
    "were": {
        "the": 2
    },
    "nice": {
        "<end>": 5,
        "to": 3
    },
    "limits": {
        "<end>": 2
    },
    "since": {
        "when": 3,
        "you": 2,
        "i": 3
    },
    "when": {
        "i": 4,
        "my": 2
    },
    "did": {
        "you": 3
    },
    "was": {
        "a": 4,
        "still": 2,
        "fun": 2,
        "at": 2,
        "your": 2,
        "awake": 2
    },
    "or": {
        "something": 2,
        "what": 2,
        "i": 2,
        "a": 2
    },
    "we": {
        "are": 2
    },
    "decided": {
        "to": 2,
        "it": 2
    },
    "in": {
        "the": 12,
        "shining": 2,
        "a": 4,
        "this": 3,
        "life": 3,
        "my": 2,
        "some": 2
    },
    "agree": {
        "to": 2
    },
    "disagree": {
        "<end>": 2
    },
    "your": {
        "day": 3
    },
    "mine": {
        "is": 2
    },
    "why": {
        "not": 2,
        "i": 3,
        "<end>": 2,
        "are": 2
    },
    "all": {
        "that": 3,
        "<end>": 4
    },
    "that": {
        "for": 2,
        "<end>": 6,
        "was": 5,
        "i": 3,
        "day": 2,
        "is": 2,
        "say": 2,
        "matters": 2,
        "whispers": 2,
        "says": 3
    },
    "ama": {
        "<end>": 3
    },
    "...": {
        "<end>": 2,
        "it": 2
    },
    "of": {
        "course": 6,
        "being": 3,
        "it": 2,
        "the": 14,
        "his": 2,
        "its": 2,
        "me": 3,
        "my": 5,
        "them": 3
    },
    "more": {
        "like": 2,
        "about": 2
    },
    "like": {
        "it": 3,
        "a": 5,
        "that": 2,
        "you": 2
    },
    "princess": {
        "y": 2
    },
    "so": {
        "<end>": 5,
        "you're": 2,
        "i": 4
    },
    "course": {
        "<end>": 5
    },
    "there": {
        "are": 3
    },
    "not": {
        "<end>": 5,
        "sure": 2,
        "to": 2,
        "yet": 2,
        "the": 2,
        "from": 2,
        "really": 2,
        "at": 2
    },
    "they": {
        "had": 2,
        "were": 3
    },
    "had": {
        "a": 2,
        "to": 2
    },
    "good": {
        "foundation": 2,
        "morning": 11,
        "<end>": 2,
        "night": 3,
        "luck": 2,
        "for": 2
    },
    ".": {
        "i": 18,
        "but": 3,
        "the": 5,
        "they": 2,
        "hope": 2,
        "a": 5,
        "it": 4,
        "not": 8,
        "<end>": 3,
        "and": 7,
        "lemanuel": 3,
        "because": 2,
        "time": 3
    },
    "want": {
        "to": 3
    },
    "shining": {
        "armor": 2
    },
    "will": {
        "be": 5,
        "take": 2,
        "become": 2,
        "never": 4
    },
    "wouldn't": {
        "want": 2
    },
    "as": {
        "long": 3,
        "he": 2,
        "well": 2
    },
    "it": {
        "is": 6,
        "was": 10,
        "to": 2,
        "<end>": 15,
        "out": 2,
        "had": 3,
        "wanted": 3,
        "?": 2,
        "i": 2,
        ".": 5,
        "because": 2,
        "for": 2
    },
    "long": {
        "as": 3,
        "<end>": 2
    },
    "over": {
        "here": 2
    },
    "then": {
        "why": 2,
        "<end>": 5
    },
    "what": {
        "if": 2,
        "is": 2,
        "i": 2,
        "<end>": 2
    },
    "it's": {
        "a": 4,
        "not": 3,
        "fine": 2,
        "okay": 8,
        "cool": 2,
        "ok": 2
    },
    "hair": {
        "is": 2
    },
    "afterwards": {
        "<end>": 2
    },
    "jelous": {
        "<end>": 2
    },
    "do": {
        "that": 3,
        "<end>": 2,
        "you": 2
    },
    "taking": {
        "care": 3
    },
    "care": {
        "of": 3
    },
    "lot": {
        "of": 2
    },
    "work": {
        "<end>": 3
    },
    "yours": {
        "<end>": 3
    },
    "should": {
        "be": 3
    },
    "yeah": {
        "<end>": 3
    },
    "kind": {
        "of": 2
    },
    "lazy": {
        "to": 2
    },
    "right": {
        "now": 4
    },
    "now": {
        "<end>": 4,
        "?": 2
    },
    "too": {
        "lazy": 2,
        "<end>": 5
    },
    "out": {
        "for": 2,
        "of": 3,
        "<end>": 2
    },
    "je": {
        "vais": 3
    },
    "bon": {
        "nuit": 3,
        "matin": 3
    },
    "better": {
        "now": 2,
        "<end>": 3
    },
    "his": {
        "shadow": 4
    },
    "before": {
        "i": 2
    },
    "here": {
        "<end>": 3
    },
    "sure": {
        "if": 2
    },
    "if": {
        "you": 4
    },
    "something": {
        "in": 2
    },
    "me": {
        "<end>": 8,
        "since": 2,
        ".": 2,
        "to": 4,
        "too": 2
    },
    "off": {
        "<end>": 2
    },
    "am": {
        "i": 3,
        "a": 4,
        "successful": 2
    },
    "supposed": {
        "to": 3
    },
    "mirror": {
        "mirror": 5,
        "on": 4
    },
    "never": {
        "make": 2,
        "believe": 2,
        "heard": 2
    },
    "its": {
        "own": 2,
        "amazing": 2
    },
    "know": {
        "more": 2,
        "<end>": 2
    },
    "knew": {
        "you": 2
    },
    "princesses": {
        "than": 2
    },
    "than": {
        "the": 2
    },
    "i've": {
        "never": 2,
        "been": 4
    },
    "fine": {
        "<end>": 4
    },
    "say": {
        "i": 4,
        "so": 3
    },
    "nothing": {
        "to": 2
    },
    "ok": {
        "<end>": 3
    },
    "dora": {
        "<end>": 2
    },
    "tu": {
        "<end>": 2
    },
    "vais": {
        "bien": 2
    },
    "bien": {
        "<end>": 3
    },
    "toi": {
        "<end>": 4
    },
    "moi": {
        "<end>": 2
    },
    "moment": {
        "<end>": 3
    },
    "pendant": {
        "les": 2
    },
    "week": {
        "<end>": 3
    },
    "hi": {
        "<end>": 5
    },
    "time": {
        "<end>": 3
    },
    "thank": {
        "you": 4
    },
    "believe": {
        "the": 4
    },
    "tell": {
        "you": 2,
        "me": 3
    },
    "thanks": {
        "<end>": 6
    },
    "due": {
        "to": 2
    },
    "times": {
        "<end>": 2
    },
    "sleep": {
        "<end>": 4
    },
    "stay": {
        "up": 2
    },
    "cool": {
        "<end>": 3
    },
    "eish": {
        "sawa": 2
    },
    "came": {
        "to": 2
    },
    "part": {
        "of": 2
    },
    "day": {
        "<end>": 2
    },
    "wanted": {
        "to": 4
    },
    "change": {
        "me": 2
    },
    "accept": {
        "the": 2
    },
    "only": {
        "to": 2
    },
    "able": {
        "to": 2
    },
    "after": {
        "working": 2
    },
    "edge": {
        "of": 2
    },
    "wall": {
        ".": 2
    },
    "accustomed": {
        "to": 2
    },
    "darkness": {
        "of": 2
    },
    "though": {
        "it": 2,
        "<end>": 3
    },
    "far": {
        ".": 2
    },
    "act": {
        "of": 2
    },
    "into": {
        "the": 2
    },
    "asked": {
        ".": 2
    },
    "down": {
        "<end>": 2
    },
    "fell": {
        "asleep": 2
    },
    "life": {
        ".": 2
    },
    "trying": {
        "to": 2
    },
    "went": {
        "back": 2
    },
    "tried": {
        "to": 2
    },
    "future": {
        ".": 2
    },
    "today": {
        "<end>": 2
    },
    "again": {
        "he": 2
    },
    "them": {
        "all": 2
    },
    "song": {
        "<end>": 3,
        "...": 2
    },
    "please": {
        "<end>": 2
    },
    "great": {
        "<end>": 2
    },
    "really": {
        "<end>": 3,
        "enjoyed": 3
    },
    "morning": {
        "<end>": 10
    },
    "bored": {
        ".": 2
    },
    "because": {
        "it": 4
    },
    "didn": {
        "t": 3
    },
    "t": {
        "make": 2
    },
    "woke": {
        "up": 3
    },
    "preferred": {
        "artists": 2
    },
    "heard": {
        "the": 2
    },
    "also": {
        "this": 2,
        "i'm": 2
    },
    "by": {
        ".": 2
    },
    "which": {
        "one": 2
    },
    "beneath": {
        "the": 2
    },
    "well": {
        "<end>": 4
    },
    "get": {
        "to": 2,
        "out": 2
    },
    "back": {
        "to": 4
    },
    "things": {
        "<end>": 2
    },
    "listen": {
        "to": 6
    },
    "second": {
        "one": 2
    },
    "next": {
        "week": 2
    },
    "hear": {
        "the": 2,
        "<end>": 2
    },
    "first": {
        "one": 2
    },
    "sound": {
        "mind": 2
    },
    "dreams": {
        "<end>": 3
    },
    "hard": {
        "and": 2
    },
    "failure": {
        "i": 2
    },
    "reject": {
        "the": 3
    },
    "statistics": {
        "that": 2
    },
    "successful": {
        ".": 4
    },
    "working": {
        "hard": 2
    },
    "toiling": {
        "strong": 2
    },
    "strong": {
        "i": 2
    },
    "sacrifice": {
        "and": 2
    },
    "attitude": {
        "will": 2
    },
    "take": {
        "you": 2
    },
    "luck": {
        "is": 2
    },
    "matters": {
        "in": 2
    },
    "become": {
        "something": 2
    },
    "lie": {
        "that": 3
    },
    "won": {
        "t": 2
    },
    "make": {
        "it": 6
    },
    "silence": {
        "the": 2
    },
    "fight": {
        "on": 2
    },
    "sits": {
        "on": 2
    },
    "throne": {
        "i": 2
    },
    "says": {
        "i": 2
    },
    "hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii": {
        "<end>": 2
    },
    "pm": {
        "<end>": 2
    },
    "hey": {
        "<end>": 5
    },
    "sister": {
        "<end>": 2
    },
    "rise": {
        "and": 2
    },
    "sorry": {
        "<end>": 8
    },
    "what's": {
        "up": 2
    },
    "done": {
        "by": 2
    },
    "much": {
        "better": 3,
        "<end>": 2
    },
    "brethren": {
        "<end>": 3
    },
    "hiiiiiiiiiiiiiii": {
        "<end>": 2
    },
    "fairing": {
        "on": 2
    },
    "deleted": {
        "this": 2
    },
    "message": {
        "<end>": 2
    },
    "music": {
        "<end>": 2
    },
    "tired": {
        "<end>": 2
    },
    "help": {
        "<end>": 3
    },
    "hiiiiii": {
        "<end>": 3
    },
    "nuit": {
        "<end>": 2
    },
    "nooooooooooooh": {
        "<end>": 3
    },
    "guess": {
        "what": 2
    },
    "evening": {
        "<end>": 2
    },
    "maiden": {
        "<end>": 2
    },
    "food": {
        "and": 2
    },
    "kid": {
        "and": 2
    },
    "forgiven": {
        "<end>": 2
    },
    "starry": {
        "session": 3
    },
    "session": {
        "<end>": 2
    },
    "matin": {
        "<end>": 2
    },
    "à": {
        "toi": 2
    },
    "ideas": {
        "<end>": 2
    },
    "sleepy": {
        "head": 2
    },
    "head": {
        "<end>": 2
    },
    "awake": {
        "by": 2
    },
    "bonjour": {
        "<end>": 2
    },
    "yaaaaaaaaaayyyyyyy": {
        "<end>": 2
    },
    "strenuous": {
        "work": 2
    },
    "elsieeeeeeeeeeeeeeeeee": {
        "<end>": 2
    },
    "artists": {
        "<end>": 2
    },
    "ed": {
        "sheeran": 2
    },
    "imagine": {
        "dragons": 2
    }
}

_NGRAM_TRIGRAMS_FLAT = {
    "how's\u0001you": {
        "<end>": 3
    },
    "you\u0001doing": {
        "<end>": 2
    },
    "this\u0001is": {
        "the": 2
    },
    "the\u0001st": {
        "century": 2
    },
    "i\u0001didn't": {
        "get": 2
    },
    "i\u0001would": {
        "have": 2
    },
    "and\u0001i'll": {
        "be": 2
    },
    "are\u0001you": {
        "sure": 2
    },
    "i\u0001thought": {
        "you": 2
    },
    "up\u0001to": {
        "the": 2
    },
    "the\u0001one": {
        "who": 2
    },
    "in\u0001the": {
        "future": 2
    },
    "agree\u0001to": {
        "disagree": 2
    },
    "to\u0001disagree": {
        "<end>": 2
    },
    "all\u0001that": {
        "matters": 2
    },
    "of\u0001course": {
        "<end>": 5
    },
    "but\u0001at": {
        "least": 2
    },
    "they\u0001had": {
        "a": 2
    },
    "had\u0001a": {
        "good": 2
    },
    "a\u0001good": {
        "foundation": 2
    },
    "in\u0001shining": {
        "armor": 2
    },
    ".\u0001i": {
        "will": 2,
        "accept": 2,
        "silence": 2
    },
    "it\u0001is": {
        "<end>": 3
    },
    "as\u0001long": {
        "as": 3
    },
    "long\u0001as": {
        "he": 2
    },
    "like\u0001it": {
        "<end>": 3
    },
    "would\u0001i": {
        "be": 2
    },
    "taking\u0001care": {
        "of": 3
    },
    "a\u0001lot": {
        "of": 2
    },
    "that's\u0001why": {
        "i": 2
    },
    "of\u0001it": {
        "<end>": 2
    },
    "at\u0001the": {
        "moment": 2
    },
    "i'm\u0001too": {
        "lazy": 2
    },
    "too\u0001lazy": {
        "to": 2
    },
    "can\u0001you": {
        "listen": 2
    },
    "do\u0001that": {
        "<end>": 2
    },
    "to\u0001do": {
        "that": 2
    },
    "maybe\u0001not": {
        "<end>": 2
    },
    "oh\u0001okay": {
        "<end>": 3
    },
    "i\u0001supposed": {
        "to": 2
    },
    "with\u0001me": {
        "<end>": 2
    },
    "know\u0001more": {
        "about": 2
    },
    "more\u0001about": {
        "princesses": 2
    },
    "about\u0001princesses": {
        "than": 2
    },
    "i\u0001should": {
        "be": 2
    },
    "say\u0001i": {
        "will": 3
    },
    "i\u0001am": {
        "a": 4,
        "successful": 2
    },
    "was\u0001a": {
        "kid": 2
    },
    "je\u0001vais": {
        "bien": 2
    },
    "can\u0001i": {
        "help": 2
    },
    "i'm\u0001not": {
        "sure": 2
    },
    "not\u0001sure": {
        "if": 2
    },
    "it's\u0001okay": {
        "<end>": 5
    },
    "thank\u0001you": {
        "<end>": 2
    },
    "say\u0001so": {
        "<end>": 3
    },
    "the\u0001time": {
        "<end>": 2
    },
    "to\u0001stay": {
        "up": 2
    },
    "a\u0001part": {
        "of": 2
    },
    "part\u0001of": {
        "me": 2
    },
    "of\u0001me": {
        "<end>": 2
    },
    "i\u0001knew": {
        "you": 2
    },
    "to\u0001change": {
        "me": 2
    },
    "be\u0001able": {
        "to": 2
    },
    "is\u0001all": {
        "that": 2
    },
    "on\u0001the": {
        "throne": 2,
        "wall": 5
    },
    "the\u0001wall": {
        ".": 2
    },
    ".\u0001it": {
        "was": 3
    },
    "about\u0001me": {
        "<end>": 2
    },
    "i\u0001fell": {
        "asleep": 2
    },
    "will\u0001be": {
        "a": 2,
        "successful": 2
    },
    "one\u0001of": {
        "my": 3
    },
    "good\u0001morning": {
        "<end>": 9
    },
    "because\u0001it": {
        "had": 2
    },
    "it\u0001wanted": {
        "to": 3
    },
    "wanted\u0001to": {
        "be": 2
    },
    "be\u0001a": {
        "failure": 2
    },
    "not\u0001from": {
        "the": 2
    },
    "if\u0001you": {
        "say": 2
    },
    "went\u0001back": {
        "to": 2
    },
    "back\u0001to": {
        "sleep": 2
    },
    "you\u0001listen": {
        "to": 2
    },
    "the\u0001first": {
        "one": 2
    },
    "that's\u0001nice": {
        "<end>": 4,
        "to": 2
    },
    "listen\u0001to": {
        "this": 4
    },
    "i\u0001love": {
        "it": 2
    },
    "love\u0001it": {
        "<end>": 2
    },
    "over\u0001here": {
        "<end>": 2
    },
    "i\u0001will": {
        "be": 4,
        "become": 2,
        "never": 4
    },
    "a\u0001failure": {
        "i": 2
    },
    "i\u0001reject": {
        "the": 3
    },
    "reject\u0001the": {
        "statistics": 2
    },
    "the\u0001statistics": {
        "that": 2
    },
    "statistics\u0001that": {
        "say": 2
    },
    "that\u0001say": {
        "i": 2
    },
    "be\u0001successful": {
        ".": 2
    },
    "successful\u0001.": {
        "i": 2
    },
    "after\u0001working": {
        "hard": 2
    },
    "working\u0001hard": {
        "and": 2
    },
    "hard\u0001and": {
        "toiling": 2
    },
    "and\u0001toiling": {
        "strong": 2
    },
    "toiling\u0001strong": {
        "i": 2
    },
    "believe\u0001the": {
        "lie": 2
    },
    "sacrifice\u0001and": {
        "attitude": 2
    },
    "and\u0001attitude": {
        "will": 2
    },
    "attitude\u0001will": {
        "take": 2
    },
    "will\u0001take": {
        "you": 2
    },
    "take\u0001you": {
        "far": 2
    },
    "you\u0001far": {
        ".": 2
    },
    "luck\u0001is": {
        "all": 2
    },
    "that\u0001matters": {
        "in": 2
    },
    "matters\u0001in": {
        "life": 2
    },
    "in\u0001life": {
        ".": 2
    },
    "life\u0001.": {
        "i": 2
    },
    "will\u0001become": {
        "something": 2
    },
    "become\u0001something": {
        "in": 2
    },
    "something\u0001in": {
        "the": 2
    },
    "the\u0001future": {
        ".": 2
    },
    "future\u0001.": {
        "i": 2
    },
    "i\u0001accept": {
        "the": 2
    },
    "the\u0001lie": {
        "that": 3
    },
    "won\u0001t": {
        "make": 2
    },
    "t\u0001make": {
        "it": 2
    },
    "make\u0001it": {
        ".": 4,
        "because": 2
    },
    "it\u0001.": {
        "i": 3
    },
    "i\u0001silence": {
        "the": 2
    },
    "fight\u0001on": {
        "you": 2
    },
    "as\u0001he": {
        "sits": 2
    },
    "he\u0001sits": {
        "on": 2
    },
    "sits\u0001on": {
        "the": 2
    },
    "the\u0001throne": {
        "i": 2
    },
    "throne\u0001i": {
        "will": 2
    },
    "will\u0001never": {
        "make": 2,
        "believe": 2
    },
    "never\u0001make": {
        "it": 2
    },
    "never\u0001believe": {
        "the": 2
    },
    "lie\u0001that": {
        "says": 2
    },
    "that\u0001says": {
        "i": 2
    },
    "am\u0001successful": {
        ".": 2
    },
    "the\u0001second": {
        "one": 2
    },
    "it's\u0001ok": {
        "<end>": 2
    },
    "my\u0001sister": {
        "<end>": 2
    },
    "i\u0001really": {
        "enjoyed": 2
    },
    "rise\u0001and": {
        "shine": 2
    },
    "...\u0001it": {
        "was": 2
    },
    "and\u0001woke": {
        "up": 2
    },
    "what's\u0001up": {
        "<end>": 2
    },
    "since\u0001i": {
        "was": 2
    },
    "i\u0001was": {
        "a": 2,
        "awake": 2
    },
    "i'm\u0001sorry": {
        "<end>": 4
    },
    "much\u0001better": {
        "<end>": 3
    },
    "nice\u0001to": {
        "hear": 2
    },
    "to\u0001hear": {
        "<end>": 2
    },
    "to\u0001you": {
        "as": 2,
        "too": 2,
        "<end>": 2
    },
    "you\u0001as": {
        "well": 2
    },
    "have\u0001you": {
        "been": 2
    },
    "them\u0001all": {
        "<end>": 2
    },
    "mirror\u0001mirror": {
        "on": 4
    },
    "why\u0001are": {
        "you": 2
    },
    "you\u0001deleted": {
        "this": 2
    },
    "deleted\u0001this": {
        "message": 2
    },
    "this\u0001message": {
        "<end>": 2
    },
    "mirror\u0001on": {
        "the": 4
    },
    "okay\u0001if": {
        "you": 2
    },
    "you\u0001say": {
        "so": 2
    },
    "next\u0001week": {
        "<end>": 2
    },
    "i'll\u0001be": {
        "done": 3
    },
    "be\u0001done": {
        "by": 2
    },
    "how\u0001can": {
        "i": 3
    },
    "bon\u0001nuit": {
        "<end>": 2
    },
    "you\u0001too": {
        "<end>": 2
    },
    "how\u0001was": {
        "your": 2
    },
    "was\u0001your": {
        "day": 2
    },
    "a\u0001kid": {
        "and": 2
    },
    "for\u0001you": {
        "<end>": 4
    },
    "but\u0001of": {
        "course": 2
    },
    "a\u0001starry": {
        "session": 2
    },
    "bon\u0001matin": {
        "<end>": 2
    },
    "à\u0001toi": {
        "<end>": 2
    },
    "how\u0001are": {
        "you": 2
    },
    "the\u0001moment": {
        "<end>": 2
    },
    "sleepy\u0001head": {
        "<end>": 2
    },
    "was\u0001awake": {
        "by": 2
    },
    "good\u0001for": {
        "you": 2
    },
    "how\u0001did": {
        "you": 2
    },
    "how\u0001have": {
        "you": 2
    },
    "strenuous\u0001work": {
        "<end>": 2
    },
    "from\u0001one": {
        "of": 2
    },
    "preferred\u0001artists": {
        "<end>": 2
    },
    "not\u0001at": {
        "all": 2
    },
    "at\u0001all": {
        "<end>": 2
    },
    "no\u0001no": {
        "no": 2
    }
}

def _load_trigram_table():
    """Splits the flat "word1\\x01word2" string keys back into proper
    (word1, word2) tuple keys - done here rather than storing tuple
    keys directly, since JSON (used to train/prune this table offline)
    has no native tuple-key support."""
    table = {}
    for flat_key, continuations in _NGRAM_TRIGRAMS_FLAT.items():
        w1, w2 = flat_key.split("\x01")
        table[(w1, w2)] = continuations
    return table


class ConversationalLanguageModel:
    """
    A classic trigram-with-backoff word-prediction model (see the
    Section 14 module docstring above for the full explanation and the
    privacy note about what is/isn't embedded). This is the closest
    thing to "predict the next word" that makes sense to actually train
    and ship inside an offline, dependency-light chatbot: no GPU, no
    gigabytes of weights, just counted word-transition frequencies -
    and unlike LLMConnector (Section 6I), it needs no network, no API
    key, and no external service to be "real."
    """

    def __init__(self):
        self.unigrams = _NGRAM_UNIGRAMS
        self.starters = _NGRAM_STARTERS
        self.bigrams = _NGRAM_BIGRAMS
        self.trigrams = _load_trigram_table()
        self._unigram_total = sum(self.unigrams.values())

    @staticmethod
    def _tokenize(text: str):
        text = text.lower().strip()
        return re.findall(r"[a-zà-ÿ']+|[.!?]+", text)

    def _weighted_sample(self, distribution: dict, rng: random.Random):
        words = list(distribution.keys())
        weights = list(distribution.values())
        return rng.choices(words, weights=weights, k=1)[0]

    def predict_next_words(self, text: str, top_k: int = 5):
        """
        Returns up to top_k (word, probability) pairs predicting what
        word is most likely to come next after `text`, using trigram
        context if available, backing off to bigram, then to the
        overall unigram frequency table (guaranteeing a prediction even
        for a context never seen in training - the classic backoff
        idea, simplified from full Katz/Kneser-Ney smoothing).
        """
        tokens = self._tokenize(text)
        candidates = None
        source = None

        if len(tokens) >= 2:
            key = (tokens[-2], tokens[-1])
            if key in self.trigrams:
                candidates = self.trigrams[key]
                source = "trigram"
        if candidates is None and tokens:
            last = tokens[-1]
            if last in self.bigrams:
                candidates = self.bigrams[last]
                source = "bigram"
        if candidates is None:
            candidates = self.unigrams
            source = "unigram"

        total = sum(candidates.values())
        ranked = sorted(candidates.items(), key=lambda pair: pair[1], reverse=True)[:top_k]
        return [(word, count / total) for word, count in ranked if word != "<end>"], source

    def format_prediction(self, text: str, top_k: int = 5) -> str:
        predictions, source = self.predict_next_words(text, top_k=top_k)
        if not predictions:
            return "I don't have a strong prediction for what comes next there."
        formatted = ", ".join(f"'{w}' ({p:.0%})" for w, p in predictions)
        return f"Most likely next word(s) (via {source} backoff): {formatted}"

    def continue_text(self, seed_text: str = "", max_words: int = 12, seed: int = None) -> str:
        """
        Generates a short continuation in the trained conversational
        register, word by word, sampling from the trigram/bigram/
        unigram backoff distribution at each step (same backoff logic
        as predict_next_words, but SAMPLING rather than just reporting
        top candidates) until it samples the learned <end> token or
        hits max_words. If seed_text is empty, starts from a real
        learned SENTENCE-STARTER word instead of an arbitrary one, so
        generated text opens the way real turns in the corpus did.
        """
        rng = random.Random(seed) if seed is not None else random.Random()
        tokens = self._tokenize(seed_text) if seed_text else []

        if not tokens:
            starter = self._weighted_sample(self.starters, rng)
            tokens = [starter]

        generated = list(tokens)
        for _ in range(max_words):
            key = (generated[-2], generated[-1]) if len(generated) >= 2 else None
            candidates = self.trigrams.get(key) if key else None
            if candidates is None:
                candidates = self.bigrams.get(generated[-1])
            if candidates is None:
                candidates = self.unigrams

            next_word = self._weighted_sample(candidates, rng)
            if next_word == "<end>":
                break
            generated.append(next_word)

        return self._detokenize(generated)

    @staticmethod
    def _detokenize(tokens: list) -> str:
        """Joins tokens back into a readable string: no space before
        punctuation, capitalize the first letter (the model itself is
        trained entirely lowercase, matching the casual source
        register, but a leading capital reads more naturally as a
        finished sentence)."""
        text = ""
        for tok in tokens:
            if re.fullmatch(r"[.!?]+", tok):
                text = text.rstrip() + tok
            elif text:
                text += " " + tok
            else:
                text = tok
        return text[0].upper() + text[1:] if text else text

    def format_continuation(self, seed_text: str = "", max_words: int = 12) -> str:
        result = self.continue_text(seed_text, max_words=max_words)
        if not result:
            return "I couldn't generate a continuation from that."
        return result


# ==============================================================================
# SECTION 14B: TINY SELF-ATTENTION LANGUAGE MODEL ("transformer-like", torch)
# ==============================================================================
#
# ConversationalLanguageModel above is genuinely rule-based: fixed
# trigram/bigram/unigram frequency tables, no learned weights, no
# gradient descent - real, but simple. This section adds an actual
# small TRANSFORMER architecture on top of it, used automatically when
# torch is available ("online mode" in the sense of "a real learned
# model is running", NOT network access - nothing here calls out to
# the internet): token + positional embeddings, causally-masked
# multi-head self-attention, a feedforward block, and a linear output
# head predicting the next token - the same core recipe real
# transformer language models use (GPT included), just at toy scale
# (~300,000 parameters instead of billions, a couple of layers instead
# of dozens). Calling this "transformer-like" rather than "a
# transformer" or "an LLM" is deliberate and accurate: the
# architecture is a real, if tiny, transformer, but nothing about its
# scale, training data, or capability resembles an actual production
# language model.
#
# TRAINING DATA - an important privacy detail: this model is NOT
# trained on the pruned n-gram counts directly, and never touches the
# original chat export at all (that file was only ever used once,
# offline, to build the pruned counts baked into Section 14 - see that
# section's docstring). At startup, this model asks
# ConversationalLanguageModel to GENERATE a batch of fresh synthetic
# sentences by sampling its own trigram distribution, and trains on
# THOSE - a form of self-distillation (a smaller/different model
# learning from a first model's outputs, a well-established technique)
# that keeps this transformer's exposure to the private corpus twice
# removed from any private source text. The private corpus alone only
# has ~624 unique words, though, nowhere near enough to fill a
# 1500-word vocabulary - so this model's OTHER training source is real
# sentences pulled from this file's own already-public jokes, quotes,
# riddles, trivia questions, and stories (see
# _collect_public_corpus_sentences() below). Every one of those was
# already hand-written and shipped elsewhere in this bot; reusing them
# here means a bigger vocabulary is genuinely trained on real
# sentences, not just an unused cap most of which would sit at random,
# never-updated embeddings.
#
# OFFLINE / RULE-BASED FALLBACK: if torch isn't installed, every method
# here simply delegates straight to ConversationalLanguageModel's
# trigram backoff - genuinely rule-based, zero learned parameters,
# exactly as before Section 14B existed.

class TransformerLanguageModel:
    """
    A tiny, real self-attention transformer for next-word prediction/
    text continuation - see the Section 14B module docstring above for
    the full architecture description, the "transformer-like" naming
    rationale, and the self-distillation training-data explanation.
    """

    MAX_SEQ_LEN = 20  # up from 16, alongside the rest of this upgrade
    # EMBED_DIM/NUM_HEADS/FF_DIM tuned together (with MAX_VOCAB below).
    # Widened from (72, 4 heads, 2 layers, ff=128) to (96, 6 heads, 3
    # layers, ff=192) - deeper AND wider, landing near 700,000
    # parameters (was ~300,000). 96 is evenly divisible by NUM_HEADS=6
    # (required by multi-head attention) - see last_training_info for
    # the exact LIVE count every run.
    EMBED_DIM = 96
    NUM_HEADS = 6
    NUM_LAYERS = 3
    FF_DIM = 192
    DROPOUT = 0.1
    EPOCHS = 20
    BATCH_SIZE = 32  # was trained one sequence at a time - real
    # mini-batching added alongside this upgrade so the extra depth/
    # width/data below doesn't make training impractically slow on a
    # phone CPU: batching cuts Python-level per-step overhead by
    # roughly BATCH_SIZE and lets torch's matmul run on more data per
    # call, which matters far more than raw FLOP count for wall-clock
    # time at this scale.
    SYNTHETIC_SENTENCES = 600  # up from 400
    # Raised from 1500 to 2000. The private chat corpus alone (Section
    # 14) only has ~624 unique words, nowhere near 2000 - so reaching
    # 2000 for real (rather than just raising an unused cap) means
    # pulling in genuinely trainable vocabulary from elsewhere. See
    # _collect_public_corpus_sentences() below: this model's training
    # data is now the privacy-safe synthetic corpus PLUS real sentences
    # drawn from this file's own already-public jokes/quotes/riddles/
    # trivia/stories AND (added alongside this upgrade) a set of
    # smalltalk response banks (greetings/farewells/thanks/how-are-you),
    # which comfortably cover 2000+ unique words on their own.
    MAX_VOCAB = 2000

    SPECIAL_TOKENS = ["<pad>", "<unk>", "<bos>", "<eos>"]

    def __init__(self, ngram_model: "ConversationalLanguageModel"):
        self.ngram_model = ngram_model
        self.backend = "transformer" if TORCH_AVAILABLE else "trigram_backoff"
        self.model = None
        self.word2id = {}
        self.id2word = {}
        self.last_training_info = None
        if self.backend == "transformer":
            self._fit()

    # ---- self-distillation + public-content training data -----------------

    def _collect_public_corpus_sentences(self):
        """
        Pulls in additional REAL sentences from other already-embedded,
        already-PUBLIC content in this same file - jokes, quotes,
        riddles, trivia questions, and story text (see Sections 5/6B) -
        to broaden the vocabulary well past what the private chat
        corpus alone could ever support (~624 unique words). None of
        this is private data: it's the same hand-written jokes/quotes/
        riddles/trivia/stories already shipped elsewhere in this bot,
        reused here as additional short training sentences, so a
        larger vocabulary means genuinely MORE TRAINED words, not just
        a bigger unused cap most of which would sit at random,
        never-updated embeddings.
        """
        fun = FunExtras()
        storyteller = StoryTeller()
        sentences = []

        for setup, punchline in fun.JOKES.get("en", []):
            sentences.append(setup)
            sentences.append(punchline)

        for quote, _author in fun.QUOTES:
            sentences.append(quote)

        for riddle, answer in fun.RIDDLES:
            sentences.append(riddle)
            sentences.append(f"the answer is {answer}")

        for item in fun.TRIVIA.get("en", []):
            sentences.append(item["question"])
            for choice in item["choices"]:
                sentences.append(f"the choice is {choice}")

        for category_stories in storyteller.stories.get("en", {}).values():
            for story in category_stories:
                flattened = story["text"].replace("\n", " ").replace("{name}", "someone")
                for raw_sentence in re.split(r"(?<=[.!?])\s+", flattened):
                    raw_sentence = raw_sentence.strip()
                    # Keep only sentences short enough to fit comfortably
                    # within MAX_SEQ_LEN once tokenized, so nothing gets
                    # silently truncated mid-thought during training.
                    if raw_sentence and len(raw_sentence.split()) <= self.MAX_SEQ_LEN - 2:
                        sentences.append(raw_sentence)

        # Added alongside the depth/width upgrade: a handful of
        # smalltalk response banks (Section 8) - already-public,
        # already-shipped short conversational sentences, in the
        # bot's own casual register, which broaden vocabulary/style
        # further without adding a single new content source to
        # maintain (these dicts already exist for the bot's own
        # replies; this just reuses their English entries as more
        # training sentences for THIS model too).
        smalltalk_banks = [
            GREETING_RESPONSES, FAREWELL_RESPONSES, THANKS_RESPONSES, HOW_ARE_YOU_RESPONSES,
        ]
        for bank in smalltalk_banks:
            for raw_sentence in bank.get("en", []):
                if len(raw_sentence.split()) <= self.MAX_SEQ_LEN - 2:
                    sentences.append(raw_sentence)

        return sentences

    def _generate_synthetic_corpus(self):
        """
        Combines two sources of training sentences: (1) fresh sentences
        SAMPLED from the trigram model's own learned distribution - see
        the module docstring above for why this, rather than any stored
        text, is what represents the private corpus here - and (2) real
        sentences pulled from this file's own public content (see
        _collect_public_corpus_sentences), which is what lets the
        vocabulary genuinely reach MAX_VOCAB rather than stopping at
        the private corpus's much smaller natural ceiling.
        """
        sentences = []
        for i in range(self.SYNTHETIC_SENTENCES):
            text = self.ngram_model.continue_text(max_words=self.MAX_SEQ_LEN - 2, seed=i)
            if text and len(text.split()) >= 2:
                sentences.append(text)
        sentences.extend(self._collect_public_corpus_sentences())
        return sentences

    def _build_vocab(self, sentences):
        counts = Counter()
        for s in sentences:
            for tok in self.ngram_model._tokenize(s):
                counts[tok] += 1
        top_words = [w for w, _c in counts.most_common(self.MAX_VOCAB)]
        vocab = list(self.SPECIAL_TOKENS) + top_words
        self.word2id = {w: i for i, w in enumerate(vocab)}
        self.id2word = {i: w for w, i in self.word2id.items()}

    def _encode(self, tokens):
        unk = self.word2id["<unk>"]
        return [self.word2id.get(t, unk) for t in tokens]

    # ---- model definition ---------------------------------------------------

    def _build_model(self, vocab_size):
        """
        Defines the transformer as a LOCAL class, same reasoning as
        _SentenceEncoder in Section 6H3: this way `nn.Module` is only
        ever referenced once torch is confirmed importable, so nothing
        here breaks module import on a machine without torch.
        """
        embed_dim, num_heads = self.EMBED_DIM, self.NUM_HEADS
        num_layers, ff_dim, dropout = self.NUM_LAYERS, self.FF_DIM, self.DROPOUT
        max_len = self.MAX_SEQ_LEN

        class _TinyTransformerLM(nn.Module):
            def __init__(self):
                super().__init__()
                self.token_embedding = nn.Embedding(vocab_size, embed_dim)
                self.position_embedding = nn.Embedding(max_len, embed_dim)
                encoder_layer = nn.TransformerEncoderLayer(
                    d_model=embed_dim, nhead=num_heads, dim_feedforward=ff_dim,
                    dropout=dropout, batch_first=True,
                )
                # A causally-masked TransformerEncoder is the standard,
                # well-documented way to build a decoder-only ("GPT-style")
                # next-token model without needing the separate encoder/
                # decoder cross-attention machinery a full seq2seq
                # Transformer would need - there's no second sequence to
                # attend to here, just "predict what comes next."
                self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
                self.ln_out = nn.LayerNorm(embed_dim)
                self.lm_head = nn.Linear(embed_dim, vocab_size)

            def forward(self, input_ids):
                batch_size, seq_len = input_ids.shape
                positions = torch.arange(seq_len, device=input_ids.device).unsqueeze(0).expand(batch_size, seq_len)
                x = self.token_embedding(input_ids) + self.position_embedding(positions)
                # Standard causal mask: position i may attend to
                # positions <= i only (upper triangle, excluding the
                # diagonal, set to -inf so softmax zeroes it out) -
                # this is what makes self-attention here autoregressive
                # rather than seeing "future" tokens during training.
                causal_mask = torch.triu(
                    torch.full((seq_len, seq_len), float("-inf"), device=input_ids.device), diagonal=1
                )
                x = self.transformer(x, mask=causal_mask)
                x = self.ln_out(x)
                return self.lm_head(x)

        torch.manual_seed(42)
        return _TinyTransformerLM()

    # ---- training -------------------------------------------------------

    def _fit(self):
        sentences = self._generate_synthetic_corpus()
        if len(sentences) < 20:
            # Not enough synthetic training signal (can happen if the
            # underlying trigram model itself has very little data) -
            # fail closed to the rule-based path rather than training
            # a transformer on almost nothing.
            self.backend = "trigram_backoff"
            self.last_training_info = {"note": "too little synthetic data - fell back to trigram backoff"}
            return

        self._build_vocab(sentences)
        vocab_size = len(self.word2id)
        pad_id = self.word2id["<pad>"]

        sequences = []
        for s in sentences:
            toks = ["<bos>"] + self.ngram_model._tokenize(s) + ["<eos>"]
            ids = self._encode(toks)[: self.MAX_SEQ_LEN]
            if len(ids) >= 2:
                sequences.append(ids)

        self.model = self._build_model(vocab_size)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.003)
        rng = random.Random(42)

        final_loss = None
        for _epoch in range(self.EPOCHS):
            rng.shuffle(sequences)
            epoch_losses = []
            for batch_start in range(0, len(sequences), self.BATCH_SIZE):
                batch = sequences[batch_start:batch_start + self.BATCH_SIZE]
                # Pad every sequence in the batch to the same length so
                # they can be stacked into one tensor and processed in
                # a single forward/backward pass - real mini-batching,
                # not the one-sequence-at-a-time loop this used to be.
                batch_max_len = max(len(seq) for seq in batch) - 1  # -1: predicting input[1:] from input[:-1]
                padded_inputs, padded_targets = [], []
                for seq in batch:
                    input_ids = seq[:-1]
                    target_ids = seq[1:]
                    pad_amount = batch_max_len - len(input_ids)
                    padded_inputs.append(input_ids + [pad_id] * pad_amount)
                    padded_targets.append(target_ids + [pad_id] * pad_amount)

                input_tensor = torch.tensor(padded_inputs, dtype=torch.long)
                target_tensor = torch.tensor(padded_targets, dtype=torch.long)

                logits = self.model(input_tensor)
                loss = nn.functional.cross_entropy(
                    logits.reshape(-1, vocab_size), target_tensor.reshape(-1), ignore_index=pad_id
                )

                optimizer.zero_grad()
                loss.backward()
                # Gradient clipping added alongside the depth increase
                # (2 -> 3 layers): deeper transformers are more prone to
                # occasional gradient spikes early in training, and this
                # is the standard, cheap mitigation.
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                optimizer.step()
                epoch_losses.append(loss.item())
            if epoch_losses:
                final_loss = sum(epoch_losses) / len(epoch_losses)

        self.model.eval()
        total_params = sum(p.numel() for p in self.model.parameters())
        self.last_training_info = {
            "final_loss": round(final_loss, 4) if final_loss is not None else None,
            "vocab_size": vocab_size,
            "total_parameters": total_params,
            "synthetic_sentences_trained_on": len(sequences),
            "architecture": (f"{self.NUM_LAYERS}-layer, {self.NUM_HEADS}-head causal "
                              f"self-attention, embed_dim={self.EMBED_DIM}, "
                              f"~{total_params:,} parameters"),
        }

    # ---- inference --------------------------------------------------------

    def predict_next_words(self, text: str, top_k: int = 5):
        """Same return shape as ConversationalLanguageModel.
        predict_next_words() (a list of (word, probability) pairs plus
        a source label) so callers/handlers don't need to know which
        backend answered."""
        if self.backend != "transformer":
            return self.ngram_model.predict_next_words(text, top_k=top_k)

        tokens = ["<bos>"] + self.ngram_model._tokenize(text)
        tokens = tokens[-(self.MAX_SEQ_LEN):]
        ids = self._encode(tokens)
        input_tensor = torch.tensor([ids], dtype=torch.long)

        with torch.no_grad():
            logits = self.model(input_tensor)
        last_logits = logits[0, -1]
        probs = torch.softmax(last_logits, dim=0)
        top_probs, top_ids = torch.topk(probs, min(top_k + len(self.SPECIAL_TOKENS), len(probs)))

        results = []
        for p, i in zip(top_probs.tolist(), top_ids.tolist()):
            word = self.id2word.get(i, "<unk>")
            if word not in self.SPECIAL_TOKENS:
                results.append((word, p))
            if len(results) >= top_k:
                break
        return results, "self-attention transformer"

    def format_prediction(self, text: str, top_k: int = 5) -> str:
        if self.backend != "transformer":
            return self.ngram_model.format_prediction(text, top_k=top_k)
        predictions, source = self.predict_next_words(text, top_k=top_k)
        if not predictions:
            return "I don't have a strong prediction for what comes next there."
        formatted = ", ".join(f"'{w}' ({p:.0%})" for w, p in predictions)
        return f"Most likely next word(s) (via {source}): {formatted}"

    def continue_text(self, seed_text: str = "", max_words: int = 12, temperature: float = 0.9) -> str:
        """
        Autoregressive generation: repeatedly predict a probability
        distribution over the next token, SAMPLE from it (temperature
        controls how sharply peaked that sampling is - lower is more
        conservative/repetitive, higher is more varied/riskier), append
        it, and repeat - the standard generation loop transformer LMs
        use, stopping early on a sampled <eos> exactly the way the
        trigram model stops on its own learned <end> token.
        """
        if self.backend != "transformer":
            return self.ngram_model.continue_text(seed_text, max_words=max_words)

        tokens = ["<bos>"] + (self.ngram_model._tokenize(seed_text) if seed_text else [])
        generated = list(tokens)

        for _ in range(max_words):
            window = generated[-(self.MAX_SEQ_LEN):]
            ids = self._encode(window)
            input_tensor = torch.tensor([ids], dtype=torch.long)
            with torch.no_grad():
                logits = self.model(input_tensor)
            last_logits = logits[0, -1] / max(temperature, 0.05)
            probs = torch.softmax(last_logits, dim=0)
            next_id = torch.multinomial(probs, 1).item()
            next_word = self.id2word.get(next_id, "<unk>")
            if next_word == "<eos>":
                break
            generated.append(next_word)

        output_tokens = [t for t in generated if t not in self.SPECIAL_TOKENS]
        return self.ngram_model._detokenize(output_tokens)

    def format_continuation(self, seed_text: str = "", max_words: int = 12) -> str:
        if self.backend != "transformer":
            return self.ngram_model.format_continuation(seed_text, max_words=max_words)
        result = self.continue_text(seed_text, max_words=max_words)
        if not result:
            return "I couldn't generate a continuation from that."
        return result


# ==============================================================================
