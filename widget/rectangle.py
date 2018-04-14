import pygame
from pygame.sprite import Sprite, Group

class Rectangle():

    def __init__(self, x, y, width, height, color, alpha, action, arg):
        self.type = 'Rectangle'
        self.items = []
        self.action = action
        self.arg = arg
        self.alpha = alpha
        self.hover= pygame.Rect(x, y, width, height)
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.level = 0

    def draw(self, screen):
        s = pygame.Surface((self.rect.width,self.rect.height))
        s.set_alpha(self.alpha)
        s.fill(self.color)
        screen.blit(s, (self.rect.x,self.rect.y))

    def do(self, window, screen):
        if self.action != None:
            self.action(self, window, screen, *self.arg)

    def up(self):
        for item in self.items:
            item.level += 1

    def set_type(self, type):
        self.type = type
