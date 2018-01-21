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
import random
import os

# IMPORTS DE FICHIERS

from widget.button_img import *
from widget.button_txt import *
from widget.entry import *
from widget.info_bar import *
from widget.item_list import *
from widget.label import *
from widget.progress_bar import *


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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if event.button == 1:
                        for liste_items in self.items:
                            for item in liste_items:
                                if item.rect.collidepoint(mouse_pos):
                                    item.do(self,screen)

                                if item.type == 'item_list':
                                    for sub_item in item.items:
                                        if sub_item.rect.collidepoint(mouse_pos):
                                            sub_item.do(self, screen)

                    elif event.button == 4 or event.button == 5:
                        for liste_items in self.items:
                            for item in liste_items:
                                if item.type == 'item_list' and item.hover.collidepoint(mouse_pos):
                                    if event.button == 4:
                                        item.move(self, screen, -40)
                                    else:
                                        item.move(self, screen, 40)

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
                item.draw(screen)

    def draw_nav_button(self):
        items = []
        for i in range(0,len(self.button_nav)):

            path = 'img/icon/' + self.button_nav[i]
            y =  i * 80 + i * 2

            if i == int(self.current):
                button = Button_img(i, path + '_focus.png', 0, y, change_tab)
            else:
                button = Button_img(i, path + '.png', 0, y, change_tab)
            items.append(button)
        return items

    def draw_item_list(self):

        # items, list_x, list_y, item_width, item_height,
        # scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height
        items = []

        for i in range(20):
            item = Button_txt(0, 0, 930, random.randint(50,200), (255,255,255), [], test)
            items.append(item)

        item_list = Item_list(items, 330, 40,
                              1260, 40, 20, 680)

        return [item_list]

    def draw_info(self):
        info_bar = Info_bar()

        return [info_bar]

    def quit(self):
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
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Start-up Simulator')

    window = Window(screen)
    window.loop(screen)
    window.quit()

    pygame.quit()

def test(x, y, z):
    print('test')

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
