from src.chess.chess_consts import material
from src.chess.chess_state import fen_to_state
from src.chess.chess_movement import get_moves, is_attacked_by, Move
from src.chess.chess_strategy import horizon_outcome
from src.chess.chess_agency import ChessAgent
from src.vector2 import v2_range


# fen = "6k1/8/8/8/8/3n4/P6P/R3K2R w KQ - 0 50"
fen = "1Q2kb1r/p2n1ppp/4q3/4p1B1/4P3/8/PPP2PPP/2KR4 b - - 0 50"
s1 = fen_to_state(fen)

# s1.apply(
#     Move(from_=(1, 3), to_=(0, 1), victim="Q")
# )
ca = ChessAgent(3)
best_path = list(ca.start_game(s1))
print(best_path)
