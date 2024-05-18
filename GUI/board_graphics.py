import pygame
import os
import chess

from GUI.piece import Piece

unicode_to_algebraic = {
    '♚': 'K', '♛': 'Q', '♜': 'R', '♝': 'B', '♞': 'N', '♟': 'P',
    '♔': 'k', '♕': 'q', '♖': 'r', '♗': 'b', '♘': 'n', '♙': 'p'
}

promotion_list = ['queen', 'rook', 'bishop', 'knight']

def draw_board(board, screen):
    board.update()
    background_img = pygame.image.load('data/imgs/background-main.jpg')
    background_img = pygame.transform.scale(background_img, (screen.get_width() - board.width, screen.get_height()))

    # draw background
    screen.blit(background_img, (board.width, 0))
    for x in range(8):
        for y in range(8):
            loc = (x * (board.square_width), y * (board.square_height))
            color = 'light' if (x + y) % 2 == 1 else 'dark'
            pos = chr(y + ord('a')) + chr((7 - x) + ord('1'))
            piece = board.board.piece_at(chess.parse_square(pos))
            draw_color = (238, 238, 210) if color == 'light' else (118, 150, 86)
            selected_color = (150, 255, 100)
            rect = pygame.Rect(loc[1], loc[0], board.square_width, board.square_height)
            pygame.draw.rect(screen, selected_color if board.draw_board[7-x][y][1] == 1 else draw_color, rect)

            if piece is not None:
                piece_code = unicode_to_algebraic[piece.unicode_symbol()]
                team_code = 'white' if piece_code.islower() else 'black'
                piece_pos = (loc[1] + board.square_width // 2, loc[0] + board.square_height // 2)
                piece_obj = Piece(piece_code, team_code, board.square_width, board.square_height)
                piece_obj.draw(screen, piece_pos)


    # background_img = pygame.image.load('data/imgs/background_mainChess.jpg')
    # background_img = pygame.transform.scale(background_img, (200,600))

    # # Vẽ background
    # screen.blit(background_img, (600, 0))
    

    if board.player[0] + board.player[1] > 0:
        undo_button_img = pygame.image.load('data/imgs/undo_button.png')
        undo_button_img = pygame.transform.scale(undo_button_img, (board.square_width*2, board.square_height))
        screen.blit(undo_button_img, (600 + 20, board.square_height * 7))
        
    if board.promotion is not None:
        draw_promotion(board, screen)
    
    if board.list_valid_moves:
        render_valid_moves(board, screen)

def render_valid_moves(board, screen): #render
        
        for move in board.list_valid_moves:
            if move != board.selected_piece:
                square_center = (move[1] * board.square_width + board.square_width // 2, 
                move[0] * board.square_height + board.square_height // 2)
                pygame.draw.circle(screen, (255, 255, 100), square_center, board.square_width // 5.5)

def add_text(screen, pos, text, color=(0, 0, 0), backgroundColor=(255, 255, 255), button=False):
    title = pygame.font.SysFont('Arial', 25).render(text, True, color)
    temp_surface = pygame.Surface(title.get_size())
    temp_surface.fill(backgroundColor)
    temp_surface.blit(title, (0, 0))
    screen.blit(temp_surface, (pos[0], pos[1]))

def draw_promotion(board, screen):
    team = 'white' if board.board.turn == chess.WHITE else 'black'
    for i in range(4):
        loc = board.square_height * i
        draw_color = (0, 0, 0)
        rect = pygame.Rect(600 + 20, loc + i * 2, board.square_width, board.square_height)
        pygame.draw.rect(screen, draw_color, rect, 2)
        img_path = f'./data/imgs/{team}-{promotion_list[i]}.png'
        dude_path = os.path.join(img_path)
        image = pygame.image.load(dude_path)
        image = pygame.transform.scale(image, (board.square_width, board.square_height))
        centering_rect = image.get_rect()
        centering_rect.center = rect.center
        screen.blit(image, centering_rect.topleft)