from copy import deepcopy

from src.python.chess.chess_state import fen_to_state
from src.python.chess.chess_movement import get_moves, Move

king_castle = Move(
    from_=(7, 4), to_=(7, 6), victim=None, new_en_passant_target=None, ept_cap=None,
    new_castling_available='-', castle='K'
)
queen_castle = Move(
    from_=(7, 4), to_=(7, 2), victim=None, new_en_passant_target=None, ept_cap=None,
    new_castling_available='-', castle='Q'
)

castling_moves = set([king_castle, queen_castle])


def doesnt_contain(s1, s2):
    return not len(s1.intersection(s2))


def test_castling_basic():
    s1 = fen_to_state("6k1/8/8/8/8/8/P6P/R3K2R w KQ - 0 50")
    s2 = deepcopy(s1)
    s3 = deepcopy(s1)

    assert set([
        Move(
            from_=(7, 0), to_=(7, 1), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='K', castle=None
        ),
        Move(
            from_=(7, 0), to_=(7, 2), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='K', castle=None
        ),
        Move(
            from_=(7, 0), to_=(7, 3), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='K', castle=None
        ),
        king_castle,
        queen_castle,
        Move(
            from_=(7, 7), to_=(7, 6), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='Q', castle=None
        ),
        Move(
            from_=(7, 7), to_=(7, 5), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='Q', castle=None
        )
    ]).issubset(get_moves(s1))

    s2_back = s2.apply(king_castle)
    assert s2.pos(king_castle.to_) == "K"
    assert s2.pos((7, 5)) == "R"
    s2.undo(s2_back)
    assert s2.pos(king_castle.from_) == "K"
    assert s2.pos((7, 7)) == "R"

    s3_back = s3.apply(queen_castle)
    assert s3.pos(queen_castle.to_) == "K"
    assert s3.pos((7, 3)) == "R"
    s3.undo(s3_back)
    assert s3.pos(queen_castle.from_) == "K"
    assert s3.pos((7, 0)) == "R"


def test_castling_blocked():
    s1 = fen_to_state("6k1/8/8/8/8/8/P6P/Rn2KN1R w KQ - 0 50")
    assert doesnt_contain(set(get_moves(s1)), castling_moves)


def test_castling_in_check():
    s1 = fen_to_state("6k1/8/8/8/8/3n4/P6P/R3K2R w KQ - 0 50")
    moves = get_moves(s1)
    print(moves)
    assert doesnt_contain(set(get_moves(s1)), castling_moves)


def test_castling_attacked_space():
    s1 = fen_to_state("6k1/8/8/8/8/4b3/8/R3K2R w KQ - 0 50")
    assert doesnt_contain(set(get_moves(s1)), castling_moves)


def test_castling_attacked_castle_space():
    s1 = fen_to_state("6k1/8/8/8/4b3/8/P6P/R3K2R w KQ - 0 50")
    assert set([
        Move(
            from_=(7, 4), to_=(7, 2), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='-', castle='Q'
        ),
        Move(
            from_=(7, 4), to_=(7, 6), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='-', castle='K'
        )
    ]).issubset(get_moves(s1))


def test_castling_removes_availability():
    s1 = fen_to_state("r3k2r/p6p/8/8/8/8/P6P/R3K2R w KQkq - 0 50")
    assert set([
        Move(
            from_=(7, 4), to_=(7, 2), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='kq', castle='Q'
        ),
        Move(
            from_=(7, 4), to_=(7, 6), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='kq', castle='K'
        )
    ]).issubset(get_moves(s1))

    s1 = fen_to_state("r3k2r/p6p/8/8/8/8/P6P/R3K2R b KQkq - 0 50")
    assert set([
        Move(
            from_=(0, 4), to_=(0, 2), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='KQ', castle='q'
        ),
        Move(
            from_=(0, 4), to_=(0, 6), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='KQ', castle='k'
        )
    ]).issubset(get_moves(s1))
