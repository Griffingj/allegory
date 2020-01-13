from src.chess.chess_state import fen_to_state
from src.chess.chess_agency import ChessAgent
from src.chess.chess_movement import Move


def test_obvious_mate():
    s1 = fen_to_state("2r3k1/1p3p1p/p5p1/4p3/4P2B/8/PP1n1PPP/6K1 b - - 0 25")
    ca = ChessAgent(3)
    assert list(ca.start_game(s1)) == [
        Move(from_=(0, 2), to_=(7, 2), victim=None, new_en_passant_target=None, ept_cap=None, new_castling_available=None, castle=None)
    ]

# Queen Sac Mate
# fen = "1b2kb1r/p2n1ppp/4q3/4p1B1/4P3/1Q6/PPP2PPP/2KR4 w - - 0 24"  # "Opera" queen sac mate




# Doesn't play rest of game??
# Fen:
# 1Q2kb1r/p2n1ppp/4q3/4p1B1/4P3/8/PPP2PPP/2KR4 b - - 0 24

# CriticalPath:
#          5344487 function calls (5303362 primitive calls) in 2.364 seconds