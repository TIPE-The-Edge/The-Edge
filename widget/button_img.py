import pygame
from pygame.sprite import Sprite, Group

class Button_img():
    def __init__(self, num, img, x, y, action):
        self.type = 'button_img'
        self.num = num
        self.img = pygame.image.load(img)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.action = action

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def do(self, window, screen):
        self.action(self, window, screen)
