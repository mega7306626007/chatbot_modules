"""Section 4B: COUNTDOWN DASHBOARD (rule-based, layered on top of the
existing important_dates table - Section 1B/2)

Beyond the original "track several named yearly countdowns together"
feature, this adds:
  - categories/tags per countdown (e.g. "work", "personal") so the
    dashboard can be filtered - kept in an in-memory dict rather than
    a new SQLite column, since altering the shared schema is riskier
    than it's worth for a tag; it resets each session, which is
    disclosed rather than silently assumed.
  - custom-interval recurring reminders ("every 14 days starting
    2026-08-01") in addition to the existing annual-recurrence
    handling - these use modular arithmetic on days-since-start to
    find the next occurrence, since a fixed month/day (like a
    birthday) can't represent "every N days".
Both integrate into the same sorted, soonest-first dashboard view.
"""
import datetime as dt


class CountdownDashboard:
    def __init__(self, memory):
        self.memory = memory
        self._categories = {}          # label -> category string (session-only)
        self._recurring = {}           # label -> (start_date, interval_days)

    @staticmethod
    def _next_occurrence(month: int, day: int, year, today: dt.date):
        """If a year was explicitly stored, count down to that exact
        date (a one-off event, possibly in the past). Otherwise treat
        it as annual and always return the next upcoming occurrence."""
        if year:
            try:
                return dt.date(year, month, day)
            except ValueError:
                return None
        for candidate_year in (today.year, today.year + 1):
            try:
                candidate = dt.date(candidate_year, month, day)
            except ValueError:
                continue
            if candidate >= today:
                return candidate
        return None

    @staticmethod
    def _next_recurring_occurrence(start: dt.date, interval_days: int, today: dt.date):
        if interval_days <= 0:
            return None
        days_since_start = (today - start).days
        if days_since_start < 0:
            return start
        cycles_elapsed = days_since_start // interval_days
        candidate = start + dt.timedelta(days=cycles_elapsed * interval_days)
        if candidate < today:
            candidate += dt.timedelta(days=interval_days)
        return candidate

    def add(self, label: str, date: dt.date, category: str = None) -> str:
        self.memory.remember_important_date(label, date)
        if category:
            self._categories[label] = category
        cat_note = f" (category: {category})" if category else ""
        return f"Got it - I'll track '{label}' ({date.strftime('%B %-d')}){cat_note}."

    def add_recurring(self, label: str, start: dt.date, interval_days: int, category: str = None) -> str:
        if interval_days <= 0:
            return "The repeat interval needs to be at least 1 day."
        self._recurring[label] = (start, interval_days)
        if category:
            self._categories[label] = category
        cat_note = f" (category: {category})" if category else ""
        return f"Got it - I'll track '{label}' every {interval_days} days, starting {start.strftime('%B %-d, %Y')}{cat_note}."

    def remove(self, label: str) -> str:
        removed = self.memory.forget_important_date(label)
        was_recurring = self._recurring.pop(label, None) is not None
        self._categories.pop(label, None)
        if removed or was_recurring:
            return f"Removed '{label}' from your countdowns."
        return f"I didn't have a countdown called '{label}'."

    def _format_entry(self, label, occurrence, today, category=None):
        days_left = (occurrence - today).days
        if days_left == 0:
            when = "today!"
        elif days_left == 1:
            when = "tomorrow"
        elif days_left < 0:
            when = f"{abs(days_left)} days ago"
        else:
            when = f"in {days_left} days"
        cat_note = f" [{category}]" if category else ""
        return days_left, f"  - {label}{cat_note}: {occurrence.strftime('%B %-d')} ({when})"

    def dashboard(self, today: dt.date = None, category_filter: str = None) -> str:
        today = today or dt.date.today()
        entries = []

        for row in self.memory.list_important_dates():
            label, month, day, year = row["label"], row["month"], row["day"], row["year"]
            if label in self._recurring:
                continue  # recurring entries are handled below instead
            category = self._categories.get(label)
            if category_filter and category != category_filter:
                continue
            occurrence = self._next_occurrence(month, day, year, today)
            if occurrence is None:
                continue
            days_left, line = self._format_entry(label, occurrence, today, category)
            entries.append((days_left, line))

        for label, (start, interval_days) in self._recurring.items():
            category = self._categories.get(label)
            if category_filter and category != category_filter:
                continue
            occurrence = self._next_recurring_occurrence(start, interval_days, today)
            if occurrence is None:
                continue
            days_left, line = self._format_entry(label, occurrence, today, category)
            entries.append((days_left, line))

        if not entries:
            if category_filter:
                return f"No countdowns tagged '{category_filter}'."
            return "You don't have any countdowns yet - say 'countdown to <label> on <date>' to add one."

        entries.sort(key=lambda e: e[0])
        header = f"Your countdowns" + (f" tagged '{category_filter}'" if category_filter else "") + ":"
        return "\n".join([header] + [line for _, line in entries])
