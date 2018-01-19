import pygame
from pygame.sprite import Sprite, Group

class Widget():

    def __init__(self, num, img, x, y, width, height, action):
        self.type = ''
        self.items =
        self.action = action

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

    def do(self, window, screen):
        self.action(self, window, screen)
