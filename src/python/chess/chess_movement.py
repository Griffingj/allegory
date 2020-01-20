from itertools import cycle
from collections import namedtuple

from src.python.chess.chess_consts import black_pieces, white_pieces, pawns, knights, bishops, rooks, queens,\
    kings, white, white_castling, black_castling, castling_block, castling_check, castling_rooks, white_pinners,\
    black_pinners, pinners, not_pawns_l

from src.python.primitive import subtract, intersect

from src.python.vector2 import is_shared_cardinal, is_shared_diag, is_shared_union_jack, v2_range, difference, v2_abs

# all 2d coords are in (y, x) form where positive y is down (from white's perspective),
# this is to ease working with 2d array board representation
# e.g. (0, 0) -> a8; (0, 7) -> h8; (7, 0) -> a1; (7,7) -> h1
knight_o = {
    (-2, -1), (-1, -2), (1, -2), (2, -1),
    (-2,  1), (-1,  2), (1,  2), (2,  1)
}

# unit grid right, up, left, down
cardinal = {
    (0, 1), (-1, 0), (0, -1), (1, 0)
}
cardinal_dir = cycle(cardinal)

dir_left_right = {
    -1, 1
}

# unit grid NE, NW, SW, SE
diag = {
    (-1, 1), (-1, -1), (1, -1), (1, 1)
}
diag_dir = cycle(diag)

# Queens/Kings
omni = cardinal.union(diag)
omni_dir = cycle(omni)

# maximum number of spaces to check to cover all possible board offsets for bishops and rooks
four_ray_iter = [range(1, 8)] * 4

# maximum number of spaces to check to cover all possible board offsets for queens
eight_ray_iter = [range(1, 8)] * 8

Move = namedtuple("Move", [
    "from_",
    "to_",
    "victim",
    "new_en_passant_target",
    "ept_cap",
    "new_castling_available",
    "castle"
], defaults=(None, None, None, None, None, None, None))

abs_unit_d = {
    (1, 1), (0, 1), (1, 0)
}

abs_unit_one = (1, 1)

empty_set = set()

is_in_ray = {
    "q": is_shared_union_jack,
    "Q": is_shared_union_jack,
    "r": is_shared_cardinal,
    "R": is_shared_cardinal,
    "b": is_shared_diag,
    "B": is_shared_diag
}

bishops_rooks_queens = bishops | rooks | queens
knights_kings = knights | kings


def in_board(v2):
    return v2[0] >= 0 and v2[0] <= 7 and v2[1] >= 0 and v2[1] <= 7


def is_attacked_by(chess_state, pos, attacker_pos, enemies_only=True, ignored=empty_set):
    (i, j) = pos
    attacker = chess_state.pos(attacker_pos)
    friends = white_pieces if chess_state.active_color == white else black_pieces

    if attacker is None or pos == attacker_pos or (enemies_only and attacker in friends):
        return False
    elif attacker in pawns:
        diff = difference(pos, attacker_pos)

        if enemies_only:
            fwd_dir = -1 if chess_state.active_color == white else 1
            return fwd_dir == -diff[0] and v2_abs(diff) == abs_unit_one
        else:
            return v2_abs(diff) == abs_unit_one
    elif attacker in pinners:
        if is_in_ray[attacker]([pos, attacker_pos]):
            for i_pos in v2_range(pos, attacker_pos):
                if i_pos in ignored:
                    continue
                if chess_state.pos(i_pos) is not None:
                    return False
            return True
        else:
            return False
    elif attacker in knights:
        abs_diff = v2_abs(difference(pos, attacker_pos))
        return 2 == abs_diff[0] * abs_diff[1]
    elif attacker in kings:
        return v2_abs(difference(pos, attacker_pos)) in abs_unit_d


def is_attacked(chess_state, pos, ignored=empty_set):
    (i, j) = pos
    pinners = black_pinners if chess_state.active_color == white else white_pinners
    enemy_knights = "n" if chess_state.active_color == white else "N"
    enemy_king = "k" if chess_state.active_color == white else "K"
    enemy_pawns = "p" if chess_state.active_color == white else "P"
    fwd_dir = -1 if chess_state.active_color == white else 1

    for d in dir_left_right:
        to = (i + fwd_dir, j + d)

        if in_board(to):
            p = chess_state.pos(to)

            if p is not None and p in enemy_pawns:
                return True

    for piece in pinners | set(enemy_knights + enemy_king):
        for a_pos in chess_state.positions[piece]:
            if is_attacked_by(chess_state, pos, a_pos, True, ignored):
                return True
    return False


def targeted_by(chess_state, pos):
    (i, j) = pos
    enemies = white_pieces if chess_state.active_color == white else black_pieces
    enemy_pawn = "p" if chess_state.active_color == white else "P"
    friend_pawn = "P" if chess_state.active_color == white else "p"
    fwd_dir = -1 if chess_state.active_color == white else 1
    enemy_targeters = []
    friendly_targeters = []
    # Preserve order of piece assessment so that attacker lists are sorted from least material to greatest
    # this avoids the need to sort the lists when used for trade off scoring

    for piece in not_pawns_l:
        for attack_pos in chess_state.positions[piece]:
            if is_attacked_by(chess_state, pos, attack_pos, False):
                attacker = chess_state.pos(attack_pos)
                if attacker in enemies:
                    enemy_targeters.append((attack_pos, attacker))
                else:
                    friendly_targeters.append((attack_pos, attacker))

    for vert_o in dir_left_right:
        for horz_o in dir_left_right:
            to = (i + vert_o, j + horz_o)

            if in_board(to):
                attacker = chess_state.pos(to)

                if attacker is not None:
                    if attacker in enemy_pawn and vert_o == fwd_dir:
                        enemy_targeters.append((to, enemy_pawn))
                    elif attacker in friend_pawn and vert_o != fwd_dir:
                        friendly_targeters.append((to, friend_pawn))

    return (enemy_targeters, friendly_targeters)


def get_moves(chess_state):
    # all 2d coords are in (y, x) form where positive y is down, this is to ease working with 2d array
    # board representation

    # Short hand
    # i -> row, 2d array first dimension i, reverse rank ascending down, [0, 7]
    # j -> column, 2d array second dimension i, file as number ascending left to right, [0, 7]
    # ept -> en passant target, from opponents move prior if available
    # ca -> castling availability

    enemy_pieces = black_pieces if chess_state.active_color == white else white_pieces
    friendly_pieces = white_pieces if chess_state.active_color == white else black_pieces
    color_castling = white_castling if chess_state.active_color == white else black_castling
    moves = []
    ca = "" if chess_state.castling_available is None else intersect(chess_state.castling_available, color_castling)

    for piece in chess_state.positions:
        if piece in enemy_pieces:
            continue

        for from_ in chess_state.positions[piece]:
            (i, j) = from_

            if piece in pawns:
                forward = -1 if chess_state.active_color == white else 1
                i_tar = i + forward
                short_to = (i_tar, j)

                if in_board(short_to) and chess_state.board[i_tar][j] is None:
                    moves.append(Move(from_, short_to))

                    # Pawn "leap" move
                    leap_file = 6 if chess_state.active_color == white else 1

                    if i == leap_file and chess_state.board[i_tar + forward][j] is None:
                        to = (i_tar + forward, j)
                        moves.append(Move(from_, to, None, short_to))

                # Attacks
                for left_right in dir_left_right:
                    j_tar = j + 1 * left_right
                    to = (i_tar, j_tar)

                    if in_board(to):
                        victim = chess_state.board[i_tar][j_tar]

                        if to == chess_state.en_passant_target:
                            ep_victim = chess_state.board[i][j_tar]
                            ept_cap = (to, ep_victim)
                            moves.append(Move(from_, to, None, None, ept_cap))

                        elif victim in enemy_pieces:
                            moves.append(Move(from_, to, victim))

            # Fixed offset assessment (knights, kings)
            elif piece in knights_kings:
                offsets = knight_o if piece in knights else omni
                new_ca = subtract(ca, color_castling)
                ca_to = "-" if new_ca is not None and len(new_ca) == 0 else new_ca

                for (i_offset, j_offset) in offsets:
                    i_tar = i_offset + i
                    j_tar = j_offset + j
                    to = (i_tar, j_tar)

                    if in_board(to):
                        victim = chess_state.board[i_tar][j_tar]

                        if victim not in friendly_pieces:
                            if piece in kings:
                                # Castle invalidation if king moves
                                moves.append(Move(from_, to, victim, None, None, ca_to))
                            else:
                                moves.append(Move(from_, to, victim))

                # Castling for kings
                if piece in kings and len(ca):
                    # Can't castle out of check
                    if is_attacked(chess_state, from_):
                        continue

                    for castling_key in ca:
                        # Can't castle if any of the positions between king and rook are occupied
                        for (p_i, p_j) in castling_block[castling_key]:
                            if chess_state.board[p_i][p_j] is not None:
                                break
                        else:
                            # Can't castle if the king moves through a space that is attacked
                            for pos in castling_check[castling_key]:
                                if is_attacked(chess_state, pos, set([from_])):
                                    break
                            else:
                                new_ca = subtract(chess_state.castling_available, color_castling)
                                to = None

                                if castling_key == "K":
                                    to = (7, 6)
                                elif castling_key == "Q":
                                    to = (7, 2)
                                elif castling_key == "k":
                                    to = (0, 6)
                                else:
                                    to = (0, 2)

                                ca_to = "-" if len(new_ca) == 0 else new_ca
                                moves.append(Move(from_, to, None, None, None, ca_to, castling_key))

            # Radiance style move assessment (Rooks, Bishops, Queens)
            elif piece in bishops_rooks_queens:
                dir_itr = diag_dir if piece in bishops else (cardinal_dir if piece in rooks else omni_dir)
                ray_itr = eight_ray_iter if piece in queens else four_ray_iter

                for ray in ray_itr:
                    (i_dir, j_dir) = next(dir_itr)

                    for distance in ray:
                        i_tar = i_dir * distance + i
                        j_tar = j_dir * distance + j
                        to = (i_tar, j_tar)

                        if in_board(to):
                            victim = chess_state.board[i_tar][j_tar]
                            friendly = victim in friendly_pieces

                            if not friendly:
                                new_ca = None

                                # Castle invalidation if rook, can't castle with a rook that has moved
                                if piece in rooks:
                                    for castling_key in ca:
                                        if castling_rooks[castling_key] == from_:
                                            new_ca = subtract(ca, castling_key)

                                ca_to = "-" if new_ca is not None and len(new_ca) == 0 else new_ca
                                moves.append(Move(from_, to, victim, None, None, ca_to))

                                if victim is not None:
                                    break

                            elif friendly:
                                break
                        else:
                            break
    return moves
