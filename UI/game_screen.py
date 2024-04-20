import pygame
import os
import chess
from UI.screen import Screen
from UI.render import PieceRenderer
unicode_to_algebraic = {
    '♚': 'K', '♛': 'Q', '♜': 'R', '♝': 'B', '♞': 'N', '♟': 'P',
    '♔': 'k', '♕': 'q', '♖': 'r', '♗': 'b', '♘': 'n', '♙': 'p'
}

promotion_code = ['q', 'r', 'b', 'n']
promotion_list = ['queen', 'rook', 'bishop', 'knight']

class game_screen(Screen):
    def __init__(self, window_size):
        super().__init__(window_size)
        self.square_height = self.height // 8
        self.square_width = self.width // 8
        self.piece_renderer = PieceRenderer(self.square_width, self.square_height)
        
    def click(self, mx, my):
        """_summary_

        Args:
            mx (int): x coordinate of mouse click
            my (int): y coordinate of mouse click
            
        return:
            (x, y): tile coordinates of the click
        """
        y = mx // self.square_width
        x = my // self.square_height
        return x, y
    def draw_square(self, screen, x, y, draw_board):
        loc = (x * (self.square_width), y * (self.square_height)) #position relative to the screen (pixel)

        color = 'light' if (x + y) % 2 == 1 else 'dark'
        draw_color = (238, 238, 210) if color == 'light' else (118, 150, 86)
        selected_color = (150, 255, 100)
        rect = pygame.Rect(loc[1], loc[0], self.square_width, self.square_height)
        
        pygame.draw.rect(screen, selected_color if draw_board[7-x][y][1] == 1 else draw_color, rect)
        return rect
        
    def draw(self, screen, board, draw_board, game_mode):
        screen.fill('white')
        selected_color = (150, 255, 100)
        
        for x in range(8):
            for y in range(8):
                # 0, 0 = a, 8; 0, 1 = b, 8 --> x 

                self.draw_square(screen, x, y, draw_board)
                
                self.piece_renderer.render_pieces(screen, board)

                

        if game_mode[0] + game_mode[1] > 0:
            pygame.draw.rect(screen, selected_color, pygame.Rect(600 + 20, self.square_height * 7, self.square_width, self.square_height))
            self.addText(screen, (630, self.square_height * 7 + (self.square_height * 1) // 5), "Undo")
        pygame.display.update()
        
    def addText(self, screen, pos, text, color = (0, 0, 0), backgroundColor = (255, 255, 255), button=False):
        title = pygame.font.SysFont('Arial', 25).render(text, True, color)
        temp_surface = pygame.Surface(title.get_size())
        temp_surface.fill(backgroundColor)
        temp_surface.blit(title, (0, 0))
        screen.blit(temp_surface, (pos[0], pos[1]))
        
