"""Section 6J: NAME GENERATOR (character-level Markov chain, no ML libs)

Previously just concatenated a random first-half + random second-half
from two fixed word lists (a handful of possible combinations, and
never anything not already implicit in those lists). This version
trains a small order-2 character Markov chain directly on a seed
corpus of real-sounding fantasy names, then GENERATES new names
character-by-character by sampling from the learned
P(next_char | previous 2 chars) distribution - the exact same
technique as the n-gram language model elsewhere in this file
(Section 14), just trained on characters instead of words. This can
produce names that never appeared anywhere in the training corpus,
while still "sounding like" the training set, because it's learned
the corpus's actual letter-transition statistics rather than just
reshuffling whole fixed fragments.
"""
import random
from collections import defaultdict, Counter

_NAME_SEED_CORPUS = [
    "Thalindor", "Brenwyn", "Kaelith", "Isolde", "Vorathis", "Elendra",
    "Driscoll", "Wynethra", "Orindel", "Faelwyn", "Gwyndor", "Morwenna",
    "Silvarien", "Torvald", "Nyxandra", "Aerendil", "Bralthor", "Cynwise",
    "Thalorien", "Brenmar", "Kaelwyn", "Isolwen", "Vorendil", "Elenmoor",
    "Drisandra", "Wynmar", "Oristhas", "Faelmere", "Gwynshade", "Morwyn",
]

_ADJECTIVES = [
    "swift", "quiet", "brave", "clever", "bright", "hidden", "bold",
    "calm", "wild", "gentle", "sharp", "lucky", "steady", "curious",
]
_NOUNS = [
    "otter", "falcon", "ember", "willow", "comet", "harbor", "maple",
    "raven", "pebble", "lantern", "sparrow", "thistle", "cinder",
]
_PROJECT_NOUNS = [
    "Compass", "Anchor", "Beacon", "Bridge", "Horizon", "Ledger",
    "Signal", "Atlas", "Forge", "Nexus", "Trellis", "Cascade",
]

_ORDER = 2       # how many previous characters condition the next one
_END = "\0"      # sentinel marking "name ends here"


class _CharMarkovChain:
    def __init__(self, corpus, order=_ORDER):
        self.order = order
        self.transitions = defaultdict(Counter)
        for word in corpus:
            padded = ("\0" * order) + word + _END
            for i in range(len(padded) - order):
                state = padded[i:i + order]
                nxt = padded[i + order]
                self.transitions[state][nxt] += 1

    def generate(self, max_len=12, min_len=4):
        for _attempt in range(20):  # a few tries in case we hit min_len too early
            state = "\0" * self.order
            chars = []
            for _ in range(max_len):
                counts = self.transitions.get(state)
                if not counts:
                    break
                population = list(counts.elements())
                nxt = random.choice(population)
                if nxt == _END:
                    if len(chars) >= min_len:
                        break
                    else:
                        continue  # too short, keep going instead of ending
                chars.append(nxt)
                state = (state + nxt)[-self.order:]
            if len(chars) >= min_len:
                return "".join(chars)
        return "".join(chars) if chars else random.choice(_NAME_SEED_CORPUS)


class NameGenerator:
    def __init__(self):
        self._chain = _CharMarkovChain(_NAME_SEED_CORPUS)

    def fantasy_name(self) -> str:
        raw = self._chain.generate()
        return raw[0].upper() + raw[1:].lower()

    def username(self) -> str:
        return f"{random.choice(_ADJECTIVES)}_{random.choice(_NOUNS)}{random.randint(1, 999)}"

    def project_name(self) -> str:
        return f"Project {random.choice(_ADJECTIVES).capitalize()} {random.choice(_PROJECT_NOUNS)}"

    def format_batch(self, kind: str, count: int = 5) -> str:
        count = max(1, min(count, 20))
        generator = {"fantasy": self.fantasy_name, "username": self.username,
                     "project": self.project_name}.get(kind, self.fantasy_name)
        names = set()
        attempts = 0
        while len(names) < count and attempts < count * 10:
            names.add(generator())
            attempts += 1
        return "\n".join(f"- {n}" for n in list(names)[:count])
