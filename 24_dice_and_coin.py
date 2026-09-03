"""Section 3I: DICE ROLLER & COIN FLIP (rule-based, secrets-backed RNG)

Parses full tabletop dice expressions, not just a single "NdM":
  - multiple terms:      "2d6+1d4+3"
  - advantage/disadv:    "2d20 adv"  (roll twice, keep higher)
                         "2d20 disadv" (roll twice, keep lower)
  - exploding dice:      "3d6!" (any max-value roll is rerolled and
                          added, chaining while it keeps maxing out)

Uses `secrets` rather than `random` for the actual rolls - same
reasoning as the existing password generator: no cryptographic need
here, but it costs nothing and avoids ever having to reason about
whether `random`'s seed state matters.
"""
import re
import secrets

_TERM_RE = re.compile(r"([+-]?)\s*(\d*)d(\d+)(!)?|([+-]?)\s*(\d+)(?!d)", re.IGNORECASE)
_ADV_RE = re.compile(r"\b(adv|advantage|disadv|disadvantage)\b", re.IGNORECASE)

MAX_DICE_PER_TERM = 100
MAX_SIDES = 1000
MAX_EXPLOSIONS = 20  # hard safety cap on exploding-die chains


class DiceRoller:
    def _roll_die(self, sides: int) -> int:
        return secrets.randbelow(sides) + 1

    def _roll_exploding(self, sides: int) -> list:
        rolls = [self._roll_die(sides)]
        chain = 0
        while rolls[-1] == sides and chain < MAX_EXPLOSIONS:
            rolls.append(self._roll_die(sides))
            chain += 1
        return rolls

    def roll(self, notation: str) -> str:
        notation = notation.strip()

        adv_match = _ADV_RE.search(notation)
        adv_mode = None
        if adv_match:
            word = adv_match.group(1).lower()
            adv_mode = "advantage" if word.startswith("adv") else "disadvantage"
            notation = _ADV_RE.sub("", notation).strip()

        terms = list(_TERM_RE.finditer(notation))
        if not terms:
            return ("Use dice notation like '2d6', 'd20', '3d8+2', "
                    "'2d20 adv' (advantage), or '3d6!' (exploding).")

        if adv_mode:
            return self._roll_with_advantage(notation, adv_mode)

        total = 0
        breakdown_parts = []
        for match in terms:
            dice_sign, count_str, sides_str, explode, flat_sign, flat_str = match.groups()
            if sides_str:
                sign = -1 if dice_sign == "-" else 1
                count = int(count_str) if count_str else 1
                sides = int(sides_str)
                if count < 1 or count > MAX_DICE_PER_TERM:
                    return f"Please roll between 1 and {MAX_DICE_PER_TERM} dice per term."
                if sides < 2 or sides > MAX_SIDES:
                    return f"Dice need between 2 and {MAX_SIDES} sides."

                term_rolls = []
                for _ in range(count):
                    if explode:
                        chain = self._roll_exploding(sides)
                        term_rolls.append(sum(chain))
                        if len(chain) > 1:
                            breakdown_parts.append(
                                f"{'+' if sign > 0 else '-'}d{sides}!({'+'.join(map(str, chain))})")
                        else:
                            breakdown_parts.append(f"{'+' if sign > 0 else '-'}d{sides}!({chain[0]})")
                    else:
                        term_rolls.append(self._roll_die(sides))
                if not explode:
                    breakdown_parts.append(
                        f"{'+' if sign > 0 else '-'}{count}d{sides}[{', '.join(map(str, term_rolls))}]")
                total += sign * sum(term_rolls)
            else:
                sign = -1 if flat_sign == "-" else 1
                flat = int(flat_str)
                total += sign * flat
                breakdown_parts.append(f"{'+' if sign > 0 else '-'}{flat}")

        breakdown = " ".join(breakdown_parts).lstrip("+").strip()
        return f"Rolled {notation}: {breakdown} = {total}"

    def _roll_with_advantage(self, notation: str, mode: str) -> str:
        m = re.match(r"\s*(\d*)d(\d+)\s*([+-]\s*\d+)?\s*$", notation, re.IGNORECASE)
        if not m:
            return "Advantage/disadvantage only works with a single die term, e.g. '1d20 adv'."
        count = int(m.group(1)) if m.group(1) else 1
        sides = int(m.group(2))
        modifier = int(m.group(3).replace(" ", "")) if m.group(3) else 0
        if count != 1:
            return "Advantage/disadvantage rolls one die twice and keeps the better/worse - use '1d20 adv', not multiple dice."
        if sides < 2 or sides > MAX_SIDES:
            return f"Dice need between 2 and {MAX_SIDES} sides."

        roll_a, roll_b = self._roll_die(sides), self._roll_die(sides)
        kept = max(roll_a, roll_b) if mode == "advantage" else min(roll_a, roll_b)
        total = kept + modifier
        mod_text = f" {'+' if modifier >= 0 else '-'} {abs(modifier)}" if modifier else ""
        return (f"Rolled 1d{sides} with {mode}: [{roll_a}, {roll_b}] -> kept {kept}"
                f"{mod_text} = {total}")

    def flip_coin(self) -> str:
        return "Heads!" if secrets.randbelow(2) == 0 else "Tails!"
