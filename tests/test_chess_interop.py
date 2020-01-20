from test_movement_castling import queen_castle, king_castle
from src.python.chess.chess_interop import format_move
from src.python.chess.chess_movement import Move


def test_format_move():
    assert format_move(queen_castle) == ["e1-c1", "a1-d1"]
    assert format_move(king_castle) == ["e1-g1", "h1-f1"]

    m1 = Move(
        from_=(4, 5), to_=(3, 6), victim='r', new_en_passant_target=None, ept_cap=None,
        new_castling_available=None, castle=None
    )
    assert format_move(m1) == ["f4-g5"]
