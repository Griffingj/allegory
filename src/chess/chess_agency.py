from copy import deepcopy

from src.chess.chess_movement import get_moves
from src.chess.chess_consts import material, kings, pawns, white
from src.search import lowest, highest, GameSearch
from src.chess.chess_state import initial_state
from src.primitive import clamp

# Enhancements
# Static_Exchange_Evaluation https://www.chessprogramming.org/Static_Exchange_Evaluation
# Quiescence_Search https://www.chessprogramming.org/Quiescence_Search
#   see https://www.chessprogramming.org/Horizon_Effect
# Transposition Table https://www.chessprogramming.org/Transposition_Table
# Killer Heuristic https://www.chessprogramming.org/Killer_Heuristic
# Last_Best_Reply https://www.chessprogramming.org/Last_Best_Reply


def score_state(chess_state):
    # Enhancements https://www.chessprogramming.org/Evaluation#2015_...
    return chess_state.material_balance


def score_move(move, piece):
    bonus_co = 11
    penalty_co = 0.9

    base_score = 100 if piece in kings or piece in pawns else 200

    if move.castle is not None:
        base_score *= bonus_co

    if move.victim is not None or move.ept_cap is not None:
        p_material = abs(material[piece])
        v_material = abs(material[move.victim or move.ept_cap[1]])
        base_score *= ((clamp(0, v_material - p_material) + 100) / 500 + bonus_co)

    if move.new_castling_available:
        base_score *= penalty_co

    return -base_score


def next_actions(chess_state):
    moves = get_moves(chess_state)
    return sorted(moves, key=lambda m: score_move(m, chess_state.pos(m.from_)))


def next_actions_debug(chess_state):
    debug = []

    for m in get_moves(chess_state):
        score = score_move(m, chess_state.pos(m.from_))
        debug.append((score, m))

    return debug


def apply_action(chess_state, move):
    undo = chess_state.apply(move)
    return (chess_state, undo)


def undo_action(chess_state, back):
    redo = chess_state.undo(back)
    return (chess_state, redo)


def is_last_action(move):
    return move.victim in kings


def score_end(chess_state):
    return highest if chess_state.active_color is white else lowest


class Diag():
    def __init__(self):
        self.counts = dict()
        self.history = []
        self.info = {
            "donePaths": []
        }

    def count(self, key):
        self.counts[key] = self.counts.get(key, 0) + 1


class ChessAgent():
    def __init__(self, search_depth):
        self.game_search = GameSearch(score_state, next_actions, apply_action, undo_action, score_end, is_last_action)
        self.search_depth = search_depth
        self.best_move = dict()
        self.diag = Diag()

    def start_game(self, state=initial_state):
        self.game = deepcopy(state)
        return self.search()

    def search(self):
        search_basis = deepcopy(self.game)
        (ab, move) = self.game_search.alpha_beta_enh(search_basis, self.diag, self.search_depth)
        self.best_move[self.game.to_fen()] = move
        print({
            "bestMove": self.best_move,
            "counts": self.diag.counts,
            "donePaths": self.diag.info["donePaths"]
        })
        return move

    def apply(self, move):
        self.game.apply(move)
