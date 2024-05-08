import chess
import chess.syzygy
import time
import ai1
import chess.polyglot


if __name__ == "__main__":
    board = chess.Board()
    # board = chess.Board("r2q1rk1/1bpnbppp/p3pn2/1p6/3P1B2/2NBPN2/PPQ2PPP/R4RK1 w - - 2 12")
    # board = chess.Board("6k1/pp4p1/2p5/2bp4/8/P5Pb/1P3rrP/2BRRN1K b - - 0 1")
    # board = chess.Board("8/5P2/8/8/8/6K1/3k4/8 w - - 1 9")
    # board = chess.Board("r2q1rk1/1bpnbppp/p3pn2/1p6/3P1B2/2NBPN2/PPQ2PPP/R4RK1 w - - 2 12")
    # board = chess.Board("4q1k1/5ppp/1p6/2p5/p1P5/P2P1N2/1b2rPPP/1Q1R1K2 w - - 0 28") 
    # board = chess.Board("6k1/5ppp/1p6/2p1q3/p1Pb4/P2P3N/6PP/1Q1R1K2 w - - 5 32")
    # board = chess.Board("8/5k2/1p2p3/2p2p2/p1Pn2q1/P2Q2P1/1P3P2/5BK1 b - - 0 37")
    # board = chess.Board("6r1/7p/5k1P/1pP5/5p2/3n4/5PPK/2q5 w - - 0 46")
    # board = chess.Board("r7/4k1Pp/2n1p3/1pb5/3p3N/3P4/2P2PPP/4BRK1 w - - 0 29")
    # board = chess.Board("6k1/5pp1/1p2q3/2p4p/p1P5/P2P4/6PP/1Q4K1 w - - 0 37")
    # board = chess.Board("2k2bnr/rp3b1p/p1q2N2/P1p1ppB1/3p4/3P2NP/1PP2PP1/1R1Q1RK1 w - - 7 25")
    # board = chess.Board("r1bqkb1r/pp1ppppp/2n2n2/2p5/2P5/2N2N2/PP1PPPPP/R1BQKB1R w KQkq - 3 4")
    # board = chess.Board("r2q1rk1/1bpnbppp/p3pn2/1p6/3P1B2/2NBPN2/PPQ2PPP/R4RK1 w - - 2 12")
    # board = chess.Board("4q1k1/5ppp/1p6/2p5/p1P5/P2P1N2/1b2rPPP/1Q1R1K2 w - - 0 28")
    # board = chess.Board("6k1/5ppp/1p6/2p1q3/p1Pb4/P2P3N/6PP/1Q1R1K2 w - - 5 32")
    # board = chess.Board("r7/4k1Pp/2n1p3/1pb5/3p3N/3P4/2P2PPP/4BRK1 w - - 0 29")
    # board = chess.Board("r7/4k1Pp/2n1p3/1p6/1b5N/2pP4/5PPP/5RK1 w - - 0 31")
    # board = chess.Board("8/5k2/1p2p3/2p2p2/p1Pn2q1/P2Q2P1/1P3P2/5BK1 b - - 0 37")
    # board = chess.Board("5k2/Q6p/3p2p1/1P1P4/1PK3P1/P7/5P2/3q4 b - - 0 38")
    # board = chess.Board("5k2/Q6p/3p2p1/1P1P4/1P1K2P1/P7/2q2P2/8 b - - 2 39")
    # board = chess.Board("4k3/8/8/8/8/8/8/4KBN1 w - - 0 1")
    # board = chess.Board("1k6/1N6/1K2B3/8/8/8/8/8 w - - 54 28")
    # board = chess.Board("4k3/8/8/8/8/8/8/4KBN1 w - - 0 1") 
    # board = chess.Board("4k3/8/8/8/8/3B4/8/4K1N1 b - - 1 1")

    start_time = time.time()
    move = ai1.get_best_move(board)
    end_time = time.time()  
    print(move, end_time - start_time)

    # board = chess.Board("4k3/8/8/8/8/8/8/4KBN1 w - - 0 1")
    # board = chess.Board("8/4k3/8/8/8/3B4/8/4K1N1 w - - 2 2")
    # board = chess.Board("8/4k3/8/8/8/3B4/8/4K1N1 w - - 2 2")
    # board = chess.Board("k7/3B4/NK6/8/8/8/8/8 w - - 60 31")
    # board = chess.Board("1k6/3B4/1K6/2N5/8/8/8/8 w - - 58 30")
    # board = chess.Board("4k3/8/8/8/8/3B4/8/4K1N1 b - - 1 1")

    # board = chess.Board("1k6/8/1K2B3/2N5/8/8/8/8 b - - 55 28")
    # path_to_tablebase = "ai1/data/syzygy/3-4-5"
    # tablebase = chess.syzygy.open_tablebase(path_to_tablebase)
    # start_time = time.time()
    # z = tablebase.probe_wdl(board)
    # end_time = time.time()  
    # print(z)
    # print(end_time - start_time)

    # hàm lấy số quân cờ trên bàn cờ
    # OPENING_BOOK = chess.polyglot.open_reader("ai1/data/opening_book/3210elo.bin")
    # move = OPENING_BOOK.weighted_choice(board).move
    # move = OPENING_BOOK.get(board).move
    # print(move)
    