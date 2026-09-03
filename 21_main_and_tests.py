"""Main program loop + self-test/accuracy harness (Sections 10, 15)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 10: MAIN PROGRAM LOOP
# ==============================================================================

def print_banner(bot: ChatBot):
    width = 70
    print("=" * width)
    title = f"{bot.bot_name()} - Offline Rule-Based Chatbot v{APP_VERSION}"
    print(title.center(width))
    print("=" * width)
    visit_count = bot.memory.get_visit_count()
    name = bot.user_name()
    if name and visit_count > 1:
        print(f"Welcome back, {name}! This is visit number {visit_count}.")
    elif name:
        print(f"Hello, {name}!")
    else:
        print("Hello! I don't think we've met - tell me your name any time.")
    print("Type 'help' to see what I can do, or 'quit' to exit.")
    print("-" * width)


def run_chat_loop():
    bot = ChatBot()
    print_banner(bot)

    try:
        while bot.running:
            try:
                user_input = input(f"\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\n(Session interrupted.)")
                break

            if not user_input:
                continue

            bot.logger.log("user", user_input)
            reply = bot.respond(user_input)
            bot.logger.log("bot", reply)

            print(f"\n{bot.bot_name()}: {reply}")

    finally:
        bot.memory.save()
        bot.logger.flush_to_disk()
        print("\n(Your memory and conversation log have been saved.)")


# ==============================================================================
# SECTION 15: QUALITY / ACCURACY TEST HARNESS
# ==============================================================================
#
# A real (if small) held-out test set: hand-written (message, expected_
# intent) pairs, run through the ACTUAL intent-matching pipeline
# (typo correction -> IntentEngine, same path respond() uses), with a
# genuine hit-rate reported - rather than an impression of how well
# things work. This is deliberately SEPARATE from the neural
# classifiers' own reported validation accuracy (Section 6G): those
# numbers are measured on held-out examples drawn from the SAME
# distribution as their training data (paraphrases of the same
# hand-written examples), which measures fit to that distribution, not
# real-world phrasing robustness. This harness's examples were written
# independently, specifically trying a few natural, slightly-off-
# pattern ways someone might actually phrase each request, which is a
# meaningfully different (and harder) test.
ACCURACY_TEST_CASES = [
    ("hello there", "greeting"),
    ("hey what's up", "greeting"),
    ("good morning", "greeting"),
    ("gotta go, bye", "farewell"),
    ("see you later", "farewell"),
    ("thanks a lot", "thanks"),
    ("appreciate it", "thanks"),
    ("how are you doing today", "how_are_you"),
    ("what's 15 + 27", "simple_math"),
    ("calculate 8 times 6", "simple_math"),
    ("square root of 64", "sqrt_tool"),
    ("2 to the power of 8", "power_tool"),
    ("what is 25% of 80", "percentage_tool"),
    ("tell me a joke", "tell_joke"),
    ("say something funny", "tell_joke"),
    ("give me a riddle", "tell_riddle"),
    ("tell me a story", "tell_story"),
    ("write me a haiku", "write_haiku"),
    ("what's my name", "ask_my_name"),
    ("remember that I like coffee", "remember_fact"),
    ("what time is it", "current_time"),
    ("what's today's date", "current_date"),
    ("convert 10 miles to km", "unit_convert"),
    ("convert 5 gb to mb", "unit_convert"),
    ("generate a password", "generate_password"),
    ("convert hello world to snake case", "text_case_convert"),
    ("what's the weather in Nairobi", "weather_lookup"),
    ("convert 100 usd to eur", "currency_convert"),
    ("define serendipity", "define_word"),
    ("quiz me", "flashcards_start"),
    ("draw me a red circle", "generate_image"),
    ("generate a qr code for: hello", "generate_qr_code"),
    ("what's my tone", "tone_status"),
    ("help", "help"),
    ("what can you do", "help"),
]


def run_accuracy_test(bot: "ChatBot", verbose: bool = True):
    """
    Runs every (message, expected_intent) pair in ACCURACY_TEST_CASES
    through the bot's REAL matching pipeline - IntentEngine.handle(),
    the exact same method respond() calls, not just a first-regex-match
    check - and reports a genuine hit rate, plus every miss (so
    failures are actually actionable, not just a percentage). Using
    handle() specifically (rather than checking Intent.match() in a
    loop by hand) matters: several intents are registered behind a
    broader pattern that can match first but then deliberately returns
    None to defer to a more specific intent further down the list
    (e.g. simple_math's broad "what is X" pattern falling through to
    percentage_tool) - only handle() reproduces that real fallthrough
    behavior correctly.

    NOTE: this calls real handlers, which may have real side effects
    (starting a flashcard session, appending to to-do lists, etc.) -
    fine for a diagnostic run, but don't treat this as a pure/read-only
    check if you extend the test-case list with stateful commands.
    """
    hits, misses = [], []
    for message, expected_intent in ACCURACY_TEST_CASES:
        corrected = bot.typo_corrector.correct_text(message)
        bot.engine.last_matched_intent = None
        bot.engine.handle(corrected, bot)
        matched_intent = bot.engine.last_matched_intent
        if matched_intent == expected_intent:
            hits.append((message, expected_intent))
        else:
            misses.append((message, expected_intent, matched_intent))

    total = len(ACCURACY_TEST_CASES)
    hit_rate = len(hits) / total if total else 0.0

    if verbose:
        print(f"Accuracy test: {len(hits)}/{total} ({hit_rate:.0%})")
        if misses:
            print("Misses:")
            for message, expected, got in misses:
                print(f"  {message!r}: expected '{expected}', matched '{got}'")

    return {"hit_rate": hit_rate, "total": total, "hits": len(hits), "misses": misses}


def scan_for_typo_collisions(sample_size: int = 3000) -> list:
    """
    Proactively hunts for the exact class of bug that kept surfacing
    by accident during development (blur->blue, world->would,
    back->black, test->text): a legitimate word sitting at edit-
    distance 1 from an unrelated word in COMMON_WORDS, which the
    edit-distance fallback then "corrects" into. For every word in
    COMMON_WORDS, generates all single-character-substitution
    neighbors and checks whether any of them ALSO sit in COMMON_WORDS -
    if so, that pair is a genuine ambiguity: typing either word risks
    being silently rewritten into the other. Returns a list of
    (word_a, word_b) collision pairs. Capped at sample_size candidate
    words purely to bound runtime on this being an O(n * word_length *
    26) scan; COMMON_WORDS is currently well under that cap, so in
    practice the whole list gets checked.
    """
    tc = TypoCorrector()
    words = sorted(tc._known_words)[:sample_size]
    word_set = set(words)
    collisions = []
    seen_pairs = set()

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for word in words:
        for i in range(len(word)):
            for letter in alphabet:
                if letter == word[i]:
                    continue
                candidate = word[:i] + letter + word[i + 1:]
                if candidate in word_set and candidate != word:
                    pair = tuple(sorted((word, candidate)))
                    if pair not in seen_pairs:
                        seen_pairs.add(pair)
                        collisions.append(pair)
    return collisions


def format_typo_collision_report(collisions: list) -> str:
    if not collisions:
        return "No edit-distance-1 collisions found in the known-words list."
    lines = [f"Found {len(collisions)} potential typo-correction collision(s):"]
    for word_a, word_b in collisions[:40]:
        lines.append(f"  '{word_a}' <-> '{word_b}'")
    if len(collisions) > 40:
        lines.append(f"  ...and {len(collisions) - 40} more.")
    return "\n".join(lines)


def run_self_test():
    """
    A lightweight, offline smoke test you can run with:
        python chatbot.py --test
    Exercises the main code paths without requiring interactive input,
    useful for quickly verifying the IDE setup works end to end.
    """
    print("Running self-test (no interactive input required)...\n")
    bot = ChatBot()

    test_inputs = [
        "hello",
        "my name is Jordan",
        "what's my name",
        "my favorite color is teal",
        "what's my favorite color",
        "what do you know about me",
        "what time is it",
        "what's the date",
        "how many days until christmas",
        "what day is 2026-12-25",
        "what day is tomorrow",
        "what day is next friday",
        "how many days between 2026-01-01 and 2026-12-25",
        "what date is 10 days after 2026-01-01",
        "how old would i be if born on 2000-01-01",
        "is 2024 a leap year",
        "tell me a fantasy story",
        "write a haiku about the ocean",
        "write an acrostic for Jordan",
        "write a poem about love",
        "what is 12 * 4",
        "tell me a joke",
        "tell me a quote",
        "tell me a riddle",
        "give me a trivia question",
        "count the words in: a quick brown fox",
        "is: racecar a palindrome",
        "reverse text: hello world",
        "pig latin: hello world",
        "is 17 prime",
        "factorial of 5",
        "first 10 fibonacci",
        "spell out 1234",
        "convert 10 miles to km",
        "describe these numbers: 1, 2, 3, 4, 100",
        "add buy milk to my to-do list",
        "remind me to call the dentist",
        "show my to-do list",
        "mark 1 as done",
        "cluster my to-do list",
        "play hangman",
        "show stats",
        "search my memory for color",
        "mood forecast",
        "weather in Nairobi",
        "convert 100 USD to EUR",
        "online trivia",
        "what's in the news",
        "color palette of: /nonexistent.png",
        "draw me a red circle",
        "generate an image of a blue hexagon",
        "what color is the shape in: /nonexistent.png",
        "generate a qr code for: hello world",
        "style transfer: /nonexistent.png with /nonexistent.png",
        "sha256 hash of: hello",
        "base64 encode: hello world",
        "validate this json: {\"a\": 1}",
        "extract entities from: email bob@example.com or visit https://example.com",
        "what would you retrieve for: my favorite things",
        "heyyy what's up lol",
        "what's my tone",
        "run the accuracy test",
        "scan for typo collisions",
        "square root of 81",
        "convert 5 gb to mb",
        "generate a password",
        "convert my Variable Name to snake case",
        "what were we discussing before that",
        "quiz me",
        "flashcard progress",
        "count objects in: /nonexistent.png",
        "check contrast of: /nonexistent.png",
        "define: serendipity",
        "detect text in: /nonexistent.png",
        "visualize my embeddings",
        "ml backends status",
        "find duplicate facts",
        "tool call demo",
        "predict next word after: how are",
        "continue this: hello",
        "summarize this conversation",
        "thank you",
        "are you an ai",
        "this is total gibberish asdkj zzxy nonsense",
        "bye",
    ]

    for line in test_inputs:
        print(f"You: {line}")
        bot.logger.log("user", line)
        reply = bot.respond(line)
        bot.logger.log("bot", reply)
        print(f"{bot.bot_name()}: {reply}\n")

    bot.memory.save()
    bot.logger.flush_to_disk()
    print("Self-test complete - no exceptions were raised.\n")

    print("--- Section 15: accuracy test harness ---")
    run_accuracy_test(bot)
    print()
    print("--- Section 15: typo-collision scan ---")
    collisions = scan_for_typo_collisions()
    print(format_typo_collision_report(collisions))


if __name__ == "__main__":
    if "--test" in sys.argv:
        run_self_test()
    elif "--text" in sys.argv:
        run_chat_loop()
    elif "--gui" in sys.argv or KIVY_AVAILABLE:
        # BUGFIX: this used to only launch the Kivy window when
        # "--gui" was explicitly passed on the command line. Tapping
        # Pydroid 3's plain Run button passes NO arguments at all, and
        # there's no easy way to add one from the main editor screen -
        # so in practice the graphical window was NEVER reachable this
        # way, and every run silently fell through to the bare-bones
        # text chat loop instead (which is also almost certainly why
        # this seemed far simpler than everything actually built into
        # it). Now: if Kivy is installed, the GUI opens BY DEFAULT with
        # no flags needed. Pass --text explicitly if the plain terminal
        # chat is what you actually want instead.
        run_gui()
    else:
        run_chat_loop()
