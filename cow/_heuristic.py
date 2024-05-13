from chess import Board, Move, PAWN, QUEEN, KING, scan_reversed
from chess.syzygy import open_tablebase
from ._pesto_evaluation import calculate_score
from ._piece_evaluation import get_move_static_score

END_GAME_SCORE = 1000000
EGTABLEBASE = open_tablebase("cow/data/syzygy/3-4-5")

def score(board: Board, is_end_game: bool, is_game_over: bool = False) -> float:
    if is_game_over:
        if board.is_check(): return END_GAME_SCORE + END_GAME_SCORE / (board.fullmove_number + 1)
        return 0
    if is_end_game:
        dtz = -EGTABLEBASE.get_dtz(board, 0)
        if dtz > 0: return END_GAME_SCORE - dtz
        if dtz < 0: return -END_GAME_SCORE - dtz
    return calculate_score(board) 

PIECE_VALUES = [10, 30, 30, 50, 90, 1000]  # pawn, knight, bishop, rook, queen, king

def get_move_score(board: Board, move: Move) -> int:
    if move.promotion == QUEEN: return 1
    if board.is_capture(move): 
        if board.is_en_passant(move): return 0
        if not board.attackers(not board.turn, move.to_square): return PIECE_VALUES[board.piece_type_at(move.to_square) - 1]
        return PIECE_VALUES[board.piece_type_at(move.to_square) - 1] - PIECE_VALUES[board.piece_type_at(move.from_square) - 1]
    return (-2 * PIECE_VALUES[KING - 1]) + get_move_static_score(board, move)

def organize_moves_quiescence(board: Board) -> list[Move]:
    moves = [move for move in board.generate_legal_moves() if (get_move_score(board, move) > 0)]
    moves.sort(key=lambda move: get_move_score(board, move), reverse=True)
    return moves

def organize_moves(board: Board) -> list[Move]:
    moves = list(board.generate_legal_moves())
    moves.sort(key=lambda move: get_move_score(board, move), reverse=True)
    return moves

def is_null_ok(board: Board) -> bool:
    if board.is_check(): return False
    if board.peek == Move.null(): return False
    for square in scan_reversed(board.occupied):
        piece = board.piece_at(square)
        if (piece.color == board.turn) and (piece.piece_type not in [KING, PAWN]):
            return True
    return False



