"""Section 3J: CIPHER TOOLS (Caesar, ROT13, Vigenere, substitution, Morse)

Five classic ciphers/codes, ordered roughly by increasing complexity:
  - Caesar / ROT13: single fixed shift - breakable by trying all 26.
  - Vigenere: a REPEATING KEYWORD shift cipher - each letter of the
    keyword gives a different Caesar shift, cycling through the
    keyword letter by letter. Historically called "le chiffre
    indechiffrable" (the indecipherable cipher) because simple
    frequency analysis (which breaks Caesar/substitution trivially)
    doesn't work directly against it - the same plaintext letter maps
    to different ciphertext letters depending on position.
  - Keyed substitution: a full 26-letter permutation alphabet derived
    from a keyword (keyword letters first, deduped, then the rest of
    the alphabet in order) - the classic "secret decoder ring" cipher.
  - Morse code: not a cipher (no secrecy - it's a public, standardized
    encoding), included alongside these for the same "text transform
    toy" reason as before.

None of this is remotely strong enough to be real encryption - all
five are textbook-broken by modern cryptanalysis in seconds. They're
here as an educational/for-fun text-transform toy, same spirit as the
existing pig-latin/reverse-text tools.
"""

_MORSE_TABLE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
}
_MORSE_REVERSE = {v: k for k, v in _MORSE_TABLE.items()}
_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class CipherTools:
    # ---- Caesar / ROT13 -----------------------------------------------

    @staticmethod
    def caesar(text: str, shift: int) -> str:
        shift %= 26
        out = []
        for ch in text:
            if ch.isupper():
                out.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
            elif ch.islower():
                out.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))
            else:
                out.append(ch)
        return "".join(out)

    @classmethod
    def rot13(cls, text: str) -> str:
        return cls.caesar(text, 13)

    @staticmethod
    def caesar_brute_force(ciphertext: str) -> str:
        """Tries all 26 shifts - useful when you don't know the shift
        used to encode a Caesar-ciphered message."""
        lines = []
        for shift in range(26):
            lines.append(f"shift {shift:2d}: {CipherTools.caesar(ciphertext, -shift)}")
        return "\n".join(lines)

    # ---- Vigenere -------------------------------------------------------

    @staticmethod
    def _vigenere_transform(text: str, keyword: str, decode: bool) -> str:
        keyword = "".join(ch for ch in keyword.upper() if ch.isalpha())
        if not keyword:
            return text
        out = []
        key_index = 0
        for ch in text:
            if ch.isalpha():
                shift = ord(keyword[key_index % len(keyword)]) - ord("A")
                if decode:
                    shift = -shift
                base = ord("A") if ch.isupper() else ord("a")
                out.append(chr((ord(ch) - base + shift) % 26 + base))
                key_index += 1
            else:
                out.append(ch)
        return "".join(out)

    @classmethod
    def vigenere_encode(cls, text: str, keyword: str) -> str:
        return cls._vigenere_transform(text, keyword, decode=False)

    @classmethod
    def vigenere_decode(cls, text: str, keyword: str) -> str:
        return cls._vigenere_transform(text, keyword, decode=True)

    # ---- Keyed substitution cipher ---------------------------------------

    @staticmethod
    def _substitution_alphabet(keyword: str) -> str:
        keyword = "".join(ch for ch in keyword.upper() if ch.isalpha())
        seen = []
        for ch in keyword + _ALPHABET:
            if ch not in seen:
                seen.append(ch)
        return "".join(seen)

    @classmethod
    def substitution_encode(cls, text: str, keyword: str) -> str:
        cipher_alphabet = cls._substitution_alphabet(keyword)
        mapping = {plain: cipher for plain, cipher in zip(_ALPHABET, cipher_alphabet)}
        out = []
        for ch in text:
            if ch.isupper():
                out.append(mapping[ch])
            elif ch.islower():
                out.append(mapping[ch.upper()].lower())
            else:
                out.append(ch)
        return "".join(out)

    @classmethod
    def substitution_decode(cls, text: str, keyword: str) -> str:
        cipher_alphabet = cls._substitution_alphabet(keyword)
        mapping = {cipher: plain for plain, cipher in zip(_ALPHABET, cipher_alphabet)}
        out = []
        for ch in text:
            if ch.isupper():
                out.append(mapping[ch])
            elif ch.islower():
                out.append(mapping[ch.upper()].lower())
            else:
                out.append(ch)
        return "".join(out)

    # ---- Morse code -------------------------------------------------------

    @staticmethod
    def to_morse(text: str) -> str:
        words = text.upper().split(" ")
        encoded_words = []
        for word in words:
            letters = []
            for ch in word:
                if ch in _MORSE_TABLE:
                    letters.append(_MORSE_TABLE[ch])
                # silently skip characters with no Morse mapping
                # (punctuation beyond digits/letters), rather than
                # crashing or inserting an ambiguous placeholder
            encoded_words.append(" ".join(letters))
        return " / ".join(encoded_words)

    @staticmethod
    def from_morse(code: str) -> str:
        words = code.strip().split(" / ")
        decoded_words = []
        for word in words:
            letters = []
            for token in word.split(" "):
                if token in _MORSE_REVERSE:
                    letters.append(_MORSE_REVERSE[token])
            decoded_words.append("".join(letters))
        return " ".join(decoded_words)
