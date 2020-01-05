from copy import deepcopy

from src.chess.chess_consts import initial_fen
from src.chess.chess_state import fen_to_state, Undo
from src.chess.chess_movement import Move


def test_fen_to_initial_state():
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
    assert state.en_passant_target is None
    assert state.halfmoves == 0
    assert state.move == 1
    assert state.material_balance == 0
    assert state.king_pos == {
        "k": (0, 4),
        "K": (7, 4)
    }
    assert state.check_state is False


def test_fen_to_check_state():
    # Opera game move 16
    state = fen_to_state("1Q2kb1r/p2n1ppp/4q3/4p1B1/4P3/8/PPP2PPP/2KR4 b - - 0 16")
    assert state.board == [
        [None, "Q",  None, None, "k",  "b",  None, "r"],
        ["p",  None, None, "n",  None, "p",  "p",  "p"],
        [None, None, None, None, "q",  None, None, None],
        [None, None, None, None, "p",  None, "B",  None],
        [None, None, None, None, "P",  None, None, None],
        [None, None, None, None, None, None, None, None],
        ["P",  "P",  "P",  None, None, "P",  "P",  "P"],
        [None, None, "K",  "R",  None, None, None, None]
    ]
    assert not state.is_done
    assert state.active_color == "b"
    assert state.castling_available is None
    assert state.en_passant_target is None
    assert state.halfmoves == 0
    assert state.move == 16
    assert state.material_balance == -150
    assert state.king_pos == {
        "k": (0, 4),
        "K": (7, 2)
    }
    assert state.check_state is True


def test_to_fen():
    state = fen_to_state(initial_fen)
    fen = state.to_fen()
    assert fen == initial_fen


def assert_state_board_diff(s1, s2):
    assert s1.is_done == s2.is_done
    assert s1.active_color == s2.active_color
    assert s1.castling_available == s2.castling_available
    assert s1.en_passant_target == s2.en_passant_target
    assert s1.halfmoves == s2.halfmoves
    assert s1.move == s2.move
    assert s1.material_balance == s2.material_balance
    assert s1.king_pos == s2.king_pos
    assert s1.check_state == s2.check_state
    assert s1.board != s2.board


def assert_state_eq(s1, s2):
    assert s1.is_done == s2.is_done
    assert s1.active_color == s2.active_color
    assert s1.castling_available == s2.castling_available
    assert s1.en_passant_target == s2.en_passant_target
    assert s1.halfmoves == s2.halfmoves
    assert s1.move == s2.move
    assert s1.material_balance == s2.material_balance
    assert s1.king_pos == s2.king_pos
    assert s1.check_state == s2.check_state
    assert s1.board == s2.board


def test_board_apply_typical():
    s1 = fen_to_state("7k/8/8/8/8/8/4P3/K7 w - - 0 50")
    s2 = deepcopy(s1)
    from_ = (6, 4)
    to_ = (4, 4)
    expected = [
        (from_, "P"),
        (to_, None)
    ]
    move = Move(from_, to_, None, (3, 4), None, None)
    undo = s1.board_apply(move)
    assert undo == expected
    assert_state_board_diff(s1, s2)
    s1.board_undo(undo)
    assert_state_eq(s1, s2)


def test_board_apply_castling():
    s1 = fen_to_state("4k3/8/8/8/8/8/8/R3K2R w KQ - 0 50")
    s2 = deepcopy(s1)
    from_ = (7, 4)
    to_ = (7, 6)
    expected = [
        (from_, "K"),
        (to_, None),
        ((7, 7), "R"),
        ((7, 5), None)
    ]
    move = Move(from_, to_, None, None, None, "-", "K")
    undo = s1.board_apply(move)
    assert undo == expected
    # board_apply is like a soft apply it shouldn't change anything except positional state
    # this is a workaround to make check testing easier for now
    assert s1.active_color == s2.active_color
    assert s1.castling_available == s2.castling_available
    assert s1.board != s2.board
    assert s1.king_pos != s2.king_pos
    s1.board_undo(undo)
    assert_state_eq(s1, s2)


def test_apply_typical():
    s1 = fen_to_state("6k1/8/8/8/8/8/4P3/R3K3 w Q - 0 50")
    s2 = deepcopy(s1)
    from_ = (6, 4)
    to_ = (4, 4)
    board_undo = [
        (from_, "P"),
        (to_, None)
    ]
    move = Move(from_, to_)
    expected = Undo(
        s2.material_balance,
        s2.castling_available,
        s2.en_passant_target,
        board_undo,
        s2.check_state,
        move
    )
    back = s1.apply(move)
    assert back == expected
    s1.undo(back)
    assert_state_eq(s1, s2)


def test_apply_castling():
    s1 = fen_to_state("4k3/8/8/8/8/8/8/R3K2R w KQ - 0 50")
    s2 = deepcopy(s1)
    from_ = (7, 4)
    to_ = (7, 6)
    board_undo = [
        (from_, "K"),
        (to_, None),
        ((7, 7), "R"),
        ((7, 5), None)
    ]
    move = Move(from_, to_, None, None, None, "-", "K")
    expected = Undo(
        s2.material_balance,
        s2.castling_available,
        s2.en_passant_target,
        board_undo,
        s2.check_state,
        move
    )
    back = s1.apply(move)
    assert back == expected
    s1.undo(back)
    assert_state_eq(s1, s2)


def test_apply_ep_capture():
    s1 = fen_to_state("4k3/8/8/2pP4/8/8/8/R3K2R w KQ c6 0 50")
    s2 = deepcopy(s1)
    from_ = (3, 3)
    to_ = (2, 2)
    ept_cap = ((3, 2), "p")
    board_undo = [
        (from_, "P"),
        (to_, None),
        ept_cap
    ]
    move = Move(from_, to_, None, None, ept_cap)
    expected = Undo(
        s2.material_balance,
        s2.castling_available,
        s2.en_passant_target,
        board_undo,
        s2.check_state,
        move
    )
    back = s1.apply(move)
    assert s1.board[2][2] == "P"
    assert s1.material_balance == 1150
    assert back == expected
    s1.undo(back)
    assert_state_eq(s1, s2)


def test_apply_from_check():
    s1 = fen_to_state("4k3/8/8/8/8/8/3p4/R3K2R w KQ - 0 50")
    assert s1.check_state
    s2 = deepcopy(s1)
    from_ = (7, 4)
    to_ = (6, 3)
    board_undo = [
        (from_, "K"),
        (to_, "p")
    ]
    move = Move(from_, to_, "p")
    expected = Undo(
        s2.material_balance,
        s2.castling_available,
        s2.en_passant_target,
        board_undo,
        s2.check_state,
        move
    )
    back = s1.apply(move)
    assert not s1.check_state
    assert back == expected
    s1.undo(back)
    assert_state_eq(s1, s2)
