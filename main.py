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
import datetime
import uuid
import math

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
from widget.rectangle import *
from world.function import *
from world.objets import *
from world.outils import *
from world.RH import *


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
        self.info_bar = []
        self.nav = []
        self.nav_name = []
        self.button_info = []
        self.body = []
        self.body_tmp = []
        self.overbody = []
        self.items = []

        self.draw_opening()

        self.display(screen)

        self.individus    = []
        self.produits     = []
        self.operations   = []
        self.materiaux    = []
        self.formations   = []
        self.populations  = []
        self.fournisseurs = []
        self.machines     = []
        self.transports   = []
        self.stocks       = []
        self.candidats    = []
        self.departs      = []
        self.couts        = []


        self.temps = None
        self.lesRH = None
        self.month = 0
        self.argent = 0

        self.sha = ''
        self.user_first_name = ''
        self.user_surname = ''

    def loop(self, screen):
        clock = pygame.time.Clock()

        while self.run:
            delta_t = clock.tick( FRAME_RATE )

            if self.nav != []:
                self.check_update_nav(screen)

            # INPUT
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                uppest_item = get_uppest_item(self.items, mouse_pos)

                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.overbody == []:
                        if self.nav == []:
                            return
                        else:
                            change_tab(self.nav[6], self, screen)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
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
                    if event.button == 1:
                        if uppest_item != None:
                            uppest_item.do(self,screen)

                # if uppest_item != None:
                #     if uppest_item.type == "button_img":
                #         draw_shadow(self, screen, uppest_item)
                #     elif len(self.overbody) == 1:
                #         self.set_overbody([])
                #         self.display(screen)


            # update display
            pygame.display.update()

    def display(self, screen):
        self.items = []
        # Draw background
        bg_color = (236,240,241)
        screen.fill(bg_color)

        draw_part(self, self.body, screen)

        draw_part(self, self.body_tmp, screen)

        draw_part(self, self.info_bar, screen)

        if self.nav != []:
            # Draw nav background
            nav_rect = pygame.Rect(0, 0, 80, 720)
            pygame.draw.rect(screen, (44,62,80), nav_rect)
        draw_part(self, self.nav, screen)

        draw_part(self, self.nav_name, screen)

        if self.overbody == [] and self.nav != []:
            self.button_info[0].remove_focus()
        draw_part(self, self.button_info, screen)

        if self.overbody != []:
            self.items = []
            s = pygame.Surface((1280,720))
            s.set_alpha(128)
            s.fill((0,0,0))
            screen.blit(s, (0,0))
            draw_part(self, self.overbody, screen)

    def draw_opening(self):

        labels = []

        new = create_label('Commencer une partie', 'font/colvetica/colvetica.ttf', 30, (236, 240, 241), (52,73,94), 0, 0, None, create_game, [])
        load = create_label('Charger une partie', 'font/colvetica/colvetica.ttf', 30, (236, 240, 241), (52,73,94), 0, 0, None, None, [])
        leave = create_label('Quitter', 'font/colvetica/colvetica.ttf', 30, (236, 240, 241), (52,73,94), 0, 0, None, quit, [])
        labels.extend([new, load, leave])

        for label in labels:
            label.set_padding(20,0,20,20)
            label.set_direction('horizontal')
            label.resize(300,"auto")
            label.set_align('center')
            label.make_pos()

        frame_v = Frame(0, 0, labels, None, [])
        frame_v.set_direction('vertical')
        frame_v.set_items_pos('auto')
        frame_v.resize(400, 'auto')
        frame_v.set_align('center')
        frame_v.set_marge_items(20)
        frame_v.set_bg_color((44, 62, 80))
        frame_v.make_pos()

        frame_left = Frame(0, 0, [frame_v], None, [])
        frame_left.set_direction('horizontal')
        frame_left.set_items_pos('auto')
        frame_left.set_align('center')
        frame_left.resize('auto', 720)
        frame_left.set_bg_color((44, 62, 80))
        frame_left.make_pos()

        title = Button_img(None, 'img/title', 0, 0, None, [])

        frame_right = Frame(400, 0, [title], None, [])
        frame_right.set_direction('horizontal')
        frame_right.set_items_pos('auto')
        frame_right.set_align('center')
        frame_right.resize('auto', 720)
        frame_right.set_bg_color((236,240,241))
        frame_right.make_pos()

        self.body = [frame_left, frame_right]

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
        button = Button_img(0, path, 0, y, draw_alert, [msg_type, msg, clear_overbody, []])
        self.button_info = [button]

    def draw_info(self):
        info_bar = Info_bar()

        self.info_bar = [info_bar]

    def set_body(self, items):
        self.draw_button_info('Aide', 'Pas d\'astuce sur cet onglet !')
        self.body = items
        self.body_tmp = []

    def set_body_tmp(self, items):
        self.body_tmp = items

    def set_overbody(self, items):
        self.overbody = items

    def quit(self):
        self.run = False

    def gen_world(self):
        self.sha = uuid.uuid4().hex
        for i in range (10):
            self.candidats.append(Individu())
        self.lesRH = RH()
        self.temps = datetime.datetime(2018,1,1) # Temps en semaines
        self.month = 1
        print(self.sha)

    def unload_world(self):
        self.individus    = []
        self.produits     = []
        self.operations   = []
        self.materiaux    = []
        self.formations   = []
        self.populations  = []
        self.fournisseurs = []
        self.machines     = []
        self.transports   = []
        self.stocks       = []
        self.candidats    = []
        self.departs      = []
        self.couts        = []

        self.temps = None
        self.lesRH = None
        self.month = 0
        self.argent = 0

    def empty_window(self):
        self.overbody = []
        self.items = []
        self.nav = []
        self.nav_name = []
        self.info_bar = []
        self.button_info = []
        self.body = []
        self.body_tmp = []


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
