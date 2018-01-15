import pygame
from pygame.sprite import Sprite, Group

class Label():
    def __init__(self, text, font, msg_color, bg_color, x, y):
        self.image = font.render(text, True, msg_color, bg_color)
        self.rect = self.image.get_rect()
        self.items = []
        self.rect.x = x
        self.rect.y = y
        # self.action =

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)
            
        screen.blit(self.image, self.rect)

    def do(self, window, screen):
        pass
