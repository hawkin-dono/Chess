import pygame

class EndGameWindow:
    def __init__(self, window_size, result):
        self.window_size = window_size
        self.result = result
        self.font = pygame.font.Font(None, 36)

    def draw_window(self, screen):
        screen.fill('white')
        text_surface = self.font.render(self.result, True, 'black')
        text_rect = text_surface.get_rect()
        text_rect.center = (self.window_size[0] // 2, self.window_size[1] // 2)
        screen.blit(text_surface, text_rect)
        pygame.display.update()

    def show(self, screen):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_window(screen)