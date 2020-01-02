from src.chess.chess_consts import initial_fen
from src.chess.chess_state import fen_to_state


def test_fen_to_state():
    state = fen_to_state(initial_fen)
    assert state.board == [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"]
    ]
    assert not state.is_done
    assert state.active_color == "w"
    assert state.castling_available == "KQkq"
    assert state.en_passant_target == "-"
    assert state.halfmoves == 0
    assert state.move == 1
    assert state.material_balance == 0


def test_to_fen():
    state = fen_to_state(initial_fen)
    fen = state.to_fen()
    assert fen == initial_fen
