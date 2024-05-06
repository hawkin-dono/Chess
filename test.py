import chess
import time
import ai1

if __name__ == "__main__":
    board = chess.Board("r2q1rk1/1bpnbppp/p3pn2/1p6/3P1B2/2NBPN2/PPQ2PPP/R4RK1 w - - 2 12")
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

    start_time = time.time()
    move = ai1.get_best_move(board)
    end_time = time.time()  
    print(move, end_time - start_time)
    board.is_check()