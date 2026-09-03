"""Hangman mini-game (Section 6E)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 6E: HANGMAN MINI-GAME
# ==============================================================================

class HangmanGame:
    """
    A complete, self-contained Hangman game state machine. The bot holds
    one HangmanGame instance per session; calling start() begins a new
    round, and guess_letter() advances the game one turn at a time.

    This is a rigid turn-based state machine - no AI opponent, no
    learning, just word lists and a fixed set of game rules.
    """

    MAX_WRONG_GUESSES = 6

    WORD_BANK = {
        "easy": ["python", "code", "robot", "music", "happy", "river",
                  "cloud", "tiger", "ocean", "smile", "plant", "stone"],
        "medium": ["chatbot", "keyboard", "function", "variable", "asteroid",
                   "mountain", "elephant", "sandwich", "calendar", "umbrella"],
        "hard": ["algorithm", "dictionary", "philosophy", "constellation",
                 "refactoring", "encyclopedia", "metamorphosis", "hieroglyphics"],
    }

    HANGMAN_STAGES = [
        "  +---+\n      |\n      |\n      |\n     ===",
        "  +---+\n  O   |\n      |\n      |\n     ===",
        "  +---+\n  O   |\n  |   |\n      |\n     ===",
        "  +---+\n  O   |\n /|   |\n      |\n     ===",
        "  +---+\n  O   |\n /|\\  |\n      |\n     ===",
        "  +---+\n  O   |\n /|\\  |\n /    |\n     ===",
        "  +---+\n  O   |\n /|\\  |\n / \\  |\n     ===",
    ]

    def __init__(self):
        self.active = False
        self.word = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.difficulty = "medium"

    def start(self, difficulty: str = "medium") -> str:
        difficulty = difficulty if difficulty in self.WORD_BANK else "medium"
        self.difficulty = difficulty
        self.word = random.choice(self.WORD_BANK[difficulty]).lower()
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.active = True
        return self.render()

    def render(self) -> str:
        display_word = " ".join(
            letter if letter in self.guessed_letters else "_" for letter in self.word
        )
        stage_idx = min(self.wrong_guesses, len(self.HANGMAN_STAGES) - 1)
        hangman_art = self.HANGMAN_STAGES[stage_idx]
        guessed_str = ", ".join(sorted(self.guessed_letters)) if self.guessed_letters else "(none yet)"
        remaining = self.MAX_WRONG_GUESSES - self.wrong_guesses
        return (
            f"{hangman_art}\n\n"
            f"Word: {display_word}\n"
            f"Guessed letters: {guessed_str}\n"
            f"Wrong guesses remaining: {remaining}"
        )

    def guess_letter(self, letter: str):
        """
        Process one guessed letter. Returns a tuple:
            (message: str, game_over: bool, won: bool)
        """
        if not self.active:
            return "There's no active game - say 'play hangman' to start one!", True, False

        letter = letter.strip().lower()
        if len(letter) != 1 or not letter.isalpha():
            return "Please guess a single letter.", False, False

        if letter in self.guessed_letters:
            return f"You already guessed '{letter}'. Try a different letter.", False, False

        self.guessed_letters.add(letter)

        if letter not in self.word:
            self.wrong_guesses += 1

        won = all(ch in self.guessed_letters for ch in self.word)
        lost = self.wrong_guesses >= self.MAX_WRONG_GUESSES

        message = self.render()

        if won:
            self.active = False
            message += f"\n\nYou won! The word was '{self.word}'."
            return message, True, True
        if lost:
            self.active = False
            message += f"\n\nYou ran out of guesses. The word was '{self.word}'."
            return message, True, False

        return message, False, False

    def guess_word(self, guess: str):
        """Process a full-word guess. Same return signature as guess_letter."""
        if not self.active:
            return "There's no active game - say 'play hangman' to start one!", True, False

        guess = guess.strip().lower()
        if guess == self.word:
            self.guessed_letters.update(self.word)
            self.active = False
            return f"{self.render()}\n\nYou won! The word was '{self.word}'.", True, True

        self.wrong_guesses += 1
        if self.wrong_guesses >= self.MAX_WRONG_GUESSES:
            self.active = False
            return f"{self.render()}\n\nYou ran out of guesses. The word was '{self.word}'.", True, False

        return f"That's not the word. {self.render()}", False, False


# ==============================================================================
