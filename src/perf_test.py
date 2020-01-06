import cProfile
import pstats
import io
from pstats import SortKey

from src.chess.chess_state import fen_to_state
from src.chess.chess_agency import ChessAgent


def do_test():
    pr = cProfile.Profile()
    pr.enable()


    # s1 = fen_to_state("4k3/8/8/8/4q3/3P4/8/4K3 w - - 0 50")
    s1 = fen_to_state("2r3k1/1pq2p1p/p2Q1np1/4p3/2r1P3/2N1R2P/P1P2PP1/3R2K1 b - - 0 25") # GM game
    # s1 = fen_to_state("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    ca = ChessAgent(4)
    best = ca.start_game(s1)
    print(best)

    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s)\
        .sort_stats(SortKey.CUMULATIVE)
        # .sort_stats(SortKey.TIME)

    ps.print_stats()
    print(s.getvalue())
