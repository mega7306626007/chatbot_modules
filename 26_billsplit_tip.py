"""Section 3K: TIP CALCULATOR & BILL SPLITTER (single-function, no eval())

Same philosophy as the existing scientific calculator: one rigid
pattern per operation, plain arithmetic, no eval() of arbitrary
expressions.

Two modes:
  - even split: one bill total, tip %, split N ways evenly.
  - itemized split: each person's own item subtotal, tip % applied
    proportionally to each person's share of the pre-tip bill (so
    someone who ordered more pays proportionally more of the tip too,
    not an equal share of it) - this is how tip splitting is actually
    supposed to work when people order unevenly, and is meaningfully
    more work than dividing one number by N.
"""


class TipCalculator:
    @staticmethod
    def calculate(bill: float, tip_percent: float, num_people: int = 1, round_up: bool = False) -> str:
        if bill < 0 or tip_percent < 0:
            return "Bill amount and tip percent should both be zero or positive."
        if num_people < 1:
            return "Number of people to split between should be at least 1."

        tip = bill * (tip_percent / 100)
        total = bill + tip
        per_person = total / num_people
        if round_up:
            import math
            per_person = math.ceil(per_person * 100) / 100

        lines = [
            f"Bill: {bill:.2f}",
            f"Tip ({tip_percent:g}%): {tip:.2f}",
            f"Total: {total:.2f}",
        ]
        if num_people > 1:
            lines.append(f"Split {num_people} ways: {per_person:.2f} each" +
                         (" (rounded up)" if round_up else ""))
        return "\n".join(lines)

    @staticmethod
    def calculate_itemized(items: dict, tip_percent: float) -> str:
        """items: {person_name: their_subtotal_before_tip}. Each
        person's tip is proportional to their share of the bill, so
        the total tip still equals bill_total * tip_percent."""
        if tip_percent < 0:
            return "Tip percent should be zero or positive."
        if not items:
            return "I need at least one person's item subtotal to split the bill."
        if any(v < 0 for v in items.values()):
            return "Item subtotals should all be zero or positive."

        bill_total = sum(items.values())
        if bill_total == 0:
            return "Everyone's subtotal is 0 - nothing to split."

        lines = [f"Bill total: {bill_total:.2f}  |  Tip: {tip_percent:g}%"]
        grand_total = 0.0
        for name, subtotal in items.items():
            share = subtotal / bill_total
            person_tip = bill_total * (tip_percent / 100) * share
            person_total = subtotal + person_tip
            grand_total += person_total
            lines.append(f"  {name}: subtotal {subtotal:.2f} + tip {person_tip:.2f} = {person_total:.2f}")
        lines.append(f"Grand total: {grand_total:.2f}")
        return "\n".join(lines)
