import pygame
from pygame.sprite import Sprite, Group

class Rectangle():

    def __init__(self, x, y, width, height, color, action, arg):
        self.type = 'Rectangle'
        self.items = []
        self.action = action
        self.arg = arg
        self.hover= pygame.Rect(x, y, width, height)
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.level = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def do(self, window, screen):
        if self.action != None:
            self.action(self, window, screen, *self.arg)

    def up(self):
        for item in self.items:
            item.level += 1
