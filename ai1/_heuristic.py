import chess
import chess.syzygy
from ._pesto_evaluation import calculate_score
from ._piece_evaluation import get_move_static_score

END_GAME_SCORE = 1000000000
TABLEBASE = chess.syzygy.open_tablebase("ai1/data/syzygy/3-4-5")

def score(board: chess.Board, is_end_game: bool, is_game_over: bool = False):
    if is_game_over:
        if board.is_check(): return END_GAME_SCORE + END_GAME_SCORE / (board.fullmove_number + 1)
        else: return 0
    if is_end_game:
        dtz = -TABLEBASE.probe_dtz(board)
        if dtz > 0: return END_GAME_SCORE - dtz
        if dtz < 0: return -END_GAME_SCORE - dtz
        return 0
    return calculate_score(board) 

PIECE_VALUES = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 1000,
}

def get_move_score(board: chess.Board, move: chess.Move):
    if move.promotion == chess.QUEEN: return 1
    if board.is_capture(move): 
        if board.is_en_passant(move): return 0
        if len(board.attackers(not board.turn, move.to_square)) == 0: return PIECE_VALUES[board.piece_type_at(move.to_square)]
        return PIECE_VALUES[board.piece_type_at(move.to_square)] - PIECE_VALUES[board.piece_type_at(move.from_square)]
    return get_move_static_score(board, move, PIECE_VALUES[chess.KING])

def organize_moves_quiescence(board: chess.Board):
    moves = [move for move in board.legal_moves if (get_move_score(board, move) > 0)]
    moves.sort(key=lambda move: get_move_score(board, move), reverse=True)
    return moves

def organize_moves(board: chess.Board):
    moves = list(board.legal_moves)
    moves.sort(key=lambda move: get_move_score(board, move), reverse=True)
    return moves

def is_null_ok(board: chess.Board) -> bool:
    if board.is_check(): return False
    if board.peek == chess.Move.null(): return False
    for piece in board.piece_map().values():
        if (piece.color == board.turn) and (piece.piece_type not in [chess.KING, chess.PAWN]):
            return True
    return False

