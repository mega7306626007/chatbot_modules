"""Date & time engine (Section 4)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

import datetime as dt
from datetime import timezone, timedelta

# Default timezone offset (e.g., -3 for UTC-3)
DEFAULT_TZ_OFFSET = +3
DEFAULT_TZ = timezone(timedelta(hours=DEFAULT_TZ_OFFSET))

class DateTimeEngine:
    """
    Handles every date/time related question the bot can answer:
    current time, current date, day of week, days until a holiday,
    days between two dates, what day a given date falls on, etc.

    All rule-based: regex extraction of dates/holidays + plain
    datetime arithmetic. No external time/NLP libraries.
    """

    MONTH_NAMES = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December",
    }

    WEEKDAY_NAMES = {
        0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
        4: "Friday", 5: "Saturday", 6: "Sunday",
    }

    # A small built-in table of fixed-date holidays (month, day).
    # Holidays that move every year (like Thanksgiving) are intentionally
    # left out to keep the logic simple and rigid rather than guessing.
    HOLIDAYS = {
        "new year": (1, 1),
        "new years": (1, 1),
        "new year's day": (1, 1),
        "valentine's day": (2, 14),
        "valentines day": (2, 14),
        "valentine": (2, 14),
        "independence day": (7, 4),
        "halloween": (10, 31),
        "christmas": (12, 25),
        "christmas eve": (12, 24),
        "new year's eve": (12, 31),
        "new years eve": (12, 31),
    }

    @staticmethod
    def now() -> dt.datetime:
        return dt.datetime.now(DEFAULT_TZ)

    def current_time_str(self) -> str:
        now = self.now()
        return now.strftime("%I:%M %p").lstrip("0")

    def current_date_str(self) -> str:
        now = self.now()
        weekday = self.WEEKDAY_NAMES[now.weekday()]
        month = self.MONTH_NAMES[now.month]
        suffix = self._day_suffix(now.day)
        return f"{weekday}, {month} {now.day}{suffix}, {now.year}"

    def full_datetime_str(self) -> str:
        return f"{self.current_date_str()} — it's currently {self.current_time_str()}"

    @staticmethod
    def _day_suffix(day: int) -> str:
        if 11 <= day <= 13:
            return "th"
        return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    def days_until_holiday(self, holiday_key: str, today: dt.date = None):
        """Return (days_remaining, holiday_date) for the next occurrence
        of a known holiday, or None if the holiday isn't recognized.

        Accepts an optional pre-computed `today` so callers that already
        have one (e.g. resolve_date_phrase) don't force a second,
        redundant dt.datetime.now() call for what should be the same
        logical "now" within a single request.
        """
        key = holiday_key.strip().lower()
        if key not in self.HOLIDAYS:
            return None
        month, day = self.HOLIDAYS[key]
        if today is None:
            today = self.now().date()
        candidate = dt.date(today.year, month, day)
        if candidate < today:
            candidate = dt.date(today.year + 1, month, day)
        delta = (candidate - today).days
        return delta, candidate

    def day_of_week_for(self, date: dt.date) -> str:
        return self.WEEKDAY_NAMES[date.weekday()]

    @staticmethod
    def try_parse_date(text: str):
        """
        Attempt to parse a date out of free text using a handful of
        common rigid formats. Returns a datetime.date or None.
        Supported formats (deliberately limited & explicit):
          - YYYY-MM-DD
          - MM/DD/YYYY  or MM-DD-YYYY
          - "March 5 2026", "March 5, 2026", "5 March 2026"
        """
        text = text.strip()

        # YYYY-MM-DD
        m = re.search(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", text)
        if m:
            try:
                return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except ValueError:
                pass

        # MM/DD/YYYY or MM-DD-YYYY
        m = re.search(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b", text)
        if m:
            try:
                return dt.date(int(m.group(3)), int(m.group(1)), int(m.group(2)))
            except ValueError:
                pass

        # "Month D, YYYY" or "Month D YYYY"
        months_pattern = "|".join(DateTimeEngine._month_name_variants())
        m = re.search(
            rf"\b({months_pattern})\.?\s+(\d{{1,2}})(?:st|nd|rd|th)?,?\s+(\d{{4}})\b",
            text, re.IGNORECASE,
        )
        if m:
            month_num = DateTimeEngine._month_name_to_num(m.group(1))
            if month_num:
                try:
                    return dt.date(int(m.group(3)), month_num, int(m.group(2)))
                except ValueError:
                    pass

        # "D Month YYYY"
        m = re.search(
            rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+({months_pattern})\.?,?\s+(\d{{4}})\b",
            text, re.IGNORECASE,
        )
        if m:
            month_num = DateTimeEngine._month_name_to_num(m.group(2))
            if month_num:
                try:
                    return dt.date(int(m.group(3)), month_num, int(m.group(1)))
                except ValueError:
                    pass

        # Bare 4-digit year as a last resort (e.g. "born in 2000"), with
        # no month/day given. Resolves to January 1st of that year -
        # the natural default when someone says "born in <year>" rather
        # than a full date. Deliberately tried LAST and only matches a
        # standalone 4-digit number bounded by word edges, so it can't
        # accidentally eat the year portion out of a fuller date that
        # one of the patterns above should have already caught.
        m = re.search(r"\b(19|20)\d{2}\b", text)
        if m:
            try:
                return dt.date(int(m.group(0)), 1, 1)
            except ValueError:
                pass

        return None

    @staticmethod
    def _month_name_variants():
        full = list(DateTimeEngine.MONTH_NAMES.values())
        abbrev = [m[:3] for m in full]
        return full + abbrev

    @staticmethod
    def _month_name_to_num(name: str):
        name = name.strip().lower()
        for num, full in DateTimeEngine.MONTH_NAMES.items():
            if name == full.lower() or name == full[:3].lower():
                return num
        return None

    # ---- relative date parsing (fixes: tomorrow/yesterday/next <weekday>) ----

    WEEKDAY_NAME_TO_NUM = {
        "monday": 0, "mon": 0, "tuesday": 1, "tue": 1, "tues": 1,
        "wednesday": 2, "wed": 2, "thursday": 3, "thu": 3, "thurs": 3,
        "friday": 4, "fri": 4, "saturday": 5, "sat": 5, "sunday": 6, "sun": 6,
    }

    def try_parse_relative_date(self, text: str, today: dt.date = None):
        """
        Parse common relative date phrases that the original parser
        couldn't handle: 'today', 'tomorrow', 'yesterday', 'next friday',
        'last monday', 'in 5 days', '10 days from now', '5 days ago'.
        Returns a datetime.date or None if nothing relative is found.

        Accepts an optional pre-computed `today` for the same reason as
        days_until_holiday above - avoids a redundant now() call when
        the caller (resolve_date_phrase) already took one this request.
        """
        text = text.strip().lower()
        if today is None:
            today = self.now().date()

        if re.search(r"\btoday\b", text):
            return today
        if re.search(r"\btomorrow\b", text):
            return today + dt.timedelta(days=1)
        if re.search(r"\byesterday\b", text):
            return today - dt.timedelta(days=1)

        # "in N days" / "N days from now" -> future
        m = re.search(r"\bin\s+(\d+)\s+days?\b", text) or re.search(r"\b(\d+)\s+days?\s+from now\b", text)
        if m:
            return today + dt.timedelta(days=int(m.group(1)))

        # "N days ago" -> past
        m = re.search(r"\b(\d+)\s+days?\s+ago\b", text)
        if m:
            return today - dt.timedelta(days=int(m.group(1)))

        # "N weeks from now" / "in N weeks" / "N weeks ago"
        m = re.search(r"\bin\s+(\d+)\s+weeks?\b", text) or re.search(r"\b(\d+)\s+weeks?\s+from now\b", text)
        if m:
            return today + dt.timedelta(weeks=int(m.group(1)))
        m = re.search(r"\b(\d+)\s+weeks?\s+ago\b", text)
        if m:
            return today - dt.timedelta(weeks=int(m.group(1)))

        # "next <weekday>" / "last <weekday>" / "this <weekday>"
        weekday_pattern = "|".join(self.WEEKDAY_NAME_TO_NUM.keys())
        m = re.search(rf"\b(next|last|this)\s+({weekday_pattern})\b", text)
        if m:
            direction = m.group(1)
            target_weekday = self.WEEKDAY_NAME_TO_NUM[m.group(2)]
            return self._nearest_weekday(today, target_weekday, direction)

        return None

    @staticmethod
    def _nearest_weekday(today: dt.date, target_weekday: int, direction: str) -> dt.date:
        """Find the date of 'next', 'last', or 'this' occurrence of a weekday."""
        current_weekday = today.weekday()
        if direction == "next":
            days_ahead = (target_weekday - current_weekday) % 7
            days_ahead = days_ahead if days_ahead != 0 else 7
            return today + dt.timedelta(days=days_ahead)
        elif direction == "last":
            days_back = (current_weekday - target_weekday) % 7
            days_back = days_back if days_back != 0 else 7
            return today - dt.timedelta(days=days_back)
        else:  # "this"
            days_ahead = (target_weekday - current_weekday) % 7
            return today + dt.timedelta(days=days_ahead)

    def resolve_date_phrase(self, text: str):
        """
        Unified date resolver: tries relative phrases first (tomorrow,
        next friday, in 5 days, etc.), then known holiday names
        (christmas, halloween, etc.), then falls back to absolute
        calendar date parsing (2026-12-25, March 5 2026, etc.).
        Returns a datetime.date or None.

        Takes ONE now() snapshot for the whole call and threads it
        through to try_parse_relative_date/days_until_holiday, rather
        than letting each of those independently call now() again -
        previously this could call dt.datetime.now() up to 3 times for
        a single date phrase, which was both wasted work and a (very
        rare but real) correctness risk: if two of those calls landed
        on opposite sides of midnight, "today" could silently disagree
        with itself partway through resolving one phrase.
        """
        today = self.now().date()

        relative = self.try_parse_relative_date(text, today=today)
        if relative is not None:
            return relative

        holiday_key = text.strip().lower()
        if holiday_key in self.HOLIDAYS:
            result = self.days_until_holiday(holiday_key, today=today)
            if result is not None:
                return result[1]

        return self.try_parse_date(text)

    # ---- date arithmetic (fixes: "days between", "N days from a date") ------

    def days_between_dates(self, date1: dt.date, date2: dt.date) -> int:
        """Absolute number of calendar days between two dates."""
        return abs((date2 - date1).days)

    def add_days(self, date: dt.date, num_days: int) -> dt.date:
        return date + dt.timedelta(days=num_days)

    def subtract_days(self, date: dt.date, num_days: int) -> dt.date:
        return date - dt.timedelta(days=num_days)

    # ---- age calculator (fixes: "how old would i be if born on X") --------

    def calculate_age(self, birth_date: dt.date, as_of: dt.date = None) -> int:
        """
        Calculate age in whole years as of a given date (default: today).
        Correctly handles birthdays that haven't occurred yet this year,
        and leap-year birthdays (Feb 29) on non-leap years by treating
        the anniversary as having occurred once Feb 28 / Mar 1 passes.
        """
        if as_of is None:
            as_of = self.now().date()

        years = as_of.year - birth_date.year
        # Has the birthday anniversary happened yet this year?
        try:
            anniversary_this_year = birth_date.replace(year=as_of.year)
        except ValueError:
            # Feb 29 birthday on a non-leap "as_of" year -> treat as Mar 1
            anniversary_this_year = dt.date(as_of.year, 3, 1)

        if as_of < anniversary_this_year:
            years -= 1
        return years

    def days_until_next_birthday(self, birth_date: dt.date, as_of: dt.date = None) -> int:
        if as_of is None:
            as_of = self.now().date()
        try:
            next_bday = birth_date.replace(year=as_of.year)
        except ValueError:
            next_bday = dt.date(as_of.year, 3, 1)
        if next_bday < as_of:
            try:
                next_bday = birth_date.replace(year=as_of.year + 1)
            except ValueError:
                next_bday = dt.date(as_of.year + 1, 3, 1)
        return (next_bday - as_of).days

    def is_leap_year(self, year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# ==============================================================================
