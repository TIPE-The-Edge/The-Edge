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
        self.level = 0

        self.items = items
        self.items_pos = 'relative' # relative, fixed, auto

        # Position du coin supérieur gauche
        self.x = x
        self.y = y

        # Si les items peuvent changer de taille
        self.resize_items = False

        # Alignement
        self.align = 'left' # left(top), right(bottom), center

        # Taille de la frame
        self.size_w = 'fixed' # fixed, auto
        self.width = 0
        self.size_h = 'fixed' # fixed, auto
        self.height = 0

        # Couleur du background
        self.color = (0, 0, 0)

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
        # width : entier ou 'auto' ou anything
        # height : entier ou 'auto' ou anything
    """
    def resize(self, width, height):
        if width == 'auto':
            self.size_w = 'auto'
        elif type(width) == int:
            self.size_w = 'fixed'
            self.width = width

        if height == 'auto':
            self.size_h = 'auto'
        elif type(height) == int:
            self.size_h = 'fixed'
            self.height = height

    """ Modifie la couleur du background
    Entrée :
        # self
        # value : triple d'entier
    """
    def set_bg_color(self, value):
        self.color = value

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


    """ Modifie le paramètre d'alignement des items
    Entrée :
        # self
        # value: 'left', 'right', 'center'
    """
    def set_align(self, value):
        self.align = value


    """ Modifie le paramètre du sens d'alignement des items
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

    """ Modifie la position des items dans la frame
    Entrée :
        # self
    """
    def make_pos(self):
        if self.items_pos == 'fixed':
            pass

        elif self.items_pos == 'relative':
            for item in self.items:

                if self.size_w == 'auto':
                    new_width = self.padding_left + item.rect.width + self.padding_right + item.rect.x
                    if new_width > self.width:
                        self.width = new_width

                if self.size_h == 'auto':
                    new_height = self.padding_top + item.rect.height + self.padding_bottom + item.rect.y
                    if new_height > self.height:
                        self.height = new_height

                item.rect.x = item.rect.x + self.x + self.padding_left
                item.rect.y = item.rect.y + self.y + self.padding_top

                for sub_item in item.items:
                    sub_item.rect.x = sub_item.rect.x + item.rect.x
                    sub_item.rect.y = sub_item.rect.y + item.rect.y
                    if sub_item.type == 'item_list':
                        print('test')
                        sub_item.replace(item.rect.x, item.rect.y)
                    item.items.extend(sub_item.items)

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

                    elif self.size_w == 'fixed' and self.resize_items:
                        max_width = self.width - self.padding_left - self.padding_right
                        if item.rect.width < max_width:
                            try:
                                item.resize(max_width)
                            except:
                                pass

                    item.rect.y = sum_size

                    items_tmp = []
                    items_tmp += item.items
                    for sub_item in items_tmp:
                        sub_item.rect.y = sub_item.rect.y + item.rect.y
                        if sub_item.type == 'item_list':
                            print('test')
                            sub_item.replace(0, item.rect.y)
                        items_tmp.extend(sub_item.items)

                    sum_size += item.rect.height + self.marge_items

                elif self.direction == 'horizontal':
                    if self.size_h == 'auto':
                        new_height = self.padding_top + item.rect.height + self.padding_bottom
                        if new_height > self.height:
                            self.height = new_height

                    elif self.size_h == 'fixed' and self.resize_items:
                        max_height = self.height - self.padding_top - self.padding_bottom
                        if item.rect.height < max_height:
                            try:
                                item.resize(max_height)
                            except:
                                pass

                    item.rect.x = sum_size

                    items_tmp = []
                    items_tmp += item.items
                    for sub_item in items_tmp:
                        sub_item.rect.x = sub_item.rect.x + item.rect.x
                        if sub_item.type == 'item_list':
                            print('test')
                            sub_item.replace(item.rect.x, 0)
                        items_tmp.extend(sub_item.items)

                    sum_size += item.rect.width + self.marge_items

            for item in self.items:

                if self.direction == 'vertical':
                    if self.align == 'left':
                        item.rect.x = self.x + self.padding_left
                    elif self.align == 'right':
                        item.rect.x = self.x + self.width - self.padding_right - item.rect.width
                    elif self.align == 'center':
                        item.rect.x = (self.padding_left + self.width)//2 - (item.rect.width//2) + self.x

                    items_tmp = []
                    items_tmp += item.items
                    for sub_item in items_tmp:
                        sub_item.rect.x = sub_item.rect.x + item.rect.x
                        if sub_item.type == 'item_list':
                            print('test')
                            sub_item.replace(item.rect.x, 0)
                        items_tmp.extend(sub_item.items)

                elif self.direction == 'horizontal':
                    if self.align == 'left':
                        item.rect.y = self.y + self.padding_top
                    elif self.align == 'right':
                        item.rect.y = self.y + self.height - self.padding_bottom - item.rect.height
                    elif self.align == 'center':
                        item.rect.y = (self.padding_top + self.height)//2 - (item.rect.height//2) + self.y

                    items_tmp = []
                    items_tmp += item.items
                    for sub_item in items_tmp:
                        sub_item.rect.y = sub_item.rect.y + item.rect.y
                        if sub_item.type == 'item_list':
                            print('test')
                            sub_item.replace(0, item.rect.y)
                        items_tmp.extend(sub_item.items)

            if self.direction == 'vertical':
                if self.size_h == 'auto':
                    sum_size += self.padding_bottom - self.y - self.marge_items
                    self.height = sum_size

            elif self.direction == 'horizontal':
                if self.size_w == 'auto':
                    sum_size += self.padding_right - self.x - self.marge_items
                    self.width = sum_size

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hover = pygame.Rect(self.x, self.y, self.width, self.height)

    """ Dessine les items de la frame en fonction de ses paramètres
    Entrée :
        # self
        # screen
    """
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


    def do(self, window, screen):
        if self.action != None:
            self.action(self, window, screen)

    def up(self):
        for item in self.items:
            item.level += 1
