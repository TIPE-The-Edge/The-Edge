import pygame
from pygame.sprite import Sprite, Group

class Button_img():
    def __init__(self, num, path, x, y, action):
        self.items = []
        self.type = 'button_img'
        self.path = path
        self.num = num
        self.img = pygame.image.load(path+'.png')
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.action = action
        self.level = 0

    def set_focus(self):
        self.img = pygame.image.load(self.path+'_focus.png')

    def remove_focus(self):
        self.img = pygame.image.load(self.path+'.png')

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def do(self, window, screen):
        if self.action != None:
            self.action(self, window, screen)

    def up(self):
        for item in self.items:
            item.level += 1
