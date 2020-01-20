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

# states = [
#     "4k3/1P6/8/8/8/8/8/4K3 w - - 0 25",
#     "1Q2k3/8/8/8/8/8/8/4K3 b - - 0 25",
#     "1Q6/4k3/8/8/8/8/8/4K3 w - - 0 26"
# ]

# moves = [
#     Move(from_=(1, 1), to_=(0, 1)),
#     Move(from_=(0, 4), to_=(1, 4))
# ]

# undos = []

# s1 = fen_to_state(states[0])

# for i, m in enumerate(moves):
#     undos.append(s1.apply(m))
#     assert s1.to_fen() == states[i + 1]

# for i, u in enumerate(reversed(undos)):
#     s1.undo(u)
#     assert s1.to_fen() == states[len(states) - 2 - i]
m = Move(
    (4, 1),
    (4, 3)
)

s1 = fen_to_state("3r2k1/q7/8/8/1Q6/2K5/4N3/8 w - - 0 50")
s1.apply(m)
assert horizon_outcome(s1, "Q", m.to_) == -(material["r"] + material["Q"])
