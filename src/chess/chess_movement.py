from itertools import cycle
from collections import namedtuple

from src.chess.chess_consts import b_range, black_pieces, white_pieces, pawns, knights, bishops, rooks, queens, kings,\
    white, white_castling, black_castling, castling_block, castling_check, castling_rooks

from src.primitive import subtract, intersect

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
    # "attacking",  # TODO add this stuff back and use for calcs
    # "defending",
    # "attacked_by",
    # "promotion",
    "new_en_passant_target",
    "ept_cap",
    "new_castling_available",
    "castle"
], defaults=(None, None, None, None, None, None, None))


def is_attacked(chess_state, pos):
    (i, j) = pos
    friendly_pieces = white_pieces if chess_state.active_color == white else black_pieces

    # radiance style check for attacks covering blockages due to friendly pieces and all attack possibilites
    # except knights which are handled separately below
    for ray in eight_ray_iter:
        direction = next(omni_dir)
        (i_dir, j_dir) = direction

        for distance in ray:
            i_tar = i_dir * distance + i
            j_tar = j_dir * distance + j

            if i_tar in b_range and j_tar in b_range:
                piece = chess_state.board[i_tar][j_tar]

                if piece in friendly_pieces:
                    break
                elif piece in pawns:
                    fwd_dir = -1 if chess_state.active_color == white else 1

                    if distance == 1 and i_tar == i + fwd_dir and direction in diag:
                        return True
                    else:
                        break
                elif piece in knights:
                    break
                elif piece in bishops:
                    if direction in diag:
                        return True
                    else:
                        break
                elif piece in rooks:
                    if direction in cardinal:
                        return True
                    else:
                        break
                elif piece in queens:
                    return True
                elif piece in kings:
                    if distance == 1:
                        return True
                    else:
                        break

    for (i_offset, j_offset) in knight_o:
        i_tar = i + i_offset
        j_tar = j + j_offset

        if i_tar in b_range and j_tar in b_range:
            piece = chess_state.board[i_tar][j_tar]

            if piece in knights and piece not in friendly_pieces:
                return True

    return False


def is_check_locked(chess_state, move):
    back = chess_state.board_apply(move)
    king_piece = "K" if chess_state.active_color == white else "k"
    is_check = is_attacked(chess_state, chess_state.king_pos[king_piece])
    chess_state.board_undo(back)
    return is_check


def get_moves(chess_state):
    # all 2d coords are in (y, x) form where positive y is down, this is to ease working with 2d array
    # board representation

    # Short hand
    # i -> row, 2d array first dimension i, reverse rank ascending down, [0, 7]
    # j -> column, 2d array second dimension i, file as number ascending left to right, [0, 7]
    # ept -> en passant target, from opponents move prior if available
    # k -> key, as in map key ~ symbolic id
    # ca -> castling availability

    color_fwd = -1 if chess_state.active_color == white else 1
    leap_file = 6 if chess_state.active_color == white else 1
    enemy_pieces = black_pieces if chess_state.active_color == white else white_pieces
    friendly_pieces = white_pieces if chess_state.active_color == white else black_pieces
    color_castling = white_castling if chess_state.active_color == white else black_castling

    ca = "" if chess_state.castling_available is None else intersect(chess_state.castling_available, color_castling)
    moves = []

    for i in b_range:
        for j in b_range:
            piece = chess_state.board[i][j]

            if piece is None or piece in enemy_pieces:
                continue

            from_ = (i, j)

            if piece in pawns:
                if chess_state.board[i + 1 * color_fwd][j] is None:
                    short_to = (i + 1 * color_fwd, j)
                    move = Move(from_, short_to)

                    if not is_check_locked(chess_state, move):
                        moves.append(move)

                    # Pawn "leap" move
                    if chess_state.board[leap_file + 2 * color_fwd][j] is None and i == leap_file:
                        to = (leap_file + 2 * color_fwd, j)
                        move = Move(from_, to, None, short_to)

                        if not is_check_locked(chess_state, move):
                            moves.append(move)

                # Attacks
                for left_right in dir_left_right:
                    i_tar = i + 1 * color_fwd
                    j_tar = j + 1 * left_right

                    if j_tar in b_range:
                        to = (i_tar, j_tar)
                        victim = chess_state.board[i_tar][j_tar]

                        if to == chess_state.en_passant_target:
                            ep_victim = chess_state.board[i_tar - color_fwd][j_tar]
                            ept_cap = (to, ep_victim)
                            move = Move(from_, to, None, None, ept_cap)

                            if not is_check_locked(chess_state, move):
                                moves.append(move)

                        elif victim in enemy_pieces:
                            move = Move(from_, to, victim)

                            if not is_check_locked(chess_state, move):
                                moves.append(move)

            # Fixed offset assessment (knights, kings)
            elif piece in knights or piece in kings:
                offsets = knight_o if piece in knights else omni

                for (i_offset, j_offset) in offsets:
                    i_tar = i_offset + i
                    j_tar = j_offset + j

                    if i_tar in b_range and j_tar in b_range:
                        victim = chess_state.board[i_tar][j_tar]

                        if victim not in friendly_pieces:
                            # castle invalidation if king moves
                            new_ca = subtract(ca, color_castling) if piece in kings else None
                            move = Move(
                                from_,
                                (i_tar, j_tar),
                                victim,
                                None,
                                None,
                                "-" if new_ca is not None and len(new_ca) == 0 else new_ca
                            )

                            if not is_check_locked(chess_state, move):
                                moves.append(move)

                        # elif friendly:
                        # TODO add guard logic here

                # Castling for kings
                if piece in kings and len(ca):
                    for k in ca:
                        cont = False

                        # Can't castle if any of the positions between king and rook are occupied
                        for (p_i, p_j) in castling_block[k]:
                            if chess_state.board[p_i][p_j] is not None:
                                cont = True
                                break
                        if cont:
                            continue

                        # Can't castle if the king moves through a space that is attacked
                        for pos in castling_check[k]:
                            if is_attacked(chess_state, pos):
                                cont = True
                                break
                        if cont:
                            continue

                        new_ca = subtract(ca, color_castling)
                        to = None

                        if k == "K":
                            to = (7, 6)
                        elif k == "Q":
                            to = (7, 2)
                        elif k == "k":
                            to = (0, 6)
                        else:
                            to = (0, 2)

                        move = Move(
                            from_,
                            to,
                            None,
                            None,
                            None,
                            "-" if len(new_ca) == 0 else new_ca,
                            k
                        )

                        if not is_check_locked(chess_state, move):
                            moves.append(move)

            # Radiance style move assessment (Rooks, Bishops, Queens)
            elif piece in bishops or piece in rooks or piece in queens:
                dir_itr = diag_dir if piece in bishops else (cardinal_dir if piece in rooks else omni_dir)
                ray_itr = eight_ray_iter if piece in queens else four_ray_iter

                for ray in ray_itr:
                    (i_dir, j_dir) = next(dir_itr)

                    for distance in ray:
                        i_tar = i_dir * distance + i
                        j_tar = j_dir * distance + j

                        if i_tar in b_range and j_tar in b_range:
                            victim = chess_state.board[i_tar][j_tar]
                            friendly = victim in friendly_pieces

                            if not friendly:
                                new_ca = None

                                # Castle invalidation if rook, can't castle with a rook that has moved
                                if piece in rooks:
                                    for k in ca:
                                        if castling_rooks[k] == from_:
                                            new_ca = subtract(ca, k)

                                move = Move(
                                    from_,
                                    (i_tar, j_tar),
                                    victim,
                                    None,
                                    None,
                                    "-" if new_ca is not None and len(new_ca) == 0 else new_ca
                                )

                                if not is_check_locked(chess_state, move):
                                    moves.append(move)

                                if victim is not None:
                                    break

                            elif friendly:
                                break
                                # TODO add guard logic here
    return moves
