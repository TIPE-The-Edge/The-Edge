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

from function import *
from widget.button_img import *
from widget.button_txt import *
from widget.entry import *
from widget.info_bar import *
from widget.item_list import *
from widget.label import *
from widget.progress_bar import *
from widget.frame import *


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

        self.items = []
        self.nav = self.draw_nav_button()
        self.info_bar = self.draw_info()
        self.button_info = []
        self.body = []

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
                        uppest_item = None
                        for item in self.items:
                            if item.rect.collidepoint(mouse_pos):
                                if uppest_item == None:
                                    uppest_item = item
                                elif uppest_item.level <= item.level:
                                    uppest_item = item

                        if uppest_item != None:
                            uppest_item.do(self,screen)

                    elif event.button == 4 or event.button == 5:
                        for item in self.items:
                            if item.type == 'item_list' and item.hover.collidepoint(mouse_pos):
                                if event.button == 4:
                                    item.move(self, screen, -40)
                                else:
                                    item.move(self, screen, 40)

            # update display
            pygame.display.update()


    def display(self, screen):
        # Draw background
        bg_color = (236,240,241)
        screen.fill(bg_color)

        draw_part(self.body, screen)

        draw_part(self.info_bar, screen)

        # Draw nav background
        nav_rect = pygame.Rect(0, 0, 80, 720)
        pygame.draw.rect(screen, (44,62,80), nav_rect)
        draw_part(self.nav, screen)

        draw_part(self.button_info, screen)

        self.items = self.info_bar + self.nav + self.button_info + self.body


    def draw_nav_button(self):
        items = []

        for i in range(0,6):
            path = 'img/icon/nav_icon_' + str(i)
            y =  i * 80 + i * 2
            button = Button_img(i, path, 0, y, change_tab)
            if i == 0:
                button.set_focus()
            items.append(button)

        return items


    def draw_info(self):
        info_bar = Info_bar()

        return [info_bar]


    def quit(self):
        pass


####################################################
##################| FONCTIONS |#####################
####################################################

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Start-up Simulator')

    window = Window(screen)
    window.loop(screen)
    window.quit()

    pygame.quit()

####################################################
################| TESTS UNITAIRES |#################
####################################################

# class Test(unittest.TestCase) :
#
#     """&
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
