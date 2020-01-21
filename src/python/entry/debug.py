from src.python.chess.chess_consts import material
from src.python.chess.chess_state import fen_to_state
from src.python.chess.chess_movement import get_moves, is_attacked_by, Move
from src.python.chess.chess_strategy import horizon_outcome
from src.python.chess.chess_agency import ChessAgent
from src.python.vector2 import v2_range


# fen = "2r3k1/1pq2p1p/p4Qp1/4p3/2B1P2B/4b2P/P1P2PP1/3n2K1 b - - 0 25"
# fen = "1Q2kb1r/p2n1ppp/4q3/4p1B1/4P3/8/PPP2PPP/2KR4 b - - 0 50"

# fen = "r1b1k1nr/Ppqp1ppp/8/8/3p4/5P2/P1PPP1PP/R3KB1R b KQkq - 47 6"

# fen = 'r3k1nr/Pp1p1ppp/8/8/3p4/2P2P2/P2PP1P1/R3KB1q b KQ - 52 9'
fen = "2b1k2r/1p1pnppp/8/8/8/2PP1P2/rq1PR1PP/2K2B1R w k - 58 29"

fen = "r1b1k1nr/Ppqp1ppp/8/8/3p4/5P2/P1PPP1PP/R3KB1R b KQkq - 47 23"
fen = "2bk2nr/rp3pp1/7p/3p2q1/3K2PP/3PPP2/P2P4/1R3B1R b - h3 67 33"
fen = "2b1k1nr/rp1p1ppp/8/6q1/8/1K1P1P2/P2PP1PP/1R3B1R w k - 58 29"
s1 = fen_to_state(fen)

# m = Move(
#     (3, 0),
#     (5, 0),
#     "K"
# )
# s1.apply(m)
# assert s1.is_done

# Test get_move issue
# print(get_moves(s1))

# m = Move(
#     (4, 1),
#     (4, 3)
# )


# # Test trade off issue
# s1.apply(m)
# print(horizon_outcome(s1, "w", "Q", m.to_))

# # Test high level
