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


def create_label(text, police, fontsize, msg_color, bg_color, x, y, size, action):
    if size == None:
        label =  Label(text, police, fontsize, msg_color, bg_color, x, y, action)

        frame = Frame(x, y, [label], action)

    else:
        words = text.split(' ')
        lines = []
        while len(words) > 0:
            i = 0
            line = words[i]
            label = Label(line, police, fontsize, msg_color, bg_color, x, y, action)

            while label.rect.width <= size:
                i += 1
                if i >= len(words):
                    old_line = line
                    break
                else:
                    old_line = line
                    line += ' ' + words[i]
                    label = Label(line, police, fontsize, msg_color, bg_color, x, y, action)
            words = words[i:]
            label = Label(old_line, police, fontsize, msg_color, bg_color, x, y, action)
            lines.append(label)

        frame = Frame(x, y, lines, action)

    frame.set_direction('vertical')
    frame.set_items_pos('auto')
    frame.resize('auto', 'auto')
    frame.set_align('left')
    frame.set_bg_color(bg_color)
    frame.make_pos()

    return frame


def draw_part(item_group, screen):
    i = 1
    for item in item_group:
        item.draw(screen)
        item.up()
        for sub_item in item.items:
            if sub_item.action == None:
                sub_item.action = item.action
        item_group[i:i] = item.items
        i += 1


def change_tab(button, window, screen):
    for icon in window.nav:
        if icon.num == button.num:
            icon.set_focus()

            if icon.num == 0:
                window.body = []
            elif icon.num == 1:
                window.body = draw_rh()
            elif icon.num == 2:
                window.body = []
            elif icon.num == 3:
                window.body = []
            elif icon.num == 4:
                window.body = []
            elif icon.num == 5:
                window.body = []
        else:
            icon.remove_focus()


    window.display(screen)

def draw_rh():
    frame_left = Frame(80, 40, [], None)
    frame_left.set_direction('vertical')
    frame_left.set_items_pos('auto')
    frame_left.resize(600, 680)
    frame_left.set_padding(10,10,10,10)
    frame_left.set_marge_items(10)
    frame_left.set_bg_color((189, 195, 198))
    frame_left.make_pos()

    text = 'Liste des employés'
    label = create_label(text, 'arial', 30, (255,255,255), (52,73,94), 680, 40, None, None)
    label.set_direction('horizontal')
    label.set_padding(30,10,10,10)
    label.resize(680, 80)
    label.set_align('center')
    label.make_pos()

    a = []
    for i in range(20):
        entry1 = Entry(0, 0, 100, 50, None, True)
        frame = Frame(0,0, [entry1], None)
        frame.set_direction('horizontal')
        frame.set_items_pos('auto')
        frame.resize(580, 'auto')
        frame.set_align('left')
        frame.set_padding(10,10,10,10)
        frame.set_marge_items(10)
        frame.make_pos()
        a.append(frame)

    item_list_employe = Item_list(a, 680, 120, 1260, 120, 20, 680)

    return [item_list_employe, label, frame_left]
