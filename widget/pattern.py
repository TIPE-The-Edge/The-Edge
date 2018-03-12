import pygame
from pygame.sprite import Sprite, Group

class Widget():

    def __init__(self, num, img, x, y, width, height, action, arg):
        self.type = ''
        self.items = []
        self.action = action
        self.arg = arg
        self.hover= pygame.Rect(x, y, width, height)
        self.level = 0

    def draw(self, screen):


    def do(self, window, screen):
        if self.action != None:
            self.action(self, window, screen, *self.arg)

    def up(self):
        for item in self.items:
            item.level += 1
