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
import time

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

        self.run = True
        self.overbody = []
        self.items = []

        self.nav = []
        self.draw_nav_button()

        self.nav_name = []

        self.info_bar = []
        self.draw_info()

        self.button_info = []
        self.draw_button_info('Aide', 'Il n\'y en a pas')

        self.body = []

        self.display(screen)

    def loop(self, screen):
        clock = pygame.time.Clock()

        while self.run:
            delta_t = clock.tick( FRAME_RATE )

            self.check_update_nav(screen)

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
                            if uppest_item.type == 'item_list':
                                uppest_item.do(self,screen)

                    elif event.button == 4 or event.button == 5:
                        for item in self.items:
                            if item.type == 'item_list' and item.hover.collidepoint(mouse_pos):
                                if event.button == 4:
                                    item.move(self, screen, -40)
                                else:
                                    item.move(self, screen, 40)

                if event.type == pygame.MOUSEBUTTONUP:
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

        draw_part(self.nav_name, screen)

        if self.overbody == []:
            self.button_info[0].remove_focus()
        draw_part(self.button_info, screen)

        self.items = self.info_bar + self.nav + self.button_info + self.body

        if self.overbody != []:
            s = pygame.Surface((1280,720))
            s.set_alpha(128)
            s.fill((0,0,0))
            screen.blit(s, (0,0))
            draw_part(self.overbody, screen)
            self.items = self.overbody


    def draw_nav_button(self):
        items = []

        for i in range(0,7):
            path = 'img/icon/nav_icon_' + str(i)
            y =  i * 80 + i * 2
            button = Button_img(i, path, 0, y, change_tab, [])
            if i == 0:
                button.set_focus()
            items.append(button)

        self.nav = items

    def draw_nav_name(self):

        items = []

        icons_name = ['Home', 'Ressources Humaines', 'Recherche & Développement', 'Production', 'Finances', 'Ventes', 'Options']
        for name in icons_name:
            label = create_label(name, 'font/colvetica/colvetica.ttf', 30, (236,240,241), (52,73,94), 0, 0, None, quit, [])
            label.set_marge_items(20)
            label.set_bg_color((52,73,94))
            label.set_padding(20,0,0,0)
            label.make_pos()
            items.append(label)

        label_opt = create_label('Aide', 'font/colvetica/colvetica.ttf', 30, (236,240,241), (52,73,94), 0, 0, None, quit, [])
        label_opt.set_marge_items(20)
        label_opt.set_bg_color((52,73,94))
        label_opt.set_padding(20,0,58,0)
        label_opt.make_pos()
        items.append(label_opt)

        frame = Frame(80, 0, items, None, [])
        frame.set_direction('vertical')
        frame.set_items_pos('auto')
        frame.resize('auto', 720)
        frame.set_align('left')
        frame.set_marge_items(62)
        frame.set_bg_color((52,73,94))
        frame.set_padding(0,20,30,0)
        frame.make_pos()

        frame_bg = Frame(80, 0, [], None, [])
        frame_bg.resize(frame.rect.width+5, 720)
        frame_bg.set_bg_color((41,128,185))
        frame_bg.make_pos()

        self.nav_name = [frame_bg ,frame]

    def check_update_nav(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] <= 80 and self.overbody == [] and self.nav_name == []:
            self.draw_nav_name()
            self.display(screen)
            # s = pygame.Surface((1000,720))
            # s.set_alpha(128)
            # s.fill((0,0,0))
            # screen.blit(s, (80+self.nav_name[0].rect.width,0))
        elif mouse_pos[0] > 80 and self.nav_name != [] or self.overbody != []:
            self.nav_name = []
            self.display(screen)

    def draw_button_info(self, msg_type, msg, *arg):
        path = 'img/icon/nav_icon_info'
        y = 720 - 80
        button = Button_img(0, path, 0, y, draw_alert, [msg_type, msg])
        self.button_info = [button]

    def draw_info(self):
        info_bar = Info_bar()

        self.info_bar = [info_bar]

    def set_body(self, items):
        self.draw_button_info('Aide', 'Pas d\'astuce sur cet onglet !')
        self.body = items

    def set_overbody(self, items):
        self.overbody = items

    def quit(self):
        self.run = False


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
