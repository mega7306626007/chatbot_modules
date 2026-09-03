"""Section 16C: TIC-TAC-TOE (minimax with selectable difficulty, no ML)

Full minimax over the (tiny, 9-cell) game tree, same as before, but
now with three difficulty levels instead of one fixed unbeatable bot:
  - "easy":   plays a uniformly random legal move.
  - "medium": mostly plays optimally, but has a chance per move to
              instead play randomly (so it still blocks/wins often,
              but is beatable) - this is the standard trick for
              turning a solved game into a tunable-strength opponent
              without writing a second, weaker evaluation function.
  - "hard":   full minimax, mathematically unbeatable (best case draw).
"""
import random


class TicTacToeGame:
    DIFFICULTY_RANDOM_CHANCE = {"easy": 1.0, "medium": 0.35, "hard": 0.0}

    def __init__(self):
        self.board = [" "] * 9
        self.active = False
        self.user_symbol = "X"
        self.bot_symbol = "O"
        self.difficulty = "hard"

    def set_difficulty(self, level: str) -> str:
        level = level.strip().lower()
        if level not in self.DIFFICULTY_RANDOM_CHANCE:
            return "Difficulty should be 'easy', 'medium', or 'hard'."
        self.difficulty = level
        return f"Tic-Tac-Toe difficulty set to '{level}'."

    def start(self) -> str:
        self.board = [" "] * 9
        self.active = True
        return ("New Tic-Tac-Toe game (difficulty: " + self.difficulty + ")! "
                "You're X, I'm O. Cells are numbered 1-9 left-to-right, "
                "top-to-bottom. Say 'play 5' to take a cell.\n" + self.render())

    def render(self) -> str:
        rows = []
        for r in range(3):
            cells = [self.board[r * 3 + c] for c in range(3)]
            rows.append(" | ".join(cell if cell != " " else str(r * 3 + c + 1)
                                    for c, cell in enumerate(cells)))
        return "\n---------\n".join(rows)

    @staticmethod
    def _winner(board):
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
                 (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for a, b, c in lines:
            if board[a] != " " and board[a] == board[b] == board[c]:
                return board[a]
        if " " not in board:
            return "draw"
        return None

    def _minimax(self, board, is_bot_turn):
        winner = self._winner(board)
        if winner == self.bot_symbol:
            return 1, None
        if winner == self.user_symbol:
            return -1, None
        if winner == "draw":
            return 0, None

        best_move = None
        if is_bot_turn:
            best_score = -2
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.bot_symbol
                    score, _ = self._minimax(board, False)
                    board[i] = " "
                    if score > best_score:
                        best_score, best_move = score, i
            return best_score, best_move
        else:
            best_score = 2
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.user_symbol
                    score, _ = self._minimax(board, True)
                    board[i] = " "
                    if score < best_score:
                        best_score, best_move = score, i
            return best_score, best_move

    def _choose_bot_move(self):
        legal = [i for i in range(9) if self.board[i] == " "]
        random_chance = self.DIFFICULTY_RANDOM_CHANCE.get(self.difficulty, 0.0)
        if random_chance >= 1.0 or (random_chance > 0 and random.random() < random_chance):
            return random.choice(legal)
        _, best_move = self._minimax(self.board[:], True)
        return best_move if best_move is not None else random.choice(legal)

    def play(self, cell_number: int):
        """Returns (message, game_over, outcome) where outcome is
        'user_win' / 'bot_win' / 'draw' / None."""
        idx = cell_number - 1
        if not self.active:
            return "There's no active game - say 'play tic tac toe' to start one.", False, None
        if not (0 <= idx <= 8):
            return "Pick a cell from 1 to 9.", False, None
        if self.board[idx] != " ":
            return "That cell's taken - pick another.", False, None

        self.board[idx] = self.user_symbol
        winner = self._winner(self.board)
        if winner:
            self.active = False
            outcome = "draw" if winner == "draw" else "user_win"
            msg = ("It's a draw!" if winner == "draw" else "You win! Nicely played.") + "\n" + self.render()
            return msg, True, outcome

        bot_move = self._choose_bot_move()
        if bot_move is not None:
            self.board[bot_move] = self.bot_symbol
        winner = self._winner(self.board)
        if winner:
            self.active = False
            outcome = "draw" if winner == "draw" else "bot_win"
            msg = ("It's a draw!" if winner == "draw" else "I win this one!") + "\n" + self.render()
            return msg, True, outcome

        return self.render(), False, None
