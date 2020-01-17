from src.python.chess.chess_state import fen_to_state
from src.python.chess.chess_movement import is_attacked_by, is_attacked, targeted_by


def test_is_attacked_by():
    # Pawns
    s1 = fen_to_state("5k2/8/8/2p1p3/3K4/8/8/8 w - - 0 50")
    assert is_attacked_by(s1, (4, 3), (3, 2))
    assert is_attacked_by(s1, (4, 3), (3, 4))

    s1 = fen_to_state("3r2kb/b7/2n1n3/1n3n2/r2K3r/1n3n2/2n1n3/b2r2b1 w - - 0 50")
    # Knights
    assert is_attacked_by(s1, (4, 3), (2, 4))
    assert is_attacked_by(s1, (4, 3), (2, 2))
    assert is_attacked_by(s1, (4, 3), (3, 5))
    assert is_attacked_by(s1, (4, 3), (3, 1))
    assert is_attacked_by(s1, (4, 3), (5, 5))
    assert is_attacked_by(s1, (4, 3), (5, 1))
    assert is_attacked_by(s1, (4, 3), (6, 4))
    assert is_attacked_by(s1, (4, 3), (6, 2))
    # Bishops
    assert is_attacked_by(s1, (4, 3), (0, 7))
    assert is_attacked_by(s1, (4, 3), (1, 0))
    assert is_attacked_by(s1, (4, 3), (7, 6))
    assert is_attacked_by(s1, (4, 3), (7, 0))
    # Rooks
    assert is_attacked_by(s1, (4, 3), (0, 3))
    assert is_attacked_by(s1, (4, 3), (4, 7))
    assert is_attacked_by(s1, (4, 3), (4, 0))
    assert is_attacked_by(s1, (4, 3), (7, 3))

    # Queens
    s1 = fen_to_state("3q2kq/q7/8/8/q2K3q/8/8/3q4 w - - 0 50")
    assert is_attacked_by(s1, (4, 3), (7, 3))
    assert is_attacked_by(s1, (4, 3), (4, 0))
    assert is_attacked_by(s1, (4, 3), (4, 7))
    assert is_attacked_by(s1, (4, 3), (0, 7))
    assert is_attacked_by(s1, (4, 3), (0, 3))
    assert is_attacked_by(s1, (4, 3), (1, 0))

    # Kings
    s1 = fen_to_state("8/8/8/2kkk3/2kKk3/2kkk3/8/8 w - - 0 50")
    assert is_attacked_by(s1, (4, 3), (4, 2))
    assert is_attacked_by(s1, (4, 3), (4, 4))
    assert is_attacked_by(s1, (4, 3), (5, 2))
    assert is_attacked_by(s1, (4, 3), (5, 3))
    assert is_attacked_by(s1, (4, 3), (5, 4))
    assert is_attacked_by(s1, (4, 3), (3, 2))
    assert is_attacked_by(s1, (4, 3), (3, 3))
    assert is_attacked_by(s1, (4, 3), (3, 4))


def test_is_attacked():
    s1 = fen_to_state("5k2/8/8/2p1p3/3K4/8/8/8 w - - 0 50")
    assert is_attacked(s1, (4, 3))
    assert not is_attacked(s1, (4, 4))
    s1 = fen_to_state("3r2kb/b7/2n1n3/1n3n2/r2K3r/1n3n2/2n1n3/b2r2b1 w - - 0 50")
    assert is_attacked(s1, (4, 3))
    assert not is_attacked(s1, (6, 6))
    s1 = fen_to_state("3q2kq/q7/8/8/q2K3q/8/8/3q4 w - - 0 50")
    assert is_attacked(s1, (4, 3))
    assert not is_attacked(s1, (6, 6))
    s1 = fen_to_state("8/8/8/2kkk3/2kKk3/2kkk3/8/8 w - - 0 50")
    assert is_attacked(s1, (4, 3))
    assert not is_attacked(s1, (6, 6))


def sort_targeters(groups):
    return tuple(map(sorted, groups))


def test_targeted_by():
    s1 = fen_to_state("8/8/8/2p1P3/3R4/2P1p3/8/8 w - - 0 50")
    assert targeted_by(s1, (4, 3)) == (
        [((3, 2), "p")],
        [((5, 2), "P")]
    )

    # Rooks, Knights, Bishops
    s1 = fen_to_state("3R2kb/B5P1/2n1N3/1N3n2/r2P2pr/1n3N2/2NPnpK1/b2R2B1 w - - 0 50")
    assert sort_targeters(targeted_by(s1, (4, 3))) == sort_targeters((
        [
            ((2, 4), "N"),
            ((3, 1), "N"),
            ((5, 5), "N"),
            ((6, 2), "N"),
            ((1, 0), "B"),
            ((0, 3), "R")
        ],
        [
            ((2, 2), "n"),
            ((3, 5), "n"),
            ((5, 1), "n"),
            ((6, 4), "n"),
            ((4, 0), "r"),
            ((7, 0), "b")
        ]
    ))

    # Queens
    s1 = fen_to_state("3q2kQ/Q7/1p6/8/q2P2Pq/8/6K1/3Q4 w - - 0 50")
    assert sort_targeters(targeted_by(s1, (4, 3))) == sort_targeters((
        [
            ((0, 7), "Q"),
            ((7, 3), "Q")
        ],
        [
            ((4, 0), "q"),
            ((0, 3), "q")
        ]
    ))

    # Kings
    s1 = fen_to_state("8/8/8/1k2k3/2KP1K2/3kK3/8/8 w - - 0 50")
    assert sort_targeters(targeted_by(s1, (4, 3))) == sort_targeters((
        [
            ((5, 4), "K"),
            ((4, 2), "K")
        ],
        [
            ((3, 4), "k"),
            ((5, 3), "k")
        ]
    ))
