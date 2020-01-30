import pygame
from pygame.sprite import Sprite, Group
from widget.rectangle import *

class Progress_bar():

    def __init__(self, x, y, width, height, action, arg,
                 value, max_value, color, color_bg):
        self.type = 'progress_bar'
        self.level = 0

        self.width_bar = value * width // max_value

        self.bg_color = color_bg
        self.rect = pygame.Rect(x, y, width, height)

        self.color = color

        self.items = []
        self.action = action
        self.arg = arg


    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        width = self.rect.width
        self.rect.width = self.width_bar
        pygame.draw.rect(screen, self.color, self.rect)
        self.rect.width = width

    def do(self, window, screen):
        if self.action != None:
            self.action(self, window, screen, *self.arg)

    def up(self):
        for item in self.items:
            item.level += 1

    def set_type(self, type):
        self.type = type
