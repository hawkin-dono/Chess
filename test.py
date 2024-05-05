import chess
import time
import ai1

if __name__ == "__main__":
    # board = chess.Board("r2q1rk1/1bpnbppp/p3pn2/1p6/3P1B2/2NBPN2/PPQ2PPP/R4RK1 w - - 2 12")
    board = chess.Board("6k1/pp4p1/2p5/2bp4/8/P5Pb/1P3rrP/2BRRN1K b - - 0 1")
    start_time = time.time()
    move, heu = ai1.get_best_move(board)
    end_time = time.time()  
    print(move, heu, end_time - start_time)