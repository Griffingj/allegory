from src.chess.chess_consts import material
from src.chess.chess_state import fen_to_state
from src.chess.chess_movement import get_moves, is_attacked_by, Move
from src.chess.chess_strategy import horizon_outcome
from src.chess.chess_agency import ChessAgent
from src.vector2 import v2_range


fen = "2r3k1/1pq2p1p/p4Qp1/4p3/2B1P2B/4b2P/P1P2PP1/3n2K1 b - - 0 25"
fen = "1Q2kb1r/p2n1ppp/4q3/4p1B1/4P3/8/PPP2PPP/2KR4 b - - 0 50"
s1 = fen_to_state(fen)

# s1.apply(
#     Move(from_=(1, 3), to_=(0, 1), victim="Q")
# )
ca = ChessAgent(4)
best_path = list(ca.start_game(s1))
print(best_path)
