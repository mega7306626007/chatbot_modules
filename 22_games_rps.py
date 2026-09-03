"""Section 16B: ROCK-PAPER-SCISSORS (adaptive opponent, no external ML)

Two opponent modes:
  - "random": uniform random - unbeatable by the user in expectation,
    since RPS has no exploitable structure against true randomness.
  - "smart" (default once enough history exists): builds a 2nd-order
    Markov model of the user's own move sequence (P(next move | last
    two moves)) from the actual rounds played this session, then plays
    the counter to whichever move that model finds most likely. This
    is exactly the same "predict from observed transition frequencies"
    idea as the n-gram language model elsewhere in this file, just
    applied to a 3-symbol alphabet instead of words - genuinely
    exploits any pattern a human unconsciously falls into (repeating
    their last win, cycling rock->paper->scissors, avoiding repeats,
    etc.), which real people reliably do more often than chance.
"""
import random
from collections import defaultdict, Counter


class RockPaperScissorsGame:
    MOVES = ("rock", "paper", "scissors")
    BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    COUNTERS = {v: k for k, v in BEATS.items()}  # counters[move] beats move

    MIN_HISTORY_FOR_SMART = 4  # rounds of history before the model engages

    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.history = []  # user's moves, in order
        self.mode = "auto"  # "auto", "random", or "smart"
        # transition_counts[(prev2, prev1)][next_move] = count
        self.transition_counts = defaultdict(Counter)

    def set_mode(self, mode: str) -> str:
        mode = mode.strip().lower()
        if mode not in ("auto", "random", "smart"):
            return "Mode should be 'auto', 'random', or 'smart'."
        self.mode = mode
        return f"RPS opponent mode set to '{mode}'."

    def _predict_user_move(self):
        """Returns the user's most likely next move given the last two
        moves they played, or None if there isn't enough matching
        history yet to make a prediction."""
        if len(self.history) < 2:
            return None
        key = (self.history[-2], self.history[-1])
        counts = self.transition_counts.get(key)
        if not counts:
            return None
        return counts.most_common(1)[0][0]

    def _choose_bot_move(self):
        use_smart = self.mode == "smart" or (
            self.mode == "auto" and len(self.history) >= self.MIN_HISTORY_FOR_SMART
        )
        if use_smart:
            predicted = self._predict_user_move()
            if predicted:
                return self.COUNTERS[predicted], True
        return random.choice(self.MOVES), False

    def play(self, user_move: str) -> str:
        user_move = user_move.strip().lower()
        if user_move not in self.MOVES:
            return "Play rock, paper, or scissors - e.g. 'rock'."

        bot_move, was_prediction = self._choose_bot_move()

        # record the transition BEFORE appending this move, using the
        # state that was true when the prediction was (or would have
        # been) made
        if len(self.history) >= 2:
            key = (self.history[-2], self.history[-1])
            self.transition_counts[key][user_move] += 1
        self.history.append(user_move)

        if user_move == bot_move:
            self.ties += 1
            outcome = f"I also played {bot_move} - it's a tie!"
        elif self.BEATS[user_move] == bot_move:
            self.wins += 1
            outcome = f"I played {bot_move}. You win this round!"
        else:
            self.losses += 1
            outcome = f"I played {bot_move}. I win this round!"
            if was_prediction:
                outcome += " (saw that coming)"

        return f"{outcome} (Score - you: {self.wins}, me: {self.losses}, ties: {self.ties})"

    def score_text(self) -> str:
        total = self.wins + self.losses + self.ties
        if total == 0:
            return "We haven't played rock-paper-scissors yet - say 'play rock paper scissors' to start."
        mode_note = (f" I'm adapting to your patterns after {self.MIN_HISTORY_FOR_SMART} rounds (mode: auto)."
                     if self.mode == "auto" else f" (mode: {self.mode})")
        return (f"Rock-Paper-Scissors score: you {self.wins}, me {self.losses}, "
                f"ties {self.ties} (out of {total} rounds).{mode_note}")
