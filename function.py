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
import math
import re
import string
import pickle
import time
import datetime

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
from world.innov import *
from world.contracterPret import *
from lib.save import *

'''
================================================================================
AUTRES
================================================================================
'''

def create_label(text, police, fontsize, msg_color, bg_color, x, y, size, action, *arg):

    if type(text) != list:
        text = [text]

    if size == None:
        labels = []
        for element in text:
            label = Label(element, police, fontsize, msg_color, bg_color, x, y, action, *arg)
            labels.append(label)
        frame = Frame(x, y, labels, action, *arg)

    else:
        lines = []

        for element in text:
            words = element.split(' ')

            check_words = True
            for word in words:
                label_word = Label(word, police, fontsize, msg_color, bg_color, x, y, action, *arg)
                if label_word.rect.width > size:
                    check_words = False
                    lines.append(Label('error', police, fontsize, msg_color, bg_color, x, y, action, *arg))

            while len(words) > 0 and check_words:
                i = 0
                line = words[i]
                label = Label(line, police, fontsize, msg_color, bg_color, x, y, action, *arg)

                while label.rect.width <= size:
                    i += 1
                    if i >= len(words):
                        old_line = line
                        break
                    else:
                        old_line = line
                        line += ' ' + words[i]
                        label = Label(line, police, fontsize, msg_color, bg_color, x, y, action, *arg)
                words = words[i:]
                label = Label(old_line, police, fontsize, msg_color, bg_color, x, y, action, *arg)
                lines.append(label)

        frame = Frame(x, y, lines, action, *arg)

    frame.set_direction('vertical')
    frame.set_items_pos('auto')
    frame.resize('auto', 'auto')
    frame.set_align('left')
    frame.set_bg_color(bg_color)
    frame.make_pos()

    return frame

def create_label_value(labels, font1, font2, size1, size2, color1, color2, color_bg1, color_bg2, width1, width):
    items = []
    if width1 == 'auto':
        size = None
    else:
        size = width1
    for element in labels:
        label = create_label(element[0] + ' : ', font1, size1, color1, color_bg1, 0, 0, size, None, [])
        label.resize(width1, 'auto')
        label.make_pos()
        value = create_label(str(element[1]), font2, size2, color2, color_bg2, 0, 0, None, None, [])

        frame_tmp = Frame(0, 0, [label,value], None, [])
        frame_tmp.set_direction('horizontal')
        frame_tmp.set_items_pos('auto')
        frame_tmp.set_bg_color(color_bg2)
        frame_tmp.set_marge_items(50)
        frame_tmp.resize(width, 'auto')
        frame_tmp.make_pos()

        items.append(frame_tmp)

    return items

def create_button(text, police, fontsize, msg_color, bg_color, x, y, width, height, action, *arg):
    button = create_label(text, police, fontsize, msg_color, bg_color, x, y, None, action, *arg)
    button.resize(width,'auto')
    button.set_align('center')
    button.make_pos()

    frame_tmp = Frame(0, 0, [button], action, *arg)
    frame_tmp.set_direction('horizontal')
    frame_tmp.set_items_pos('auto')
    frame_tmp.resize('auto', height)
    frame_tmp.set_align('center')
    frame_tmp.set_bg_color(bg_color)
    frame_tmp.make_pos()

    return frame_tmp

def check_string(widget, window, screen, regex, text, error_msg, *arg):
    if re.match(regex, text) == None:
        draw_alert(widget, window, screen, "Erreur", error_msg, clear_overbody, [])
        return False
    else:
        return True

def draw_part(window, item_group, screen):
    item_group_tmp = []
    item_group_tmp += item_group
    i = 1
    for item in item_group_tmp:
        item.draw(screen)
        item.up()
        for sub_item in item.items:
            if sub_item.action == None:
                sub_item.action = item.action
                sub_item.arg = item.arg
        item_group_tmp[i:i] = item.items
        i += 1
    window.items += item_group_tmp

def get_uppest_item(items, mouse_pos):
    uppest_item = None
    for item in items:
        if item.rect.collidepoint(mouse_pos):
            if uppest_item == None:
                uppest_item = item
            elif uppest_item.level <= item.level:
                uppest_item = item

    return uppest_item

def clear_body(widget, window, screen, *arg):
    window.set_body(arg[0](*arg))
    window.display(screen)

def quit(widget, window, screen, *arg):
    window.quit()

def get_entry(widget, window, screen, *arg):
    entry_values = {}
    for item in window.items:
        if item.type == 'entry':
            entry_values.update({item.id: item.entry})
    return entry_values

'''INCOMPLET'''
def change_tab(button, window, screen, *arg):
    for icon in window.nav:
        if icon.num == button.num:
            icon.set_focus()
            window.num_window = icon.num
            if icon.num == 0:
                draw_home(None, window, screen)
            elif icon.num == 1:
                draw_rh(None, window, screen)
            elif icon.num == 2:
                draw_rd(None, window, screen, 0)
            elif icon.num == 3:
                window.set_body([])
            elif icon.num == 4:
                draw_finance(None, window, screen, 0)
            elif icon.num == 5:
                draw_sales_product(None, window, screen, 0, 0)
            elif icon.num == 6:
                draw_option(None, window, screen)
        else:
            icon.remove_focus()

    window.draw_nav_name()
    window.display(screen)

def draw_alert_tmp(widget, window, screen, msg_type, msg, *arg):
    items = []
    try:
        widget.set_focus()
    except:
        pass

    rect = Rectangle(0, 0, 1280, 720, (0,0,0), 0, clear_overbody, [])

    if msg_type != '':
        label_type = create_label(msg_type, 'font/colvetica/colvetica.ttf', 50, (44, 62, 80), (236,240,241), 0, 0, 1280//3, None, [])
        label_type.set_align('center')
        label_type.make_pos()
        items.append(label_type)

    label_msg = create_label(msg, 'font/colvetica/colvetica.ttf', 30, (52, 73, 95), (236,240,241), 0, 0, 1280//3, None, [])
    label_msg.set_align('center')
    label_msg.make_pos()
    items.append(label_msg)

    label_msg_save = create_label("Partie sauvegardé", 'font/colvetica/colvetica.ttf', 30, (52, 73, 95), (236,240,241), 0, 0, 1280//3, None, [])
    label_msg_save.set_align('center')
    label_msg_save.make_pos()
    items.append(label_msg_save)

    frame = Frame(0, 0, items, clear_overbody, [])
    frame.set_direction('vertical')
    frame.set_items_pos('auto')
    frame.resize('auto', 'auto')
    frame.set_align('center')
    frame.set_marge_items(50)
    frame.set_bg_color((236,240,241))
    frame.set_padding(50,50,30,30)
    frame.make_pos()

    frame.move(1280/2 - frame.rect.width//2, 720/2 - frame.rect.height//2)

    window.set_overbody([rect, frame])
    window.display(screen)

def draw_alert(widget, window, screen, msg_type, msg, *arg):
    items = []
    try:
        widget.set_focus()
    except:
        pass

    if msg_type != '':
        label_type = create_label(msg_type, 'font/colvetica/colvetica.ttf', 50, (44, 62, 80), (236,240,241), 0, 0, 1280//3, None, [])
        label_type.set_align('center')
        label_type.make_pos()
        items.append(label_type)

    label_msg = create_label(msg, 'font/colvetica/colvetica.ttf', 30, (52, 73, 95), (236,240,241), 0, 0, 1280//3, None, [])
    label_msg.set_align('center')
    label_msg.make_pos()
    items.append(label_msg)

    button_close = create_label("Fermer", 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230,126,34), 0, 0, None, clear_overbody, [])
    button_close.set_direction('horizontal')
    button_close.set_padding(30,30,10,10)
    button_close.make_pos()
    items.append(button_close)

    frame = Frame(0, 0, items, None, [])
    frame.set_direction('vertical')
    frame.set_items_pos('auto')
    frame.resize('auto', 'auto')
    frame.set_align('center')
    frame.set_marge_items(50)
    frame.set_bg_color((236,240,241))
    frame.set_padding(50,50,30,30)
    frame.make_pos()

    frame.move(1280/2 - frame.rect.width//2, 720/2 - frame.rect.height//2)

    window.set_overbody([frame])
    window.display(screen)

def draw_alert_option(widget, window, screen, msg_type, msg, callbacks, *arg):
    items = []
    try:
        widget.set_focus()
    except:
        pass

    if msg_type != '':
        label_type = create_label(msg_type, 'font/colvetica/colvetica.ttf', 50, (44, 62, 80), (236,240,241), 0, 0, 1280//3, None, [])
        label_type.set_align('center')
        label_type.make_pos()
        items.append(label_type)

    label_msg = create_label(msg, 'font/colvetica/colvetica.ttf', 30, (52, 73, 95), (236,240,241), 0, 0, 1280//3, None, [])
    label_msg.set_align('center')
    label_msg.make_pos()
    items.append(label_msg)

    buttons = []
    for element in callbacks:
        button = create_label(element[0], 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230,126,34), 0, 0, None, element[1], element[2])
        button.set_padding(30,30,10,10)
        button.make_pos()
        buttons.append(button)
    frame_button = Frame(0, 0, buttons, None, [])
    frame_button.set_direction('horizontal')
    frame_button.set_items_pos('auto')
    frame_button.resize('auto', 'auto')
    frame_button.set_bg_color((236,240,241))
    frame_button.set_marge_items(50)
    frame_button.make_pos()
    items.append(frame_button)

    frame = Frame(0, 0, items, None, [])
    frame.set_direction('vertical')
    frame.set_items_pos('auto')
    frame.resize('auto', 'auto')
    frame.set_align('center')
    frame.set_marge_items(50)
    frame.set_bg_color((236,240,241))
    frame.set_padding(50,50,30,30)
    frame.make_pos()

    frame.move(1280/2 - frame.rect.width//2, 720/2 - frame.rect.height//2)

    window.set_overbody([frame])
    window.display(screen)

def clear_overbody(widget, window, screen, *arg):
    window.set_overbody([])
    window.items = window.info_bar + window.nav + window.button_info + window.body + window.body_tmp
    window.display(screen)

def draw_ask_name(widget, window, screen, *arg):
    path = 'img/icon/left_gray_arrow'
    button_arrow = Button_img(0, path, 0, 0, reset_game, [])

    label1 = create_label('Avant de commencer,', 'font/colvetica/colvetica.ttf', 45, (127, 140, 141), (236, 240, 241), 0, 0 , None, None, [])
    label2 = create_label('Quel est votre nom ?', 'font/colvetica/colvetica.ttf', 45, (127, 140, 141), (236, 240, 241), 0, 0 , None, None, [])
    entry = Entry(0, 0, 500, 60, False, 'user_name', 0, None)

    button_submit = create_label('Continuer', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, set_name, [])
    button_submit.set_direction('vertical')
    button_submit.resize(500,'auto')
    button_submit.set_align('center')
    button_submit.make_pos()

    frame_v = Frame(0, 0, [button_submit], set_name, [])
    frame_v.set_direction('horizontal')
    frame_v.set_items_pos('auto')
    frame_v.resize('auto', 60)
    frame_v.set_align('center')
    frame_v.set_bg_color((230, 126, 34))
    frame_v.make_pos()

    frame_v1 = Frame(0, 0, [label1, label2, entry, frame_v], None, [])
    frame_v1.set_direction('vertical')
    frame_v1.set_items_pos('auto')
    frame_v1.set_marge_items(20)
    frame_v1.resize(1280, 'auto')
    frame_v1.set_align('center')
    frame_v1.set_bg_color((236, 240, 241))
    frame_v1.make_pos()

    frame = Frame(0, 0, [frame_v1], None, [])
    frame.set_direction('horizontal')
    frame.set_items_pos('auto')
    frame.resize('auto', 720)
    frame.set_align('center')
    frame.set_bg_color((236, 240, 241))
    frame.make_pos()

    window.body = [frame, button_arrow]
    window.display(screen)

def set_name(widget, window, screen, *arg):
    entry = get_entry(widget, window, screen, *arg)
    if check_string(widget, window, screen, r"^[a-zA-Zéèàùç\-]+$", entry['user_name'], "Des caractères ne sont pas acceptés"):
        window.user_name = entry['user_name']
        create_game(widget, window, screen, *arg)

def create_game(widget, window, screen, *arg):
    window.gen_world()

    start_game(window, screen)

def reset_game(widget, window, screen, *arg):
    window.set_window()
    window.set_var()
    window.draw_opening()
    window.display(screen)

def close_game(widget, window, screen, *arg):
    window.run = False

'''INCOMPLET'''
def draw_load_game(widget, window, screen, *arg):
    text = 'Sauvegardes'
    label = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 64, 48 , None, None, [])
    label.set_direction('horizontal')
    label.set_padding(20,10,10,10)
    label.resize(512, 80)
    label.set_align('center')
    label.make_pos()

    a = []
    for save in window.save.getSaves():
        save_info = []

        save_info.append(create_label(save[1], 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        frame_save_info = Frame(0, 0, save_info, draw_save, [save[0]])
        frame_save_info.set_direction('vertical')
        frame_save_info.set_items_pos('auto')
        frame_save_info.resize(492, 'auto')
        frame_save_info.set_padding(20,0,20,20)
        frame_save_info.set_bg_color((236, 240, 241))
        frame_save_info.make_pos()

        a.append(frame_save_info)

    item_list_save = Item_list(a, 64, 128, 556, 128, 20, 448, 'sauvegarde')

    text = 'Informations sur la sauvegarde'
    label_save = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (149,165,166), 640, 0, None, None, [])
    label_save.set_direction('horizontal')
    label_save.set_padding(20,10,10,10)
    label_save.resize(640, 80)
    label_save.set_align('center')
    label_save.make_pos()

    text = 'Sélectionner une sauvegarde'
    label_void = create_label(text, 'font/colvetica/colvetica.ttf', 40, (189, 195, 198), (236,240,241), 0, 0, 660, None, [])
    label_void.set_direction('horizontal')
    label_void.resize('auto', 'auto')
    # label_void.set_padding(0,10,10,10)
    label_void.set_align('center')
    label_void.make_pos()

    frame_right = Frame(640, 375, [label_void], None, [])
    frame_right.set_direction('vertical')
    frame_right.set_items_pos('auto')
    frame_right.resize(640, 'auto')
    frame_right.set_align('center')
    frame_right.set_bg_color((236,240,241))
    frame_right.make_pos()

    button_return = create_label( 'Menu principal', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, reset_game, [])
    button_return.set_direction('vertical')
    button_return.resize(514,'auto')
    button_return.set_align('center')
    button_return.make_pos()

    frame_v = Frame(64, 605, [button_return], reset_game, [])
    frame_v.set_direction('horizontal')
    frame_v.set_items_pos('auto')
    frame_v.resize('auto', 68)
    frame_v.set_align('center')
    frame_v.set_bg_color((230, 126, 34))
    frame_v.make_pos()

    rect0 = Rectangle(0, 0, 640, 720, (44,62,80), None, None, [])
    rect1 = Rectangle(64, 0, 512, 48, (44,62,80), None, None, [])
    rect2 = Rectangle(64, 576, 512, 145, (44,62,80), None, None, [])

    window.body = [rect0, item_list_save, rect1, rect2, label, label_save, frame_right, frame_v]
    window.display(screen)

'''IMCOMPLET'''
def draw_save(widget, window, screen, save_name, *arg):
    save = window.save.getSave(save_name)

    title = create_label(save.user_name, 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
    title.set_padding(0,0,0,20)
    title.make_pos()

    info1, info2, info3, info4, info5 = [], [], [], [], []
    info1.append(['Date de création', save.date_creation.strftime('%d/%m/%y')])
    info1.append(['Temps d\'utilisation', time_convert(save.total_time)])
    info1.append(['Dernière utilisation', save.last_used.strftime('%d/%m/%y')])

    infos = [info1, info2, info3, info4, info5]
    frame_labels = []
    for info in infos:
        label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 25, 20, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 200, 0)
        frame_tmp = Frame(0, 0, label_tmp, None, [])
        frame_tmp.set_items_pos('auto')
        frame_tmp.set_marge_items(10)
        frame_tmp.set_direction('vertical')
        frame_tmp.resize('auto', 'auto')
        frame_tmp.set_bg_color((236, 240, 241))
        frame_tmp.make_pos()
        frame_labels.append(frame_tmp)


    frame_right = Frame(640, 70, [title] + frame_labels, None, [])
    frame_right.set_direction('vertical')
    frame_right.set_items_pos('auto')
    frame_right.resize(640, 537)
    frame_right.set_padding(30,0,30,0)
    frame_right.set_bg_color((236,240,241))
    frame_right.make_pos()

    button_load = create_label( 'Charger', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, load, [save_name])
    button_load.set_direction('vertical')
    button_load.resize(514,'auto')
    button_load.set_align('center')
    button_load.make_pos()

    frame_v1 = Frame(704, 605, [button_load], load, [save_name])
    frame_v1.set_direction('horizontal')
    frame_v1.set_items_pos('auto')
    frame_v1.resize('auto', 68)
    frame_v1.set_align('center')
    frame_v1.set_bg_color((230, 126, 34))
    frame_v1.make_pos()

    window.set_body_tmp([frame_right, frame_v1])
    window.display(screen)

def load(widget, window, screen, save_name,*arg):
    window.save.load(window, save_name)
    start_game(window, screen)

def start_game(window, screen):
    window.time_start = round(time.time())
    window.draw_info()
    window.draw_nav_button()
    window.draw_button_info('Aide', 'Il n\'y en a pas')
    draw_home(None, window, screen)

def get_with_id(group, ind_id):
    for ind in group:
        if ind.id == ind_id:
            return ind
    return None

def time_convert(time):
    hour = (time // 3600)
    min = (time // 60)

    if hour == 1:
        return str(hour) + ' heure'
    elif hour > 1 :
        return str(hour) + ' heures'
    elif min == 1:
        return str(min) + ' minute'
    elif min > 1 :
        return str(min) + ' minutes'
    else:
        return str(time) + ' secondes'



'''
================================================================================
HOME
================================================================================
'''

'''IMCOMPLET'''
def draw_home(widget, window, screen, *arg):
    text = 'Notification'
    label = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 80, 40, None, None, [])
    label.set_direction('horizontal')
    label.set_padding(20,10,10,10)
    label.resize(600, 80)
    label.set_align('center')
    label.make_pos()

    a = []
    # for nottif in window.candidats:
    #     employee_info = []
    #
    #     employee_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
    #     employee_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
    #     employee_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
    #     employee_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
    #
    #     frame_employee = Frame(0, 0, employee_info, draw_individu, [ind.id])
    #     frame_employee.set_direction('vertical')
    #     frame_employee.set_items_pos('auto')
    #     frame_employee.resize(580, 'auto')
    #     frame_employee.set_padding(20,0,20,20)
    #     frame_employee.set_bg_color((236, 240, 241))
    #     frame_employee.make_pos()
    #
    #     a.append(frame_employee)

    item_list_notif = Item_list(a, 80, 120, 660, 120, 20, 600, 'notification')

    button_next = create_label('Tour suivant', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, next_tour, [])
    button_next.set_padding(20,20,15,15)
    button_next.make_pos()
    button_next.set_pos(1280-10-button_next.width, 720-10-button_next.height)
    button_next.make_pos()

    window.set_body([label, item_list_notif, button_next])
    window.draw_button_info('Aide', 'Salut')
    window.display(screen)

def next_tour(widget, window, screen, *arg):

    #>>> partie RD
    window.projets = avance(window.projets, window.paliers, window.individus)
    # Il faut faire apparaitre les nootifications.
    window.projets, frais_RD, notifications = allProgression(window.projets, window.individus, window.paliers)
    for i in range(len(frais_RD)) :
        window.depenses.append(frais_RD[i])
    completedProject(window.projets, window.produits, window.individus)

    # # Affichage des notifications
    # for notification in notifications :
    #     draw_alert(widget, window, screen, 'Message', notification, clear_overbody, [])

    save(widget, window, screen, *arg)
    draw_alert_tmp(widget, window, screen, 'Nouvelle semaine', "Semaine x", [])



'''
================================================================================
RH
================================================================================
'''

def draw_rh(widget, window, screen, *arg):
    rh = window.lesRH

    info1, info2, info3, info4 = [], [], [], []
    info1.append(['Nombre d\'employés', rh.nbr_employes])
    # info.append(['Bonheur moyen', rh.bonheur_moy])
    info1.append(['Âge moyen', rh.age_moy])
    info2.append(['Temps moyen passé dans la start-up', rh.exp_start_up_moy])
    info2.append(['Expérience moyenne en R&D', rh.exp_RetD_moy])
    info3.append(['Nombre d\'arrivées durant le dernier mois', rh.nbr_arrivees])
    # info.append(['Taux d\'arrivées', rh.taux_arrivees])
    info3.append(['Nombre de départs durant le dernier mois', rh.nbr_departs])
    # info.append(['Taux de départ', rh.taux_departs])
    # info.append(['what', rh.taux_rotation])
    # info.append(['Coût de formations', rh.cout_formations])
    # info.append(['Moyenne formations', rh.moy_formations])
    info4.append(['Salaire moyen', rh.salaire_moy])
    info4.append(['Masse salariale brute', rh.masse_sal_brute])
    info4.append(['Masse salariale nette', rh.masse_sal_nette])
    info4.append(['Coût de l\'emploi', rh.cout_emploi])
    info4.append(['Coût moyen de l\'emploi', rh.cout_moy_emploi])
    info4.append(['Part de la masse salariale dans le budget de l\'entreprise', rh.part_masse_sal])

    infos = [info1, info2, info3, info4]
    frame_labels = []
    for info in infos:
        label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 25, 20, (255,255,255), (255,255,255), (189,195,198), (189,195,198), 400, 'auto')
        frame_tmp = Frame(0, 0, label_tmp, None, [])
        frame_tmp.set_items_pos('auto')
        frame_tmp.set_marge_items(10)
        frame_tmp.set_direction('vertical')
        frame_tmp.resize('auto', 'auto')
        frame_tmp.set_bg_color((189,195,198))
        frame_tmp.make_pos()
        frame_labels.append(frame_tmp)

    button_hired = create_label( 'Recruter', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, draw_recruit, [])
    button_hired.set_padding(0,0,15,15)
    button_hired.set_direction('vertical')
    button_hired.resize(300,"auto")
    button_hired.set_align('center')
    button_hired.make_pos()

    frame_v = Frame(0, 0, [button_hired], None, [])
    frame_v.set_direction('vertical')
    frame_v.set_items_pos('auto')
    frame_v.resize(560, 'auto')
    frame_v.set_align('center')
    frame_v.set_padding(0,0,20,0)
    frame_v.set_bg_color((189, 195, 198))
    frame_v.make_pos()

    frame_left = Frame(80, 40, frame_labels + [frame_v] , None, [])
    frame_left.set_direction('vertical')
    frame_left.set_items_pos('auto')
    frame_left.resize(600, 680)
    frame_left.set_padding(20,20,20,20)
    frame_left.set_marge_items(50)
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
    for ind in window.individus:
        employee_info = []

        employee_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        employee_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
        employee_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        employee_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        frame_employee = Frame(0, 0, employee_info, draw_employee, [ind.id, 0])
        frame_employee.set_direction('vertical')
        frame_employee.set_items_pos('auto')
        frame_employee.resize(580, 'auto')
        frame_employee.set_padding(20,0,20,20)
        frame_employee.set_bg_color((236, 240, 241))
        frame_employee.make_pos()

        a.append(frame_employee)

    item_list_employe = Item_list(a, 680, 120, 1260, 120, 20, 600, 'employé')

    window.set_body([item_list_employe, label, frame_left])
    window.draw_button_info('Aide', 'Informe toi sur les ressources humaines et intéragis avec les employées !')
    window.display(screen)

def draw_employee(widget, window, screen, ind_id, i, *arg):
    ind = get_with_id(window.individus, ind_id)

    items = []

    path = 'img/icon/right_white_arrow'
    button_arrow = Button_img(0, path, 0, 0, None, [])
    text = 'Employé ' + str(ind_id)
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

    attribute = create_label("Caractéristique", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee, [ind_id, 0])
    role = create_label("Changer de rôle", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee, [ind_id,1])
    formation = create_label("Formation", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee, [ind_id,2])

    f1 = ["Oui", fired_ind, [ind_id]]
    f2 = ["Non", clear_overbody, []]
    fired = create_label("Licencier", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_alert_option, ['', 'Voulez-vous vraiment licencier ' + ind.prenom + ' ' + ind.nom + ' ?',[f1, f2]])

    focus_color = (41,128,185)
    if i == 0:
        attribute = create_label("Caractéristique", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [ind_id,0])

        title = create_label(ind.prenom + ' ' + ind.nom, 'font/colvetica/colvetica.ttf', 50, (44,62,80), (236,240,241), 0, 0, None, None, [])
        title.set_padding(0,0,0,30)
        title.make_pos()

        info1, info2, info3, info4, info5 = [], [], [], [], []
        info1.append(['Genre', ind.genre])
        info1.append(['Âge', ind.age])
        info2.append(['Expérience en R&D', ind.exp_RetD])
        info2.append(['Expérience start-up', ind.exp_startup])
        info3.append(['Compétence de coopération', ind.competence_groupe])
        info3.append(['Compétence en recherche', ind.competence_recherche])
        info3.append(['Compétence en management', ind.competence_direction])
        info4.append(['Statut', ind.statut])
        info4.append(['Rôle', ind.role])
        info5.append(['Salaire', ind.salaire])

        infos = [info1, info2, info3, info4, info5]
        frame_labels = []
        for info in infos:
            label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 30, 20, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 400, 'auto')
            frame_tmp = Frame(0, 0, label_tmp, None, [])
            frame_tmp.set_items_pos('auto')
            frame_tmp.set_marge_items(10)
            frame_tmp.set_direction('vertical')
            frame_tmp.resize('auto', 'auto')
            frame_tmp.set_bg_color((236, 240, 241))
            frame_tmp.make_pos()
            frame_labels.append(frame_tmp)

        frame_right = Frame(330, 40, [title] + frame_labels, None, [])
        frame_right.set_direction('vertical')
        frame_right.set_items_pos('auto')
        frame_right.set_padding(50,0,50,0)
        frame_right.set_marge_items(30)
        frame_right.set_bg_color((236,240,241))
        frame_right.make_pos()

        items.append(frame_right)

    elif i == 1:
        role = create_label("Changer de rôle", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [ind_id,1])
        roles = []
        item_list_role = Item_list(roles, 330, 40, 1260, 40, 20, 680, 'rôle')
        items.append(item_list_role)

    elif i == 2:
        formation = create_label("Formation", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [ind_id,2])
        formations = []
        item_list_formation = Item_list(formations, 330, 40, 1260, 40, 20, 680, 'formation')
        items.append(item_list_formation)


    list_tmp = [attribute, role, formation, fired]
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

    window.set_body(items)
    window.display(screen)

def draw_recruit(widget, window, screen, *arg):
    text = 'Liste des candidats'
    label = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 80, 40, None, draw_rh, [])
    label.set_direction('horizontal')
    label.set_padding(20,10,10,10)
    label.resize(600, 80)
    label.set_align('center')
    label.make_pos()

    a = []
    for ind in window.candidats:
        employee_info = []

        employee_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        employee_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
        employee_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        employee_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        frame_employee = Frame(0, 0, employee_info, draw_individu, [ind.id])
        frame_employee.set_direction('vertical')
        frame_employee.set_items_pos('auto')
        frame_employee.resize(580, 'auto')
        frame_employee.set_padding(20,0,20,20)
        frame_employee.set_bg_color((236, 240, 241))
        frame_employee.make_pos()

        a.append(frame_employee)

    item_list_employe = Item_list(a, 80, 120, 660, 120, 20, 600, 'candidats')

    text = 'Candidat'
    label_cand = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (149,165,166), 680, 40, None, None, [])
    label_cand.set_direction('horizontal')
    label_cand.set_padding(20,10,10,10)
    label_cand.resize(600, 80)
    label_cand.set_align('center')
    label_cand.make_pos()

    text = "Sélectionner un candidat"
    label_void = create_label(text, 'font/colvetica/colvetica.ttf', 40, (189, 195, 198), (236,240,241), 0, 0, 660, None, [])
    label_void.set_direction('horizontal')
    label_void.resize('auto', 600)
    # label_void.set_padding(0,10,10,10)
    label_void.set_align('center')
    label_void.make_pos()

    frame_right = Frame(680, 120, [label_void], None, [])
    frame_right.set_direction('vertical')
    frame_right.set_items_pos('auto')
    frame_right.resize(600, 600)
    frame_right.set_align('center')
    frame_right.set_bg_color((236,240,241))
    frame_right.make_pos()

    window.set_body([item_list_employe, label, label_cand, frame_right])
    window.draw_button_info('Aide', 'Clique sur un candidat pour voir ses caractéristiques et engage le si ce dernier t\'intéresse !')
    window.display(screen)

def recruit(widget, window, screen, ind_id, *arg):
    RH.recruter(window.individus, window.candidats, ind_id)
    window.lesRH.update(window.individus, window.departs, 3, 3)
    ind = get_with_id(window.individus, ind_id)
    title_msg = 'Bravo !'
    msg = 'Vous avez recruté ' + ind.prenom + ' ' + ind.nom
    draw_recruit(widget, window, screen)
    draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])

def draw_individu(widget, window, screen, ind_id, *arg):
    ind = get_with_id(window.candidats, ind_id)

    title = create_label(ind.prenom+' '+ind.nom, 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
    title.set_padding(0,0,0,20)
    title.make_pos()

    info1, info2, info3, info4, info5 = [], [], [], [], []
    info1.append(['Genre', ind.genre])
    info1.append(['Âge', ind.age])
    info2.append(['Expérience en R&D', ind.exp_RetD])
    info2.append(['Expérience start-up', ind.exp_startup])
    info3.append(['Compétence de coopération', ind.competence_groupe])
    info3.append(['Compétence en recherche', ind.competence_recherche])
    info3.append(['Compétence en management', ind.competence_direction])
    info4.append(['Statut', ind.statut])
    info4.append(['Rôle', ind.role])
    info5.append(['Salaire', ind.salaire])

    infos = [info1, info2, info3, info4, info5]
    frame_labels = []
    for info in infos:
        label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 30, 20, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 400, 520)
        frame_tmp = Frame(0, 0, label_tmp, None, [])
        frame_tmp.set_items_pos('auto')
        frame_tmp.set_marge_items(10)
        frame_tmp.set_direction('vertical')
        frame_tmp.resize('auto', 'auto')
        frame_tmp.set_bg_color((236, 240, 241))
        frame_tmp.make_pos()
        frame_labels.append(frame_tmp)

    button_hired = create_label('Recruter', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 700, 650, None, recruit, [ind_id])
    button_hired.set_padding(20,20,15,15)
    button_hired.make_pos()

    frame_employee = Frame(680, 120, [title] + frame_labels, None, [])
    frame_employee.set_direction('vertical')
    frame_employee.set_items_pos('auto')
    frame_employee.resize(600, 600)
    frame_employee.set_padding(30,0,30,0)
    frame_employee.set_bg_color((236, 240, 241))
    frame_employee.set_marge_items(30)
    frame_employee.make_pos()

    window.set_body_tmp([frame_employee, button_hired])
    window.display(screen)

def fired_ind(widget, window, screen, ind_id, *arg):
    ind = get_with_id(window.individus, ind_id)
    title_msg = ''
    msg = 'Vous avez licencié ' + ind.prenom + ' ' + ind.nom
    RH.licencier(window.individus, window.departs, ind_id)
    window.lesRH.update(window.individus, window.departs, 3, 3)
    draw_rh(widget, window, screen)
    draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])



'''
================================================================================
RD
================================================================================
'''

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
        label_add_project.set_align('center')
        label_add_project.make_pos()

        path = 'img/icon/grey_sum'
        icon_sum = Button_img(0, path, 0, 0, None, [])

        individus = []
        for ind in window.individus :
            if ind.projet == None :
                individus.append(ind)

        button_add_project = Frame(330, 40, [label_add_project, icon_sum], draw_add_project, [individus, []])
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

        for project in window.projets:
            project_info = []

            project_info.append(create_label(project.nom, 'font/colvetica/colvetica.ttf', 50, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            project_info.append(create_label(' ', 'font/colvetica/colvetica.ttf', 5, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))

            label_phase = create_label("Phase :", 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
            label_phase.resize(200, 'auto')
            label_phase.set_items_pos('auto')
            label_phase.make_pos()
            label_phase_value = create_label(nomPhase(project.phase), 'calibri', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

            frame_tmp1 = Frame(0, 0, [label_phase, label_phase_value], None, [])
            frame_tmp1.set_direction('horizontal')
            frame_tmp1.set_items_pos('auto')
            frame_tmp1.resize('auto', 'auto')
            frame_tmp1.set_align('center')
            frame_tmp1.set_marge_items(10)
            frame_tmp1.set_bg_color((236, 240, 241))
            frame_tmp1.make_pos()
            project_info.append(frame_tmp1)

            label_avancement = create_label("Avancement :", 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
            label_avancement.resize(200, 'auto')
            label_avancement.set_items_pos('auto')
            label_avancement.make_pos()

            pourcentage = str(int(project.avancement * 100 / window.paliers[project.phase-1]))
            label_pourcentage = create_label(pourcentage+'%', 'calibri', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
            progress_bar = Progress_bar(0, 0, 600, 30, None, [], project.avancement, window.paliers[project.phase-1], (46, 204, 113), (255, 255, 255))
            frame_progress_bar = Frame(0, 0, [label_pourcentage, progress_bar], None, [])
            frame_progress_bar.set_direction('horizontal')
            frame_progress_bar.set_items_pos('auto')
            frame_progress_bar.set_align('center')
            frame_progress_bar.set_marge_items(20)
            frame_progress_bar.set_bg_color((236, 240, 241))
            frame_progress_bar.make_pos()

            frame_tmp2 = Frame(0, 0, [label_avancement, frame_progress_bar], None, [])
            frame_tmp2.set_direction('horizontal')
            frame_tmp2.set_items_pos('auto')
            frame_tmp2.resize('auto', 'auto')
            frame_tmp2.set_align('center')
            frame_tmp2.set_marge_items(10)
            frame_tmp2.set_padding(0,0,0,0)
            frame_tmp2.set_bg_color((236, 240, 241))
            frame_tmp2.make_pos()
            project_info.append(frame_tmp2)

            frame_project = Frame(0, 0, project_info, draw_project, [project.id, 0])
            frame_project.set_direction('vertical')
            frame_project.set_items_pos('auto')
            frame_project.resize(930, 'auto')
            frame_project.set_marge_items(20)
            frame_project.set_padding(20,0,20,20)
            frame_project.set_bg_color((236, 240, 241))
            frame_project.make_pos()

            projects.append(frame_project)

        item_list_project = Item_list(projects, 330, 120, 1260, 120, 20, 600, 'projet')

        items.append(item_list_project)

    elif i == 1:
        button_product = create_label("Produit", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_rd, [1])

        products = []

        for product in window.produits:
            product_info = []

            product_info.append(create_label(product.nom, 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            product_info.append(create_label(' ', 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))

            frame_product = Frame(0, 0, product_info, draw_product, [0, 0])
            frame_product.set_direction('vertical')
            frame_product.set_items_pos('auto')
            frame_product.resize(930, 'auto')
            frame_product.set_padding(20,0,20,20)
            frame_product.set_bg_color((236, 240, 241))
            frame_product.make_pos()

            products.append(frame_product)

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

    window.set_body(items)
    window.draw_button_info('Aide', 'Clique sur un projet pour voir ses caractéristiques ou crée un projet innovant !')
    window.display(screen)

def draw_add_project(widget, window, screen, lst_ind, lst_ajout, *arg):
    items = []

    text = 'Liste des employés'
    label_employe = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 80, 40, None, None, [])
    label_employe.set_direction('horizontal')
    label_employe.set_padding(20,10,10,10)
    label_employe.resize(600, 80)
    label_employe.set_align('center')
    label_employe.make_pos()

    a = []
    for i in range(0,len(lst_ind)):
        employee_info = []
        ind = lst_ind[i]
        lst_ind_tmp = []
        lst_ind_tmp += lst_ind
        lst_ind_tmp.pop(i)

        employee_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        employee_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
        employee_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        employee_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        frame_employee = Frame(0, 0, employee_info, draw_add_project, [lst_ind_tmp, lst_ajout + [ind]])
        frame_employee.set_direction('vertical')
        frame_employee.set_items_pos('auto')
        frame_employee.resize(580, 'auto')
        frame_employee.set_padding(20,0,20,20)
        frame_employee.set_bg_color((236, 240, 241))
        frame_employee.make_pos()

        a.append(frame_employee)

    item_list_employe = Item_list(a, 80, 120, 660, 120, 20, 600, 'employé')
    items.append(item_list_employe)
    items.append(label_employe)

    text = 'Liste des employés ajoutés'
    label_ajout = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (44,62,80), 680, 40, None, None, [])
    label_ajout.set_direction('horizontal')
    label_ajout.set_padding(20,10,10,10)
    label_ajout.resize(600, 80)
    label_ajout.set_align('center')
    label_ajout.make_pos()

    lst_tmp = []
    for i in range(0,len(lst_ajout)):
        employee_info = []

        ind = lst_ajout[i]
        lst_ajout_tmp = []
        lst_ajout_tmp += lst_ajout
        lst_ajout_tmp.pop(i)

        employe_name = create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, draw_add_project, [lst_ind + [ind], lst_ajout_tmp])
        employe_name.set_items_pos('auto')
        employe_name.resize(580, 'auto')
        employe_name.set_padding(20,0,20,20)
        employe_name.make_pos()

        lst_tmp.append(employe_name)

    item_ajoute = Item_list(lst_tmp, 680, 120, 1260, 120, 20, 400, 'employé')
    items.append(item_ajoute)
    items.append(label_ajout)

    entry_name_project = create_label('Nom du projet', 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
    entry = Entry(0, 0, 400, 40, False, 'name_project', 0, None)
    frame_tmp_entry = Frame(0, 0, [entry_name_project, entry], None, [])
    frame_tmp_entry.set_direction('vertical')
    frame_tmp_entry.set_items_pos('auto')
    frame_tmp_entry.set_marge_items(10)
    frame_tmp_entry.set_bg_color((236, 240, 241))
    frame_tmp_entry.make_pos()

    button_submit = create_label('Ajouter le projet', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, create_project, [lst_ajout])
    button_submit.set_padding(20,20,15,15)
    button_submit.set_direction('vertical')
    button_submit.make_pos()

    frame_tmp = Frame(680, 520, [frame_tmp_entry, button_submit], None, [])
    frame_tmp.set_direction('vertical')
    frame_tmp.set_items_pos('auto')
    frame_tmp.set_padding(20,0,30,0)
    frame_tmp.set_marge_items(30)
    frame_tmp.set_bg_color((236, 240, 241))
    frame_tmp.make_pos()
    items.append(frame_tmp)

    window.set_body(items)
    window.draw_button_info('Aide', 'Sélectionne des employés pour ton nouveau projet et donne lui un nom !')
    window.display(screen)

def create_project(widget, window, screen, lst_emp, *arg):
    entry = get_entry(widget, window, screen, *arg)
    if check_string(widget, window, screen, r"^[a-zA-Z0-9 ]+$", entry['name_project'], "Nom de projet incorrect") and lst_emp != []:
        window.projets.append(Projet(entry['name_project']))
        for ind in lst_emp:
            addChercheurs(window.projets[-1], window.individus, ind.id)
        title_msg = 'Bravo !'
        msg = 'Le projet ' + entry['name_project'] + ' a bien été crée.'
        draw_rd(widget, window, screen, 0)
        draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])
    elif lst_emp == []:
        draw_alert(widget, window, screen, "Erreur", "Aucun employé sélectionné", clear_overbody, [])

def actionPhase(widget, window, screen, projet, choix , *arg) :
    return(window.depenses.append(Projet.progression(projet, window.individus, window.paliers, choix)))

def status(widget, window, screen, projet, *arg) :
    msg_general = []
    boutons = []
    if projet.phase==1 and projet.attente==True:
        msg_general.append("Les résultats de l'étude de marché sont arrivés !")
        msg_general.append("Veuillez sélectionner la population que ciblera votre concept de produit pour faire avancer le projet à la phase suivante :")
        bouton_1 = [["Jeunes :", projet.produit.appreciation[0][0]], actionPhase, [projet, "Jeunes"]]
        bouton_2 = [["Actifs :", projet.produit.appreciation[1][0]], actionPhase, [projet, "Actifs"]]
        bouton_3 = [["Seniors :", projet.produit.appreciation[2][0]], actionPhase, [projet, "Seniors"]]
        boutons.append(bouton_1)
        boutons.append(bouton_2)
        boutons.append(bouton_3)
    elif projet.phase==2 and projet.attente==True:
        msg_general.append("Vos chercheurs sont près à passer à la phase expérimentale.")
        msg_general.append("Voulez-vous réaliser un premier prototype ? Cela vous coutera : "+str(round(projet.produit.cout, 2))+" euros.")
        boutons.append(["Accepter", actionPhase, [projet, True]])
    elif projet.phase==4 :
        if projet.attente==False :
            msg_general.append("Vos chercheurs pensent qu'il serait bénéfique de mettre votre prototype à l'essai, cela permettrait d'accélérer la création du produit final")
            msg_general.append("Voulez-vous mettre votre prototype à l'essai ? Cela vous coutera : "+str(50)+" euros.")
            boutons.append(["Accepter", actionPhase, [projet, True]])
        else :
            msg_general.append("Votre prototype est en passe de devenir un de vos produits. Il vous faut cependant déposer un brevet pour sécuriser cette nouvelle propriété.")
            msg_general.append("Voulez-vous déposer un brevet ? Cela vous coutera : "+str(50)+" euros.")
            boutons.append(["Accepter", actionPhase, [projet, True]])
    else :
        msg_general = "En cours."

    return(msg_general, boutons)

def draw_project(widget, window, screen, proj_id, i, *arg):
    projet = get_with_id(window.projets, proj_id)

    items = []

    path = 'img/icon/right_white_arrow'
    button_arrow = Button_img(0, path, 0, 0, None, [])
    text = 'Projet ' + str(proj_id)
    name = create_label(text, 'font/colvetica/colvetica.ttf', 40, (255,255,255), (149,165,166), 0, 0, None, None, [])
    frame_back = Frame(0,0, [button_arrow, name], draw_rd, [0])
    frame_back.set_direction('horizontal')
    frame_back.set_items_pos('auto')
    frame_back.resize(250, 80)
    frame_back.set_align('center')
    frame_back.set_padding(10,0,0,0)
    frame_back.set_marge_items(10)
    frame_back.set_bg_color((149, 165, 166))
    frame_back.make_pos()

    attribute = create_label("Caractéristique", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_project, [proj_id,0])
    participants  = create_label("Participants", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_project, [proj_id,1])

    f1 = ["Oui", del_proj, [proj_id]]
    f2 = ["Non", clear_overbody, []]
    delete  = create_label("Supprimer", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_alert_option, ['', 'Voulez-vous vraiment supprimer le projet ' +  projet.nom + ' ?',[f1, f2]])

    focus_color = (41,128,185)
    if i == 0:
        attribute = create_label("Caractéristique", 'calibri', 30, (255,255,255), focus_color, 0, 0, 250, draw_project, [proj_id,0])

        title = create_label(projet.nom, 'font/colvetica/colvetica.ttf', 50, (44,62,80), (236,240,241), 0, 0, None, None, [])
        title.set_padding(0,0,0,30)
        title.make_pos()

        frame_labels = []

        label_phase = create_label("Phase :", 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
        label_phase.resize(200, 'auto')
        label_phase.set_items_pos('auto')
        label_phase.make_pos()

        label_phase_value = create_label(nomPhase(projet.phase), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

        frame_tmp1 = Frame(0, 0, [label_phase, label_phase_value], None, [])
        frame_tmp1.set_direction('horizontal')
        frame_tmp1.set_items_pos('auto')
        frame_tmp1.resize('auto', 'auto')
        frame_tmp1.set_align('center')
        frame_tmp1.set_marge_items(10)
        frame_tmp1.set_padding(0,0,0,0)
        frame_tmp1.set_bg_color((236, 240, 241))
        frame_tmp1.make_pos()
        frame_labels.append(frame_tmp1)

        label_avancement = create_label("Avancement :", 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
        label_avancement.resize(200, 'auto')
        label_avancement.set_items_pos('auto')
        label_avancement.make_pos()

        pourcentage = str(int(projet.avancement * 100 / window.paliers[projet.phase-1]))
        label_pourcentage = create_label(pourcentage+'%', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
        progress_bar = Progress_bar(0, 0, 600, 20, None, [], projet.avancement, window.paliers[projet.phase-1], (46, 204, 113), (255, 255, 255))
        frame_progress_bar = Frame(0, 0, [label_pourcentage, progress_bar], None, [])
        frame_progress_bar.set_direction('horizontal')
        frame_progress_bar.set_items_pos('auto')
        frame_progress_bar.set_align('center')
        frame_progress_bar.set_marge_items(20)
        frame_progress_bar.set_bg_color((236, 240, 241))
        frame_progress_bar.make_pos()

        frame_tmp2 = Frame(0, 0, [label_avancement, frame_progress_bar], None, [])
        frame_tmp2.set_direction('horizontal')
        frame_tmp2.set_items_pos('auto')
        frame_tmp2.resize('auto', 'auto')
        frame_tmp2.set_align('center')
        frame_tmp2.set_marge_items(10)
        frame_tmp2.set_padding(0,0,0,0)
        frame_tmp2.set_bg_color((236, 240, 241))
        frame_tmp2.make_pos()
        frame_labels.append(frame_tmp2)


        status_msg, status_button = status(widget, window, screen, projet)
        label_status_msg = create_label(status_msg, 'font/colvetica/colvetica.ttf', 30, (52, 73, 95), (236,240,241), 0, 0, 1280//2, None, [])

        buttons = []
        for element in status_button:
            button = create_button(element[0], 'font/colvetica/colvetica.ttf', 30, (255, 255, 255), (230, 126, 34), 0, 0, 'auto', 'auto', element[1], element[2])
            button.set_padding(30,30,10,10)
            button.make_pos()
            buttons.append(button)

        frame_button = Frame(0, 0, buttons, None, [])
        frame_button.set_direction('horizontal')
        frame_button.set_items_pos('auto')
        frame_button.set_marge_items(20)
        frame_button.resize('auto', 'auto')
        frame_button.set_bg_color((236, 240, 241))
        frame_button.make_pos()

        label_status = create_label("Status :", 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
        frame_labels.append(label_status)

        frame_status = Frame(0, 0, [label_status_msg, frame_button], None, [])
        frame_status.set_direction('vertical')
        frame_status.set_items_pos('auto')
        frame_status.resize(1280-330-50, 'auto')
        frame_status.set_align('center')
        frame_status.set_marge_items(20)
        frame_status.set_padding(0,0,20,20)
        frame_status.set_bg_color((236, 240, 241))
        frame_status.make_pos()
        frame_labels.append(frame_status)

        frame_right = Frame(330, 40, [title] + frame_labels, None, [])
        frame_right.set_direction('vertical')
        frame_right.set_items_pos('auto')
        frame_right.set_padding(50,0,50,0)
        frame_right.set_marge_items(30)
        frame_right.set_bg_color((236,240,241))
        frame_right.make_pos()

        items.append(frame_right)

    elif i == 1:
        participants  = create_label("Participants", 'calibri', 30, (255,255,255), focus_color, 0, 0, 250, draw_project, [proj_id,1])
        a = []
        for ind in window.individus:
            if ind.projet == projet.nom:
                employee_info = []

                employee_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
                employee_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
                employee_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
                employee_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

                frame_employee = Frame(0, 0, employee_info, draw_employee_project, [ind.id, 0, projet.id])
                frame_employee.set_direction('vertical')
                frame_employee.set_items_pos('auto')
                frame_employee.resize(930, 'auto')
                frame_employee.set_padding(20,0,20,20)
                frame_employee.set_bg_color((236, 240, 241))
                frame_employee.make_pos()

                a.append(frame_employee)

        item_list_employe = Item_list(a, 330, 40, 1260, 40, 20, 640, 'employé')
        items.append(item_list_employe)

        lst_ind = []
        for ind in window.individus:
            if ind.projet == None:
                lst_ind.append(ind)

        button_add = create_label('Ajouter des participants', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, draw_add_to_project, [lst_ind, [], projet.id])
        button_add.set_direction('vertical')
        button_add.resize(950,'auto')
        button_add.set_align('center')
        button_add.make_pos()

        frame_v1 = Frame(330, 640, [button_add], draw_add_to_project, [lst_ind, [], projet.id])
        frame_v1.set_direction('horizontal')
        frame_v1.set_items_pos('auto')
        frame_v1.resize('auto', 80)
        frame_v1.set_align('center')
        frame_v1.set_bg_color((230, 126, 34))
        frame_v1.make_pos()

        items.append(frame_v1)

    list_tmp = [attribute, participants, delete]
    for element in list_tmp:
        element.set_direction('horizontal')
        element.resize(250, 'auto')
        element.set_padding(10,0,20,20)
        element.set_align('center')
        element.make_pos()

    frame_left = Frame(80, 40, [frame_back] + list_tmp, None, [])
    frame_left.set_direction('vertical')
    frame_left.set_items_pos('auto')
    frame_left.resize(250, 680)
    frame_left.set_marge_items(2)
    frame_left.set_bg_color((189, 195, 198))
    frame_left.make_pos()

    items.append(frame_left)

    window.set_body(items)
    window.draw_button_info('Aide', 'Informez-vous sur l\'avancement du projet et sur les actions à réaliser !')
    window.display(screen)

def draw_employee_project(widget, window, screen, ind_id, i, proj_id, *arg):
    ind = get_with_id(window.individus, ind_id)

    items = []

    path = 'img/icon/right_white_arrow'
    button_arrow = Button_img(0, path, 0, 0, None, [])
    text = 'Employé ' + str(ind_id)
    name = create_label(text, 'font/colvetica/colvetica.ttf', 40, (255,255,255), (149,165,166), 0, 0, None, None, [])
    frame_back_rh = Frame(0,0, [button_arrow, name], draw_project, [proj_id, 1])
    frame_back_rh.set_direction('horizontal')
    frame_back_rh.set_items_pos('auto')
    frame_back_rh.resize(250, 80)
    frame_back_rh.set_align('center')
    frame_back_rh.set_padding(10,0,0,0)
    frame_back_rh.set_marge_items(10)
    frame_back_rh.set_bg_color((149, 165, 166))
    frame_back_rh.make_pos()

    attribute = create_label("Caractéristique", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee_project, [ind_id, 0, proj_id, 1])
    role = create_label("Changer de rôle", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee_project, [ind_id,1, proj_id, 1])
    formation = create_label("Formation", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee_project, [ind_id,2, proj_id, 1])

    f1 = ["Oui", remove_from_project, [ind_id, proj_id]]
    f2 = ["Non", clear_overbody, []]
    fired = create_label("Retirer", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_alert_option, ['', 'Voulez-vous retirer ' + ind.prenom + ' ' + ind.nom + ' du projet ?',[f1, f2]])

    focus_color = (41,128,185)
    if i == 0:
        attribute = create_label("Caractéristique", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee_project, [ind_id, 0, proj_id, 1])

        title = create_label(ind.prenom + ' ' + ind.nom, 'font/colvetica/colvetica.ttf', 50, (44,62,80), (236,240,241), 0, 0, None, None, [])
        title.set_padding(0,0,0,30)
        title.make_pos()

        info1, info2, info3, info4, info5 = [], [], [], [], []
        info1.append(['Genre', ind.genre])
        info1.append(['Âge', ind.age])
        info2.append(['Expérience en R&D', ind.exp_RetD])
        info2.append(['Expérience start-up', ind.exp_startup])
        info3.append(['Compétence de coopération', ind.competence_groupe])
        info3.append(['Compétence en recherche', ind.competence_recherche])
        info3.append(['Compétence en management', ind.competence_direction])
        info4.append(['Statut', ind.statut])
        info4.append(['Rôle', ind.role])
        info5.append(['Salaire', ind.salaire])

        infos = [info1, info2, info3, info4, info5]
        frame_labels = []
        for info in infos:
            label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 30, 20, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 300, 'auto')
            frame_tmp = Frame(0, 0, label_tmp, None, [])
            frame_tmp.set_items_pos('auto')
            frame_tmp.set_marge_items(10)
            frame_tmp.set_direction('vertical')
            frame_tmp.resize('auto', 'auto')
            frame_tmp.set_bg_color((236, 240, 241))
            frame_tmp.make_pos()
            frame_labels.append(frame_tmp)

        frame_right = Frame(330, 40, [title] + frame_labels, None, [])
        frame_right.set_direction('vertical')
        frame_right.set_items_pos('auto')
        frame_right.set_padding(50,0,50,0)
        frame_right.set_marge_items(30)
        frame_right.set_bg_color((236,240,241))
        frame_right.make_pos()

        items.append(frame_right)

    elif i == 1:
        role = create_label("Changer de rôle", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee_project, [ind_id,1, proj_id, 1])
        roles = []
        item_list_role = Item_list(roles, 330, 40, 1260, 40, 20, 680, 'rôle')
        items.append(item_list_role)

    elif i == 2:
        formation = create_label("Formation", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee_project, [ind_id,2, proj_id, 1])
        formations = []
        item_list_formation = Item_list(formations, 330, 40, 1260, 40, 20, 680, 'formation')
        items.append(item_list_formation)


    list_tmp = [attribute, role, formation, fired]
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

    window.set_body(items)
    window.display(screen)

def del_proj(widget, window, screen, proj_id, *arg):
    projet = get_with_id(window.projets, proj_id)
    title_msg = ''
    msg = 'Le projet ' + projet.nom + ' a été supprimé.'
    delProject(window.projets, window.individus, proj_id)
    draw_rd(widget, window, screen, 0)
    draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])

def remove_from_project(widget, window, screen, ind_id, proj_id, *arg):
    projet = get_with_id(window.projets, proj_id)
    ind = get_with_id(window.individus, ind_id )
    ind.prenom + ' ' + ind.nom
    title_msg = ''
    msg = 'L\'employé ' + ind.prenom + ' ' + ind.nom + ' a été retiré du projet.'
    delChercheurs(projet, window.individus, ind_id)
    draw_project(widget, window, screen, proj_id, 1)
    draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])

def draw_add_to_project(widget, window, screen, lst_ind, lst_ajout, proj_id, *arg):
    items = []

    text = 'Liste des employés'
    label_employe = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 80, 40, None, None, [])
    label_employe.set_direction('horizontal')
    label_employe.set_padding(20,10,10,10)
    label_employe.resize(600, 80)
    label_employe.set_align('center')
    label_employe.make_pos()

    a = []
    for i in range(0,len(lst_ind)):
        employee_info = []
        ind = lst_ind[i]
        lst_ind_tmp = []
        lst_ind_tmp += lst_ind
        lst_ind_tmp.pop(i)

        employee_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        employee_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
        employee_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        employee_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        frame_employee = Frame(0, 0, employee_info, draw_add_to_project, [lst_ind_tmp, lst_ajout + [ind], proj_id])
        frame_employee.set_direction('vertical')
        frame_employee.set_items_pos('auto')
        frame_employee.resize(580, 'auto')
        frame_employee.set_padding(20,0,20,20)
        frame_employee.set_bg_color((236, 240, 241))
        frame_employee.make_pos()

        a.append(frame_employee)

    item_list_employe = Item_list(a, 80, 120, 660, 120, 20, 600, 'employé')
    items.append(item_list_employe)
    items.append(label_employe)

    text = 'Liste des employés ajoutés'
    label_ajout = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (44,62,80), 680, 40, None, None, [])
    label_ajout.set_direction('horizontal')
    label_ajout.set_padding(20,10,10,10)
    label_ajout.resize(600, 80)
    label_ajout.set_align('center')
    label_ajout.make_pos()

    lst_tmp = []
    for i in range(0,len(lst_ajout)):
        employee_info = []

        ind = lst_ajout[i]
        lst_ajout_tmp = []
        lst_ajout_tmp += lst_ajout
        lst_ajout_tmp.pop(i)

        employe_name = create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, draw_add_to_project, [lst_ind + [ind], lst_ajout_tmp, proj_id])
        employe_name.set_items_pos('auto')
        employe_name.resize(580, 'auto')
        employe_name.set_padding(20,0,20,20)
        employe_name.make_pos()

        lst_tmp.append(employe_name)

    item_ajoute = Item_list(lst_tmp, 680, 120, 1260, 120, 20, 400, 'employé')
    items.append(item_ajoute)
    items.append(label_ajout)

    button_submit = create_label('Ajouter au projet', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, add_to_project, [lst_ajout, proj_id])
    button_submit.resize(200,'auto')
    button_submit.set_align('center')
    button_submit.make_pos()

    frame_v1 = Frame(0, 0, [button_submit], add_to_project, [lst_ajout, proj_id])
    frame_v1.set_direction('horizontal')
    frame_v1.set_items_pos('auto')
    frame_v1.resize('auto', 60)
    frame_v1.set_align('center')
    frame_v1.set_bg_color((230, 126, 34))
    frame_v1.make_pos()

    button_back = create_label('Retour', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, draw_project, [proj_id, 1])
    button_back.resize(200,'auto')
    button_back.set_align('center')
    button_back.make_pos()

    frame_v2 = Frame(0, 0, [button_back], draw_project, [proj_id, 1])
    frame_v2.set_direction('horizontal')
    frame_v2.set_items_pos('auto')
    frame_v2.resize('auto', 60)
    frame_v2.set_align('center')
    frame_v2.set_bg_color((230, 126, 34))
    frame_v2.make_pos()

    frame_tmp = Frame(680, 520, [frame_v1, frame_v2], None, [])
    frame_tmp.set_direction('vertical')
    frame_tmp.set_items_pos('auto')
    frame_tmp.set_padding(20,0,30,0)
    frame_tmp.set_marge_items(30)
    frame_tmp.set_bg_color((236, 240, 241))
    frame_tmp.make_pos()
    items.append(frame_tmp)

    window.set_body(items)
    window.display(screen)

def add_to_project(widget, window, screen, lst_ind, proj_id):
    projet = get_with_id(window.projets, proj_id)
    if lst_ind == []:
        draw_alert(widget, window, screen, 'Erreur', 'Aucun employé sélectionné', clear_overbody, [])
    else:
        for ind in lst_ind:
            addChercheurs(projet, window.individus, ind.id)

        msg = 'Les employés ont bien été ajouté au projet'
        draw_project(widget, window, screen, proj_id, 1)
        draw_alert(widget, window, screen, '', msg, clear_overbody, [])

'''INCOMPLET'''
def draw_product(widget, window, screen, prod_id, i, *arg):
    items = []

    path = 'img/icon/right_white_arrow'
    button_arrow = Button_img(0, path, 0, 0, None, [])
    text = 'Produit #'
    name = create_label(text, 'font/colvetica/colvetica.ttf', 40, (255,255,255), (149,165,166), 0, 0, None, None, [])
    frame_back = Frame(0,0, [button_arrow, name], draw_rd, [0])
    frame_back.set_direction('horizontal')
    frame_back.set_items_pos('auto')
    frame_back.resize(250, 80)
    frame_back.set_align('center')
    frame_back.set_padding(10,0,0,0)
    frame_back.set_marge_items(10)
    frame_back.set_bg_color((149, 165, 166))
    frame_back.make_pos()

    attribute = create_label("Caractéristique", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_product, [prod_id, 0])
    update = create_label("Améliorer", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_product, [prod_id,1])

    focus_color = (41,128,185)
    if i == 0:
        attribute = create_label("Caractéristique", 'calibri', 30, (255,255,255), focus_color, 0, 0, 250, draw_product, [prod_id,0])

    elif i == 1:
        update = create_label("Améliorer", 'calibri', 30, (255,255,255), focus_color, 0, 0, 250, draw_product, [prod_id,1])

    list_tmp = [attribute, update]
    for element in list_tmp:
        element.set_direction('horizontal')
        element.resize(250, 'auto')
        element.set_padding(10,0,20,20)
        element.set_align('center')
        element.make_pos()

    frame_left = Frame(80, 40, [frame_back] + list_tmp, None, [])
    frame_left.set_direction('vertical')
    frame_left.set_items_pos('auto')
    frame_left.resize(250, 680)
    frame_left.set_marge_items(2)
    frame_left.set_bg_color((189, 195, 198))
    frame_left.make_pos()

    items.append(frame_left)

    window.set_body(items)
    window.display(screen)

'''INCOMPLET'''
def draw_upgrade_product(widget, window, screen, lst_ind, lst_ajout, *arg):
    items = []

    text = 'Liste des employés'
    label_employe = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 80, 40, None, None, [])
    label_employe.set_direction('horizontal')
    label_employe.set_padding(20,10,10,10)
    label_employe.resize(600, 80)
    label_employe.set_align('center')
    label_employe.make_pos()

    a = []
    for i in range(0,len(lst_ind)):
        employee_info = []
        ind = lst_ind[i]
        lst_ind_tmp = []
        lst_ind_tmp += lst_ind
        lst_ind_tmp.pop(i)

        employee_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        employee_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
        employee_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        employee_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        frame_employee = Frame(0, 0, employee_info, draw_add_project, [lst_ind_tmp, lst_ajout + [ind]])
        frame_employee.set_direction('vertical')
        frame_employee.set_items_pos('auto')
        frame_employee.resize(580, 'auto')
        frame_employee.set_padding(20,0,20,20)
        frame_employee.set_bg_color((236, 240, 241))
        frame_employee.make_pos()

        a.append(frame_employee)

    item_list_employe = Item_list(a, 80, 120, 660, 120, 20, 600, 'employé')
    items.append(item_list_employe)
    items.append(label_employe)

    text = 'Liste des employés ajoutés'
    label_ajout = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (44,62,80), 680, 40, None, None, [])
    label_ajout.set_direction('horizontal')
    label_ajout.set_padding(20,10,10,10)
    label_ajout.resize(600, 80)
    label_ajout.set_align('center')
    label_ajout.make_pos()

    lst_tmp = []
    for i in range(0,len(lst_ajout)):
        employee_info = []

        ind = lst_ajout[i]
        lst_ajout_tmp = []
        lst_ajout_tmp += lst_ajout
        lst_ajout_tmp.pop(i)

        employe_name = create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, draw_add_project, [lst_ind + [ind], lst_ajout_tmp])
        employe_name.set_items_pos('auto')
        employe_name.resize(580, 'auto')
        employe_name.set_padding(20,0,20,20)
        employe_name.make_pos()

        lst_tmp.append(employe_name)

    item_ajoute = Item_list(lst_tmp, 680, 120, 1260, 120, 20, 500, 'employé')
    items.append(item_ajoute)
    items.append(label_ajout)

    button_submit = create_label('Améliorer le produit', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, None, [])
    button_submit.set_padding(20,20,15,15)
    button_submit.set_direction('vertical')
    button_submit.make_pos()

    frame_tmp = Frame(680, 620, [button_submit], None, [])
    frame_tmp.set_direction('vertical')
    frame_tmp.resize(1260-680,'auto')
    frame_tmp.set_items_pos('auto')
    frame_tmp.set_align('right')
    frame_tmp.set_padding(20,0,30,0)
    frame_tmp.set_bg_color((236, 240, 241))
    frame_tmp.make_pos()
    items.append(frame_tmp)

    window.set_body(items)
    window.display(screen)



'''
================================================================================
PRODUCTION
================================================================================
'''



'''
================================================================================
FINANCE
================================================================================
'''

def draw_finance(widget, window, screen, i, *arg):
    items = []
    items_tmp = []

    button_pret = create_label("Prêt", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_finance, [0])
    button_bilan = create_label("Produit", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_finance, [1])
    button_compte = create_label("Compte de résultat", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_finance, [2])
    button_macro = create_label("Macroéconomie", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_finance, [3])

    lst_button_pret = [button_pret]

    focus_color = (41,128,185)

    if 0 <= i < 1:
        button_pret = create_label("Prêt", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_finance, [0])
        lst_button_pret = [button_pret]

        button_resume_pret = create_label("     Résumé", 'calibri', 20, (255,255,255), (127, 140, 141), 0, 0, None, draw_finance, [0])
        button_lst_pret = create_label("     Liste des prêts", 'calibri', 20, (255,255,255), (127, 140, 141), 0, 0, None, draw_finance, [0.1])
        button_ask_pret = create_label("     Contracter un prêt", 'calibri', 20, (255,255,255), (127, 140, 141), 0, 0, None, draw_finance, [0.2])

        if i == 0:
            button_resume_pret = create_label("     Résumé", 'calibri', 20, (255,255,255), (52, 152, 219), 0, 0, None, draw_finance, [0])
        elif i == 0.1:
            button_lst_pret = create_label("     Liste des prêts", 'calibri', 20, (255,255,255), (52, 152, 219), 0, 0, None, draw_finance, [0.1])
        elif i == 0.2:
            button_ask_pret = create_label("     Contracter un prêt", 'calibri', 20, (255,255,255), (52, 152, 219), 0, 0, None, draw_finance, [0.2])

            variationInteret = variationInteretTotal(window.donneesF)

            #Texte à trous
            if variationInteret < (-2):
                texte1 = "nous pouvons vous faire confiance"
                texte2 = "bas"
            elif variationInteret > 2:
                texte1 = "nous sommes méfiants en votre capacité à rembourser vos prêts"
                texte2 = "élevé"
            else:
                texte1 = "nous sommes assez confiants en votre capacité à rembourser vos prêts"
                texte2 = "correct"

            text = "Après une analyse de la situation de votre start-up, nous avons conclu "+ "que "+ texte1 +". Nous vous proposons donc un prêt à taux d'intérêt "+ texte2 +"."

            label_analyse = create_label(text, 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 800, None, [])
            label_signature = create_label("Votre banque."
                                           , 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
            choose_pret = create_label("Choisissez votre type de prêt :", 'font/colvetica/colvetica.ttf', 30, (44,62,80), (236,240,241), 0, 0, None, None, [])
            choose_pret.set_padding(0,0,20,0)
            choose_pret.make_pos()

            interetCourt = round(1.5 + (variationInteret/2),1)
            interetMoyen = round(1.6 + variationInteret,1)
            interetLong = round(2.1 + variationInteret,1)

            court = ["Court", dureePret("court"), interetCourt]
            moyen = ["Moyen", dureePret("moyen"), interetMoyen]
            long = ["Long", dureePret("long"), interetLong]

            lst_interet = [court, moyen, long]

            items1 = []

            for element in lst_interet:
                button = create_button(element[0], 'font/colvetica/colvetica.ttf', 40, (236, 240, 241), (230, 126, 34), 0, 0, 200, 60, draw_get_pret, [element[0], element[2], element[1][0].split()[0], '0'])

                info = []
                info.append(['Durée', 'De ' + element[1][0] + ' à ' + element[1][1]])
                info.append(['Taux d\'intérêt', str(element[2]) + '%'])

                labels = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 25, 20, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 'auto', 'auto')

                frame_tmp1 = Frame(0, 0, labels, None, [])
                frame_tmp1.set_direction('vertical')
                frame_tmp1.set_items_pos('auto')
                frame_tmp1.resize('auto', 'auto')
                frame_tmp1.set_marge_items(0)
                frame_tmp1.set_padding(0,0,0,0)
                frame_tmp1.set_bg_color((236, 240, 241))
                frame_tmp1.make_pos()

                frame_tmp = Frame(0, 0, [button, frame_tmp1], None, [])
                frame_tmp.set_direction('horizontal')
                frame_tmp.set_items_pos('auto')
                frame_tmp.resize('auto', 'auto')
                frame_tmp.set_align('center')
                frame_tmp.set_marge_items(20)
                frame_tmp.set_padding(0,0,0,0)
                frame_tmp.set_bg_color((236, 240, 241))
                frame_tmp.make_pos()

                items1.append(frame_tmp)

            frame_right = Frame(330, 40, [label_analyse, label_signature, choose_pret] + items1, None, [])
            frame_right.set_direction('vertical')
            frame_right.set_items_pos('auto')
            frame_right.resize('auto', 'auto')
            frame_right.set_marge_items(30)
            frame_right.set_padding(50,0,50,0)
            frame_right.set_bg_color((236, 240, 241))
            frame_right.make_pos()
            items_tmp.append(frame_right)


        lst_button_pret.append(button_resume_pret)
        lst_button_pret.append(button_lst_pret)
        lst_button_pret.append(button_ask_pret)

    elif i == 1:
        button_bilan = create_label("Produit", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_finance, [1])
    elif i == 2:
        button_compte = create_label("Compte de résultat", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_finance, [2])
    elif i == 3:
        button_macro = create_label("Macroéconomie", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_finance, [3])


    list_tmp = lst_button_pret + [button_bilan, button_compte, button_macro]
    for element in list_tmp:
        element.set_direction('horizontal')
        if element.color == (189,195,198) or element.color == focus_color:
            element.resize(250, 80)
        else:
            element.resize(250, 50)
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

    window.set_body(items)
    window.set_body_tmp(items_tmp)
    window.display(screen)

def draw_get_pret(widget, window, screen, type_pret, taux_interet, duree_entry, montant_entry, *arg):
    info1, info2 = [], []
    info1.append(['Type de prêt', type_pret])

    info2.append(['Taux d\'interêt', str(taux_interet)+'%'])
    info2.append(['Assurance', '2%'])

    infos = [info1, info2]
    frame_labels = []
    for info in infos:
        label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 40, 30, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 500, 'auto')
        frame_tmp = Frame(0, 0, label_tmp, None, [])
        frame_tmp.set_items_pos('auto')
        frame_tmp.set_marge_items(10)
        frame_tmp.set_direction('vertical')
        frame_tmp.resize('auto', 'auto')
        frame_tmp.set_bg_color((236, 240, 241))
        frame_tmp.make_pos()
        frame_labels.append(frame_tmp)

    label_duree = create_label('Durée du prêt : ', 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
    duree = dureePret(type_pret.lower())
    label_scale_duree = create_label('compris entre '+ duree[0] + ' et ' + duree[1] , 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

    frame_duree_labels = Frame(0, 0, [label_duree, label_scale_duree], None, [])
    frame_duree_labels.set_direction('vertical')
    frame_duree_labels.set_items_pos('auto')
    frame_duree_labels.resize(420, 'auto')
    frame_duree_labels.set_marge_items(10)
    frame_duree_labels.set_bg_color((236, 240, 241))
    frame_duree_labels.make_pos()

    entry_duree = Entry(0, 0, 200, 40, True, 'duree', 0, None)
    entry_duree.set_entry(duree_entry)

    frame_duree = Frame(0, 0, [frame_duree_labels, entry_duree], None, [])
    frame_duree.set_direction('horizontal')
    frame_duree.set_items_pos('auto')
    frame_duree.resize('auto', 'auto')
    frame_duree.set_marge_items(10)
    frame_duree.set_bg_color((236, 240, 241))
    frame_duree.make_pos()

    montant_max = montantPret(dureePretMois(type_pret.lower(), int(duree_entry)))

    label_montant = create_label('Montant du prêt : ', 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
    label_scale_montant = create_label('compris entre 0 et '+ str(montant_max)+ ' €', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

    frame_montant_labels = Frame(0, 0, [label_montant, label_scale_montant], None, [])
    frame_montant_labels.set_direction('vertical')
    frame_montant_labels.set_items_pos('auto')
    frame_montant_labels.resize(420, 'auto')
    frame_montant_labels.set_marge_items(10)
    frame_montant_labels.set_padding(0,0,0,20)
    frame_montant_labels.set_bg_color((236, 240, 241))
    frame_montant_labels.make_pos()

    entry_montant = Entry(0, 0, 200, 40, True, 'montant', 0, None)
    entry_montant.set_entry(montant_entry)


    frame_montant = Frame(0, 0, [frame_montant_labels, entry_montant], None, [])
    frame_montant.set_direction('horizontal')
    frame_montant.set_items_pos('auto')
    frame_montant.resize('auto', 'auto')
    frame_montant.set_marge_items(10)
    frame_montant.set_bg_color((236, 240, 241))
    frame_montant.make_pos()

    generate_button = create_button("Génerez", 'font/colvetica/colvetica.ttf', 40, (255, 255, 255), (230, 126, 34), 0, 0, 400, 60, get_pret, [type_pret, taux_interet])

    label_bilan = create_label('Bilan du prêt : ', 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
    label_sub_bilan = create_label('géneré à partir des données ci-dessus', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

    frame_bilan = Frame(0, 0, [label_bilan, label_sub_bilan], None, [])
    frame_bilan.set_direction('vertical')
    frame_bilan.set_items_pos('auto')
    frame_bilan.resize('auto', 'auto')
    frame_bilan.set_marge_items(10)
    frame_bilan.set_padding(0,0,20,20)
    frame_bilan.set_bg_color((236, 240, 241))
    frame_bilan.make_pos()

    duree = dureePretMois(type_pret.lower(),int(duree_entry))

    assurance = round(int(montant_entry)*(2/100),2)
    assuranceMois = round(assurance/duree,2)

    interet = round(int(montant_entry)*(taux_interet/100),2)
    total = int(montant_entry)+interet
    totalMois = round(total/duree,2)

    info1, info2 = [], []
    info1.append(['Prix de l\'assurance', str(assurance)+"€"])
    info1.append(['Prix de l\'assurance par mois', str(assuranceMois)+"€"])

    info2.append(['Montant du prêt', montant_entry+"€"])
    info2.append(['Montant de l\'intérêt', str(interet)+"€"])
    info2.append(['Total', str(total)+"€"])
    info2.append(['Prix du prêt par mois', str(totalMois)+"€"])

    infos = [info1, info2]
    frame_labels1 = []
    for info in infos:
        label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 40, 30, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 500, 'auto')
        frame_tmp = Frame(0, 0, label_tmp, None, [])
        frame_tmp.set_items_pos('auto')
        frame_tmp.set_marge_items(10)
        frame_tmp.set_direction('vertical')
        frame_tmp.resize('auto', 'auto')
        frame_tmp.set_bg_color((236, 240, 241))
        frame_tmp.make_pos()
        frame_labels1.append(frame_tmp)

    button_ok = create_button("Ok", 'font/colvetica/colvetica.ttf', 40, (255, 255, 255), (230, 126, 34), 0, 0, 400, 60, None, [])

    main_frame = Frame(0, 0, frame_labels + [frame_duree, frame_montant, generate_button, frame_bilan] + frame_labels1 + [button_ok], None, [])
    main_frame.set_direction('vertical')
    main_frame.set_items_pos('auto')
    main_frame.resize(910, 'auto')
    main_frame.set_padding(50,0,50,0)
    main_frame.set_marge_items(30)
    main_frame.set_bg_color((236, 240, 241))
    main_frame.make_pos()

    item_list = Item_list([main_frame], 330, 40, 1260, 40, 20, 680, 'salut')
    item_list.bg_color = (236, 240, 241)

    window.set_body_tmp([item_list])
    window.display(screen)

def get_pret(widget, window, screen, type_pret, taux_interet, *arg):
    entry = get_entry(widget, window, screen, *arg)

    duree = dureePret(type_pret.lower())
    for i in range(len(duree)):
        duree[i] = int(duree[i].split()[0])

    montant_max = montantPret(dureePretMois(type_pret.lower() ,int(entry['duree'])))
    if duree[0] <= int(entry['duree']) <= duree[1] and 0 <= int(entry['montant']) <= montant_max:
        draw_get_pret(widget, window, screen, type_pret, taux_interet, entry['duree'], entry['montant'])
    else:
        draw_alert(widget, window, screen, "Erreur", "Les données entrées sont invalides", clear_overbody, [])



'''
================================================================================
VENTES
================================================================================
'''

'''INCOMPLET'''
def draw_sales(widget, window, screen, *arg):
    pass

'''INCOMPLET'''
def draw_sales_product(widget, window, screen, prod_id, i, *arg):
    # ind = get_with_id(window.individus, ind_id)

    items = []

    path = 'img/icon/right_white_arrow'
    button_arrow = Button_img(0, path, 0, 0, None, [])
    text = 'Produit #'
    name = create_label(text, 'font/colvetica/colvetica.ttf', 40, (255,255,255), (149,165,166), 0, 0, None, None, [])
    frame_back = Frame(0,0, [button_arrow, name], draw_sales, [])
    frame_back.set_direction('horizontal')
    frame_back.set_items_pos('auto')
    frame_back.resize(250, 80)
    frame_back.set_align('center')
    frame_back.set_padding(10,0,0,0)
    frame_back.set_marge_items(10)
    frame_back.set_bg_color((149, 165, 166))
    frame_back.make_pos()

    info_market = create_label("Infos marché", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_sales_product, [prod_id, 0])
    text_product_kill = "Mettre en vente" #"Arrêter la distribution"
    make_sale = create_label(text_product_kill, 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_sales_product, [prod_id,1])

    focus_color = (41,128,185)
    if i == 0:
        info_market = create_label("Infos marché", 'calibri', 30, (255,255,255), focus_color, 0, 0, 250, draw_sales_product, [prod_id,0])

    elif i == 1:
        make_sale = create_label(text_product_kill, 'calibri', 30, (255,255,255), focus_color, 0, 0, 250, draw_sales_product, [prod_id,1])

    list_tmp = [info_market, make_sale]
    for element in list_tmp:
        element.set_direction('horizontal')
        element.resize(250, 'auto')
        element.set_padding(10,0,20,20)
        element.set_align('center')
        element.make_pos()

    frame_left = Frame(80, 40, [frame_back] + list_tmp, None, [])
    frame_left.set_direction('vertical')
    frame_left.set_items_pos('auto')
    frame_left.resize(250, 680)
    frame_left.set_marge_items(2)
    frame_left.set_bg_color((189, 195, 198))
    frame_left.make_pos()

    items.append(frame_left)

    window.set_body(items)
    window.display(screen)



'''
================================================================================
OPTIONS
================================================================================
'''

def draw_option(widget, window, screen, *arg):
    label_user = create_label("Utilisateur :", 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

    label_user_value = create_label(window.user_name, 'font/colvetica/colvetica.ttf', 50, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

    frame_tmp1 = Frame(0, 0, [label_user, label_user_value], None, [])
    frame_tmp1.set_direction('horizontal')
    frame_tmp1.set_items_pos('auto')
    frame_tmp1.resize('auto', 'auto')
    frame_tmp1.set_align('center')
    frame_tmp1.set_marge_items(50)
    frame_tmp1.set_padding(0,0,0,0)
    frame_tmp1.set_bg_color((236, 240, 241))
    frame_tmp1.make_pos()

    options = create_button("Options", 'font/colvetica/colvetica.ttf', 40, (236, 240, 241), (52,73,94), 0, 0, 500, 60, None, [])
    save_button = create_button("Sauvegarder", 'font/colvetica/colvetica.ttf', 40, (236, 240, 241), (52,73,94), 0, 0, 500, 60, save, [])
    f1 = ["Oui", reset_game, []]
    f2 = ["Non", clear_overbody, []]
    return_opening = create_button("Retourner au menu principal", 'font/colvetica/colvetica.ttf', 40, (236, 240, 241), (52,73,94), 0, 0, 500, 60, draw_alert_option, ['', 'Voulez-vous vraiment retourner au menu principal?',[f1, f2]])
    f1 = ["Oui", close_game, []]
    f2 = ["Non", clear_overbody, []]
    quit = create_button("Quitter", 'font/colvetica/colvetica.ttf', 40, (236, 240, 241), (52,73,94), 0, 0, 500, 60, draw_alert_option, ['', 'Voulez-vous vraiment quitter le jeu ?',[f1, f2]])
    f1 = ["Oui", delsave, []]
    f2 = ["Non", clear_overbody, []]
    msg = 'Supprimer la sauvegarde entraînera une perte définitive des données. Voulez-vous vraiment supprimer la sauvegarde ?'
    del_save = create_button("Supprimer la sauvegarde", 'font/colvetica/colvetica.ttf', 40, (236, 240, 241), (231, 76, 60), 0, 0, 500, 60, draw_alert_option, ['', msg,[f1, f2]])

    frame = Frame(80, 40, [frame_tmp1, options, save_button, return_opening, quit, del_save], None, [])
    frame.set_direction('vertical')
    frame.set_items_pos('auto')
    frame.resize(1200, 680)
    frame.set_marge_items(20)
    frame.set_padding(20,0,20,0)
    frame.set_bg_color((236,240,241))
    frame.make_pos()

    window.set_body([frame])
    window.display(screen)

def save(widget, window, screen, *arg):
    window.time_used = round(time.time()) - window.time_start
    window.last_used = datetime.datetime.now().date()
    window.save.save(window)
    draw_alert(widget, window, screen, "", "Partie sauvegardé !", clear_overbody, [])

def delsave(widget, window, screen, *arg):
    window.save.delete(window.sha)
    reset_game(widget, window, screen, *arg)
