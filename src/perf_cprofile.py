# import cProfile
# import pstats
# import io
# from pstats import SortKey
# import time;

from src.chess.chess_state import fen_to_state
from src.chess.chess_agency import ChessAgent
from src.chess.chess_consts import major_pieces


# def calc_depth(chess_state):
#     num_major = 0

#     for pos in s1.positions:
#         if s1.pos(pos) in major_pieces:
#             num_major += 1


if __name__ == "__main__":
    # pr = cProfile.Profile()
    # pr.enable()

    # TODO when castling one side
    # Castling issues removes all

    # t1 = time.time() * 1000
    # bug?
    # r1bqk1nr/pp2p2p/n5p1/2p1Pp2/3p4/2N5/PPP1PPPP/R2QKBNR w KQkq - 0 1
    # r1b1k1nr/pp2p2p/n5p1/qNp1Pp2/3p4/8/PPP1PPPP/R2QKBNR w KQkq - 0 1

    # WTF? (5, 2)???
    # Fen:
    # r1b1k1nr/pp2p3/7p/1q2P1p1/Pnpp1p2/1Q6/1PP1PPPP/2KR1BNR w KQkq - 0 1

    # fen = "2r3k1/1pq2p1p/p2Q1npb/b3p3/2r1P2B/1BN1R2P/PnP2PP1/3R2K1 b - - 0 25"  # GM game modified minus0major: 5: 2s, 6: 21s
    # fen = "2r3k1/1pq2p1p/p4Qp1/4p3/2B1P2B/4b2P/P1P2PP1/3n2K1 b - - 0 25"  # GM game modified minus2major 5: 3s, 6: 9s
    # fen = "2r3k1/1p3p1p/p5p1/4p3/4P2B/7P/P1P2PP1/3n2K1 b - - 0 25"  # GM game modified minus6major 5: 0.5s, 8: 30s
    # fen = "2r3k1/1pq2p1p/p4Qp1/4p3/4P2B/7P/P1P2PP1/3n2K1 b - - 0 25"  # GM game modified minus4major 5: 2s, 6: 10s

    # fen = "4k3/8/8/8/4q3/3P4/8/4K3 w - - 0 50"
    # fen = "2r3k1/1pq2p1p/p2Q1np1/4p3/2r1P3/2N1R2P/P1P2PP1/3R2K1 b - - 0 25"  # GM game

    # fen = "1Q2kb1r/p2n1ppp/4q3/4p1B1/4P3/8/PPP2PPP/2KR4 b - - 0 24"
    # fen = "3r4/7p/7k/4b3/4N1R1/1B1P4/PP1n1PKP/R7 b - - 0 24"
    # fen = "4r3/2p3k1/p7/3P4/8/P2Kq3/1B6/8 w - - 0 1"  # Starting
    fen = "r1bk2nr/pp2p3/7p/4P1p1/q1p2p2/8/1PP1PPPP/2K2BNR w KQkq - 0 1"
    s1 = fen_to_state(fen)
    ca = ChessAgent(6)
    best_path = ca.start_game(s1)

    print()
    print("Fen:")
    print(fen)
    print()
    print("CriticalPath:")
    for m in best_path:
        print(m)

    # pr.disable()
    # s = io.StringIO()
    # ps = pstats.Stats(pr, stream=s)\
    #     .sort_stats(SortKey.TIME)
        # .sort_stats(SortKey.CUMULATIVE)

    # ps.print_stats()
    # ps.print_callers()
    # print(s.getvalue())

    # print(time.time() * 1000 - t1)
