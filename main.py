#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.2
# Pygame 3.2
# Author:
# Last modified :
# Titre du Fichier :
########################

# IMPORTS
import unittest
import pygame
from pygame.sprite import Sprite, Group

# IMPORTS DE FICHIERS



""" TO DO LIST ✔✘
"""

""" PROBLEMS
"""

""" NOTES
"""

''' Commentaires

""" A quoi sert la fonction. Comment elle marche
Entrée :
Variables :
Sortie :
Vérifié par :
"""

Effacer soit la zone fonction soit la zone classe
en fonction du type du fichier.

'''
####################################################
###################| CONSTANTES |###################
####################################################

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FRAME_RATE = 60

####################################################
###################| CLASSES |######################
####################################################


class Window():

    def __init__(self,screen):
        self.current = '0'
        self.button_nav = ['nav_icon_0','nav_icon_1','nav_icon_2','nav_icon_3','nav_icon_4','nav_icon_5']

        self.create_items(screen)
        self.display(screen)

    def loop(self, screen):
        clock = pygame.time.Clock()

        while True:
            delta_t = clock.tick( FRAME_RATE )

            # INPUT
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for liste_items in self.items:
                        for item in liste_items:
                            if item.rect.collidepoint(mouse_pos):
                                item.do(self,screen)

            # update display
            pygame.display.update()

    def create_items(self, screen):
        bg_color = (236,240,241)
        screen.fill(bg_color)

        nav_button = self.draw_nav_button()
        info_bar = self.draw_info()
        frame = self.draw_item_list()
        button_info = []

        self.items = [frame, info_bar, nav_button, button_info]

    def display(self, screen):
        nav_rect = pygame.Rect(0, 0, 80, 720)
        pygame.draw.rect(screen, (44,62,80), nav_rect)

        for liste_items in self.items:
            for item in liste_items:
                # print(item.type)
                item.draw(screen)

    def draw_nav_button(self):
        items = []
        for i in range(0,len(self.button_nav)):

            path = 'img/icon/' + self.button_nav[i]
            y =  i * 80 + i * 2

            if i == int(self.current):
                button = Button_img(i, path + '_focus.png', 0, y, 80, 80, change_tab)
            else:
                button = Button_img(i, path + '.png', 0, y, 80, 80, change_tab)
            items.append(button)
        return items

    def draw_item_list(self):

        # items, list_x, list_y, item_width, item_height,
        # scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height

        item_list = Item_list([], 330, 40, 930, 80,
                              1260, 40, 20, 680)

        return [item_list]

    def draw_info(self):
        info_bar = Info_bar()

        return [info_bar]

    def quit(self):
        pass


class Button_img():
    def __init__(self, num, img, x, y, width, height, action):
        self.type = 'button_img'
        self.num = num
        self.img = pygame.image.load(img)
        self.rect = pygame.Rect(x,y,width,height)
        self.action = action

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def do(self, window, screen):
        self.action(self, window, screen)


class Button_txt():
    def __init__(self, x, y, width, height, action):
        self.type = 'button_txt'
        self.color = (236, 240, 241)
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def do(self, window, screen):
        self.action(self, window, screen)

    def move(self, shift):
        self.rect.y -= shift

class Text():
    def __init__(self, msg, f, msg_color, bg_color, x, y):
        self.image = f.render(msg, True, msg_color, bg_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Item_list():
    def __init__(self,
                 items, list_x, list_y, item_width, item_height,
                 scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height
                ):
        self.type = 'item_list'
        self.items = []

        for i in range(0,100):
            button = Button_txt(330, (40 + i * item_height + i*2), item_width, item_height, test)
            self.items.append(button)

        self.bg_color = (189, 195, 199)
        self.bg_rect = pygame.Rect(list_x, list_y, item_width, scrollbar_height)

        self.sb_bg_color = (127, 140, 141)
        self.sb_bg_rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)

        all_items_height = len(self.items) * item_height
        if all_items_height <= scrollbar_height:
            thumb_height = 0
        else:
            thumb_height = scrollbar_height * scrollbar_height / all_items_height

        self.thumb_color = (189, 195, 199)
        self.thumb_color_pressed = (149, 165, 166)
        self.rect = pygame.Rect(scrollbar_x, scrollbar_y, scrollbar_width, thumb_height)

        self.pressed = False
        self.coord_pressed = None
        self.min_height = scrollbar_y
        self.max_height = scrollbar_y + scrollbar_height - thumb_height
        self.item_shift = all_items_height / scrollbar_height

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
                if thumb_pos_y >= self.min_height and thumb_pos_y <= self.max_height:
                    self.coord_pressed = mouse_pos
                    self.rect.y = thumb_pos_y

                    if shift != 0:
                        if shift < 0:
                            signe = -1
                        else:
                            signe = 1

                        for item in self.items:
                            item.move(self.item_shift * signe)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.pressed = False
                    self.coord_pressed = None

            window.display(screen)
            pygame.display.update()


class Info_bar():
    def __init__(self):
        self.rect = pygame.Rect(80, 0, 1200, 40)

    def draw(self,screen):
        pygame.draw.rect(screen, (230,126,34), self.rect)

    def do(self, window, screen):
        pass


####################################################
##################| FONCTIONS |#####################
####################################################

def change_tab(button, window, screen):
    main_rect = pygame.Rect(80,40,1200,680)
    pygame.draw.rect(screen, (236,240,241), main_rect)

    window.current = str(button.num)
    window.create_items(screen)
    window.display(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Start-up Simulator')

    window = Window(screen)
    window.loop(screen)
    window.quit()

    pygame.quit()

def test(x, y, z):
    pass

####################################################
################| TESTS UNITAIRES |#################
####################################################

# class Test(unittest.TestCase) :
#
#     """
#      def test_fonction(self) :
#
#         #>>> Test 1 <<<#
#         # On fait les tests de la fonction en utilisant les self.assert...
#     """
#

####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :
    main()
