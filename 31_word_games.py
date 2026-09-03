"""Section 6K: WORD SCRAMBLE GAME & ANAGRAM SOLVER (rule-based, no ML)

Reuses TypoCorrector.COMMON_WORDS (Section 7A2) as its word list rather
than hand-writing a second one.

WordScrambleGame now supports:
  - difficulty tiers (easy/medium/hard, by word length) instead of one
    fixed length range.
  - a hint system that reveals one more correct letter (in its correct
    position) per hint request, tracking how many hints were used so
    a "solved with N hints" note can be shown.

AnagramSolver now also supports MULTI-WORD phrase anagrams (does a
combination of two dictionary words use exactly the same letters as
the input?) in addition to single-word anagrams - a meaningfully
harder search problem (partitioning one letter-multiset across two
words instead of matching it against single dictionary entries).
"""
import random
from collections import Counter


class WordScrambleGame:
    DIFFICULTY_RANGES = {"easy": (4, 5), "medium": (6, 7), "hard": (8, 10)}

    def __init__(self, word_pool):
        self._all_words = [w for w in word_pool if w.isalpha()]
        self.difficulty = "medium"
        self.active = False
        self.answer = None
        self.scrambled = None
        self.revealed = []       # list of bools, one per letter of answer
        self.hints_used = 0

    def set_difficulty(self, level: str) -> str:
        level = level.strip().lower()
        if level not in self.DIFFICULTY_RANGES:
            return "Difficulty should be 'easy', 'medium', or 'hard'."
        self.difficulty = level
        return f"Word scramble difficulty set to '{level}'."

    def _pool_for_difficulty(self):
        lo, hi = self.DIFFICULTY_RANGES[self.difficulty]
        return [w for w in self._all_words if lo <= len(w) <= hi]

    @staticmethod
    def _scramble(word: str) -> str:
        letters = list(word)
        scrambled = word
        for _ in range(10):
            random.shuffle(letters)
            scrambled = "".join(letters)
            if scrambled != word:
                break
        return scrambled

    def start(self) -> str:
        pool = self._pool_for_difficulty()
        if not pool:
            return f"I don't have any words of the right length for '{self.difficulty}' difficulty."
        self.answer = random.choice(pool)
        self.scrambled = self._scramble(self.answer)
        self.active = True
        self.revealed = [False] * len(self.answer)
        self.hints_used = 0
        return (f"Unscramble this word ({self.difficulty}): {self.scrambled.upper()}  "
                "(say 'guess <word>', or 'hint' for a letter)")

    def hint(self) -> str:
        if not self.active:
            return "There's no scramble in progress - say 'scramble a word' to start."
        hidden_positions = [i for i, r in enumerate(self.revealed) if not r]
        if not hidden_positions:
            return "Every letter is already revealed - go ahead and guess!"
        pos = random.choice(hidden_positions)
        self.revealed[pos] = True
        self.hints_used += 1
        pattern = "".join(ch.upper() if shown else "_" for ch, shown in zip(self.answer, self.revealed))
        return f"Hint: {pattern}  ({self.hints_used} hint{'s' if self.hints_used != 1 else ''} used)"

    def guess(self, attempt: str):
        """Returns (message, game_over)."""
        if not self.active:
            return "There's no scramble in progress - say 'scramble a word' to start.", False
        if attempt.strip().lower() == self.answer:
            self.active = False
            hint_note = f" (solved with {self.hints_used} hints)" if self.hints_used else ""
            return f"That's it - '{self.answer}'!{hint_note} Nicely done.", True
        return "Not quite - try again, or say 'hint' or 'give up'.", False

    def give_up(self) -> str:
        if not self.active:
            return "There's no scramble in progress."
        answer = self.answer
        self.active = False
        return f"The word was '{answer}'."


class AnagramSolver:
    def __init__(self, word_pool):
        self._words = sorted({w.lower() for w in word_pool if w.isalpha()})
        self._by_key = {}
        for w in self._words:
            key = "".join(sorted(w))
            self._by_key.setdefault(key, set()).add(w)
        # only words short enough that a two-word search is tractable
        self._short_words = [w for w in self._words if 2 <= len(w) <= 8]

    def find(self, word: str, limit: int = 10):
        key = "".join(sorted(word.lower()))
        matches = sorted(m for m in self._by_key.get(key, set()) if m != word.lower())
        if not matches:
            return f"I couldn't find any anagrams of '{word}' in my word list."
        shown = matches[:limit]
        extra = f" (+{len(matches) - limit} more)" if len(matches) > limit else ""
        return f"Anagrams of '{word}': {', '.join(shown)}{extra}"

    def find_phrase(self, text: str, limit: int = 5):
        """Finds pairs of dictionary words whose combined letters are
        exactly an anagram of `text` - a genuinely different (and
        combinatorially larger) search than single-word anagrams: for
        each candidate first word that's a "sub-multiset" of the
        target letters, check whether the LEFTOVER letters exactly
        match some other dictionary word."""
        target = Counter(ch for ch in text.lower() if ch.isalpha())
        if not target:
            return "Give me some letters to find a phrase anagram for."
        total_letters = sum(target.values())
        if total_letters > 18:
            return "That's too many letters for a phrase-anagram search - try something shorter."

        results = []
        seen_pairs = set()
        for w1 in self._short_words:
            c1 = Counter(w1)
            if any(c1[ch] > target[ch] for ch in c1):
                continue
            remainder = target - c1
            if not remainder:
                continue  # w1 alone already covers everything; handled by find()
            remainder_key = "".join(sorted(remainder.elements()))
            for w2 in self._by_key.get(remainder_key, set()):
                pair = tuple(sorted((w1, w2)))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)
                results.append(f"{w1} {w2}")
                if len(results) >= limit:
                    break
            if len(results) >= limit:
                break

        if not results:
            return f"I couldn't find a two-word phrase anagram of '{text}' in my word list."
        return f"Phrase anagrams of '{text}': " + "; ".join(results)
