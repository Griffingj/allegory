from src.chess.chess_state import fen_to_state
from src.chess.chess_agency import ChessAgent
from src.chess.chess_movement import get_moves, is_attacked_by
from src.vector2 import v2_range


# s1 = fen_to_state("6k1/8/8/8/8/3n4/P6P/R3K2R w KQ - 0 50")
# moves = get_moves(s1)
# print(moves)


# s1 = fen_to_state("6k1/8/8/8/8/3n4/8/4K3 w - - 0 50")
# assert is_attacked_by(s1, (7, 4), (5, 3))


assert list(v2_range((-3, -3), (2, 2))) == [(-2, -2), (-1, -1), (0, 0), (1, 1)]
assert list(v2_range((-5, 0), (0, 0))) == [(-4, 0), (-3, 0), (-2, 0), (-1, 0)]
assert list(v2_range((3, 6), (3, 3))) == [(3, 5), (3, 4)]