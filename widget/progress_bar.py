import pygame
from pygame.sprite import Sprite, Group

class Progress_bar():

    def __init__(self, x, y, width, height, action
                 value, max_value):
        self.type = 'progress_bar'

        self.bg_color = (0,0,0)
        self.rect = pygame.Rect(x, y, width, height)

        self.color = (255,255,255)
        width_bar = int(value * width / max_value)
        self.rect_bar = pygame.Rect(x, y, width_bar, height)

        self.items = []
        self.action = action


    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.color, self.rect_bar)

    def do(self, window, screen):
        self.action(self, window, screen)
