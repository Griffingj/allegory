from itertools import cycle
from collections import namedtuple

from src.chess.chess_consts import b_range, black_pieces, white_pieces, pawns, knights, bishops, rooks, queens, kings,\
    white, white_castling, black_castling, castling_block, castling_check, castling_rooks

from src.primitive import subtract, intersect

# all 2d coords are in (y, x) form where positive y is down, this is to ease working with 2d array
# board representation
knight_o = {
    (-2, -1), (-1, -2), (1, -2), (2, -1),
    (-2,  1), (-1,  2), (1,  2), (2,  1)
}

# unit grid right, up, left, down
cardinal_o = {
    (0, 1), (-1, 0), (0, -1), (1, 0)
}
cardinal_dir = cycle(cardinal_o)

dir_left_right = {
    -1, 1
}

# unit grid NE, NW, SW, SE
diag_o = {
    (-1, 1), (-1, -1), (1, -1), (1, 1)
}
diag_dir = cycle(diag_o)

# Queens/Kings
omni_o = cardinal_o.union(diag_o)
omni_dir = cycle(omni_o)

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
    "en_passant_target",
    "castling_available_to",
    "castled_to"
], defaults=(None, None, None, None, None, None))


def is_attacked(chess_state, pos):
    (i, j) = pos
    friendly_pieces = white_pieces if chess_state.active_color == white else black_pieces

    # radiance style check for attacks covering blockages due to friendly pieces and all attack possibilites
    # except knights which are handled separately below
    for ray in eight_ray_iter:
        d = next(omni_dir)
        (i_d, j_d) = d

        for n in ray:
            i_t = i_d * n + i
            j_t = j_d * n + j

            if i_t in b_range and j_t in b_range:
                t = chess_state.board[i_t][j_t]

                if t in friendly_pieces:
                    break
                elif t in pawns:
                    fwd_d = -1 if chess_state.active_color == white else 1
                    if n == 1 and i_t == i + fwd_d and d in diag_o:
                        return True
                    else:
                        break
                elif t in knights:
                    break
                elif t in bishops:
                    if d in diag_o:
                        return True
                    else:
                        break
                elif t in rooks:
                    if d in cardinal_o:
                        return True
                    else:
                        break
                elif t in queens:
                    return True
                elif t in kings:
                    if n == 1:
                        return True
                    else:
                        break

    for (i_o, j_o) in knight_o:
        i_t = i + i_o
        j_t = j + j_o

        if i_t in b_range and j_t in b_range:
            t = chess_state.board[i_t][j_t]

            if t in knights and t not in friendly_pieces:
                return True

    return False


def is_check_locked(chess_state, move):
    back = chess_state.board_apply(move)
    king_piece = "K" if chess_state.active_color == white else "k"
    is_check = is_attacked(chess_state, chess_state.king_pos[king_piece])
    chess_state.board_undo(back)
    return is_check


def get_moves(chess_state, search_state):
    # all 2d coords are in (y, x) form where positive y is down, this is to ease working with 2d array
    # board representation

    # Short-hand
    # i -> row, 2d array first dimension i, reverse rank ascending down, [0, 7]
    # j -> column, 2d array second dimension i, file as number ascending left to right, [0, 7]
    # f -> from
    # t -> target/to
    # d -> direction, typically 2d cartesian coords for unit grid
    # ept -> en passant target, from opponents move prior if available
    # o -> offset, addens to modify current position
    # k -> key, as in map key ~ symbolic id
    # ca -> castling availability

    color_fwd = -1 if chess_state.active_color == white else 1
    leap_file = 6 if chess_state.active_color == white else 1
    enemy_pieces = black_pieces if chess_state.active_color == white else white_pieces
    friendly_pieces = white_pieces if chess_state.active_color == white else black_pieces
    color_castling = white_castling if chess_state.active_color == white else black_castling

    ca = chess_state.castling_available
    ept = chess_state.en_passant_target
    moves = []

    for i in b_range:
        for j in b_range:
            piece = chess_state.board[i][j]

            if piece is None:
                continue

            from_ = (i, j)

            if piece in pawns:
                if chess_state.board[i + 1 * color_fwd][j] is None:
                    move = Move(from_, (leap_file + 1 * color_fwd, j))

                    if not chess_state.is_check_locked(move):
                        moves.append(move)

                    # Pawn "leap" move
                    if chess_state.board[leap_file + 2 * color_fwd][j] is None and i == leap_file:
                        to = (leap_file + 2 * color_fwd, j)
                        move = Move(from_, to, None, to)

                        if not chess_state.is_check_locked(move):
                            moves.append(move)

                # Attacks
                for left_right in dir_left_right:
                    i_t = i + 1 * color_fwd
                    j_t = j + 1 * left_right

                    if j_t in b_range:
                        victim = chess_state.board[i_t][j_t]
                        to = (i_t, j_t)

                        if victim in enemy_pieces or ept == to:
                            move = Move(from_, to, victim or ept)

                            if not chess_state.is_check_locked(move):
                                moves.append(move)

            # Fixed offset assessment (knights, kings)
            elif piece in knights or piece in kings:
                offsets = knight_o if piece in knights else omni_o

                for (i_o, j_o) in offsets:
                    i_t = i_o + i
                    j_t = j_o + j

                    if i_t in b_range and j_t in b_range:
                        t = chess_state.board[i_t][j_t]
                        to = (i_t, j_t)

                        if t not in friendly_pieces or ept == to:
                            # castle invalidation if king moves
                            castling = subtract(ca, color_castling) if piece in kings else None
                            move = Move(from_, to, t or ept, None, castling)

                            if not chess_state.is_check_locked(move):
                                moves.append(move)

                        # elif friendly:
                        # TODO add guard logic here

                # Castling for kings
                cur_ca = intersect(ca, color_castling)
                if piece in kings and len(cur_ca):
                    for k in cur_ca:
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

                        move = Move(from_, to, None, None, subtract(ca, color_castling), k)

                        if not chess_state.is_check_locked(move):
                            moves.append(move)

            # Radiance style move assessment (Rooks, Bishops, Queens)
            elif piece in bishops or piece in rooks or piece in queens:
                dir_itr = diag_dir if piece in bishops else (cardinal_dir if piece in rooks else omni_dir)
                ray_itr = eight_ray_iter if piece in queens else four_ray_iter

                for ray in ray_itr:
                    (i_d, j_d) = next(dir_itr)

                    for n in ray:
                        i_t = i_d * n + i
                        j_t = j_d * n + j

                        if i_t in b_range and j_t in b_range:
                            t = chess_state.board[i_t][j_t]
                            to = (i_t, j_t)
                            friendly = t in friendly_pieces

                            if not friendly or ept == to or t is None:
                                castle_availability_to = None

                                # Castle invalidation if rook, can't castle with a rook that has moved
                                if piece in rooks:
                                    for k in intersect(ca, color_castling):
                                        if castling_rooks[k] == from_:
                                            castle_availability_to = subtract(ca, k)

                                move = Move(from_, to, t or ept, castle_availability_to)

                                if not chess_state.is_check_locked(move):
                                    moves.append(move)

                            elif friendly:
                                break
                                # TODO add guard logic here
