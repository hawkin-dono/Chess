import chess

from .board_graphics import *

unicode_to_algebraic = {
    '♚': 'K', '♛': 'Q', '♜': 'R', '♝': 'B', '♞': 'N', '♟': 'P',
    '♔': 'k', '♕': 'q', '♖': 'r', '♗': 'b', '♘': 'n', '♙': 'p'
}

promotion_code = ['q', 'r', 'b', 'n']
promotion_list = ['queen', 'rook', 'bishop', 'knight']

class board:
    def __init__(self, width, height, player):
        self.width = width
        self.height = height
        self.square_height = height // 8
        self.square_width = width // 8
        self.selected_piece = None
        self.promotion = None
        self.list_valid_moves = []

        self.board = chess.Board() 
        self.draw_board = self.convert_board()
        self.player = player
        self.turn = True

        self.move_history = []
   

        
    def convert_board(self): #type(board) == chess.Board()
        pgn = self.board.epd()
        foo = []  #Final board
        pieces = pgn.split(" ", 1)[0]
        rows = pieces.split("/")
        for row in rows:
            foo2 = []  #This is the row I make
            for thing in row:
                if thing.isdigit():
                    for i in range(0, int(thing)):
                        foo2.append(['.', 0])
                else:
                    foo2.append([thing, 0])
            foo.append(foo2)
        return foo

    def player_click(self, mx, my, screen):
        if self.player[self.turn] == 0:
            return
        y = mx // self.square_width
        x = my // self.square_height
        updated = False

        # handle promotion
        if self.promotion is not None and y >= 8 and y <= 10 and x < 4:
            move = self.promotion + promotion_code[x]
            self.move(move)
            updated = True
            self.promotion = None
            self.selected_piece = None
            self.update(0)
            print(move)
            return
        
        if x == 7 and y > 7:
            self.undo()
            if self.selected_piece is not None:
                self.selected_piece = None
            return

        if x > 7 or y > 7:
            return
    
        pos = chr(y + ord('a')) + chr((7 - x) + ord('1'))
        piece = self.board.piece_at(chess.parse_square(pos))

        if self.selected_piece is None:
            if piece is not None:
                team = chess.WHITE if unicode_to_algebraic[piece.unicode_symbol()].isupper() else chess.BLACK

                if self.board.turn != team:
                    self.selected_piece = [x, y]
                    self.draw_board[7-x][y] = [unicode_to_algebraic[piece.unicode_symbol()], 1]
                    self.show_valid_moves_to_list()
                    self.render_valid_moves(screen)   
                    updated = True

        else:
            # promotion
            piece = self.board.piece_at(chess.parse_square(chr(self.selected_piece[1] + ord('a')) + chr(7 - self.selected_piece[0] + ord('1'))))   
            move = chr(self.selected_piece[1] + ord('a')) + chr(7 - self.selected_piece[0] + ord('1')) + pos      

            if (unicode_to_algebraic[piece.unicode_symbol()] == 'p' and ((move[1] == '7' and move[3] == '8')) 
            or (unicode_to_algebraic[piece.unicode_symbol()] == 'P' and (move[1] == '2' and move[3] == '1'))):
                self.promotion = move
                draw_promotion(self,screen)
            else:
                self.promotion = None
                self.draw_board[7-self.selected_piece[0]][self.selected_piece[1]][1] = 0
                self.list_valid_moves = []

                # undo selected square by click again
                if x == self.selected_piece[0] and y == self.selected_piece[1]:
                    self.selected_piece = None
                # block illegal moves
                elif not self.board.is_legal(chess.Move.from_uci(move)):
                    self.selected_piece = None
                else:
                    self.selected_piece = None
                    self.move(move)

                draw_board(self,screen)
            updated = True
    
        if updated:
            self.update()

    def move(self, move):
        if self.board.is_legal(chess.Move.from_uci(move)):
            self.move_history.append(self.board.fen())  
            self.turn = not self.turn
            self.board.push_uci(move)
            self.update(0)
            return True
        return False
    
    def undo(self):
        if self.player[0] + self.player[1] == 0:
            return
        
        elif self.player[0] + self.player[1] == 1:
            if len(self.move_history) < 2 or self.player[self.turn] == 0:
                return
            self.move_history.pop()
            last_pos = self.move_history.pop()
            self.board = chess.Board(last_pos)
            self.update(0)
        else: 
            if len(self.move_history) == 0:
                return
            self.turn = not self.turn
            last_pos = self.move_history.pop()
            self.board = chess.Board(last_pos)
            self.update(0)
        

    def update(self, mode = 1):
        for x in range(8):
            for y in range(8):
                pos = chr(y + ord('a')) + chr((7 - x) + ord('1'))
                piece = self.board.piece_at(chess.parse_square(pos)) 
                updated = self.draw_board[x][y][1] if mode == 1 else 0
                self.draw_board[x][y] = [piece if piece is not None else ".", updated]

    def show_valid_moves_to_list(self): # xử lý
        x, y = self.selected_piece  
        selected_piece_pos = chr(y + ord('a')) + chr((7 - x) + ord('1'))  
        for i in range(8):
            for j in range(8):
                target_pos = chr(j + ord('a')) + chr((7 - i) + ord('1'))
                move = selected_piece_pos + target_pos  
                if move != selected_piece_pos + selected_piece_pos:
                    if self.board.is_legal(chess.Move.from_uci(move)):
                        self.list_valid_moves.append([i, j])

    def render_valid_moves(self, screen): #render
        
        for move in self.list_valid_moves:
            if move != self.selected_piece:
                square_center = (move[1] * self.square_width + self.square_width // 2, 
                move[0] * self.square_height + self.square_height // 2)
                pygame.draw.circle(screen, (255, 255, 100), square_center, self.square_width // 5)
