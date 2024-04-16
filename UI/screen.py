import pygame
import os

class Screen():
    def __init__(self, window_size):
        self.width, self.height = window_size
        self.font = pygame.font.SysFont('Arial', 25)
        
    def click(self, mx, my):
        return