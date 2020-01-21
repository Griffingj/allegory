from copy import deepcopy

from src.python.chess.chess_state import fen_to_state
from src.python.chess.chess_movement import get_moves, Move

king_castle = Move(from_=(7, 4), to_=(7, 6), castle='K')
queen_castle = Move(from_=(7, 4), to_=(7, 2), castle='Q')

castling_moves = set([king_castle, queen_castle])


def doesnt_contain(s1, s2):
    return not len(s1.intersection(s2))


def test_castling_basic():
    s1 = fen_to_state("6k1/8/8/8/8/8/P6P/R3K2R w KQ - 0 50")
    s2 = deepcopy(s1)
    s3 = deepcopy(s1)

    assert set([
        Move(from_=(7, 0), to_=(7, 1)),
        Move(from_=(7, 0), to_=(7, 2)),
        Move(from_=(7, 0), to_=(7, 3)),
        king_castle,
        queen_castle,
        Move(from_=(7, 7), to_=(7, 6)),
        Move(from_=(7, 7), to_=(7, 5))
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
        Move(from_=(7, 4), to_=(7, 2), castle='Q'),
        Move(from_=(7, 4), to_=(7, 6), castle='K')
    ]).issubset(get_moves(s1))


def test_castling_removes_availability():
    s1 = fen_to_state("r3k2r/p6p/8/8/8/8/P6P/R3K2R w KQkq - 0 50")
    assert set([
        Move(from_=(7, 4), to_=(7, 2), castle='Q'),
        Move(from_=(7, 4), to_=(7, 6), castle='K')
    ]).issubset(get_moves(s1))

    s1 = fen_to_state("r3k2r/p6p/8/8/8/8/P6P/R3K2R b KQkq - 0 50")
    assert set([
        Move(from_=(0, 4), to_=(0, 2), castle='q'),
        Move(from_=(0, 4), to_=(0, 6), castle='k')
    ]).issubset(get_moves(s1))


def test_moving_rook_removes_availability():
    s1 = fen_to_state("r3k2r/p6p/8/8/8/8/P6P/R3K2R w KQkq - 4 3")
    assert set([
        Move(from_=(7, 0), to_=(7, 1)),
        Move(from_=(7, 7), to_=(7, 6))
    ]).issubset(get_moves(s1))


def test_killing_rook_removes_ca():
    s1 = fen_to_state("r3k2r/pP4Pp/8/8/8/8/Pp4pP/R3K2R w KQkq - 104 52")
    s2 = deepcopy(s1)
    m1 = Move(from_=(1, 1), to_=(0, 0), victim="r")
    m2 = Move(from_=(1, 6), to_=(0, 7), victim="r")
    assert set([m1, m2]).issubset(get_moves(s1))
    s1.apply(m1)
    assert s1.castling_available == "KQk"
    s2.apply(m2)
    assert s2.castling_available == "KQq"

    s3 = fen_to_state("r3k2r/pP4Pp/8/8/8/8/Pp4pP/R3K2R b KQkq - 104 52")
    s4 = deepcopy(s3)
    m3 = Move(from_=(6, 1), to_=(7, 0), victim="R")
    m4 = Move(from_=(6, 6), to_=(7, 7), victim="R")
    assert set([m3, m4]).issubset(get_moves(s3))
    s3.apply(m3)
    assert s3.castling_available == "Kkq"
    s4.apply(m4)
    assert s4.castling_available == "Qkq"
