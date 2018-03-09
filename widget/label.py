import pygame
from pygame.sprite import Sprite, Group
from widget.frame import *

class Label():
    def __init__(self, text, police, fontsize, msg_color, bg_color, x, y, action):
        self.type = 'label'
        self.font = pygame.font.SysFont(police, fontsize)
        self.image = self.font.render(text, True, msg_color, bg_color)
        self.rect = self.image.get_rect()
        self.items = []
        self.rect.x = x
        self.rect.y = y
        self.level = 0
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def do(self, window, screen):
        if self.action != None:
            self.action(self, window, screen)

    def up(self):
        for item in self.items:
            item.level += 1
