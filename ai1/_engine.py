import random
import chess
from ._heuristic import score, sort_moves
from ._opening_book import OPENING_BOOK

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



def minimax(board : chess.Board, depth: int, alpha: float, beta: float, turn: int = 1):
    if board.is_game_over(): return None, -turn * score(board, is_game_over=True)
    if depth == 0: return None, -turn * score(board)

    legal_moves = list(board.legal_moves)
    sort_moves(board, legal_moves)
    
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
    






def _get_best_move(board: chess.Board):
    if (board.fullmove_number <= 20):
        board_fen = board.fen()
        if board_fen in OPENING_BOOK[board.turn]:
            move = random.choice(OPENING_BOOK[board.turn][board_fen])
            return chess.Move.from_uci(move), 0
    DEPTH = 4
    return minimax(board, DEPTH, -float('inf'), float('inf'))

