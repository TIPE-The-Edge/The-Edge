import pygame
from pygame.sprite import Sprite, Group

class Button_txt():
    def __init__(self, x, y, width, height, color, items, action, arg):
        self.type = 'button_txt'
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.arg = arg
        self.items = items
        self.level = 0

        self.place_items(x, y)

    def place_items(self, x, y):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def do(self, window, screen):
        if self.action != None:
            self.action(self, window, screen, *self.arg)

    def up(self):
        for item in self.items:
            item.level += 1
