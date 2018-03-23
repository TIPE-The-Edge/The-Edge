import pygame
from pygame.sprite import Sprite, Group

class Entry():
    def __init__(self, x, y, width, height, onlynum, id_, char_min, char_max):
        self.items = []
        self.type = 'entry'
        self.color = (255, 255, 255)
        self.color_unfocus = (200, 200, 200)
        self.rect = pygame.Rect(x, y, width, height)
        self.action = None
        self.arg = []
        self.level = 0
        self.id = id_
        self.char_max = char_max
        self.char_min = char_min

        fontsize = int(5 * height / 7) - 1
        self.font = pygame.font.SysFont("calibri", fontsize)

        self.focus = False
        self.entry = ""

        # Pour la position du curseur
        self.cursor_pos = 0
        self.max_cursor_pos = 0

        # Pour l'affichage
        self.entry_display = ""
        self.len_display = 0
        self.get_len_display()
        self.range_min = 0
        self.range_max = 1

        # Entry type
        if onlynum:
            self.entry_type = 'num'
        else:
            self.entry_type = 'text'

    # def get_image(self):
    #     i = 0
    #     len_txt = len(self.entry_display)
    #     img = (self.font.render(self.entry_display[:i], True, (0,0,0), self.color)).get_rect()
    #     while i < len_txt:
    #         if img.width < self.rect.width-10:
    #             i += 1
    #             img = (self.font.render(self.entry_display[:i], True, (0,0,0), self.color)).get_rect()
    #         elif i != 0:
    #             return i-2
    #         else:
    #             return 0
    #     return len_txt

    def draw(self, screen):
        # self.rect_txt = pygame.Rect(self.rect.x+5, self.rect.y+8, self.rect.width, self.rect.height)

        if self.focus == True:
            pygame.draw.rect(screen, self.color, self.rect)
            self.image = self.font.render(self.entry_display, True, (0,0,0), self.color)
        else:
            pygame.draw.rect(screen, self.color_unfocus, self.rect)
            self.image = self.font.render(self.entry_display, True, (0,0,0), self.color_unfocus)

        self.rect_txt = self.image.get_rect()
        self.rect_txt.x = self.rect.x + 5
        self.rect_txt.y = self.rect.y + self.rect.height // 2 - self.rect_txt.height // 2
        # self.rect_txt.width = self.rect.width - 10
        # print(self.rect_txt.width)
        screen.blit(self.image, self.rect_txt)

    def do(self, window, screen):
        self.focus = True
        self.cursor_pos = self.max_cursor_pos
        if self.cursor_pos > self.range_max:
            self.range_min = self.cursor_pos-self.len_display+1
            self.range_max = self.cursor_pos+1

        while self.focus:
            print('cursor_pos :',self.cursor_pos)
            print('max_cursor_pos :',self.max_cursor_pos)
            print('range_min :',self.range_min)
            print('range_max :',self.range_max)
            mouse_pos = pygame.mouse.get_pos()

            # if self.len_display == 0 and self.rect_txt.width > self.rect.width:
            #     self.len_display = len(self.entry) - 1
            # elif self.rect_txt.width < self.rect.width:
            #     self.len_display = 0

            for event in pygame.event.get():

                # Clique en dehors de l'entry
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not(self.rect.collidepoint(mouse_pos)):
                        self.focus = False

                # Clique sur l'entry
                elif event.type == pygame.KEYDOWN:
                    # Sortir de l'entry, du focus
                    if event.key == pygame.K_ESCAPE:
                        self.focus = False

                    # Se déplacer à gauche
                    elif event.key == pygame.K_LEFT and self.cursor_pos > 0:
                        self.cursor_pos -= 1
                        if self.range_min != 0:
                            self.range_max -= 1
                            self.range_min -= 1

                    # Se déplacer à droite
                    elif event.key == pygame.K_RIGHT and self.cursor_pos < self.max_cursor_pos:
                        self.cursor_pos += 1
                        if self.range_max <= self.max_cursor_pos and self.range_max - self.range_min > self.len_display:
                            self.range_max += 1
                            self.range_min += 1

                    # Supprimer un caractère
                    elif event.key == pygame.K_BACKSPACE and self.entry != "" and self.cursor_pos != 0:
                        self.entry = self.entry[:self.cursor_pos-1] + self.entry[self.cursor_pos:]
                        self.cursor_pos -= 1
                        self.max_cursor_pos -= 1

                        if self.range_min != 0:
                            self.range_max -= 1
                            self.range_min -= 1
                        elif self.range_max == self.max_cursor_pos+2:
                            self.range_max -= 1

                    # Ajouter un caractère
                    elif event.key not in [pygame.K_RETURN, pygame.K_BACKSPACE, pygame.K_LEFT, pygame.K_RIGHT]:
                        char = event.unicode
                        if self.entry_type == 'num':
                            try:
                                int(char)
                            except:
                                char = ''

                        if char != '':
                            if self.range_max - self.range_min > self.len_display:
                                self.range_max += 1
                                self.range_min += 1
                            else:
                                self.range_max += 1

                            self.entry = self.entry[:self.cursor_pos] + char + self.entry[self.cursor_pos:]
                            self.cursor_pos += 1
                            self.max_cursor_pos += 1

            self.entry_display = self.entry[:self.cursor_pos] + '|' + self.entry[self.cursor_pos:]
            self.entry_display = self.entry_display[self.range_min:self.range_max]
            self.draw(screen)
            pygame.display.update()

        self.entry_display = self.entry[self.range_min:self.range_max]
        self.draw(screen)
        pygame.display.update()

    # Récupère la taille maximum du texte à afficher
    def get_len_display(self):
        text = "A"
        img = self.font.render(text, True, (0,0,0), self.color_unfocus)
        img_rect = img.get_rect()
        while img_rect.width < self.rect.width:
            text += "A"
            img = self.font.render(text, True, (0,0,0), self.color_unfocus)
            img_rect = img.get_rect()
        self.len_display = len(text)-2

    def up(self):
        for item in self.items:
            item.level += 1

    def set_type(self, type):
        self.type = type
