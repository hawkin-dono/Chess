import chess
from ._engine import _get_best_move

def play(board: chess.Board, depth: int = 4):
    return _get_best_move(board, depth)

__all__ = ['play']