#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Pydroid run kivy
"""
main.py - application entry point.

Per the "modularize your massive file" advice: this file now contains
ONLY startup/orchestration. All the actual logic lives in the numbered
files in this same folder (01_config_and_db.py ... 21_main_and_tests.py)
plus response_banks/ (the old Section 8 response-bank data, further
split into its own subfolder since it was ~41,000 of the original
~61,000 lines on its own).

WHY A LOADER INSTEAD OF PLAIN IMPORTS:
The original file was one shared global namespace end-to-end - classes
in Section 9 reference classes from Section 6G, response handlers
reference response-bank dicts from Section 8, etc., with no imports
because they never needed any. Splitting that into fully independent
modules would require hand-tracing every one of those cross-references
across 60k+ lines, which is exactly the kind of change likely to
silently break something. So instead, this loader execs every file, in
the SAME order the original monolith defined things in, into one shared
namespace - every existing cross-reference keeps working unmodified,
while each file on disk is now small enough to open, scroll, and edit
in Pydroid 3 without lag. Run with `python main.py`, `--test`, or
`--gui` exactly as before.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))

_MODULE_FILES = [
    "01_config_and_db.py",
    "02_memory_and_logging.py",
    "03_datetime_engine.py",
    "04_creative_writing.py",
    "05_fun_extras.py",
    "06_text_number_tools.py",
    "07_continuity_and_tone.py",
    "08_hangman.py",
    "09_sklearn_tools.py",
    "10_neural_networks.py",
    "32_deep_networks.py",
    "11_llm_hybrid.py",
    "12_intent_engine.py",
    # New feature modules - must load before 14_chatbot_core.py, which
    # instantiates them in ChatBot.__init__.
    "22_games_rps.py",
    "23_games_tictactoe.py",
    "24_dice_and_coin.py",
    "25_cipher_tools.py",
    "26_billsplit_tip.py",
    "27_name_generator.py",
    "28_ascii_art.py",
    "29_markdown_table.py",
    "30_countdown_dashboard.py",
    "31_word_games.py",
    # 13_response_banks_loader.py handled separately below (it loads a
    # whole subfolder, not a single file)
    "14_chatbot_core.py",
    "15_gui_kivy.py",
    "16_vision.py",
    "17_api_connectors.py",
    "18_qr_code.py",
    "19_tool_calling.py",
    "20_language_models.py",
    "21_main_and_tests.py",
]


def _load_all():
    """Execs every module file, in original order, into one shared
    namespace (this dict), then returns it. This dict ends up holding
    every class/function/constant the original single file defined."""
    shared_globals = {"__name__": "__main__", "__file__": __file__}

    for fname in _MODULE_FILES:
        # response bank data loads right after the intent engine and
        # before the main ChatBot class, matching the original
        # Section 7C -> Section 8 -> Section 9 order
        if fname == "14_chatbot_core.py":
            loader_path = os.path.join(_HERE, "13_response_banks_loader.py")
            with open(loader_path, "r", encoding="utf-8") as f:
                loader_code = compile(f.read(), loader_path, "exec")
            loader_ns = {"__file__": loader_path}
            exec(loader_code, loader_ns)
            loader_ns["load_response_banks"](shared_globals)

        path = os.path.join(_HERE, fname)
        with open(path, "r", encoding="utf-8") as f:
            code = compile(f.read(), path, "exec")
        exec(code, shared_globals)

    return shared_globals


if __name__ == "__main__":
    # 21_main_and_tests.py already contains the original
    # `if __name__ == "__main__": ...` dispatch (--test / --gui / chat
    # loop) verbatim, and it runs inside shared_globals where
    # __name__ == "__main__", so it fires automatically as part of the
    # exec below - no extra dispatch code needed here.
    _load_all()
pip