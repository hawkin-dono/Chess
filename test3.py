from cProfile import Profile
from pstats import SortKey, Stats
import chess
from cow import play

# board = chess.Board('1k6/1N6/1K2B3/8/8/8/8/8 w - - 54 28')
board = chess.Board("r2qr1k1/1bp2ppp/p7/1p1pP3/3P2Q1/1P2R3/1P1N1PPP/R5K1 b - - 2 17")


with Profile() as profile:
    print(f"{play(board) = }")
    (
        Stats(profile)
        .strip_dirs()
        .sort_stats(SortKey.TIME)
        .print_stats()
    )