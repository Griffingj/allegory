from src.chess.chess_state import fen_to_state
from src.chess.chess_movement import get_moves, Move


def test_check_basics():
    s1 = fen_to_state("4k3/8/7b/8/4r3/8/3p4/4K3 w - - 0 50")
    assert get_moves(s1) == [
        Move(
            from_=(7, 4), to_=(7, 5), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='-', castle=None
        ),
        Move(
            from_=(7, 4), to_=(6, 5), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='-', castle=None
        ),
        Move(
            from_=(7, 4), to_=(7, 3), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='-', castle=None
        )
    ]


def test_check_capture():
    s1 = fen_to_state("4k3/8/8/8/8/8/4q3/4K3 w - - 0 50")
    assert get_moves(s1) == [
        Move(
            from_=(7, 4), to_=(6, 4), victim='q', new_en_passant_target=None, ept_cap=None,
            new_castling_available='-', castle=None
        )
    ]


def test_check_pin_expose():
    s1 = fen_to_state("4k3/8/8/8/8/4qn2/4P3/4K3 w - - 0 50")
    assert get_moves(s1) == [
        Move(
            from_=(7, 4), to_=(7, 5), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='-', castle=None
        ),
        Move(
            from_=(7, 4), to_=(7, 3), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='-', castle=None
        )
    ]


def test_check_self_block():
    s1 = fen_to_state("4k3/8/8/8/8/3P4/8/4qK2 w - - 0 50")
    assert get_moves(s1) == [
        Move(
            from_=(7, 5), to_=(6, 6), victim=None, new_en_passant_target=None, ept_cap=None,
            new_castling_available='-', castle=None
        ),
        Move(
            from_=(7, 5), to_=(7, 4), victim='q', new_en_passant_target=None, ept_cap=None,
            new_castling_available='-', castle=None
        )
    ]
