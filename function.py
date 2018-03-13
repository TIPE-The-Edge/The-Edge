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

        check_words = True
        for word in words:
            label_word = Label(word, police, fontsize, msg_color, bg_color, x, y, action, arg)
            if label_word.rect.width > size:
                check_words = False
                lines.append(Label('error', police, fontsize, msg_color, bg_color, x, y, action, arg))

        while len(words) > 0 and check_words:
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
                draw_rh(None, window, screen)
            elif icon.num == 2:
                draw_rd(None, window, screen, 0)
            elif icon.num == 3:
                window.body = []
            elif icon.num == 4:
                window.body = []
            elif icon.num == 5:
                draw_option(None, window, screen)
        else:
            icon.remove_focus()

    window.display(screen)


def draw_rh(widget, window, screen, *arg):

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

    item_list_employe = Item_list(a, 680, 120, 1260, 120, 20, 680, 'employé')

    window.body = [item_list_employe, label, frame_left]
    window.display(screen)


def draw_employee(widget, window, screen, id_, i, *arg):
    items = []

    path = 'img/icon/right_white_arrow'
    button_arrow = Button_img(0, path, 0, 0, None, [])
    text = 'Employé ' + str(id_)
    name = create_label(text, 'font/colvetica/colvetica.ttf', 40, (255,255,255), (149,165,166), 0, 0, None, None, [])
    frame_back_rh = Frame(0,0, [button_arrow, name], draw_rh, [])
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
        roles = []
        item_list_role = Item_list(roles, 330, 40, 1260, 40, 20, 680, 'rôle')
        items.append(item_list_role)

    elif i == 2:
        formation = create_label("Formation", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [id_,2])
        formations = []
        item_list_formation = Item_list(formations, 330, 40, 1260, 40, 20, 680, 'formation')
        items.append(item_list_formation)
    elif i == 3:
        project = create_label("Rejoindre un projet", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [id_, 3])
        projects = []
        item_list_project = Item_list(projects, 330, 40, 1260, 40, 20, 680, 'projet')
        items.append(item_list_project)
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

    items.append(frame_left)

    window.body = items
    window.display(screen)

def draw_rd(widget, window, screen, i, *arg):
    items = []

    button_project = create_label("Projet", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_rd, [0])
    button_product = create_label("Produit", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_rd, [1])

    focus_color = (41,128,185)
    if i == 0:
        button_project = create_label("Projet", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_rd, [0])

        label_add_project = create_label("Ajouter un projet", 'font/colvetica/colvetica.ttf', 40, (255,255,255), (52,73,94), 0, 0, None, None, [])
        label_add_project.set_direction('horizontal')
        label_add_project.resize(540, 'auto')
        label_add_project.set_padding(0,0,0,0)
        label_add_project.set_align('center')
        label_add_project.make_pos()

        path = 'img/icon/grey_sum'
        icon_sum = Button_img(0, path, 0, 0, None, [])

        button_add_project = Frame(330, 40, [label_add_project, icon_sum], None, [])
        button_add_project.set_direction('horizontal')
        button_add_project.set_items_pos('auto')
        button_add_project.resize(950, 80)
        button_add_project.set_align('center')
        button_add_project.set_padding(350,0,0,0)
        button_add_project.set_marge_items(0)
        button_add_project.set_bg_color((52,73,94))
        button_add_project.make_pos()

        items.append(button_add_project)

        projects = []

        item_list_project = Item_list(projects, 330, 120, 1260, 120, 20, 600, 'projet')

        items.append(item_list_project)

    elif i == 1:
        button_product = create_label("Produit", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_rd, [1])

        products = []

        item_list_product = Item_list(products, 330, 40, 1260, 40, 20, 680, 'produit')

        items.append(item_list_product)

    list_tmp = [button_project, button_product]
    for element in list_tmp:
        element.set_direction('horizontal')
        element.resize(250, 80)
        element.set_padding(10,0,0,0)
        element.set_align('center')
        element.make_pos()

    frame_left = Frame(80, 40, list_tmp, None, [])
    frame_left.set_direction('vertical')
    frame_left.set_items_pos('auto')
    frame_left.resize(250, 680)
    frame_left.set_marge_items(2)
    frame_left.set_bg_color((189, 195, 198))
    frame_left.make_pos()

    items.append(frame_left)

    window.body = items
    window.display(screen)

def draw_option(widget, window, screen, *arg):
    button_quit = create_label("Quitter", 'font/colvetica/colvetica.ttf', 40, (255,255,255), (255,0,0), 0, 0, None, None, [])
    button_quit.set_direction('horizontal')
    button_quit.resize('auto', 'auto')
    button_quit.set_padding(50,50,20,20)
    button_quit.set_align('left')
    button_quit.make_pos()

    frame = Frame(80, 40, [button_quit], quit, [])
    frame.set_direction('vertical')
    frame.set_items_pos('auto')
    frame.resize(1200, 680)
    frame.set_align('center')
    frame.set_marge_items(0)
    frame.set_padding(0,0,280,0)
    frame.set_bg_color((236,240,241))
    frame.make_pos()

    window.body = [frame]
    window.display(screen)

def quit(widget, window, screen, *arg):
    window.quit()
