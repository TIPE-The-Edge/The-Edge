import pygame
from pygame.sprite import Sprite, Group

class Entry():
    def __init__(self, x, y, width, height, action):
        self.type = 'entry'
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(x, y, width, height)
        self.focus = false
        self.action = action
        self.entry = ""
        self.entry_display = ""

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def do(self, window, screen):
        self.focus = true

        while self.focus:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTODOWN and event.button == 1:
                    if not(self.rect.collidepoint(mouse_pos)):
                        self.focus = false
                elif event.type == pygame.KEYDOWN:
                    print("test")
