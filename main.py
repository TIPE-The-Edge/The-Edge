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
        bg_color = (236,240,241)
        screen.fill(bg_color)
        nav_rect = pygame.Rect(0, 0, 80, 720)
        info_rect = pygame.Rect(80, 0, 1200, 40)
        pygame.draw.rect(screen, (44,62,80), nav_rect)
        pygame.draw.rect(screen, (230,126,34), info_rect)
        self.current = '0'
        self.button_nav = ['nav_icon_0','nav_icon_1','nav_icon_2','nav_icon_3','nav_icon_4','nav_icon_5']

        self.draw(screen)

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
                    for liste_items in self.items:
                        for item in liste_items:
                            if item.rect.collidepoint(mouse_pos):
                                item.do(self,screen)



            # update display
            pygame.display.update()

    def draw(self, screen):
        nav_button = self.draw_nav_button()
        perma_info = []
        frame = []
        button_info = []

        self.items = [nav_button, perma_info, frame, button_info]
        self.blit(screen)

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

    def blit(self,screen):
        for liste_items in self.items:
            for item in liste_items:
                item.blit(screen)


    def quit(self):
        pass


class Button_img():
    def __init__(self, num, img, x, y, width, height, action):
        self.num = num
        self.img = pygame.image.load(img)
        self.rect = pygame.Rect(x,y,width,height)
        self.action = action

    def blit(self, screen):
        screen.blit(self.img, self.rect)

    def do(self, window, screen):
        self.action(self, window, screen)





####################################################
##################| FONCTIONS |#####################
####################################################

def change_tab(button, window, screen):
    nav_rect = pygame.Rect(0, 0, 80, 720)
    pygame.draw.rect(screen, (44,62,80), nav_rect)
    main_rect = pygame.Rect(80,40,1200,680)
    pygame.draw.rect(screen, (236,240,241), main_rect)

    window.current = str(button.num)
    window.draw(screen)

def main():
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
