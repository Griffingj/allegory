import cProfile
import pstats
import io
from pstats import SortKey
from datetime import datetime
from os import path

from root import ROOT_DIR
from src.python.chess.chess_state import fen_to_state
from src.python.chess.chess_agency import ChessAgent


if __name__ == "__main__":
    profile = cProfile.Profile()
    profile.enable()

    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # Starting
    fen = "2r3k1/1pq2p1p/p4Qp1/4p3/2B1P2B/4b2P/P1P2PP1/3n2K1 b - - 50 25"  # GM game modified minus2major 5: 3s, 6: 9s
    fen = "2r3k1/1p3p1p/p5p1/4p3/4P2B/7P/P1P2PP1/3n2K1 b - - 50 25"  # GM game modified minus6major 5: 0.5s, 8: 30s
    fen = "2r3k1/1pq2p1p/p4Qp1/4p3/4P2B/7P/P1P2PP1/3n2K1 b - - 50 25"  # GM game modified minus4major 5: 2s, 6: 10s
    fen = "2r3k1/1pq2p1p/p2Q1npb/b3p3/2r1P2B/1BN1R2P/PnP2PP1/3R2K1 b - - 50 25"  # GM game modified minus0major: 5: 2s, 6: 21s
    fen = "r1b3kr/6pp/p1n1pp2/1pBQ2N1/4BP2/1P1P4/Pq4PP/5RK1 b - - 50 25"  # IM eric rosen youtube https://youtu.be/XqNlxdpRmp0
    fen = "r1b3kr/6pp/p1n1pp2/1pB5/2Q1BP2/1P1P1N2/Pq4PP/5RK1 w - - 50 25"  # IM double sac eric rosen youtube https://youtu.be/XqNlxdpRmp0

    # fen = "4k3/8/8/8/4q3/3P4/8/4K3 w - - 0 50"
    # fen = "2r3k1/1pq2p1p/p2Q1np1/4p3/2r1P3/2N1R2P/P1P2PP1/3R2K1 b - - 0 25"  # GM game
    # fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR"
    fen = "1b2kb1r/p2n1ppp/4q3/4p1B1/4P3/1Q6/PPP2PPP/2KR4 w - - 0 24"
    s1 = fen_to_state(fen)
    ca = ChessAgent(6)
    (balance, best_path) = ca.start_game(s1)
    buf = io.StringIO()

    print("\nCounts", file=buf)
    print(ca.diag.counts, file=buf)
    print("\nBalance", file=buf)
    print(balance, file=buf)
    print("\nDepth", file=buf)
    print(ca.search_depth, file=buf)
    print("\nFen", file=buf)
    print(fen, file=buf)
    print("\nCriticalPath", file=buf)
    for m in best_path:
        print(m, file=buf)

    print("", file=buf)
    profile.disable()
    ps = pstats.Stats(profile, stream=buf).sort_stats(SortKey.TIME)
    ps.print_stats()
    ps.print_callers()
    now = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    path = path.abspath(path.join(ROOT_DIR, "perf", f"{now}_perf.log"))

    # print(stream.getvalue())
    with open(path, "w+") as f:
        print(buf.getvalue(), file=f)
    print(f"Report written to {path}")
