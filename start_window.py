import pygame
import os

class start_screen:
    def __init__(self, window_size):
        self.max_width, self.max_height = window_size
        self.font = pygame.font.SysFont('Arial', 25)
        self.buttons = []
        self.mode = [(1, 1), (0, 0), (1, 0), (0, 1)]

    def draw_screen(self, screen):
        self.addText(screen, (self.max_width // 2, self.max_height // 3), "Chess game")
        self.addText(screen, (self.max_width // 4, (self.max_height * 3) // 5), "Player vs. Player")
        self.addText(screen, (self.max_width // 2, (self.max_height * 3) // 5), "Player vs. Bot")
        self.addText(screen, ((self.max_width // 4) * 3, (self.max_height * 3) // 5), "Bot vs. Bot")
        self.addButton(screen)

    def addText(self, screen, pos, text, color = (0, 0, 0), backgroundColor = (255, 255, 255), button=False):
        title = self.font.render(text, True, color)
        temp_surface = pygame.Surface(title.get_size())
        temp_surface.fill(backgroundColor)
        temp_surface.blit(title, (0, 0))
        title_rect = title.get_rect()
        new_rect = screen.blit(temp_surface, (pos[0] - title_rect.width // 2, pos[1] - title_rect.height // 2))
        if button:
            self.buttons.append(new_rect)

    def addButton(self, screen):
        x_pos = [self.max_width // 2 - 50, self.max_width // 2 + 50]
        y_pos = self.max_height // 2
        width = min(self.max_height, self.max_width) // 10
        height = min(self.max_height, self.max_width) // 10
        color = [(241, 211, 170), (180, 126, 82)]
        self.addText(screen, (self.max_width // 4, self.max_height // 2), "Play", color=(255,255,255), backgroundColor=(0,0,0), button=True)
        self.addText(screen, ((self.max_width * 3) // 4, self.max_height // 2), "Play", color=(255,255,255), backgroundColor=(0,0,0), button=True)
        
        for i in range(2):
            rect = pygame.Rect(x_pos[i] - width // 2, y_pos - height // 2, width, height)
            pygame.draw.rect(screen, color[i], rect)
            img_path = './data/imgs/{0}-king.png'.format('white' if i == 1 else 'black')
                        
            base_path = os.path.dirname(__file__)
            dude_path = os.path.join(base_path, img_path)
            image = pygame.image.load(dude_path)
            image = pygame.transform.scale(image, ((width * 2) // 3 , (height * 2) // 3))

            centering_rect = image.get_rect()
            centering_rect.center = rect.center
            screen.blit(image, centering_rect.topleft)
            self.buttons.append(rect)

    def click(self, mx, my):
        for i in range(4):
            current = self.buttons[i]
            print(current)
            if mx >= current.x and mx <= current.x + current.width and my >= current.y and my <= current.y + current.height:
                return self.mode[i]
        return [-1, -1]