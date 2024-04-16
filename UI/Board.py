import pygame
import chess
import os
from UI.game_screen import game_screen

unicode_to_algebraic = {
    '♚': 'K', '♛': 'Q', '♜': 'R', '♝': 'B', '♞': 'N', '♟': 'P',
    '♔': 'k', '♕': 'q', '♖': 'r', '♗': 'b', '♘': 'n', '♙': 'p'
}

promotion_code = ['q', 'r', 'b', 'n']
promotion_list = ['queen', 'rook', 'bishop', 'knight']

class board:
    def __init__(self, board_size, game_mode):
        self.width = board_size[0]
        self.height = board_size[1]
        self.square_height = self.height // 8
        self.square_width = self.width // 8
        self.selected_piece = None
        self.promotion = None

        self.board = chess.Board() 
        self.draw_board = self.convert_board()
        self.game_mode = game_mode
        self.turn = True

        self.game_screen = game_screen(board_size)
        self.move_history = []
        
    def convert_board(self): #type(board) == chess.Board()
        """
        Input: chess.Board()
        
        Output: 2D array of chess board
        [[['r', 0], ['n', 0], ['b', 0], ['q', 0], ['k', 0], ['b', 0], ['n', 0], ['r', 0]],
        [['p', 0], ['p', 0], ['p', 0], ['p', 0], ['p', 0], ['p', 0], ['p', 0], ['p', 0]],
        ....
        ]
        """
        pgn = self.board.epd() # 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -'
        foo = []  #Final board
        pieces = pgn.split(" ", 1)[0]  #'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        rows = pieces.split("/")
        for row in rows:
            foo2 = []  
            for thing in row:
                if thing.isdigit():
                    for i in range(0, int(thing)):
                        foo2.append(['.', 0])
                else:
                    foo2.append([thing, 0])
            foo.append(foo2)
        return foo

    def draw(self, screen):
        # self.update()
        self.game_screen.draw(screen, self.board, self.draw_board, self.game_mode)

    def draw_promotion(self, screen):
        self.game_screen.draw_promotion(screen)

    


