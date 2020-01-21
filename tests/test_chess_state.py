from copy import deepcopy

from src.python.chess.chess_consts import initial_fen
from src.python.chess.chess_state import fen_to_state, Undo
from src.python.chess.chess_movement import Move


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
    k_pos, = state.positions["k"]
    K_pos, = state.positions["K"]
    assert k_pos == (0, 4)
    assert K_pos == (7, 4)


def test_to_fen():
    state = fen_to_state(initial_fen)
    fen = state.to_fen()
    assert fen == initial_fen


def assert_state_eq(s1, s2):
    assert s1.is_done == s2.is_done
    assert s1.active_color == s2.active_color
    assert s1.castling_available == s2.castling_available
    assert s1.en_passant_target == s2.en_passant_target
    assert s1.halfmoves == s2.halfmoves
    assert s1.move == s2.move
    assert s1.material_balance == s2.material_balance
    assert s1.positions == s2.positions
    assert s1.board == s2.board


def test_board_apply_typical():
    s1 = fen_to_state("7k/8/8/8/8/8/4P3/K7 w - - 100 50")
    s2 = deepcopy(s1)
    from_ = (6, 4)
    to_ = (4, 4)
    expected = [
        (from_, to_, "P")
    ]
    move = Move(from_, to_, new_ept=(3, 4))
    undo = s1.board_apply(move)
    assert undo == expected
    assert s1.is_done == s2.is_done
    assert s1.active_color == s2.active_color
    assert s1.castling_available == s2.castling_available
    assert s1.en_passant_target == s2.en_passant_target
    assert s1.halfmoves == s2.halfmoves
    assert s1.move == s2.move
    assert s1.material_balance == s2.material_balance
    k_pos, = s2.positions["k"]
    K_pos, = s2.positions["K"]
    assert k_pos == (0, 7)
    assert K_pos == (7, 0)
    assert s1.board != s2.board
    s1.board_undo(undo)
    assert_state_eq(s1, s2)


def test_board_apply_castling():
    s1 = fen_to_state("4k3/8/8/8/8/8/8/R3K2R w KQ - 100 50")
    s2 = deepcopy(s1)
    from_ = (7, 4)
    to_ = (7, 6)
    c_to = (7, 5)
    expected = [
        (from_, to_, "K"),
        ((7, 7), c_to, "R")
    ]
    move = Move(from_, to_, castle="K")
    undo = s1.board_apply(move)
    assert undo == expected
    # board_apply is like a soft apply it shouldn"t change anything except positional state
    # this is a workaround to make check testing easier for now
    assert s1.active_color == s2.active_color
    assert s1.castling_available == s2.castling_available
    assert s1.board != s2.board
    assert s1.positions != s2.positions
    s1.board_undo(undo)
    assert_state_eq(s1, s2)


def test_apply_typical():
    s1 = fen_to_state("6k1/8/8/8/8/8/4P3/R3K3 w Q - 100 50")
    s2 = deepcopy(s1)
    from_ = (6, 4)
    to_ = (4, 4)
    board_undo = [
        (from_, to_, "P")
    ]
    move = Move(from_, to_)
    expected = Undo(
        s2.material_balance,
        s2.castling_available,
        s2.en_passant_target,
        board_undo,
        move
    )
    back = s1.apply(move)
    assert back == expected
    s1.undo(back)
    assert_state_eq(s1, s2)


def test_apply_castling():
    s1 = fen_to_state("4k3/8/8/8/8/8/8/R3K2R w KQ - 100 50")
    s2 = deepcopy(s1)
    from_ = (7, 4)
    to_ = (7, 6)
    c_to = (7, 5)
    board_undo = [
        (from_, to_, "K"),
        ((7, 7), c_to, "R")
    ]
    move = Move(from_, to_, castle="K")
    expected = Undo(
        s2.material_balance,
        s2.castling_available,
        s2.en_passant_target,
        board_undo,
        move
    )
    back = s1.apply(move)
    assert back == expected
    s1.undo(back)
    assert_state_eq(s1, s2)


def test_apply_ep_capture():
    s1 = fen_to_state("4k3/8/8/2pP4/8/8/8/R3K2R w KQ c6 100 50")
    s2 = deepcopy(s1)
    from_ = (3, 3)
    to_ = (2, 2)
    ept = (3, 2)
    epp = "p"
    ept_cap = (ept, epp)
    board_undo = [
        (from_, to_, "P"),
        (ept, None, epp)
    ]
    move = Move(from_, to_, ept_cap=ept_cap)
    expected = Undo(
        s2.material_balance,
        s2.castling_available,
        s2.en_passant_target,
        board_undo,
        move
    )
    back = s1.apply(move)
    assert s1.board[2][2] == "P"
    assert s1.material_balance == 1110
    assert back == expected
    s1.undo(back)
    assert_state_eq(s1, s2)


def test_apply_from_check():
    s1 = fen_to_state("4k3/8/8/8/8/8/3p4/R3K2R w KQ - 100 50")
    s2 = deepcopy(s1)
    from_ = (7, 4)
    to_ = (6, 3)
    board_undo = [
        (from_, to_, "K"),
        (to_, None, "p")
    ]
    move = Move(from_, to_, "p")
    expected = Undo(
        s2.material_balance,
        s2.castling_available,
        s2.en_passant_target,
        board_undo,
        move
    )
    back = s1.apply(move)
    assert back == expected
    s1.undo(back)
    assert_state_eq(s1, s2)


def is_sync_positions(state):
    for k in state.positions:
        coords = state.positions[k]
        for (y, x) in coords:
            assert state.board[y][x] == k


def is_stable(states, moves):
    state = fen_to_state(states[0])
    undos = []

    for i, m in enumerate(moves):
        undos.append(state.apply(m))
        is_sync_positions(state)
        assert state.to_fen() == states[i + 1]

    for i, u in enumerate(reversed(undos)):
        state.undo(u)
        is_sync_positions(state)
        assert state.to_fen() == states[len(states) - 2 - i]


def test_apply_undo_stability():
    states = [
        "2r3k1/1pq2p1p/p2Q1npb/b3p3/2r1P2B/1BN1R2P/PnP2PP1/3R2K1 b - - 50 25",
        "2r3k1/1pq2p1p/p2Q1np1/b3p3/2r1P2B/1BN1b2P/PnP2PP1/3R2K1 w - - 51 26",
        "2r3k1/1pq2p1p/p2Q1np1/b3p3/2B1P2B/2N1b2P/PnP2PP1/3R2K1 b - - 52 26",
        "2r3k1/1pq2p1p/p2Q2p1/b3p3/2B1n2B/2N1b2P/PnP2PP1/3R2K1 w - - 53 27",
    ]

    moves = [
        Move(from_=(2, 7), to_=(5, 4), victim="R"),
        Move(from_=(5, 1), to_=(4, 2), victim="r"),
        Move(from_=(2, 5), to_=(4, 4), victim="P")
    ]
    is_stable(states, moves)


def test_apply_undo_stability_castling():
    states = [
        "r3k2r/p6p/8/1p6/8/8/P6P/R3K2R w KQkq b6 50 25",
        "r3k2r/p6p/8/1p6/8/8/P6P/R4RK1 b kq - 51 25",
        "2kr3r/p6p/8/1p6/8/8/P6P/R4RK1 w - - 52 26",
        "2kr3r/p6p/8/1p6/8/8/P5KP/R4R2 b - - 53 26",
    ]

    moves = [
        Move(from_=(7, 4), to_=(7, 6), castle='K'),
        Move(from_=(0, 4), to_=(0, 2), castle='q'),
        Move(from_=(7, 6), to_=(6, 6))
    ]
    is_stable(states, moves)


def test_apply_undo_stability_promotion():
    states = [
        "4k3/1P6/8/8/8/8/8/4K3 w - - 50 25",
        "1Q2k3/8/8/8/8/8/8/4K3 b - - 51 25",
        "1Q6/4k3/8/8/8/8/8/4K3 w - - 52 26"
    ]

    moves = [
        Move(from_=(1, 1), to_=(0, 1)),
        Move(from_=(0, 4), to_=(1, 4))
    ]
    is_stable(states, moves)
