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
    for item in item_group:
        item.draw(screen)
        item.up()
        for sub_item in item.items:
            if sub_item.action == None:
                sub_item.action = item.action
        item_group.extend(item.items)

def test(x, y, z):
    print('click on the widget')

def change_tab(button, window, screen):
    for icon in window.nav:
        if icon.num == button.num:
            icon.set_focus()
        else:
            icon.remove_focus()
    
    window.body = []
    window.display(screen)
