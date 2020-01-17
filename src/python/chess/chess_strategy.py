from itertools import chain

from src.python.chess.chess_movement import get_moves, targeted_by
from src.python.chess.chess_consts import kings, pawns, white, material
from src.python.primitive import clamp, highest, lowest, interleave
from src.python.search import GameSearch


def score_end(chess_state):
    if chess_state.is_done:
        return chess_state.player_affinity() + (lowest if chess_state.active_color is white else highest)
    else:
        return 0


def horizon_outcome(chess_state, subject, pos):
    # At the leaf nodes need to assess if the position landed on is a good trade outcome if it's under attack,
    # this is my attempt to handle "The Horizon Effect"
    (attackers, avengers) = targeted_by(chess_state, pos)
    material_outcome = 0

    if attackers:
        enemies = sorted(attackers, key=lambda pp: abs(material[pp[1]]))
        friends = sorted(avengers, key=lambda pp: abs(material[pp[1]]))
        ordering = interleave(enemies, friends)
        avengers = list(chain(ordering, [enemies[len(friends)]]) if len(enemies) > len(friends) else ordering)
        victim = subject

        for i, (_, p) in enumerate(avengers):
            m1 = material[victim]
            m2 = material[p]
            if abs(m1) >= abs(m2) or i == len(avengers) - 1:
                material_outcome -= m1
                victim = p
            else:
                break

    return material_outcome


def score_state(chess_state, last_move):
    # "Evaluation" assess the balance of a position
    if chess_state.is_done:
        return score_end(chess_state)
    else:
        piece_moved = chess_state.pos(last_move.to_)
        penalty = 0

        # If moving a non-king (because king safety was already checked), need to assess a penalty if this
        # move results in a bad trade
        if piece_moved not in kings:
            penalty += horizon_outcome(chess_state, piece_moved, last_move.to_)

        return chess_state.material_balance + penalty


def ranking_score(move, piece):
    # This is used to guess at what a good move looks like, the better the guess the more likely to produce
    # an alphaBeta prune
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
    return sorted(moves, key=lambda m: ranking_score(m, chess_state.pos(m.from_)))


def next_actions_debug(chess_state):
    debug = []

    for m in get_moves(chess_state):
        score = ranking_score(m, chess_state.pos(m.from_))
        debug.append((score, m))

    return debug


def apply_action(chess_state, move):
    undo = chess_state.apply(move)
    return (chess_state, undo)


def undo_action(chess_state, back):
    redo = chess_state.undo(back)
    return (chess_state, redo)


chess_search = GameSearch(score_state, next_actions, apply_action, undo_action, score_end)
