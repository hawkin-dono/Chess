import pygame
import os
import chess

class Piece(pygame.sprite.Sprite):
    def __init__(self, team, piece_type, row, col, square_width, square_height):
        super().__init__()
        self.team = team
        self.piece_type = piece_type
        self.row = row
        self.col = col
        self.square_width = square_width
        self.square_height = square_height
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * square_width, (7 - row) * square_height)


    def load_image(self):
        root = os.path.dirname(__file__)
        open_path = 'data\\imgs\\{0}-{1}.png'.format(self.team, self.piece_type)
        img_path = os.path.join('\\'.join(root.split('\\')[:-1]), open_path)
        image = pygame.image.load(img_path)
        return pygame.transform.scale(image, (self.square_width, self.square_height))

class PieceRenderer:
    def __init__(self, square_width, square_height):
        self.square_width = square_width
        self.square_height = square_height
        self.pieces = pygame.sprite.Group()

    def render_pieces(self, screen, board):
        self.pieces.empty()  # Xóa các sprite cũ
        for pos, piece in board.piece_map().items():
            if piece is not None:
                team = 'white' if piece.color == chess.WHITE else 'black'
                piece_code = piece.symbol().lower()
                match piece_code.lower():
                    case 'r':
                        piece_type = "rook"
                    case 'n':
                        piece_type = "knight"
                    case 'b':
                        piece_type = "bishop"
                    case 'q':
                        piece_type = "queen"
                    case 'k':
                        piece_type = "king"
                    case 'p':
                        piece_type = "pawn"

                row = 7 - (pos // 8)  # Tính hàng từ vị trí
                col = pos % 8  # Tính cột từ vị trí
                self.pieces.add(Piece(team, piece_type, row, col, self.square_width, self.square_height))

        self.pieces.draw(screen)