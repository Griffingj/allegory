from src.python.chess.chess_state import fen_to_state
from src.python.chess.chess_movement import get_moves, Move


def test_pawn_move_basics():
    s1 = fen_to_state("6k1/4p3/3pP3/1pP5/1p3P2/3p1P2/1P2P3/4K3 w - b6 2 51")
    assert set([
        Move(from_=(3, 2), to_=(2, 1), ept_cap=((3, 1), 'p')),
        Move(from_=(4, 5), to_=(3, 5)),
        Move(from_=(6, 1), to_=(5, 1)),
        Move(from_=(6, 4), to_=(5, 4)),
        Move(from_=(6, 4), to_=(4, 4), new_ept=(5, 4)),
        Move(from_=(6, 4), to_=(5, 3), victim='p'),
        Move(from_=(7, 4), to_=(7, 5)),
        Move(from_=(7, 4), to_=(6, 3)),
        Move(from_=(7, 4), to_=(6, 5)),
        Move(from_=(7, 4), to_=(7, 3))
    ]).issubset(get_moves(s1))


def test_knight_move_basic():
    s1 = fen_to_state("6k1/8/1N1p4/1P1P4/2p5/8/8/4K3 w - - 0 50")
    assert set([
        Move(from_=(2, 1), to_=(4, 0)),
        Move(from_=(2, 1), to_=(0, 0)),
        Move(from_=(2, 1), to_=(4, 2), victim='p'),
        Move(from_=(2, 1), to_=(0, 2)),
        Move(from_=(2, 1), to_=(1, 3)),
        Move(from_=(7, 4), to_=(7, 5)),
        Move(from_=(7, 4), to_=(6, 3)),
        Move(from_=(7, 4), to_=(6, 5)),
        Move(from_=(7, 4), to_=(6, 4)),
        Move(from_=(7, 4), to_=(7, 3))
    ]).issubset(get_moves(s1))


def test_bishop_move_basic():
    s1 = fen_to_state("6k1/7p/3p4/5B2/4P3/7P/8/4K3 w - - 0 50")
    assert set([
        Move(from_=(3, 5), to_=(2, 6)),
        Move(from_=(3, 5), to_=(1, 7), victim='p'),
        Move(from_=(3, 5), to_=(4, 6)),
        Move(from_=(3, 5), to_=(2, 4)),
        Move(from_=(3, 5), to_=(1, 3)),
        Move(from_=(3, 5), to_=(0, 2)),
        Move(from_=(4, 4), to_=(3, 4)),
        Move(from_=(5, 7), to_=(4, 7)),
        Move(from_=(7, 4), to_=(7, 5)),
        Move(from_=(7, 4), to_=(6, 3)),
        Move(from_=(7, 4), to_=(6, 5)),
        Move(from_=(7, 4), to_=(6, 4)),
        Move(from_=(7, 4), to_=(7, 3))
    ]).issubset(get_moves(s1))


def test_rook_move_basic():
    s1 = fen_to_state("6k1/p4RPp/3p4/8/5P2/8/8/4K3 w - - 0 50")
    assert set([
        Move(from_=(1, 5), to_=(2, 5)),
        Move(from_=(1, 5), to_=(3, 5)),
        Move(from_=(1, 5), to_=(0, 5)),
        Move(from_=(1, 5), to_=(1, 4)),
        Move(from_=(1, 5), to_=(1, 3)),
        Move(from_=(1, 5), to_=(1, 2)),
        Move(from_=(1, 5), to_=(1, 1)),
        Move(from_=(1, 5), to_=(1, 0), victim='p'),
        Move(from_=(4, 5), to_=(3, 5)),
        Move(from_=(7, 4), to_=(7, 5)),
        Move(from_=(7, 4), to_=(6, 3)),
        Move(from_=(7, 4), to_=(6, 5)),
        Move(from_=(7, 4), to_=(6, 4)),
        Move(from_=(7, 4), to_=(7, 3))
    ]).issubset(get_moves(s1))


def test_queen_move_basic():
    s1 = fen_to_state("6nk/2p2QNp/3p4/3P4/5P2/8/8/4K3 w - - 0 50")
    assert set([
        Move(from_=(1, 5), to_=(0, 6), victim='n'),
        Move(from_=(1, 5), to_=(2, 6)),
        Move(from_=(1, 5), to_=(3, 7)),
        Move(from_=(1, 5), to_=(2, 4)),
        Move(from_=(1, 5), to_=(0, 5)),
        Move(from_=(1, 5), to_=(2, 5)),
        Move(from_=(1, 5), to_=(3, 5)),
        Move(from_=(1, 5), to_=(1, 4)),
        Move(from_=(1, 5), to_=(1, 3)),
        Move(from_=(1, 5), to_=(1, 2), victim='p'),
        Move(from_=(1, 5), to_=(0, 4)),
        Move(from_=(1, 6), to_=(3, 5)),
        Move(from_=(1, 6), to_=(0, 4)),
        Move(from_=(1, 6), to_=(3, 7)),
        Move(from_=(1, 6), to_=(2, 4)),
        Move(from_=(4, 5), to_=(3, 5)),
        Move(from_=(7, 4), to_=(7, 5)),
        Move(from_=(7, 4), to_=(6, 3)),
        Move(from_=(7, 4), to_=(6, 5)),
        Move(from_=(7, 4), to_=(6, 4)),
        Move(from_=(7, 4), to_=(7, 3))
    ]).issubset(get_moves(s1))
