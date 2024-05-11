import chess
from chess import scan_reversed
from chess.polyglot import zobrist_hash
from ._heuristic import is_null_ok, organize_moves, organize_moves_quiescence, score

cache = {}
is_end_game = False
OPENING_BOOK = chess.polyglot.open_reader("ai1/data/opening_book/3210elo.bin")

def quiesecence(board : chess.Board, depth: int, MAX_DEPTH: int, is_end_game: bool, alpha: float, beta: float, turn: int):
    if (depth < MAX_DEPTH) and (board.outcome() is not None): return -turn * score(board, is_end_game, is_game_over=True)
    if depth == 0: return -turn * score(board, is_end_game)

    moves = organize_moves_quiescence(board)
    if not moves: return -turn * score(board, is_end_game)
    
    if turn == 1:
        max_eval = float('-inf')
        for move in moves:
            board.push(move)
            eval = quiesecence(board, depth - 1, MAX_DEPTH, is_end_game, alpha, beta, -1)
            board.pop()
            if eval > max_eval:
                max_eval = eval
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            board.push(move)
            eval = quiesecence(board, depth - 1, MAX_DEPTH, is_end_game, alpha, beta, 1)
            board.pop()
            if eval < min_eval:
                min_eval = eval
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval    

def minimax(board : chess.Board, depth: int, cache: dict, is_end_game: bool, alpha: float = -float('inf'), beta: float = float('inf'), turn: int = 1):
    if board.outcome() is not None: return None, -turn * score(board, is_end_game, is_game_over=True)

    cache_key = (zobrist_hash(board), (depth if depth >= 0 else 0), alpha, beta, turn)
    try: return cache[cache_key]
    except: pass

    if depth <= 0: 
        eval = quiesecence(board, 12, 12, is_end_game, alpha, beta, turn)
        cache[cache_key] = (None, eval)
        return None, eval
                
    # null move pruning
    if turn == 1:
        if (not is_end_game) and (beta != float('inf')) and ((1 < depth < 4) or ((-turn * score(board, is_end_game)) >= beta)):
            if is_null_ok(board):
                board.push(chess.Move.null())
                _, eval = minimax(board, depth - 3, cache, is_end_game, alpha, beta, -1)
                board.pop()
                if eval >= beta: return None, beta
    else:
        if (not is_end_game) and (alpha != -float('inf')) and ((1 < depth < 4) or ((-turn * score(board, is_end_game)) <= alpha)):
            if is_null_ok(board):
                board.push(chess.Move.null())
                _, eval = minimax(board, depth - 3, cache, is_end_game, alpha, beta, 1)
                board.pop()
                if eval <= alpha: return None, alpha

    legal_moves = organize_moves(board)
    
    if turn == 1:
        max_eval = float('-inf')
        best_move = None
        for move in legal_moves:
            board.push(move)
            _, eval = minimax(board, depth - 1, cache, is_end_game, alpha, beta, -1)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        cache[cache_key] = (best_move, max_eval)
        return (best_move, max_eval)
    else:
        min_eval = float('inf')
        best_move = None
        for move in legal_moves:
            board.push(move)
            _, eval = minimax(board, depth - 1, cache, is_end_game, alpha, beta, 1)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        cache[cache_key] = (best_move, min_eval)
        return (best_move, min_eval)

def _get_best_move(board: chess.Board):
    try: return OPENING_BOOK.weighted_choice(board).move.uci()
    except:
        global cache, is_end_game
        if (not is_end_game) and (len(list(scan_reversed(board.occupied))) <= 5):
            is_end_game = True
            cache = {}

        move, _ = minimax(board, 4, cache, is_end_game)
        return move.uci()