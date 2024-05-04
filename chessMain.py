import random
import chess
from chess import Move
from heuristic import score
from data.opening_book import MOVES
from time import time


# def get_all_favourite_moves(board : chess.Board) -> list:
#     legal_moves = list(board.legal_moves)
#     moves = []
#     for move in legal_moves:
#         board.push(move)
#         moves.append((move, score(board)))
#         board.pop()

#     moves.sort(key = lambda x: x[1], reverse = True)
#     size = min(8, len(moves))
#     all_favourite_moves = [move for move, _ in moves[:size]]
#     return all_favourite_moves


# def is_favorable_move(board : chess.Board, move : chess.Move) -> bool:
#     return True

# def get_all_favourite_moves(board : chess.Board) -> list:
#     return [move for move in list(board.legal_moves) if is_favorable_move(board, move)]

# def quiesecence(board : chess.Board, depth, alpha, beta, turn):
#     if depth == 0 or board.is_game_over():
#         return score(board)
    
#     legal_moves = [move for move in board.legal_moves if (board.is_capture(move) or move.promotion != None)]
#     if len(legal_moves) == 0:
#         return score(board)
    
#     if turn == 1:
#         max_eval = float('-inf')
#         for move in legal_moves:
#             board.push(move)
#             eval = quiesecence(board, depth - 1, alpha, beta, -1)
#             board.pop()
#             if eval > max_eval:
#                 max_eval = eval
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for move in legal_moves:
#             board.push(move)
#             eval = quiesecence(board, depth - 1, alpha, beta, 1)
#             board.pop()
#             if eval < min_eval:
#                 min_eval = eval
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break
#         return min_eval

# def quiesecence(board : chess.Board, alpha, beta, turn):
#     stand_pat = -turn * score(board)
#     if stand_pat >= beta:
#         return beta
#     if alpha < stand_pat:
#         alpha = stand_pat
#     for move in board.legal_moves:
#         if board.is_capture(move) or move.promotion != None:
#             board.push(move)
#             value = quiesecence(board, alpha, beta, -turn)
#             board.pop()
#             if value >= beta:
#                 return beta
#             if value > alpha:
#                 alpha = value
#     return alpha



def minimax(board : chess.Board, depth, alpha, beta, turn = 1):
    if depth == 0 or board.is_game_over():
        return None, -turn * score(board)
        # return None, quiesecence(board, 3, alpha, beta, turn)

    legal_moves = board.legal_moves
    if turn == 1:
        max_eval = float('-inf')
        best_move = None
        for move in legal_moves:
            board.push(move)
            _, eval = minimax(board, depth - 1, alpha, beta, -1)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return (best_move, max_eval)
    else:
        min_eval = float('inf')
        best_move = None
        for move in legal_moves:
            board.push(move)
            _, eval = minimax(board, depth - 1, alpha, beta, 1)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return (best_move, min_eval)
        
def get_best_move(board: chess.Board, depth):
    if (board.fullmove_number <= 10):
        board_fen = board.fen()
        if board_fen in MOVES[board.turn]:
            move = random.choice(MOVES[board.turn][board_fen])
            return Move.from_uci(move), 0
    DEPTH = 4
    return minimax(board, DEPTH, -float('inf'), float('inf'))

if __name__ == "__main__":
    # Puzzle 1: 2-move checkmate (Rook Sac)
    # board = chess.Board("6k1/pp4p1/2p5/2bp4/8/P5Pb/1P3rrP/2BRRN1K b - - 0 1")   # 38  15.6
    # board = chess.Board("r2q1rk1/1bpnbppp/p3pn2/1p6/3P1B2/2NBPN2/PPQ2PPP/R4RK1 w - - 2 12")  # 51  65
    # board = chess.Board("4q1k1/5ppp/1p6/2p5/p1P5/P2P1N2/1b2rPPP/1Q1R1K2 w - - 0 28")  # 21   14
    # board = chess.Board("6k1/5ppp/1p6/2p1q3/p1Pb4/P2P3N/6PP/1Q1R1K2 w - - 5 32")  # 18    4.5
    # board = chess.Board("8/5k2/1p2p3/2p2p2/p1Pn2q1/P2Q2P1/1P3P2/5BK1 b - - 0 37")  # 29   10.8

    # board = chess.Board("6r1/7p/5k1P/1pP5/5p2/3n4/5PPK/2q5 w - - 0 46")
    # board = chess.Board("r7/4k1Pp/2n1p3/1pb5/3p3N/3P4/2P2PPP/4BRK1 w - - 0 29")

    # board = chess.Board("6k1/5pp1/1p2q3/2p4p/p1P5/P2P4/6PP/1Q4K1 w - - 0 37")


    # board = chess.Board("8/5k2/1p2p3/2p2p2/p1Pn2q1/P2Q2P1/1P3P2/5BK1 b - - 0 37")
    # board = chess.Board("r1bqkb1r/pp1ppppp/2n2n2/2p5/2P5/2N2N2/PP1PPPPP/R1BQKB1R w KQkq - 3 4")
    # board = chess.Board("1r4k1/6p1/4p3/RP4p1/4Br2/5P2/7P/6K1 w - - 0 33")
    # board = chess.Board("r7/4k1Pp/2n1p3/1p6/1b5N/2pP4/5PPP/5RK1 w - - 0 31")


    # "2k2bnr/rp3b1p/p1q2N2/P1p1ppB1/3p4/3P2NP/1PP2PP1/1R1Q1RK1 w - - 7 25"
    board = chess.Board("2k2bnr/rp3b1p/p1q2N2/P1p1ppB1/3p4/3P2NP/1PP2PP1/1R1Q1RK1 w - - 7 25")

    print(board)



    start_time = time()
    # move, heu = minimax(board, 6, 6, -float('inf'), float('inf'))
    move, heu = get_best_move(board, 4)
    end_time = time()
    print("Thời gian chạy: ", end_time - start_time, "s")

    print(move, heu)


    # test
    # board = chess.Board('8/5k2/1p2p3/2p2p2/p1P3q1/P2Q1nP1/1P3P2/5BK1 w - - 1 38')
    # print(board)
    # print(board.turn)
    # moves = list(board.legal_moves)
    # board.push(moves[0])
    # print(board.turn)
    # print(moves)
