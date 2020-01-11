from src.chess.chess_movement import get_moves
from src.chess.chess_consts import kings, pawns, white, material
from src.primitive import clamp, highest, lowest
from src.search import GameSearch

# Enhancements
# Static_Exchange_Evaluation https://www.chessprogramming.org/Static_Exchange_Evaluation
# Quiescence_Search https://www.chessprogramming.org/Quiescence_Search
#   see https://www.chessprogramming.org/Horizon_Effect
# Transposition Table https://www.chessprogramming.org/Transposition_Table
# Killer Heuristic https://www.chessprogramming.org/Killer_Heuristic
# Last_Best_Reply https://www.chessprogramming.org/Last_Best_Reply


def score_end(chess_state):
    if chess_state.is_done:
        return lowest if chess_state.active_color is white else highest
    else:
        return 0


def score_state(chess_state, last_move):
    if chess_state.is_done:
        return score_end(chess_state)
    else:
        # TODO make the stability assessment based on tradeoff value instead
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

    def get_key(m):
        return score_move(m, chess_state.pos(m.from_))

    return sorted(moves, key=get_key)


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


def is_winning_action(move):
    return move.victim in kings


chess_search = GameSearch(score_state, next_actions, apply_action, undo_action, score_end, is_winning_action)
