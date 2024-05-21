from chess import Move, QUEEN, BB_ALL, BLACK, WHITE, BB_PAWN_ATTACKS, square_rank, msb, scan_reversed

def generate_pseudo_legal_promotion_queen(board, from_mask = BB_ALL, to_mask = BB_ALL):
    pawns = board.pawns & board.occupied_co[board.turn] & from_mask
    if not pawns:
        return
    for from_square in scan_reversed(pawns):
        targets = (
            BB_PAWN_ATTACKS[board.turn][from_square] &
            board.occupied_co[not board.turn] & to_mask)

        for to_square in scan_reversed(targets):
            if square_rank(to_square) in [0, 7]:
                yield Move(from_square, to_square, QUEEN)

    if board.turn == WHITE:
        single_moves = pawns << 8 & ~board.occupied
    else:
        single_moves = pawns >> 8 & ~board.occupied
    single_moves &= to_mask

    for to_square in scan_reversed(single_moves):
        from_square = to_square + (8 if board.turn == BLACK else -8)
        if square_rank(to_square) in [0, 7]:
            yield Move(from_square, to_square, QUEEN)

def generate_legal_promotion_queen(board, from_mask = BB_ALL, to_mask = BB_ALL):
    king_mask = board.kings & board.occupied_co[board.turn]
    if king_mask:
        king = msb(king_mask)
        blockers = board._slider_blockers(king)
        checkers = board.attackers_mask(not board.turn, king)
        if checkers:
            for move in board._generate_evasions(king, checkers, from_mask, to_mask):
                if move.promotion == QUEEN and board._is_safe(king, blockers, move):
                    yield move
        else:
            for move in generate_pseudo_legal_promotion_queen(board, from_mask, to_mask):
                if board._is_safe(king, blockers, move):
                    yield move