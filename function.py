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


def create_label(text, police, fontsize, msg_color, bg_color, x, y, size, action, arg):
    if size == None:
        label =  Label(text, police, fontsize, msg_color, bg_color, x, y, action, arg)

        frame = Frame(x, y, [label], action, arg)

    else:
        words = text.split(' ')
        lines = []
        while len(words) > 0:
            i = 0
            line = words[i]
            label = Label(line, police, fontsize, msg_color, bg_color, x, y, action, arg)

            while label.rect.width <= size:
                i += 1
                if i >= len(words):
                    old_line = line
                    break
                else:
                    old_line = line
                    line += ' ' + words[i]
                    label = Label(line, police, fontsize, msg_color, bg_color, x, y, action, arg)
            words = words[i:]
            label = Label(old_line, police, fontsize, msg_color, bg_color, x, y, action, arg)
            lines.append(label)

        frame = Frame(x, y, lines, action, arg)

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
                sub_item.arg = item.arg
        item_group[i:i] = item.items
        i += 1


def clear_body(widget, window, screen, *arg):
    window.body = arg[0](*arg)
    window.display(screen)


def change_tab(button, window, screen, *arg):
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


def draw_rh(*arg):

    frame_left = Frame(80, 40, [], None, [])
    frame_left.set_direction('vertical')
    frame_left.set_items_pos('auto')
    frame_left.resize(600, 680)
    frame_left.set_padding(10,10,10,10)
    frame_left.set_marge_items(10)
    frame_left.set_bg_color((189, 195, 198))
    frame_left.make_pos()

    text = 'Liste des employés'
    label = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 680, 40, None, None, [])
    label.set_direction('horizontal')
    label.set_padding(20,10,10,10)
    label.resize(680, 80)
    label.set_align('center')
    label.make_pos()

    a = []
    for i in range(20):
        employed = create_label("employé " + str(i), 'calibri', 30, (255,255,255), (0,0,0), 0, 0, None, draw_employee, [i, 0])
        employed.set_direction('horizontal')
        employed.resize(580, 100)
        employed.set_padding(20,0,0,0)
        employed.set_align('center')
        employed.make_pos()
        a.append(employed)

    item_list_employe = Item_list(a, 680, 120, 1260, 120, 20, 680)

    return [item_list_employe, label, frame_left]


def draw_employee(widget, window, screen, id_, i, *arg):
    path = 'img/icon/right_white_arrow'
    button_arrow = Button_img(0, path, 0, 0, None, [])
    text = 'Employé ' + str(id_)
    name = create_label(text, 'font/colvetica/colvetica.ttf', 40, (255,255,255), (149,165,166), 0, 0, None, None, [])
    frame_back_rh = Frame(0,0, [button_arrow, name], clear_body, [draw_rh])
    frame_back_rh.set_direction('horizontal')
    frame_back_rh.set_items_pos('auto')
    frame_back_rh.resize(250, 80)
    frame_back_rh.set_align('center')
    frame_back_rh.set_padding(10,0,0,0)
    frame_back_rh.set_marge_items(10)
    frame_back_rh.set_bg_color((149, 165, 166))
    frame_back_rh.make_pos()

    attribute = create_label("Caractéristique", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee, [id_, 0])
    role = create_label("Changer de rôle", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee, [id_,1])
    formation = create_label("Formation", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee, [id_,2])
    project = create_label("Rejoindre un projet", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee, [id_,3])
    fired = create_label("Licencier", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee, [id_,4])

    focus_color = (41,128,185)
    if i == 0:
        attribute = create_label("Caractéristique", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [id_,0])
    elif i == 1:
        role = create_label("Changer de rôle", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [id_,1])
    elif i == 2:
        formation = create_label("Formation", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [id_,2])
    elif i == 3:
        project = create_label("Rejoindre un projet", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [id_, 3])
    elif i == 4:
        fired = create_label("Licencier", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [id_,4])


    list_tmp = [attribute, role, formation, project, fired]
    for element in list_tmp:
        element.set_direction('horizontal')
        element.resize(250, 80)
        element.set_padding(10,0,0,0)
        element.set_align('center')
        element.make_pos()

    frame_left = Frame(80, 40, [frame_back_rh] + list_tmp, None, [])
    frame_left.set_direction('vertical')
    frame_left.set_items_pos('auto')
    frame_left.resize(250, 680)
    frame_left.set_marge_items(2)
    frame_left.set_bg_color((189, 195, 198))
    frame_left.make_pos()

    window.body = [frame_left]
    window.display(screen)
