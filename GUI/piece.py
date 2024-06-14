import pygame



class Piece(pygame.sprite.Sprite):
    def __init__(self, piece_code, team_code, square_width, square_height):
        super().__init__()
        self.piece_code = piece_code
        self.team_code = team_code
        self.image = self.load_image(piece_code, team_code, square_width, square_height)
        self.rect = self.image.get_rect()

    def load_image(self, piece_code, team_code, square_width, square_height):
        piece_str = self.get_piece_string(piece_code)
        img_path = f'./res/imgs/{team_code}-{piece_str}.png'
        image = pygame.image.load(img_path)
        return pygame.transform.scale(image, (square_width, square_height))

    def get_piece_string(self, piece_code):
        match piece_code.lower():
            case 'r':
                return "rook"
            case 'n':
                return "knight"
            case 'b':
                return "bishop"
            case 'q':
                return "queen"
            case 'k':
                return "king"
            case 'p':
                return "pawn"
        
    def draw(self, screen, pos):
        self.rect.center = pos
        screen.blit(self.image, self.rect)            