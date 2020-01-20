from copy import deepcopy

from src.python.chess.chess_state import initial_state
from src.python.chess.chess_strategy import chess_search


class Diag():
    def __init__(self):
        self.counts = dict()

    def count(self, key, num=1):
        self.counts[key] = self.counts.get(key, 0) + num


class ChessAgent():
    def __init__(self, search_depth):
        self.chess_search = chess_search
        self.search_depth = search_depth
        self.diag = Diag()

    def start_game(self, state=initial_state):
        self.game = state
        return self.search()

    def stop(self):
        self.chess_search.stop()

    def search(self):
        search_basis = deepcopy(self.game)
        self.chess_search.stop(False)

        (balance, best_path) = self.chess_search.alpha_beta(
            search_basis,
            self.search_depth,
            None,
            self.diag
        )
        return (balance, reversed(best_path))
