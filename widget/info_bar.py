import pygame
from pygame.sprite import Sprite, Group

class Info_bar():
    def __init__(self):
        self.type = 'info_bar'
        self.rect = pygame.Rect(80, 0, 1200, 40)
        self.color = (230,126,34)
        # self.action =
        self.items = []
        self.level = 0
        self.action = None

    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def do(self, window, screen):
        if self.action != None:
            self.action(self, window, screen)

    def up(self):
        for item in self.items:
            item.level += 1
