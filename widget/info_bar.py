import pygame
from pygame.sprite import Sprite, Group

class Info_bar():
    def __init__(self):
        self.rect = pygame.Rect(80, 0, 1200, 40)
        self.color = (230,126,34)
        # self.action =
        self.items = []

    def draw(self,screen):
        for item in self.items:
            item.draw(screen)

        pygame.draw.rect(screen, self.color, self.rect)

    def do(self, window, screen):
        pass
