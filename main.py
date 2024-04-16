import pygame
import chess

from UI.start_screen import start_screen
from UI.Board import board

pygame.init()

window_size = (800, 600)     # window size
board_size = (600, 600)             # board size, the left 200px is for the side bar (undo, history, etc.)
mode = [-1, -1]  # (1, 1): player vs player, (1, 0): player vs bot, (0, 1): bot vs player, (0, 0): bot vs bot

screen = pygame.display.set_mode(window_size)
main_start_screen = start_screen(window_size)

while True:
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(mx, my)
            if event.button == 1:
                mode = main_start_screen.click(mx, my)
    main_start_screen.draw_screen(screen)
    if mode[0] != -1:
        break
    
# print(mode)
main_board = board(board_size, mode)

while True:
    main_board.draw(screen)

