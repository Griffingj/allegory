from src.python.chess.chess_consts import ranks, files, castling_rooks, queens
from src.python.vector2 import add

left_2 = (0, -2)
right_3 = (0, 3)


def coords_to_chess(pos):
    (y, x) = pos
    return f"{files[x]}{ranks[y]}"


def chess_to_coords(chess):
    [f, r] = list(chess)
    return (ranks.index(int(r)), files.index(f))


def format_move(move):
    main = f"{coords_to_chess(move.from_)}-{coords_to_chess(move.to_)}"
    formatted = [main]

    if move.castle is not None:
        from_ = castling_rooks[move.castle]
        to_ = add(from_, right_3) if move.castle in queens else add(from_, left_2)
        formatted.append(f"{coords_to_chess(from_)}-{coords_to_chess(to_)}")

    return formatted
