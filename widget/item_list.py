import pygame
from pygame.sprite import Sprite, Group

class Item_list():
    def __init__(self,
                 items, list_x, list_y,
                 scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height
                ):
        self.type = 'item_list'
        self.items = items

        self.place_items(list_x, list_y)

        item_width = items[0].rect.width
        item_height = items[0].rect.height

        # Set background behind items
        self.bg_color = (189, 195, 199)
        self.bg_rect = pygame.Rect(list_x, list_y, item_width, scrollbar_height)

        # Set background behind thumb
        self.sb_bg_color = (127, 140, 141)
        self.sb_bg_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)

        # Set thumb
        all_items_height = (len(self.items)+2) * item_height
        if all_items_height <= scrollbar_height:
            thumb_height = 0
        else:
            thumb_height = (scrollbar_height * scrollbar_height) // all_items_height

        self.thumb_color = (189, 195, 199)
        self.thumb_color_pressed = (149, 165, 166)
        self.rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, thumb_height)

        # Other settings
        self.pressed = False
        self.coord_pressed = None
        self.min_height = scrollbar_y
        self.max_height = scrollbar_y + scrollbar_height - thumb_height
        self.item_shift = (all_items_height // scrollbar_height) + 1

    # Forme une liste avec les items
    def place_items(self, x, y):
        for i in range(len(self.items)):
            self.items[i].rect.x = x
            self.items[i].rect.y = y + i * self.items[i].rect.height + i * 2

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.bg_rect)

        for item in self.items:
            item.draw(screen)

        pygame.draw.rect(screen, self.sb_bg_color, self.sb_bg_rect)

        if self.pressed:
            pygame.draw.rect(screen, self.thumb_color_pressed, self.rect)
        else:
            pygame.draw.rect(screen, self.thumb_color, self.rect)

    def do(self, window, screen):
        self.pressed = True

        while self.pressed:
            mouse_pos = pygame.mouse.get_pos()

            if self.coord_pressed == None:
                self.coord_pressed = mouse_pos
            else:
                shift = mouse_pos[1] - self.coord_pressed[1]
                thumb_pos_y = self.rect.y + shift

                if (self.rect.y == self.min_height and shift > 0) or (self.rect.y == self.max_height and shift < 0) or (self.min_height < self.rect.y < self.max_height):

                    self.coord_pressed = mouse_pos

                    if thumb_pos_y < self.min_height:
                        shift = thumb_pos_y - self.min_height
                        thumb_pos_y = self.min_height
                    elif thumb_pos_y > self.max_height:
                        shift = thumb_pos_y - self.max_height
                        thumb_pos_y = self.max_height

                    self.rect.y = thumb_pos_y

                    for item in self.items:
                        item.move(self.item_shift * shift)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.pressed = False
                        self.coord_pressed = None

            window.display(screen)
            pygame.display.update()
