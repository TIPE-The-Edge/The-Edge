import pygame
from pygame.sprite import Sprite, Group

class Entry():
    def __init__(self, x, y, width, action):
        self.type = 'entry'
        self.color = (255, 255, 255)
        self.color_unfocus = (0, 0, 0)
        self.rect = pygame.Rect(x, y, width, 35)
        self.rect_txt = pygame.Rect(x+5, y+8, width, 35)
        self.action = action

        self.font = pygame.font.SysFont("calibri", 25)

        self.focus = False
        self.entry = ""
        self.entry_display = ""
        self.cursor_pos = 0
        self.max_cursor_pos = 0

    def draw(self, screen):
        if self.focus == True:
            pygame.draw.rect(screen, self.color, self.rect)
            self.image = self.font.render(self.entry, True, (0,0,0), self.color)
        else:
            pygame.draw.rect(screen, self.color_unfocus, self.rect)
            self.image = self.font.render(self.entry, True, (0,0,0), self.color_unfocus)

        screen.blit(self.image, self.rect_txt)

    def do(self, window, screen):
        self.focus = True
        self.cursor_pos = self.max_cursor_pos

        while self.focus:
            print('cursor_pos :',self.cursor_pos)
            print('max_cursor_pos :',self.max_cursor_pos)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not(self.rect.collidepoint(mouse_pos)):
                        self.focus = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.focus = False

                    elif event.key == pygame.K_LEFT and self.cursor_pos > 1:
                        self.cursor_pos -= 1

                    elif event.key == pygame.K_RIGHT and self.cursor_pos < self.max_cursor_pos:
                        self.cursor_pos += 1

                    elif event.key == pygame.K_BACKSPACE and self.entry != "":
                        self.entry = self.entry[:self.cursor_pos] + self.entry[self.cursor_pos+1:]
                        self.cursor_pos -= 1
                        self.max_cursor_pos -= 1

                    elif event.key not in [pygame.K_RETURN, pygame.K_BACKSPACE, pygame.K_LEFT, pygame.K_RIGHT]:
                        self.entry += event.unicode
                        self.cursor_pos += 1
                        self.max_cursor_pos += 1

            self.draw(screen)
            pygame.display.update()
