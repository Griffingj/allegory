from src.python.chess.chess_consts import material
from src.python.chess.chess_state import fen_to_state
from src.python.chess.chess_movement import get_moves, is_attacked_by, Move
from src.python.chess.chess_strategy import horizon_outcome
from src.python.chess.chess_agency import ChessAgent
from src.python.vector2 import v2_range


# fen = "2r3k1/1pq2p1p/p4Qp1/4p3/2B1P2B/4b2P/P1P2PP1/3n2K1 b - - 0 25"
# fen = "1Q2kb1r/p2n1ppp/4q3/4p1B1/4P3/8/PPP2PPP/2KR4 b - - 0 50"
# s1 = fen_to_state(fen)

# # s1.apply(
# #     Move(from_=(1, 3), to_=(0, 1), victim="Q")
# # )
# ca = ChessAgent(4)
# best_path = list(ca.start_game(s1))
# print(best_path)



states = [
    "r3k2r/p6p/1p6/8/8/8/P6P/R3K2R w KQkq b6 0 25",
    "r3k2r/p6p/1p6/8/8/8/P6P/R4RK1 b kq - 0 25",
    "2kr3r/p6p/1p6/8/8/8/P6P/R4RK1 w - - 0 26",
    "2kr3r/p6p/1p6/8/8/8/P5KP/R4R2 b - - 0 26",
]

moves = [
    Move(from_=(7, 4), to_=(7, 6), new_castling_available='kq', castle='K'),
    Move(from_=(0, 4), to_=(0, 2), new_castling_available='-', castle='q'),
    Move(from_=(7, 6), to_=(6, 6))
]

undos = []

s1 = fen_to_state(states[0])

for i, m in enumerate(moves):
    undos.append(s1.apply(m))
    assert s1.to_fen() == states[i + 1]

for i, u in enumerate(reversed(undos)):
    s1.undo(u)
    assert s1.to_fen() == states[len(states) - 2 - i]