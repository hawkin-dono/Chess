import chess
from ._engine import _get_best_move

def get_best_move(board: chess.Board):
    return _get_best_move(board)

__all__ = ['get_best_move']