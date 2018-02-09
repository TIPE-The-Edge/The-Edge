import pygame
from pygame.sprite import Sprite, Group

class Frame():

    """ Initialisation du widget
    Entrée :
        # self
        # x
        # y
        # items
        # action
    """
    def __init__(self, x, y, items, action):
        self.type = 'frame'
        self.action = action

        self.items = items
        self.items_pos = 'relative' # relative, fixed, auto

        # Position du coin supérieur gauche
        self.x = x
        self.y = y

        # Si les items peuvent changer de taille
        self.resize_items = False

        # Taille de la frame
        self.size_w = 'fixed' # fixed, auto
        self.width = 0
        self.size_h = 'fixed' # fixed, auto
        self.height = 0

        # Couleur du background
        self.color = (189, 195, 199)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hover= pygame.Rect(self.x, self.y, self.width, self.height)

        # Direction de l'assemblage
        self.direction = 'none'
        # Marge entre les items
        self.marge_items = 0

        # Marge intérieur
        self.padding_left = 0
        self.padding_right = 0
        self.padding_top = 0
        self.padding_bottom = 0


    """ Modifie les paramètres de redimensionnement du widget
    Entrée :
        # self
        # width : entier ou 'auto'
        # height : entier ou 'auto'
    """
    def resize(self, width, height):
        if width == 'auto':
            self.size_w = 'auto'
        else:
            self.size_w = 'fixed'
            self.width = width

        if height == 'auto':
            self.size_h = 'auto'
        else:
            self.size_h = 'fixed'
            self.height = height


    """ Modifie la marge entre les items
    Entrée :
        # self
        # value : entier
    """
    def set_marge_items(self, value):
        self.marge_items = value


    """ Modifie les marges intérieurs
    Entrée :
        # self
        # left, right, top, bottom : entier
    """
    def set_padding(self, left, right, top, bottom):
        self.padding_left = left
        self.padding_right = right
        self.padding_top = top
        self.padding_bottom = bottom


    """ Modifie le paramètre de positionnement des items
    Entrée :
        # self
        # value: 'fixed', 'relative', 'auto'
    """
    def set_items_pos(self, value):
        self.items_pos = value


    """ Modifie le paramètre alignement des items
    Entrée :
        # self
        # value: 'vertical', 'horizontal', 'none'
    """
    def set_direction(self, value):
        if value == 'vertical':
            self.direction = value
            self.size_h = 'auto'
        elif value == 'horizontal':
            self.direction = value
            self.size_w = 'auto'
        else:
            self.direction = 'none'


    """ Modifie la largeur ou la hauteur
    Entrée :
        # self
        # value: entier
    """
    def set_width(self, value):
        self.size_w = 'fixed'
        self.width = value

    def set_height(self, value):
        self.size_h = 'fixed'
        self.height = value


    """ Dessine les items de la frame en fonction de ses paramètres
    Entrée :
        # self
        # value: 'vertical', 'horizontal', 'none'
    """
    def draw(self, screen):
        if self.items_pos == 'fixed':
            for item in self.items:
                item.draw(screen)

        elif self.items_pos == 'relative':
            print('relative')
            for item in self.items:

                if self.size_w == 'auto':
                    print('width')
                    new_width = self.padding_left + item.rect.width + self.padding_right + item.rect.x
                    if new_width > self.width:
                        print('new_width')
                        self.width = new_width

                if self.size_h == 'auto':
                    print('height')
                    new_height = self.padding_top + item.rect.height + self.padding_bottom + item.rect.y
                    if new_height > self.height:
                        print('new_height')
                        self.height = new_height

                item.rect.x = item.rect.x + self.x + self.padding_left
                item.rect.y = item.rect.y + self.y + self.padding_bottom

                # item.draw(screen)

        elif self.items_pos == 'auto':

            if self.direction == 'vertical':
                sum_size = self.padding_top + self.y
            elif self.direction == 'horizontal':
                sum_size = self.padding_left + self.x

            for item in self.items:

                if self.direction == 'vertical':
                    if self.size_w == 'auto':
                        new_width = self.padding_left + item.rect.width + self.padding_right
                        if new_width > self.width:
                            self.width = new_width

                    elif self.size_w == 'fixed' and self.resize:
                        max_width = self.width - self.padding_left - self.padding_right
                        if item.rect.width < max_width:
                            try:
                                item.resize(max_width)
                            except:
                                pass

                    item.rect.x = self.x + self.padding_left
                    item.rect.y = sum_size
                    sum_size += item.rect.height + self.marge_items

                elif self.direction == 'horizontal':
                    if self.size_h == 'auto':
                        new_height = self.padding_top + item.rect.height + self.padding_bottom
                        if new_height > self.height:
                            self.height = new_height

                    elif self.size_h == 'fixed' and self.resize:
                        max_height = self.height - self.padding_top - self.padding_bottom
                        if item.rect.height < max_height:
                            try:
                                item.resize(max_height)
                            except:
                                pass

                    item.rect.x = sum_size
                    item.rect.y = self.y + padding_top
                    sum_size += item.rect.width + self.marge_items

                # item.draw(screen)

            if self.direction == 'vertical':
                sum_size += self.padding_bottom - self.y - self.marge_items
                self.height = sum_size
            elif self.direction == 'horizontal':
                sum_size += self.padding_right - self.x - self.marge_items
                self.width = sum_size

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hover= pygame.Rect(self.x, self.y, self.width, self.height)

        pygame.draw.rect(screen, self.color, self.rect)

        for item in self.items:
            item.draw(screen)


    def do(self, window, screen):
        self.action(self, window, screen)
