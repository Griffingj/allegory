from copy import deepcopy

from src.chess.chess_state import initial_state
from src.chess.chess_strategy import chess_search


class Diag():
    def __init__(self):
        self.counts = dict()
        self.info = {
            "donePath": None
        }

    def count(self, key):
        self.counts[key] = self.counts.get(key, 0) + 1


class ChessAgent():
    def __init__(self, search_depth):
        self.chess_search = chess_search
        self.search_depth = search_depth
        self.best_move = dict()
        self.diag = Diag()

    def start_game(self, state=initial_state):
        self.game = deepcopy(state)
        return self.search()

    def search(self):
        search_basis = deepcopy(self.game)
        self.diag.info["longestPath"] = 0

        (ab, best_path) = self.chess_search.alpha_beta_enh_r(
            search_basis,
            self.search_depth,
            self.search_depth,
            self.diag
        )
        print({
            "counts": self.diag.counts,
            "donePath": self.diag.info["donePath"]
        })
        return reversed(best_path)

    def apply(self, move):
        self.game.apply(move)
