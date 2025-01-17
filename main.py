import pygame
import chess

from GUI.Board import board
from alphazero.AlphaZeroAI import AlphaZeroAI 
from start_window import start_screen
from GUI.board_graphics import draw_board 
from end_window import EndGameWindow
import cow
from alphazero.AlphaZeroAI import AlphaZeroAI
import time

pygame.init()

window_size = (800, 600)
board_size = (600, 600)
team = [-1, -1]


# start screen
screen = pygame.display.set_mode(window_size)
main_start_screen = start_screen(window_size)
def draw_start_screen(screen):
    #screen.blit(background, (0, 0))
    screen.fill('white')
    main_start_screen.draw_screen(screen)
    pygame.display.update()

while True:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                team = main_start_screen.click(mx, my)
    draw_start_screen(screen)
    if team[0] != -1:
        break

main_board = board(board_size[0], board_size[1], team)

def draw(screen):
    screen.fill('white')
    draw_board(main_board, screen)
    pygame.display.update()

def is_end_game(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return True, "Black wins by checkmate!"
        else:
            return True, "White wins by checkmate!"
    elif board.is_stalemate():
        return True, "Stalemate!"
    elif board.is_insufficient_material():
        return True, "Insufficient material for checkmate."
    elif board.is_fifty_moves():
        return True, "Draw due to 50-move rule."
    elif board.is_repetition(3):
        return True, "Draw due to threefold repetition."
    return False, ""

best_move = -1

###### Game loop ######
alphazero = AlphaZeroAI()

while True:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if main_board.player[main_board.turn]:
                    main_board.player_click(mx, my, screen)

    is_game_over, result = is_end_game(main_board.board)
    if (not is_game_over) and main_board.player[main_board.turn] == 0:
        draw(screen)
        start_time = time.time()
        if team[2] == 1: 
            best_move = alphazero.get_best_move(main_board.board)          
        else:
            best_move = cow.get_best_move(main_board.board)    
        end_time = time.time()   
        if (end_time - start_time) < 0.5:
            time.sleep(0.5 - (end_time - start_time))      
        
        main_board.move(best_move)
    draw(screen)

    # Result handling
    is_game_over, result = is_end_game(main_board.board)
    if is_game_over:
        
        end_game_window = EndGameWindow(window_size, result)
        end_game_window.show(screen)
        break