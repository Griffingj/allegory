from src.python.chess.chess_movement import Move
from src.python.chess.chess_consts import material
from src.python.chess.chess_state import fen_to_state
from src.python.chess.chess_strategy import score_end, score_state, horizon_outcome
from src.python.primitive import lowest, highest


def test_score_end_check_mate_white():
    s1 = fen_to_state("2k1Q3/8/2K5/8/8/8/8/8 w - - 0 50")
    m = Move(
        (0, 4),
        (0, 2),
        "k"
    )
    s1.apply(m)
    assert s1.is_done
    assert score_end(s1) == highest - 1
    assert score_state(s1, m) == highest - 1


def test_score_end_check_mate_black():
    s1 = fen_to_state("8/8/8/q7/8/K1k5/8/8 b - - 0 50")
    m = Move(
        (3, 0),
        (5, 0),
        "K"
    )
    s1.apply(m)
    assert s1.is_done
    assert score_end(s1) == lowest + 1
    assert score_state(s1, m) == lowest + 1


# This doesn't work because of lack of king safety checks for performance
# def test_score_end_draw():
#     s1 = fen_to_state("k7/8/K7/1Q6/8/8/8/8 w - - 0 50")
#     m = Move(
#         (3, 1),
#         (2, 1)
#     )
#     s1.apply(m)
#     assert not next_actions(s1)
#     assert score_end(s1) == 0


def test_horizon_outcome():
    # Equal trade king helps
    s1 = fen_to_state("6k1/q7/8/8/1Q6/2K5/8/8 w - - 0 50")
    m = Move(
        (4, 1),
        (4, 3)
    )
    s1.apply(m)
    assert horizon_outcome(s1, "Q", m.to_) == 0

    # King can't help
    s1 = fen_to_state("3r2k1/q7/8/8/1Q6/2K5/8/8 w - - 0 50")
    s1.apply(m)
    assert horizon_outcome(s1, "Q", m.to_) == -material["Q"]

    # Bad trade early out
    s1 = fen_to_state("3r2k1/q7/8/8/1Q6/2K5/4N3/8 w - - 0 50")
    s1.apply(m)
    assert horizon_outcome(s1, "Q", m.to_) == -(material["r"] + material["Q"])
