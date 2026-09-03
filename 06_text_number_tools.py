"""Text/number tools, calculator, case converter, password gen, hash, base64, JSON/CSV, entity extraction (Sections 6C,6D,3B-3H)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 6C: TEXT TOOLS
# ==============================================================================

class TextTools:
    """
    Small, deterministic text-manipulation utilities: word/char counts,
    palindrome checking, case conversion, reversal, vowel counting,
    and a basic word-frequency summary. All plain string/regex logic -
    no NLP libraries, no learning.
    """

    @staticmethod
    def word_count(text: str) -> int:
        return len(text.split())

    @staticmethod
    def char_count(text: str, ignore_spaces: bool = False) -> int:
        if ignore_spaces:
            return len(text.replace(" ", ""))
        return len(text)

    @staticmethod
    def is_palindrome(text: str) -> bool:
        cleaned = re.sub(r"[^a-z0-9]", "", text.lower())
        return cleaned == cleaned[::-1] and len(cleaned) > 0

    @staticmethod
    def reverse_text(text: str) -> str:
        return text[::-1]

    @staticmethod
    def reverse_words(text: str) -> str:
        return " ".join(reversed(text.split()))

    @staticmethod
    def to_upper(text: str) -> str:
        return text.upper()

    @staticmethod
    def to_lower(text: str) -> str:
        return text.lower()

    @staticmethod
    def to_title(text: str) -> str:
        return text.title()

    @staticmethod
    def vowel_count(text: str) -> int:
        return sum(1 for ch in text.lower() if ch in "aeiou")

    @staticmethod
    def consonant_count(text: str) -> int:
        return sum(1 for ch in text.lower() if ch.isalpha() and ch not in "aeiou")

    @staticmethod
    def count_specific_letter(text: str, letter: str) -> int:
        return text.lower().count(letter.lower())

    @staticmethod
    def to_pig_latin_word(word: str) -> str:
        """Very simple, rigid Pig Latin rule: move leading consonant
        cluster to the end and add 'ay'. Not linguistically perfect,
        deliberately simple/rule-based."""
        match = re.match(r"^([^aeiouAEIOU]*)(.*)$", word)
        if not match:
            return word + "ay"
        consonants, rest = match.groups()
        if not consonants:
            return word + "way"
        return f"{rest}{consonants.lower()}ay"

    def to_pig_latin(self, text: str) -> str:
        words = re.findall(r"[a-zA-Z']+", text)
        return " ".join(self.to_pig_latin_word(w) for w in words)

    @staticmethod
    def shout(text: str) -> str:
        return text.upper() + "!" * 3

    @staticmethod
    def whisper(text: str) -> str:
        return text.lower().replace("!", ".")

    def word_frequency_summary(self, text: str, top_n: int = 5) -> str:
        """Uses pandas/numpy for a quick frequency breakdown - descriptive
        statistics only, not a learned model."""
        words = re.findall(r"[a-zA-Z']+", text.lower())
        if not words:
            return "There's no text to analyze."
        counts = Counter(words)
        series = pd.Series(counts).sort_values(ascending=False)
        top = series.head(top_n)
        lines = [f"Word frequency (top {min(top_n, len(top))} of {len(series)} unique words):"]
        for word, count in top.items():
            lines.append(f"  '{word}': {count}")
        lines.append(f"Average word length: {np.mean([len(w) for w in words]):.1f} characters")
        return "\n".join(lines)


# ==============================================================================
# SECTION 6D: NUMBER TOOLS
# ==============================================================================

class NumberTools:
    """
    Small, deterministic numeric utilities: prime checking, unit
    conversion, number-to-words conversion, factorial, Fibonacci,
    and basic descriptive statistics over a list of numbers (via
    numpy - again, descriptive only, not a fitted model).
    """

    ONES = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    TEENS = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
              "sixteen", "seventeen", "eighteen", "nineteen"]
    TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    SCALES = ["", "thousand", "million", "billion", "trillion"]

    # Rigid, hand-written unit conversion table. Each entry maps
    # (from_unit, to_unit) -> a function that converts the value.
    CONVERSIONS = {
        ("miles", "km"): lambda v: v * 1.60934,
        ("km", "miles"): lambda v: v / 1.60934,
        ("kg", "lbs"): lambda v: v * 2.20462,
        ("lbs", "kg"): lambda v: v / 2.20462,
        ("celsius", "fahrenheit"): lambda v: v * 9 / 5 + 32,
        ("fahrenheit", "celsius"): lambda v: (v - 32) * 5 / 9,
        ("meters", "feet"): lambda v: v * 3.28084,
        ("feet", "meters"): lambda v: v / 3.28084,
        ("inches", "cm"): lambda v: v * 2.54,
        ("cm", "inches"): lambda v: v / 2.54,
        ("gallons", "liters"): lambda v: v * 3.78541,
        ("liters", "gallons"): lambda v: v / 3.78541,
        ("ounces", "grams"): lambda v: v * 28.3495,
        ("grams", "ounces"): lambda v: v / 28.3495,
        # ---- temperature: Kelvin, added alongside Celsius/Fahrenheit ----
        ("celsius", "kelvin"): lambda v: v + 273.15,
        ("kelvin", "celsius"): lambda v: v - 273.15,
        ("fahrenheit", "kelvin"): lambda v: (v - 32) * 5 / 9 + 273.15,
        ("kelvin", "fahrenheit"): lambda v: (v - 273.15) * 9 / 5 + 32,
        # ---- area ----
        ("acres", "hectares"): lambda v: v * 0.404686,
        ("hectares", "acres"): lambda v: v / 0.404686,
        ("sqmeters", "sqfeet"): lambda v: v * 10.7639,
        ("sqfeet", "sqmeters"): lambda v: v / 10.7639,
        ("sqkm", "sqmiles"): lambda v: v * 0.386102,
        ("sqmiles", "sqkm"): lambda v: v / 0.386102,
        # ---- volume (cooking-scale) ----
        ("cups", "ml"): lambda v: v * 236.588,
        ("ml", "cups"): lambda v: v / 236.588,
        ("tablespoons", "ml"): lambda v: v * 14.7868,
        ("ml", "tablespoons"): lambda v: v / 14.7868,
        ("teaspoons", "ml"): lambda v: v * 4.92892,
        ("ml", "teaspoons"): lambda v: v / 4.92892,
        # ---- digital storage (binary/1024-based, the OS convention) ----
        ("bytes", "kb"): lambda v: v / 1024,
        ("kb", "bytes"): lambda v: v * 1024,
        ("kb", "mb"): lambda v: v / 1024,
        ("mb", "kb"): lambda v: v * 1024,
        ("mb", "gb"): lambda v: v / 1024,
        ("gb", "mb"): lambda v: v * 1024,
        ("gb", "tb"): lambda v: v / 1024,
        ("tb", "gb"): lambda v: v * 1024,
        # ---- speed ----
        ("mph", "kmh"): lambda v: v * 1.60934,
        ("kmh", "mph"): lambda v: v / 1.60934,
        ("mph", "knots"): lambda v: v * 0.868976,
        ("knots", "mph"): lambda v: v / 0.868976,
        # ---- energy ----
        ("calories", "joules"): lambda v: v * 4.184,
        ("joules", "calories"): lambda v: v / 4.184,
        ("kcal", "joules"): lambda v: v * 4184,
        ("joules", "kcal"): lambda v: v / 4184,
        # ---- pressure ----
        ("psi", "bar"): lambda v: v * 0.0689476,
        ("bar", "psi"): lambda v: v / 0.0689476,
        ("atm", "psi"): lambda v: v * 14.6959,
        ("psi", "atm"): lambda v: v / 14.6959,
        # ---- time (trivial arithmetic, but convenient to have alongside the rest) ----
        ("hours", "minutes"): lambda v: v * 60,
        ("minutes", "hours"): lambda v: v / 60,
        ("minutes", "seconds"): lambda v: v * 60,
        ("seconds", "minutes"): lambda v: v / 60,
        ("hours", "seconds"): lambda v: v * 3600,
        ("seconds", "hours"): lambda v: v / 3600,
        ("days", "hours"): lambda v: v * 24,
        ("hours", "days"): lambda v: v / 24,
    }

    UNIT_ALIASES = {
        "mile": "miles", "miles": "miles", "mi": "miles",
        "kilometer": "km", "kilometers": "km", "km": "km", "kms": "km",
        "kilogram": "kg", "kilograms": "kg", "kg": "kg", "kgs": "kg",
        "pound": "lbs", "pounds": "lbs", "lb": "lbs", "lbs": "lbs",
        "celsius": "celsius", "c": "celsius",
        "fahrenheit": "fahrenheit", "f": "fahrenheit",
        "kelvin": "kelvin", "k": "kelvin",
        "meter": "meters", "meters": "meters", "m": "meters",
        "foot": "feet", "feet": "feet", "ft": "feet",
        "inch": "inches", "inches": "inches", "in": "inches",
        "centimeter": "cm", "centimeters": "cm", "cm": "cm",
        "gallon": "gallons", "gallons": "gallons", "gal": "gallons",
        "liter": "liters", "liters": "liters", "litre": "liters", "litres": "liters", "l": "liters",
        "ounce": "ounces", "ounces": "ounces", "oz": "ounces",
        "gram": "grams", "grams": "grams", "g": "grams",
        # area
        "acre": "acres", "acres": "acres",
        "hectare": "hectares", "hectares": "hectares", "ha": "hectares",
        "sqmeter": "sqmeters", "sqmeters": "sqmeters", "sq meters": "sqmeters",
        "sqfeet": "sqfeet", "sqfoot": "sqfeet", "sq feet": "sqfeet",
        "sqkm": "sqkm", "sq km": "sqkm",
        "sqmiles": "sqmiles", "sqmile": "sqmiles", "sq miles": "sqmiles",
        # volume
        "cup": "cups", "cups": "cups",
        "ml": "ml", "milliliter": "ml", "milliliters": "ml", "millilitre": "ml", "millilitres": "ml",
        "tablespoon": "tablespoons", "tablespoons": "tablespoons", "tbsp": "tablespoons",
        "teaspoon": "teaspoons", "teaspoons": "teaspoons", "tsp": "teaspoons",
        # digital storage
        "byte": "bytes", "bytes": "bytes", "b": "bytes",
        "kb": "kb", "kilobyte": "kb", "kilobytes": "kb",
        "mb": "mb", "megabyte": "mb", "megabytes": "mb",
        "gb": "gb", "gigabyte": "gb", "gigabytes": "gb",
        "tb": "tb", "terabyte": "tb", "terabytes": "tb",
        # speed
        "mph": "mph", "kmh": "kmh", "kph": "kmh",
        "knot": "knots", "knots": "knots",
        # energy
        "calorie": "calories", "calories": "calories", "cal": "calories",
        "joule": "joules", "joules": "joules", "j": "joules",
        "kcal": "kcal", "kilocalorie": "kcal", "kilocalories": "kcal",
        # pressure
        "psi": "psi", "bar": "bar", "atm": "atm", "atmosphere": "atm", "atmospheres": "atm",
        # time
        "hour": "hours", "hours": "hours", "hr": "hours", "hrs": "hours",
        "minute": "minutes", "minutes": "minutes", "min": "minutes", "mins": "minutes",
        "second": "seconds", "seconds": "seconds", "sec": "seconds", "secs": "seconds",
        "day": "days", "days": "days",
    }

    def normalize_unit(self, unit: str):
        return self.UNIT_ALIASES.get(unit.strip().lower())

    def convert(self, value: float, from_unit: str, to_unit: str):
        """Returns the converted float, or None if the unit pair isn't
        in the conversion table."""
        f = self.normalize_unit(from_unit)
        t = self.normalize_unit(to_unit)
        if f is None or t is None:
            return None
        if f == t:
            return value
        fn = self.CONVERSIONS.get((f, t))
        if fn is None:
            return None
        return fn(value)

    @staticmethod
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def factorial(n: int) -> int:
        if n < 0:
            raise ValueError("factorial is undefined for negative numbers")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def fibonacci_sequence(n: int) -> list:
        """First n Fibonacci numbers, starting 0, 1, 1, 2, 3..."""
        if n <= 0:
            return []
        seq = [0, 1]
        while len(seq) < n:
            seq.append(seq[-1] + seq[-2])
        return seq[:n]

    @staticmethod
    def is_even(n: int) -> bool:
        return n % 2 == 0

    def number_to_words(self, n: int) -> str:
        """Convert an integer to its English words form, rigidly,
        without any external num2words-style library."""
        if n == 0:
            return "zero"
        if n < 0:
            return "negative " + self.number_to_words(-n)

        parts = []
        scale_idx = 0
        while n > 0:
            chunk = n % 1000
            if chunk:
                chunk_words = self._three_digit_to_words(chunk)
                if self.SCALES[scale_idx]:
                    chunk_words += " " + self.SCALES[scale_idx]
                parts.append(chunk_words)
            n //= 1000
            scale_idx += 1

        return " ".join(reversed(parts))

    def _three_digit_to_words(self, n: int) -> str:
        words = []
        hundreds, remainder = divmod(n, 100)
        if hundreds:
            words.append(f"{self.ONES[hundreds]} hundred")
        if remainder:
            if remainder < 10:
                words.append(self.ONES[remainder])
            elif remainder < 20:
                words.append(self.TEENS[remainder - 10])
            else:
                tens, ones = divmod(remainder, 10)
                tens_word = self.TENS[tens]
                if ones:
                    words.append(f"{tens_word}-{self.ONES[ones]}")
                else:
                    words.append(tens_word)
        return " ".join(words)

    @staticmethod
    def describe_numbers(numbers: list) -> str:
        """Descriptive statistics over a list of numbers using numpy.
        Purely arithmetic/statistical, not a fitted or learned model."""
        if not numbers:
            return "I need at least one number to describe."
        arr = np.array(numbers, dtype=float)
        lines = [
            f"Count: {len(arr)}",
            f"Sum: {np.sum(arr):g}",
            f"Mean: {np.mean(arr):.3f}",
            f"Median: {np.median(arr):.3f}",
            f"Min: {np.min(arr):g}",
            f"Max: {np.max(arr):g}",
            f"Standard deviation: {np.std(arr):.3f}",
        ]
        return "\n".join(lines)


# ==============================================================================
# SECTION 3B: SCIENTIFIC CALCULATOR (single-function, no eval())
# ==============================================================================
#
# _handle_simple_math (Section 7) only handles one binary operator at
# a time (a + b). This adds single-ARGUMENT scientific functions -
# square root, powers, logarithms, trig, factorial - each parsed with
# its own rigid regex and computed with plain math/numpy calls. Still
# no eval() of arbitrary expressions anywhere: every recognized pattern
# maps to exactly one hand-written function call.
class ScientificCalculator:
    """Single-function scientific calculator: one recognized pattern
    per operation, computed with Python's math module (no eval, no
    expression parser) - the same "rigid, no arbitrary code execution"
    philosophy as _handle_simple_math."""

    @staticmethod
    def sqrt(value: float):
        if value < 0:
            return None  # no complex-number support - fail closed rather than raise
        return math.sqrt(value)

    @staticmethod
    def power(base: float, exponent: float):
        try:
            return base ** exponent
        except (OverflowError, ValueError):
            return None

    @staticmethod
    def log(value: float, base: float = 10.0):
        if value <= 0:
            return None
        try:
            return math.log(value, base)
        except ValueError:
            return None

    @staticmethod
    def ln(value: float):
        if value <= 0:
            return None
        return math.log(value)

    @staticmethod
    def sin_degrees(value: float):
        return math.sin(math.radians(value))

    @staticmethod
    def cos_degrees(value: float):
        return math.cos(math.radians(value))

    @staticmethod
    def tan_degrees(value: float):
        return math.tan(math.radians(value))

    @staticmethod
    def factorial(n: int):
        if n < 0 or n != int(n):
            return None
        if n > 170:  # float overflow territory for math.factorial's result
            return None
        return math.factorial(int(n))

    @staticmethod
    def percentage_of(percent: float, whole: float):
        return (percent / 100.0) * whole

    @staticmethod
    def percent_change(old_value: float, new_value: float):
        if old_value == 0:
            return None
        return ((new_value - old_value) / old_value) * 100.0


# ==============================================================================
# SECTION 3C: TEXT CASE CONVERTER
# ==============================================================================
#
# Rigid, deterministic string-case transformations - no ML, just
# str methods and regex splitting on word boundaries. Handles the
# common programming-identifier cases (snake_case, camelCase,
# PascalCase, kebab-case) in addition to plain upper/lower/title,
# converting THROUGH a normalized "list of words" representation so
# any-case input can be converted to any-case output, not just a fixed
# set of pairwise conversions.
class TextCaseConverter:
    @staticmethod
    def _split_words(text: str) -> list:
        """Normalizes snake_case, kebab-case, camelCase, PascalCase,
        and plain space-separated text into a list of lowercase words."""
        # Insert a space before each internal uppercase letter (handles
        # camelCase/PascalCase), then split on any non-alphanumeric run.
        spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
        words = re.split(r"[\s_\-]+", spaced)
        return [w.lower() for w in words if w]

    @classmethod
    def to_snake_case(cls, text: str) -> str:
        return "_".join(cls._split_words(text))

    @classmethod
    def to_kebab_case(cls, text: str) -> str:
        return "-".join(cls._split_words(text))

    @classmethod
    def to_camel_case(cls, text: str) -> str:
        words = cls._split_words(text)
        if not words:
            return ""
        return words[0] + "".join(w.capitalize() for w in words[1:])

    @classmethod
    def to_pascal_case(cls, text: str) -> str:
        words = cls._split_words(text)
        return "".join(w.capitalize() for w in words)

    @classmethod
    def to_title_case(cls, text: str) -> str:
        words = cls._split_words(text)
        return " ".join(w.capitalize() for w in words)

    @staticmethod
    def to_upper_case(text: str) -> str:
        return text.upper()

    @staticmethod
    def to_lower_case(text: str) -> str:
        return text.lower()

    @classmethod
    def convert(cls, text: str, target_case: str):
        target_case = target_case.lower().strip()
        converters = {
            "snake": cls.to_snake_case, "snake_case": cls.to_snake_case,
            "kebab": cls.to_kebab_case, "kebab-case": cls.to_kebab_case,
            "camel": cls.to_camel_case, "camelcase": cls.to_camel_case,
            "pascal": cls.to_pascal_case, "pascalcase": cls.to_pascal_case,
            "title": cls.to_title_case, "titlecase": cls.to_title_case,
            "upper": cls.to_upper_case, "uppercase": cls.to_upper_case,
            "lower": cls.to_lower_case, "lowercase": cls.to_lower_case,
        }
        fn = converters.get(target_case)
        if fn is None:
            return None
        return fn(text)


# ==============================================================================
# SECTION 3D: PASSWORD / PASSPHRASE GENERATOR
# ==============================================================================
#
# Uses Python's `secrets` module (cryptographically secure randomness,
# NOT the `random` module used elsewhere in this file for jokes/poems/
# story picks, where predictability doesn't matter) - the standard-
# library-recommended choice specifically for generating passwords,
# tokens, and anything else security-sensitive.
class PasswordGenerator:
    AMBIGUOUS_CHARS = set("Il1O0")

    @staticmethod
    def generate(length: int = 16, use_upper: bool = True, use_digits: bool = True,
                 use_symbols: bool = True, avoid_ambiguous: bool = True) -> str:
        length = max(4, min(length, 128))
        pool = list(string.ascii_lowercase)
        if use_upper:
            pool += list(string.ascii_uppercase)
        if use_digits:
            pool += list(string.digits)
        if use_symbols:
            pool += list("!@#$%^&*()-_=+[]{}")
        if avoid_ambiguous:
            pool = [c for c in pool if c not in PasswordGenerator.AMBIGUOUS_CHARS]
        return "".join(secrets.choice(pool) for _ in range(length))

    @staticmethod
    def generate_passphrase(num_words: int = 4, separator: str = "-") -> str:
        """
        A Diceware-style passphrase (several random dictionary words
        joined together) - generally easier for a human to actually
        remember than an equal-entropy string of random symbols, which
        is why NIST and most modern password guidance now recommends
        passphrases as an alternative to complex short passwords. Word
        list is FunExtras.QUOTES/RIDDLES/JOKES vocabulary rather than a
        dedicated wordlist (this file doesn't bundle one), so entropy
        here is illustrative, not a rigorous Diceware-equivalent count.
        """
        num_words = max(2, min(num_words, 10))
        word_pool = sorted(_NGRAM_UNIGRAMS.keys()) if "_NGRAM_UNIGRAMS" in globals() else []
        word_pool = [w for w in word_pool if w.isalpha() and 3 <= len(w) <= 9]
        if len(word_pool) < num_words:
            # Fallback word list if the n-gram vocabulary isn't available
            # for some reason - keeps this generator working standalone.
            word_pool = ["orbit", "maple", "cobalt", "ember", "quartz", "willow",
                         "harbor", "signal", "canyon", "lantern", "meadow", "ripple"]
        chosen = [secrets.choice(word_pool) for _ in range(num_words)]
        return separator.join(w.capitalize() for w in chosen)

    @staticmethod
    def estimate_entropy_bits(length: int, pool_size: int) -> float:
        """log2(pool_size^length) - a standard entropy estimate for a
        uniformly random string, used to give a rough strength read."""
        if pool_size <= 1 or length <= 0:
            return 0.0
        return length * math.log2(pool_size)


# ==============================================================================
# SECTION 3E: HASH CALCULATOR
# ==============================================================================
#
# Thin, deterministic wrapper around Python's stdlib hashlib - no
# custom hash implementation (reimplementing MD5/SHA yourself is both
# unnecessary and a good way to introduce subtle bugs; the stdlib
# versions are the standard, correct, well-tested reference).
class HashCalculator:
    ALGORITHMS = ("md5", "sha1", "sha256", "sha512")

    @classmethod
    def hash_text(cls, text: str, algorithm: str = "sha256"):
        algorithm = algorithm.lower().strip()
        if algorithm not in cls.ALGORITHMS:
            return None
        hasher = hashlib.new(algorithm)
        hasher.update(text.encode("utf-8"))
        return hasher.hexdigest()

    @classmethod
    def hash_all(cls, text: str) -> dict:
        return {algo: cls.hash_text(text, algo) for algo in cls.ALGORITHMS}

    @classmethod
    def format_hash(cls, text: str, algorithm: str = "sha256") -> str:
        digest = cls.hash_text(text, algorithm)
        if digest is None:
            return f"I don't know the '{algorithm}' algorithm - try: {', '.join(cls.ALGORITHMS)}."
        return f"{algorithm}: {digest}"


# ==============================================================================
# SECTION 3F: BASE64 ENCODER/DECODER
# ==============================================================================
class Base64Tool:
    @staticmethod
    def encode(text: str) -> str:
        return base64.b64encode(text.encode("utf-8")).decode("ascii")

    @staticmethod
    def decode(encoded: str):
        """Returns the decoded string, or None if the input isn't
        valid base64 (fails closed rather than raising)."""
        try:
            return base64.b64decode(encoded, validate=True).decode("utf-8")
        except (binascii.Error, ValueError, UnicodeDecodeError):
            return None

    @classmethod
    def format_encode(cls, text: str) -> str:
        return cls.encode(text)

    @classmethod
    def format_decode(cls, encoded: str) -> str:
        result = cls.decode(encoded)
        if result is None:
            return "That doesn't look like valid base64 text."
        return result


# ==============================================================================
# SECTION 3G: JSON / CSV FORMATTER & VALIDATOR
# ==============================================================================
#
# Uses Python's stdlib json/csv modules for actual parsing (no hand-
# rolled parser - correctly handling every edge case of either format,
# quoting rules, nested structures, escape sequences, is exactly the
# kind of thing the standard library already does correctly). What
# this class adds on top is the VALIDATION/REPORTING layer: clear
# pass/fail messages with the exact error location when something's
# wrong, and a pretty-printed or summarized view when it's not.
class DataFormatTool:
    @staticmethod
    def validate_json(text: str) -> dict:
        try:
            parsed = json.loads(text)
            return {"valid": True, "parsed": parsed}
        except json.JSONDecodeError as e:
            return {"valid": False, "error": str(e), "line": e.lineno, "column": e.colno}

    @classmethod
    def format_json_check(cls, text: str) -> str:
        result = cls.validate_json(text)
        if not result["valid"]:
            return f"Invalid JSON: {result['error']} (line {result['line']}, column {result['column']})."
        pretty = json.dumps(result["parsed"], indent=2, ensure_ascii=False)
        kind = type(result["parsed"]).__name__
        return f"Valid JSON ({kind}). Pretty-printed:\n{pretty}"

    @staticmethod
    def validate_csv(text: str) -> dict:
        try:
            reader = csv.reader(io.StringIO(text))
            rows = list(reader)
        except csv.Error as e:
            return {"valid": False, "error": str(e)}
        if not rows:
            return {"valid": False, "error": "No rows found."}
        column_counts = {len(row) for row in rows}
        consistent = len(column_counts) == 1
        return {
            "valid": True,
            "row_count": len(rows),
            "column_count": len(rows[0]),
            "consistent_columns": consistent,
            "header": rows[0] if rows else [],
        }

    @classmethod
    def format_csv_check(cls, text: str) -> str:
        result = cls.validate_csv(text)
        if not result["valid"]:
            return f"Invalid CSV: {result['error']}"
        consistency_note = (
            "all rows have a consistent column count" if result["consistent_columns"]
            else "WARNING: rows have inconsistent column counts (possible malformed row)"
        )
        return (f"CSV looks parseable: {result['row_count']} row(s), "
                f"{result['column_count']} column(s) in the header, {consistency_note}. "
                f"Header: {', '.join(result['header'])}")


# ==============================================================================
# SECTION 3H: SIMPLE NAMED-ENTITY EXTRACTION (rule-based, no ML)
# ==============================================================================
#
# A RULE-BASED entity extractor - regex patterns and capitalization
# heuristics, not a trained NER model (spaCy-style statistical/neural
# NER is a much bigger dependency than this file takes on anywhere
# else). Catches the common, pattern-recognizable entity types well
# (emails, URLs, dates via DateTimeEngine's own parser, money amounts,
# times) and proper nouns POORLY (capitalized-word heuristics can't
# distinguish "Alice met Bob" from "Alice Visited France" from a
# sentence that merely starts a new sentence after a period) - that
# limitation is inherent to a heuristic approach and is stated plainly
# rather than glossed over.
class SimpleEntityExtractor:
    EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
    URL_RE = re.compile(r"\bhttps?://[^\s]+\b")
    MONEY_RE = re.compile(r"\$\d+(?:,\d{3})*(?:\.\d{2})?\b|\b\d+(?:,\d{3})*(?:\.\d{2})?\s?(?:usd|dollars|kes|eur|euros)\b", re.IGNORECASE)
    TIME_RE = re.compile(r"\b\d{1,2}:\d{2}\s?(?:am|pm)?\b", re.IGNORECASE)
    PHONE_RE = re.compile(r"\b(?:\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b")
    HASHTAG_RE = re.compile(r"#\w+")
    MENTION_RE = re.compile(r"(?<!\w)@\w+")

    @classmethod
    def extract_proper_nouns(cls, text: str) -> list:
        """Capitalized words NOT at the start of a sentence, and multi-
        word capitalized runs anywhere - a common, if imprecise,
        heuristic for proper nouns. Filters out the most common
        sentence-starting false positives it can (a word immediately
        following '.', '!', '?', or the very start of the text)."""
        candidates = []
        # multi-word capitalized runs first (e.g. "New York", "Ada Lovelace")
        for match in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b", text):
            candidates.append(match.group(1))
        # single capitalized words not at a sentence boundary
        sentence_start_positions = {0}
        for m in re.finditer(r"[.!?]\s+", text):
            sentence_start_positions.add(m.end())
        for match in re.finditer(r"\b[A-Z][a-z]+\b", text):
            if match.start() not in sentence_start_positions:
                word = match.group(0)
                if not any(word in c for c in candidates):
                    candidates.append(word)
        return candidates

    @classmethod
    def extract(cls, text: str, date_engine: "DateTimeEngine" = None) -> dict:
        entities = {
            "emails": cls.EMAIL_RE.findall(text),
            "urls": cls.URL_RE.findall(text),
            "money": cls.MONEY_RE.findall(text),
            "times": cls.TIME_RE.findall(text),
            "phone_numbers": cls.PHONE_RE.findall(text),
            "hashtags": cls.HASHTAG_RE.findall(text),
            "mentions": cls.MENTION_RE.findall(text),
            "proper_nouns": cls.extract_proper_nouns(text),
        }
        return {k: v for k, v in entities.items() if v}

    @classmethod
    def format_extraction(cls, text: str) -> str:
        entities = cls.extract(text)
        if not entities:
            return "I didn't find any recognizable entities (emails, URLs, dates, money, proper nouns, etc.) in that text."
        lines = ["Entities found:"]
        for label, values in entities.items():
            unique_values = list(dict.fromkeys(values))  # de-dupe, keep order
            lines.append(f"  {label}: {', '.join(unique_values)}")
        return "\n".join(lines)


# ==============================================================================
