import chess
from heuristic import *

def alpha_beta_pruning(board : chess.Board, depth, alpha, beta, turn):
    if depth == 0 or board.outcome() != None:
        return None, turn * score(board)
    
    if turn == 1:
        max_eval = float('-inf')
        best_move = None
        node = list(board.legal_moves)
        for move in node:
            board.push(move)
            _, eval = alpha_beta_pruning(board, depth - 1, alpha, beta, -1)
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
        node = list(board.legal_moves)
        for move in node:
            board.push(move)
            _, eval = alpha_beta_pruning(board, depth - 1, alpha, beta, 1)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return (best_move, min_eval)
    
def get_best_move(board: chess.Board, depth):
    return alpha_beta_pruning(board, depth, -float('inf'), float('inf'), 1)

# Puzzle 1: 2-move checkmate (Rook Sac)
board = chess.Board("6k1/pp4p1/2p5/2bp4/8/P5Pb/1P3rrP/2BRRN1K b - - 0 1")
move, heu = alpha_beta_pruning(board, 5, -float('inf'), float('inf'), 1)
print(move, heu)
