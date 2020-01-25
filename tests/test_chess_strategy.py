from src.python.chess.chess_strategy import next_actions, ranking_score
from src.python.chess.chess_state import fen_to_state
from src.python.chess.chess_movement import Move


empty_move_lookup = {
    "pruners": set(),
    "critical_path": set()
}


def test_ranking_score():
    m1 = Move(from_=(2, 4), to_=(1, 3), ept_cap=((1, 3), 'p'))
    assert ranking_score(m1, empty_move_lookup, "P") == -1120.0

    m2 = Move(from_=(6, 4), to_=(5, 3), victim='p')
    assert ranking_score(m2, empty_move_lookup, "P") == -1120.0

    m3 = Move(from_=(7, 4), to_=(7, 6), castle='K')
    assert ranking_score(m3, empty_move_lookup, "K") == -1100.0

    m4 = Move(from_=(6, 4), to_=(5, 3), victim='q')
    assert ranking_score(m4, empty_move_lookup, "P") == -1328.0

    m5 = Move(from_=(7, 4), to_=(7, 5))
    assert ranking_score(m5, empty_move_lookup, "K") == -100.0

    m6 = Move(from_=(7, 5), to_=(7, 4), victim='q')
    assert ranking_score(m6, empty_move_lookup, "K") == 660.0000000000001


def test_next_actions():
    s1 = fen_to_state("6k1/4p3/3pP3/6r1/1p3P2/3p4/PP2P3/R3K3 w Q - 0 50")
    assert set([
        Move(from_=(4, 5), to_=(3, 6), victim='r'),
        Move(from_=(6, 4), to_=(5, 3), victim='p'),
        Move(from_=(7, 4), to_=(7, 2), castle='Q'),
        Move(from_=(7, 0), to_=(7, 1)),
        Move(from_=(7, 0), to_=(7, 2)),
        Move(from_=(7, 0), to_=(7, 3)),
        Move(from_=(4, 5), to_=(3, 5)),
        Move(from_=(6, 0), to_=(5, 0)),
        Move(from_=(6, 0), to_=(4, 0), new_ept=(5, 0)),
        Move(from_=(6, 1), to_=(5, 1)),
        Move(from_=(6, 4), to_=(5, 4)),
        Move(from_=(6, 4), to_=(4, 4), new_ept=(5, 4)),
        Move(from_=(7, 4), to_=(7, 5)),
        Move(from_=(7, 4), to_=(6, 3)),
        Move(from_=(7, 4), to_=(6, 5)),
        Move(from_=(7, 4), to_=(7, 3))
    ]).issubset(next_actions(s1, empty_move_lookup))
