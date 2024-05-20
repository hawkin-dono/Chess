import chess
from ._engine import _get_best_move

def get_best_move(board: chess.Board, depth: int = 4):
    return _get_best_move(board, depth)

__all__ = ['get_best_move']