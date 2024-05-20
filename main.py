import pygame
import chess

from GUI.Board import board
# from alphazero.AlphaZeroAI import AlphaZeroAI 
from start_window import start_screen
from GUI.board_graphics import draw_board 
from end_window import EndGameWindow
import cow
from alphazero.AlphaZeroAI import AlphaZeroAI

pygame.init()

window_size = (800, 600)
board_size = (600, 600)
team = [-1, -1]


#################### alpha zero ####################


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
print(main_board)

def draw(screen):
    screen.fill('white')
    draw_board(main_board, screen)
    pygame.display.update()

best_move = -1

###### Game loop ######
# ai = AlphaZeroAI()

while True:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if main_board.player[main_board.turn]:
                    main_board.player_click(mx, my, screen)
                
    if main_board.player[main_board.turn] == 0:
        print("check", main_board.turn)
        draw(screen)
        if team[2] == 1: 
            best_move = AlphaZeroAI.get_best_move_no_search(AlphaZeroAI, main_board.board)          ########alpha zero########
        else:
            best_move = cow.get_best_move(main_board.board)               ##### cow #####
        
        main_board.move(best_move)
    draw(screen)

    # Result handling
    is_game_over = False
    if main_board.board.is_checkmate():
        if main_board.board.turn == chess.WHITE:
            result = "Black wins by checkmate!"
        else:
            result = "White wins by checkmate!"
        is_game_over = True
    if main_board.board.is_stalemate():
        result = "Stalemate!"
        is_game_over = True
    if main_board.board.is_insufficient_material():
        result = "Insufficient material for checkmate."
        is_game_over = True
    if main_board.board.is_fifty_moves():
        result = "Draw due to 50-move rule."
        is_game_over = True
    if main_board.board.is_repetition(3):
        result = "Draw due to threefold repetition."
        is_game_over = True
    if is_game_over:
        end_game_window = EndGameWindow(window_size, result)
        end_game_window.show(screen)
        break