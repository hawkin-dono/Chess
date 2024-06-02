from collections import OrderedDict
from chess import Board, Move, QUEEN, BLACK, WHITE, BB_RANK_1, BB_RANK_8, msb, scan_reversed

def generate_legal_promotion_queen_non_capture(board: Board):
    """Hàm tạo các nước đi phong hậu không ăn quân đối phương."""
    pawns = board.pawns & board.occupied_co[board.turn]
    if not pawns: return

    if board.turn == WHITE: 
        to_mask = (pawns << 8 & ~board.occupied) & BB_RANK_8
    else: 
        to_mask = (pawns >> 8 & ~board.occupied) & BB_RANK_1
    if not to_mask: return

    king_mask = board.kings & board.occupied_co[board.turn]
    if king_mask:
        king = msb(king_mask)
        blockers = board._slider_blockers(king)
        checkers = board.attackers_mask(not board.turn, king)
        if checkers:
            from_mask = (to_mask >> 8) if board.turn == WHITE else (to_mask << 8)
            for move in board._generate_evasions(king, checkers, from_mask, to_mask):
                if move.promotion == QUEEN and board._is_safe(king, blockers, move):
                    yield move
        else:
            for to_square in scan_reversed(to_mask):
                from_square = to_square + (8 if board.turn == BLACK else -8)
                move = Move(from_square, to_square, QUEEN)
                if board._is_safe(king, blockers, move):
                    yield move

def is_draw(board: Board):
    return (board.is_insufficient_material() 
            or (not any(board.generate_legal_moves())) 
            or board.is_fifty_moves() 
            or board.is_repetition(3))

class TranspositionTable:
    def __init__(self, max_size: int = 100000):
        self.__max_size = max_size
        self.__table = OrderedDict()

    def add(self, key, value):
        if key in self.__table:
            self.__table.move_to_end(key)
        elif len(self.__table) >= self.__max_size:
            self.__table.popitem(last=False)
        self.__table[key] = value

    def get(self, key, depth, alpha, beta):
        if key not in self.__table: 
            return None
        
        v_depth, v_move, v_eval = self.__table[key]
        
        if depth <= v_depth: 
            if v_depth == 0:
                return v_move, v_eval
            
            if key[-1] == 1:
                if v_eval <= alpha: 
                    return v_move, v_eval
            else:
                if v_eval >= beta: 
                    return v_move, v_eval
        
        return None
    
    def __contains__(self, key):
        return key in self.__table


