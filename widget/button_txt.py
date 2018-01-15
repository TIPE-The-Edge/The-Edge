import pygame
from pygame.sprite import Sprite, Group

class Button_txt():
    def __init__(self, x, y, width, height, color, items, action):
        self.type = 'button_txt'
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.items = items

        self.place_items(x, y)

    def place_items(self, x, y):
        pass

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

        pygame.draw.rect(screen, self.color, self.rect)

    def do(self, window, screen):
        self.action(self, window, screen)

    def move(self, shift):
        self.rect.y -= shift
