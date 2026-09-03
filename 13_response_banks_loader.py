"""
Section 8 loader: loads every response-bank data file, in original order,
into the SAME shared namespace the rest of the modules run in.

WHY THIS EXISTS / HONEST DESIGN NOTE:
The original chatbot.py was a single 61k-line file where every class and
every response-bank dict lived in one shared global namespace, so any
piece of code could reference any other by name with no imports needed.
Cleanly separating that into fully independent, individually-importable
modules would mean tracing every cross-reference between ~60 sections by
hand across tens of thousands of lines - realistically infeasible to do
correctly in one pass without silently breaking something.

Instead, this split keeps the SAME shared-namespace execution model, but
physically moves the code into ~30 separate, much smaller files, each
independently readable/editable in Pydroid 3 (or any editor). main.py
loads every file below IN THE SAME ORDER as the original monolith, into
one shared dict, so every cross-reference that used to work still works
- nothing needed to be manually rewired, and nothing had to be guessed.
This is a real, meaningful modularization for the actual pain point (an
editor choking on one giant file); it is NOT a refactor into decoupled,
independently-importable packages - that would be a much larger, higher
-risk follow-up project, not something to bolt on top of a bug fix.
"""
import os

_BANK_FILES = [
    "01_core_response_banks.py",
    "02_ext1.py",
    "03_ext2.py",
    "04_ext3_casual.py",
    "05_ext4_sheng.py",
    "06_ext5.py",
    "07_ext6.py",
    "08_ext7.py",
    "09_ext8.py",
    "10_ext9.py",
    "11_ext10.py",
    "12_topic_launcher_aliases.py",
]


def load_response_banks(shared_globals):
    """Execs every response-bank file, in order, into shared_globals."""
    here = os.path.dirname(os.path.abspath(__file__))
    bank_dir = os.path.join(here, "response_banks")
    for fname in _BANK_FILES:
        path = os.path.join(bank_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            code = compile(f.read(), path, "exec")
        exec(code, shared_globals)
