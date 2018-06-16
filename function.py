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
from world.production import *
from world.majFinance import *
from world.Pret import *
from world.gameOver import *
from world.ventes import *

from lib.save import *

'''
================================================================================
AUTRES
================================================================================
'''

def create_label(text, police, fontsize, msg_color, bg_color, x, y, size, action, *arg):

    if type(text) != list:
        text = [text]
    else:
        for i in range(len(text)):
            text[i] = str(text[i])

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
        if type(element[1]) != list:
            value = create_label(str(element[1]), font2, size2, color2, color_bg2, 0, 0, None, None, [])
        else:
            value = create_label(element[1], font2, size2, color2, color_bg2, 0, 0, None, None, [])

        frame_tmp = Frame(0, 0, [label,value], None, [])
        frame_tmp.set_direction('horizontal')
        frame_tmp.set_items_pos('auto')
        frame_tmp.set_bg_color(color_bg2)
        frame_tmp.set_marge_items(0)
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

    # frame_tmp.type = 'button'
    #
    # items = []
    # items += frame_tmp.items
    # i = 1
    # for item in items:
    #     item.type = 'button'
    #     items[i:i] = item.items
    #     i += 1

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
                draw_prod(None, window, screen, 0)
            elif icon.num == 4:
                draw_finance(None, window, screen, 0)
            elif icon.num == 5:
                draw_sales(None, window, screen, 0)
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
    button_arrow = Button_img(0, path, 0, 0, reset_game, [True])

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

def check_save(widget, window, screen, tosave, callback, *arg):
    if tosave:
        save(widget, window, screen, *arg)
        callback(widget, window, screen, True, *arg)
    else:
        f1 = ["Oui", check_save, [True, callback]]
        f2 = ["Non", callback, [True]]
        draw_alert_option(widget, window, screen, "", ["La partie n'as pas été sauvegardé.", "Voulez-vous sauvegarder la partie ?"], [f1, f2])

def reset_game(widget, window, screen, force, *arg):
    if force:
        window.set_window()
        window.set_var()
        window.draw_opening()
        window.display(screen)
    else:
        check_save(widget, window, screen, False, reset_game, *arg)

def close_game(widget, window, screen, force, *arg):
    if force:
        window.run = False
    else:
        check_save(widget, window, screen, False, close_game, *arg)

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

    button_return = create_label( 'Menu principal', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, reset_game, [True])
    button_return.set_direction('vertical')
    button_return.resize(514,'auto')
    button_return.set_align('center')
    button_return.make_pos()

    frame_v = Frame(64, 605, [button_return], reset_game, [True])
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
    # window.draw_info()
    window.draw_nav_button()
    draw_home(None, window, screen)

def get_with_id(group, identifier):
    for obj in group:
        if obj.id == identifier:
            return obj
    return None

def get_with_name(group, identifier):
    for obj in group:
        if obj.nom == identifier:
            return obj
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

def do_nothing(*args):
    pass

def draw_shadow(widget, window, screen, *arg):
    pass
    # hover = Rectangle(widget.rect.x, widget.rect.y, widget.rect.width, widget.rect.height, (255,255,255), 50, None, [])
    # window.hover = [hover]
    # window.display(screen)


'''
================================================================================
HOME
================================================================================
'''

'''IMCOMPLET'''
def draw_home(widget, window, screen, *arg):
    text = 'Notifications'
    label = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 80, 40, None, None, [])
    label.set_direction('horizontal')
    label.set_padding(20,10,10,10)
    label.resize(600, 80)
    label.set_align('center')
    label.make_pos()

    nb_pop = 0
    for i in range(len(window.notifications)):
        if window.notifications[i][0] == 0:
            window.notifications.pop(i-nb_pop)
            nb_pop+=1

    window.notifications += genNotif(window.projets, window.paliers)

    a = []
    for notif in window.notifications:
        notif_content = []

        if notif[0] == 0:
            notif_content.append(create_label(notif[1], 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-700, None, []))
            notif_content.append(create_label(' ', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            notif_content.append(create_label(notif[2], 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-700, None, []))
            notif_content.append(create_label(' ', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))

            button_project = create_button("Aller au projet", 'font/colvetica/colvetica.ttf', 25, (255, 255, 255), (230, 126, 34), 0, 0, 'auto', 'auto', draw_project, [notif[3], 0])
            button_project.set_padding(15,15,10,10)
            button_project.make_pos()
            notif_content.append(button_project)
        elif notif[0] == 1:
            notif_content.append(create_label(notif[1], 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-700, None, []))
            notif_content.append(create_label(' ', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            notif_content.append(create_label(notif[2], 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-700, None, []))
            notif_content.append(create_label(' ', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))

        frame_notif = Frame(0, 0, notif_content, None, [])
        frame_notif.set_direction('vertical')
        frame_notif.set_items_pos('auto')
        frame_notif.resize(580, 'auto')
        frame_notif.set_padding(20,0,20,20)
        frame_notif.set_bg_color((236, 240, 241))
        frame_notif.make_pos()

        a.append(frame_notif)

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
    window.notifications = []
    window.temps += datetime.timedelta(weeks=1)
    #>>> partie RD
    window.projets = avance(window.projets, window.paliers, window.individus)
    window.projets, frais_RD, = allProgression(window.projets, window.individus, window.paliers, window.produits, window.materiaux, window.operations)

    for i in range(len(frais_RD)) :
        window.depenses.append(frais_RD[i])
    completedProject(window.projets, window.produits, window.individus, window.magasin)

    # Update des transports
    Transport.updateTempsTrajet(window.transports)
    window.transports = Transport.arrivees(window.transports, window.stocks, window.notifications)

    # Update des commandes
    Commande.updateCommandes(window.machines, window.individus, window.stocks[0], window.notifications)

    if (window.temps.year != window.year) :
        window.year = window.temps.year

        # Génération des consommateurs (populations)
        window.populations = consommateurs(str(window.year))


    if (window.temps.month != window.month):
       window.month = window.temps.month
           # events
           # coûts


    draw_home(widget, window, screen, *arg)
    save(widget, window, screen, *arg)
    draw_alert_tmp(widget, window, screen, 'Nouvelle semaine', "Semaine " + str(int(((window.temps - datetime.datetime(2018,1,1)).days)/7)), [])



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
        label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 25, 20, (52,73,94), (52,73,94), (189,195,199), (189,195,199), 400, 'auto')
        frame_tmp = Frame(0, 0, label_tmp, None, [])
        frame_tmp.set_items_pos('auto')
        frame_tmp.set_marge_items(10)
        frame_tmp.set_direction('vertical')
        frame_tmp.resize('auto', 'auto')
        frame_tmp.set_bg_color((189,195,199))
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
    frame_v.set_bg_color((189,195,199))
    frame_v.make_pos()

    frame_left = Frame(80, 40, frame_labels + [frame_v] , None, [])
    frame_left.set_direction('vertical')
    frame_left.set_items_pos('auto')
    frame_left.resize(600, 680)
    frame_left.set_padding(20,20,20,20)
    frame_left.set_marge_items(50)
    frame_left.set_bg_color((189,195,199))
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
    # role = create_label("Changer de rôle", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee, [ind_id,1])
    # formation = create_label("Formation", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee, [ind_id,2])

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

    # elif i == 1:
    #     role = create_label("Changer de rôle", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [ind_id,1])
    #     roles = []
    #     item_list_role = Item_list(roles, 330, 40, 1260, 40, 20, 680, 'rôle')
    #     items.append(item_list_role)

    # elif i == 2:
    #     formation = create_label("Formation", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [ind_id,2])
    #     formations = []
    #     item_list_formation = Item_list(formations, 330, 40, 1260, 40, 20, 680, 'formation')
    #     items.append(item_list_formation)


    list_tmp = [attribute, fired]
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
    button_product = create_label("Produits", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_rd, [1])

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

        button_add_project = Frame(330, 40, [label_add_project, icon_sum], draw_add_project, [individus, [], None])
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

            label_phase = create_label("Phase :", 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
            label_phase.resize(200, 'auto')
            label_phase.set_items_pos('auto')
            label_phase.make_pos()
            label_phase_value = create_label(nomPhase(project.phase, project.id), 'calibri', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

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

            if project.id < 0 :
                pourcentage = str(int(project.avancement*100 / project.palier))
            else :
                pourcentage = str(int(project.avancement * 100 / window.paliers[project.phase-1]))

            label_pourcentage = create_label(pourcentage+'%', 'calibri', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

            if project.id < 0 :
                progress_bar = Progress_bar(0, 0, 600, 30, None, [], project.avancement, project.palier, (46, 204, 113), (255, 255, 255))
            else :
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
        button_product = create_label("Produits", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_rd, [1])

        products = []

        for product in window.produits:
            product_info = []

            product_info.append(create_label(product.nom, 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            product_info.append(create_label(' ', 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            product_info.append(create_label('Nombre d\'améliorations : ' + str(product.nbr_ameliorations), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))

            frame_product = Frame(0, 0, product_info, draw_product, [product.nom, 0])
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

def draw_add_project(widget, window, screen, lst_ind, lst_ajout, product, *arg):
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

        frame_employee = Frame(0, 0, employee_info, draw_add_project, [lst_ind_tmp, lst_ajout + [ind], product])
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

        employe_name = create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, draw_add_project, [lst_ind + [ind], lst_ajout_tmp, product])
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

    if product == None:
        button_submit = create_label('Ajouter le projet', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, create_project, [lst_ajout])
    else:
        button_submit = create_label('Ajouter le projet', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, update_product, [lst_ajout, product])
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

def update_product(widget, window, screen, lst_emp, product, *arg):
    entry = get_entry(widget, window, screen, *arg)
    if check_string(widget, window, screen, r"^[a-zA-Z0-9 ]+$", entry['name_project'], "Nom de projet incorrect") and lst_emp != []:
        window.projets.append(Ameliore(product, entry['name_project']))
        for ind in lst_emp:
            addChercheurs(window.projets[-1], window.individus, ind.id)
        title_msg = 'Bravo !'
        msg = 'Le projet ' + entry['name_project'] + ' a bien été crée ! Le produit ' + product.nom +' est maintenant en cours d\'amélioration !'
        draw_rd(widget, window, screen, 0)
        draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])
    elif lst_emp == []:
        draw_alert(widget, window, screen, "Erreur", "Aucun employé sélectionné", clear_overbody, [])

def actionPhase(widget, window, screen, projet, choix , *arg) :
    if projet.id < 0 :
        window.depenses.append(Ameliore.progression(projet, choix))
    else :
        window.depenses.append(Projet.progression(projet, window.individus, window.paliers, choix, window.produits, window.materiaux, window.operations))
    draw_alert(widget, window, screen, 'Bravo', 'Le projet passe à la phase suivante', clear_overbody, [])
    draw_project(widget, window, screen, projet.id, 0)

def status(widget, window, screen, projet, *arg) :
    # Initialisation du message general à afficher
    msg_general = []
    # Initialisation de la liste des boutons à créer
    boutons = []
    # On initialise l'indicateur d'argent de l'utilisateur
    desh = False

    if projet.id < 0 :
        if projet.attente==True and projet.phase != 5 :
            msg_general.append("Vous avez amélioré votre produit. Il vous faut cependant déposer un brevet pour sécuriser cette nouvelle propriété.")
            msg_general.append("Voulez-vous déposer un brevet ? Cela vous coutera : "+str(50)+" euros.")

            if window.argent>=50 :
                boutons.append(["Accepter", actionPhase, [projet, True]])
            else :
                desh = True

        elif projet.phase == 5 :
            msg_general.append("Ce projet vient d'être achevé. Vous aurez accès à votre nouveau produit au prochain tour.")
        else :
            msg_general.append("Développement en cours.")
    else :
        if projet.phase==1 and projet.attente==True:
            msg_general.append("Les résultats de l'étude de marché sont arrivés !")
            msg_general.append("Veuillez sélectionner la population que ciblera votre concept de produit pour faire avancer le projet à la phase suivante :")
            bouton_1 = [["Jeunes :", projet.produit.appreciation[0][0][0]], actionPhase, [projet, "Jeunes"]]
            bouton_2 = [["Actifs :", projet.produit.appreciation[1][0][0]], actionPhase, [projet, "Actifs"]]
            bouton_3 = [["Seniors :", projet.produit.appreciation[2][0][0]], actionPhase, [projet, "Seniors"]]
            boutons.append(bouton_1)
            boutons.append(bouton_2)
            boutons.append(bouton_3)
        elif projet.phase==2 and projet.attente==True:
            msg_general.append("Vos chercheurs sont près à passer à la phase expérimentale.")
            msg_general.append("Voulez-vous réaliser un premier prototype ? Cela vous coutera : "+str(round(projet.produit.cout, 2))+" euros.")

            if window.argent>=round(projet.produit.cout, 2) :
                boutons.append(["Accepter", actionPhase, [projet, True]])
            else :
                desh = True

        elif projet.phase==4 :
            if projet.attente==False and projet.essai==False :
                msg_general.append("Vos chercheurs pensent qu'il serait bénéfique de mettre votre prototype à l'essai, cela permettrait d'accélérer la création du produit final")
                msg_general.append("Voulez-vous mettre votre prototype à l'essai ? Cela vous coutera : "+str(50)+" euros.")

                if window.argent>=50 :
                    boutons.append(["Accepter", actionPhase, [projet, True]])
                else :
                    desh=True

            elif projet.attente==True:
                msg_general.append("Votre prototype est en passe de devenir un de vos produits. Il vous faut cependant déposer un brevet pour sécuriser cette nouvelle propriété.")
                msg_general.append("Voulez-vous déposer un brevet ? Cela vous coutera : "+str(50)+" euros.")

                if window.argent>=50:
                    boutons.append(["Accepter", actionPhase, [projet, True]])
                else:
                    desh=True

            else :
                msg_general.append("En cours.")

        elif projet.phase==5 :
            msg_general.append("Ce projet vient d'être achevé. Vous aurez accès à votre nouveau produit au prochain tour.")

        else :
            msg_general.append("En cours.")

    if desh :
        msg_general.append("Malheureusement vous n'avez pas assez d'argent.")

    return(msg_general, boutons)

def draw_project(widget, window, screen, proj_id, i, *arg):
    projet = get_with_id(window.projets, proj_id)

    items = []

    path = 'img/icon/right_white_arrow'
    button_arrow = Button_img(0, path, 0, 0, None, [])
    if proj_id >= 0 :
        text = 'Projet ' + str(proj_id)
    else :
        text = 'Projet'  + str(proj_id)
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

        label_phase_value = create_label(nomPhase(projet.phase, projet.id), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

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

        if projet.id < 0 :
            pourcentage = str(int(projet.avancement*100 / projet.palier))
        else :
            pourcentage = str(int(projet.avancement * 100 / window.paliers[projet.phase-1]))

        label_pourcentage = create_label(pourcentage+'%', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

        if projet.id < 0 :
            progress_bar = Progress_bar(0, 0, 600, 30, None, [], projet.avancement, projet.palier, (46, 204, 113), (255, 255, 255))
        else :
            progress_bar = Progress_bar(0, 0, 600, 30, None, [], projet.avancement, window.paliers[projet.phase-1], (46, 204, 113), (255, 255, 255))

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
        frame_button.set_marge_items(50)
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
        frame_status.set_marge_items(50)
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

def draw_product(widget, window, screen, prod_name, i, *arg):

    prod = get_with_name(window.produits, prod_name)

    items = []

    path = 'img/icon/right_white_arrow'
    button_arrow = Button_img(0, path, 0, 0, None, [])
    text = 'Produit'
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

    attribute = create_label("Caractéristique", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_product, [prod_name, 0])
    individus = []
    for ind in window.individus :
        if ind.projet == None :
            individus.append(ind)
    update = create_label("Améliorer", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_add_project, [individus, [], prod])

    focus_color = (41,128,185)
    if i == 0:
        attribute = create_label("Caractéristique", 'calibri', 30, (255,255,255), focus_color, 0, 0, 250, draw_product, [prod_name,0])

        title = create_label(prod.nom, 'font/colvetica/colvetica.ttf', 50, (44,62,80), (236,240,241), 0, 0, None, None, [])
        title.set_padding(0,0,0,30)
        title.make_pos()

        info1, info2, info3, info4, info5 = [], [], [], [], []
        info1.append(['Matériaux nécessaires', affichMatOper(prod.materiaux)])
        info1.append(['Opérations nécessaires', affichMatOper(prod.operations)])
        info2.append(['Population cible', prod.cible])
        if prod.marche==True :
            info2.append(['Prix de vente', prod.prix])
            info2.append(['Nombre de vente', prod.ventes])
            info2.append(['Temps passé sur le marché', prod.age])

        info3.append(["Nombre d'améliorations effectuées", prod.nbr_ameliorations])

        infos = [info1, info2, info3]
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

    # elif i == 1:
        # update = create_label("Améliorer", 'calibri', 30, (255,255,255), focus_color, 0, 0, 250, draw_product, [prod_name,1])

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

def draw_prod(widget, window, screen, i, *arg):
    items = []
    items_tmp = []

    button_statue = create_label("Tableau de bord", 'calibri', 29, (255,255,255), (189,195,198), 0, 0, None, draw_prod, [0])
    button_appro = create_label("Approvisionnement", 'calibri', 29, (255,255,255), (189,195,198), 0, 0, None, draw_prod, [1])
    button_prod = create_label("Production", 'calibri', 29, (255,255,255), (189,195,198), 0, 0, None, draw_prod, [2])
    button_stock = create_label("Stock", 'calibri', 29, (255,255,255), (189,195,198), 0, 0, None, draw_prod, [3])
    button_machine = create_label("Machines", 'calibri', 29, (255,255,255), (189,195,198), 0, 0, None, draw_prod, [4])

    focus_color = (41,128,185)
    if i == 0:
        button_statue = create_label("Tableau de bord", 'calibri', 29, (255,255,255), focus_color, 0, 0, None, draw_prod, [0])

        text = 'Transport en cours'
        label_stock = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 330, 40, None, None, [])
        label_stock.set_direction('horizontal')
        label_stock.set_padding(20,10,10,10)
        label_stock.resize(475, 80)
        label_stock.set_align('center')
        label_stock.make_pos()

        a = []
        for element in window.transports:
            info = []

            info.append(create_label(str(element.materiaux[0][1]) + 'x ' + element.materiaux[0][0], 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            info.append(create_label('Départ : ' + element.depart, 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            info.append(create_label('Arrivée : ' + element.arrivee, 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))

            info.append(create_label('Avancement du transport : ', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            info.append(create_label( ' ', 'calibri', 15, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))

            t = element.temps_total-element.tps_trajet
            end = element.temps_total
            pourcentage = str(int(t * 100 / end))
            label_pourcentage = create_label(pourcentage+'%', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
            progress_bar = Progress_bar(0, 0, 350, 20, None, [], t, end, (46, 204, 113), (255, 255, 255))


            frame_progress_bar = Frame(0, 0, [label_pourcentage, progress_bar], None, [])
            frame_progress_bar.set_direction('horizontal')
            frame_progress_bar.set_items_pos('auto')
            frame_progress_bar.set_align('center')
            frame_progress_bar.set_marge_items(20)
            frame_progress_bar.set_bg_color((236, 240, 241))
            frame_progress_bar.make_pos()

            info.append(frame_progress_bar)

            # item_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            # item_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            # item_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            # item_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

            frame_item = Frame(0, 0, info, None, [])
            frame_item.set_direction('vertical')
            frame_item.set_items_pos('auto')
            frame_item.resize(455, 'auto')
            frame_item.set_padding(20,0,20,20)
            frame_item.set_bg_color((236, 240, 241))
            frame_item.make_pos()

            a.append(frame_item)

        item_list = Item_list(a, 330, 120, 785, 120, 20, 640, 'stock')
        items_tmp.append(item_list)
        items_tmp.append(label_stock)

        text = 'Production en cours'
        label_stock = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 805, 40, None, None, [])
        label_stock.set_direction('horizontal')
        label_stock.set_padding(20,10,10,10)
        label_stock.resize(475, 80)
        label_stock.set_align('center')
        label_stock.make_pos()

        a = []
        for machines in window.machines:
            for element in machines.commandes:
                info = []
                info.append(create_label(str(int(element.prod_totaux)) + 'x ' + str(element.produit.nom) , 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
                info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
                info.append(create_label('Produit restant : ' + str(int(element.prod_restants)), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

                info.append(create_label('Avancement du transport : ', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
                info.append(create_label( ' ', 'calibri', 15, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))

                t = element.prod_totaux-element.prod_restants
                end = element.prod_totaux
                pourcentage = str(int(t * 100 / end))
                label_pourcentage = create_label(pourcentage+'%', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
                progress_bar = Progress_bar(0, 0, 350, 20, None, [], t, end, (46, 204, 113), (255, 255, 255))


                frame_progress_bar = Frame(0, 0, [label_pourcentage, progress_bar], None, [])
                frame_progress_bar.set_direction('horizontal')
                frame_progress_bar.set_items_pos('auto')
                frame_progress_bar.set_align('center')
                frame_progress_bar.set_marge_items(20)
                frame_progress_bar.set_bg_color((236, 240, 241))
                frame_progress_bar.make_pos()

                info.append(frame_progress_bar)

                # item_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
                # item_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
                # item_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
                # item_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

                frame_item = Frame(0, 0, info, None, [])
                frame_item.set_direction('vertical')
                frame_item.set_items_pos('auto')
                frame_item.resize(455, 'auto')
                frame_item.set_padding(20,0,20,20)
                frame_item.set_bg_color((236, 240, 241))
                frame_item.make_pos()

                a.append(frame_item)

        item_list = Item_list(a, 805, 120, 1260, 120, 20, 640, 'production')
        items_tmp.append(item_list)
        items_tmp.append(label_stock)

    elif i == 1:
        button_appro = create_label("Approvisionnement", 'calibri', 29, (255,255,255), focus_color, 0, 0, None, draw_prod, [1])

        text = 'Choisir un matériau'
        label = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 330, 40, None, None, [])
        label.set_direction('horizontal')
        label.set_padding(20,10,10,10)
        label.resize(950, 80)
        label.set_align('center')
        label.make_pos()

        a = []
        for element in enhancedSort(window.materiaux, 'nom', False):
            info = []

            info.append(create_label(element.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

            frame_item = Frame(0, 0, info, draw_choose_fournisseur, [element.nom])
            frame_item.set_direction('vertical')
            frame_item.set_items_pos('auto')
            frame_item.resize(920, 'auto')
            frame_item.set_padding(20,0,20,20)
            frame_item.set_bg_color((236, 240, 241))
            frame_item.make_pos()

            a.append(frame_item)

        item_list = Item_list(a, 330, 120, 1260, 120, 20, 640, 'matériau')
        items_tmp.append(item_list)
        items_tmp.append(label)

    elif i == 2:
        button_prod = create_label("Production", 'calibri', 29, (255,255,255), focus_color, 0, 0, None, draw_prod, [2])

        text = 'Choisir un produit'
        label = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 330, 40, None, None, [])
        label.set_direction('horizontal')
        label.set_padding(20,10,10,10)
        label.resize(950, 80)
        label.set_align('center')
        label.make_pos()

        a = []
        for element in window.produits:
            info = []

            info.append(create_label(element.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

            frame_item = Frame(0, 0, info, draw_quantity_produit, [element.nom, '1'])
            frame_item.set_direction('vertical')
            frame_item.set_items_pos('auto')
            frame_item.resize(930, 'auto')
            frame_item.set_padding(20,0,20,20)
            frame_item.set_bg_color((236, 240, 241))
            frame_item.make_pos()

            a.append(frame_item)

        item_list = Item_list(a, 330, 120, 1260, 120, 20, 640, 'produit')
        items_tmp.append(item_list)
        items_tmp.append(label)

    elif i == 3:
        button_stock = create_label("Stock", 'calibri', 29, (255,255,255), focus_color, 0, 0, None, draw_prod, [3])

        items_list = []

        for element in window.stocks[0].materiaux:
            info = []

            info.append(create_label(element[0], 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            info.append(create_label(' ', 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            info.append(create_label('Quantité : ' + str(element[1]), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))

            frame_item = Frame(0, 0, info, None, [])
            frame_item.set_direction('vertical')
            frame_item.set_items_pos('auto')
            frame_item.resize(930, 'auto')
            frame_item.set_padding(20,0,20,20)
            frame_item.set_bg_color((236, 240, 241))
            frame_item.make_pos()

            items_list.append(frame_item)

        item_list_widget = Item_list(items_list, 330, 40, 1260, 40, 20, 680, 'produit')

        items.append(item_list_widget)
    elif i == 4:
        button_machine = create_label("Machines", 'calibri', 29, (255,255,255), focus_color, 0, 0, None, draw_prod, [4])

        label_magasin = create_label("Acheter une machine", 'font/colvetica/colvetica.ttf', 40, (255,255,255), (52,73,94), 0, 0, None, None, [])
        label_magasin.set_direction('horizontal')
        label_magasin.resize(540, 'auto')
        label_magasin.set_align('center')
        label_magasin.make_pos()

        path = 'img/icon/grey_sum'
        icon_sum = Button_img(0, path, 0, 0, None, [])

        button_magasin = Frame(330, 40, [label_magasin, icon_sum], draw_magasin, [])
        button_magasin.set_direction('horizontal')
        button_magasin.set_items_pos('auto')
        button_magasin.resize(950, 80)
        button_magasin.set_align('center')
        button_magasin.set_padding(350,0,0,0)
        button_magasin.set_marge_items(0)
        button_magasin.set_bg_color((52,73,94))
        button_magasin.make_pos()

        a = []
        for element in window.machines:
            info = []

            info.append(create_label(element.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            if element.utilisateur != None:
                info.append(create_label('Utilisateur : ' + element.utilisateur.nom + " " + element.utilisateur.prenom, 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            else:
                info.append(create_label('Utilisateur : Aucun', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            info.append(create_label('Opérations : ', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

            operations_label = []
            for operation in element.operations_realisables:
                operations_label.append(create_label('- ' + operation, 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

            frame_operations = Frame(0, 0, operations_label, None, [])
            frame_operations.set_direction('vertical')
            frame_operations.set_items_pos('auto')
            frame_operations.resize('auto', 'auto')
            frame_operations.set_padding(20,0,0,20)
            frame_operations.set_bg_color((236, 240, 241))
            frame_operations.make_pos()
            info.append(frame_operations)

            if element.utilisateur == None:
                button_user = create_button("Ajouter un utilisateur à la machine", 'font/colvetica/colvetica.ttf', 25, (255, 255, 255), (230, 126, 34), 0, 0, 'auto', 'auto', draw_add_user_to_machine, [element.id])
                button_user.set_padding(15,15,10,10)
                button_user.make_pos()
                info.append(button_user)
            else:
                button_user = create_button("Retirer l'utilisateur de la machine", 'font/colvetica/colvetica.ttf', 25, (255, 255, 255), (230, 126, 34), 0, 0, 'auto', 'auto', remove_machine_user, [element.id])
                button_user.set_padding(15,15,10,10)
                button_user.make_pos()
                info.append(button_user)

            frame_item = Frame(0, 0, info, None, [])
            frame_item.set_direction('vertical')
            frame_item.set_items_pos('auto')
            frame_item.resize(930, 'auto')
            frame_item.set_padding(20,0,20,20)
            frame_item.set_bg_color((236, 240, 241))
            frame_item.make_pos()

            a.append(frame_item)

        item_list = Item_list(a, 330, 120, 1260, 120, 20, 640, 'machine')
        items_tmp.append(item_list)
        items_tmp.append(button_magasin)



    list_tmp = [button_statue, button_appro, button_prod, button_stock, button_machine]
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
    window.set_body_tmp(items_tmp)
    window.draw_button_info('Aide', '')
    window.display(screen)

def draw_choose_fournisseur(widget, window, screen, mat, *arg):
    items = []

    path = 'img/icon/left_grayblu_arrow'
    button_arrow = Button_img(0, path, 0, 0, draw_prod, [1])

    text = 'Choisir un founisseur'
    label_title = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 0, 0, None, None, [])
    label_title.set_direction('horizontal')
    label_title.set_padding(10,0,0,0)
    label_title.resize(870, 80)
    label_title.set_align('center')
    label_title.make_pos()

    frame_head = Frame(330, 40, [button_arrow, label_title], None, [])
    frame_head.set_items_pos('auto')
    frame_head.set_direction('horizontal')
    frame_head.resize('auto', 'auto')
    frame_head.set_bg_color((52,73,94))
    frame_head.make_pos()

    label = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 330, 40, None, None, [])
    label.set_direction('horizontal')
    label.set_padding(20,10,10,10)
    label.resize(920, 80)
    label.set_align('center')
    label.make_pos()

    lst_fourn = Fournisseur.listeFour(window.fournisseurs, mat)

    a = []
    for element in lst_fourn:
        info = []

        info.append(create_label(element.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
        info.append(create_label('Localisation : ' + element.localisation, 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        # item_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        # item_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
        # item_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        # item_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        frame_item = Frame(0, 0, info, draw_quantity_mat, [mat, element.nom, '1'])
        frame_item.set_direction('vertical')
        frame_item.set_items_pos('auto')
        frame_item.resize(920, 'auto')
        frame_item.set_padding(20,0,20,20)
        frame_item.set_bg_color((236, 240, 241))
        frame_item.make_pos()

        a.append(frame_item)

    item_list = Item_list(a, 330, 120, 1260, 120, 20, 640, 'matériau')
    items.append(item_list)
    items.append(frame_head)

    window.set_body_tmp(items)
    window.display(screen)

def draw_quantity_mat(widget, window, screen, mat, fourn, quantity, *arg):

    fournisseur = get_with_name(window.fournisseurs, fourn)
    cout_u = Fournisseur.coutMateriau(fournisseur, mat)
    max = int(window.argent / cout_u)
    info1 = []
    info1.append(['Coût unitaire', str(cout_u) + ' €'])

    infos = [info1]
    frame_labels = []
    for info in infos:
        label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 40, 30, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 430, 'auto')
        frame_tmp = Frame(0, 0, label_tmp, None, [])
        frame_tmp.set_items_pos('auto')
        frame_tmp.set_marge_items(10)
        frame_tmp.set_direction('vertical')
        frame_tmp.resize('auto', 'auto')
        frame_tmp.set_bg_color((236, 240, 241))
        frame_tmp.make_pos()
        frame_labels.append(frame_tmp)


    path = 'img/icon/left_grayblu_arrow'
    button_arrow = Button_img(0, path, 0, 0, draw_choose_fournisseur, [mat])

    text = 'Choisir la quantité de ' + mat +  ' à acheter'
    label_title = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 0, 0, None, None, [])
    label_title.set_direction('horizontal')
    label_title.set_padding(10,0,0,0)
    label_title.resize(870, 80)
    label_title.set_align('center')
    label_title.make_pos()

    frame_head = Frame(330, 40, [button_arrow, label_title], None, [])
    frame_head.set_items_pos('auto')
    frame_head.set_direction('horizontal')
    frame_head.resize('auto', 'auto')
    frame_head.set_bg_color((52,73,94))
    frame_head.make_pos()

    label = create_label('Quantité : ', 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
    label_scale = create_label('compris entre 0 et '+ str(max), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

    frame_label = Frame(0, 0, [label, label_scale], None, [])
    frame_label.set_direction('vertical')
    frame_label.set_items_pos('auto')
    frame_label.resize(420, 'auto')
    frame_label.set_marge_items(10)
    frame_label.set_padding(0,0,0,20)
    frame_label.set_bg_color((236, 240, 241))
    frame_label.make_pos()

    entry = Entry(0, 0, 200, 40, True, 'quantity', 0, None)
    entry.set_entry(quantity)

    frame_input = Frame(0, 0, [frame_label, entry], None, [])
    frame_input.set_direction('horizontal')
    frame_input.set_items_pos('auto')
    frame_input.resize('auto', 'auto')
    frame_input.set_marge_items(10)
    frame_input.set_bg_color((236, 240, 241))
    frame_input.make_pos()

    newt_button = create_button("Suivant", 'font/colvetica/colvetica.ttf', 40, (255, 255, 255), (230, 126, 34), 0, 0, 400, 60, draw_summary_appro, [mat, fourn, max])

    frame_main = Frame(330, 120, frame_labels + [frame_input, newt_button], None, [])
    frame_main.set_direction('vertical')
    frame_main.set_items_pos('auto')
    frame_main.resize('auto', 'auto')
    frame_main.set_marge_items(20)
    frame_main.set_padding(20,0,20,0)
    frame_main.set_bg_color((236, 240, 241))
    frame_main.make_pos()

    window.set_body_tmp([frame_head, frame_main])
    window.display(screen)

def draw_summary_appro(widget, window, screen, mat, fourn, max, *arg):
    fournisseur = get_with_name(window.fournisseurs, fourn)
    entry = get_entry(widget, window, screen, *arg)

    if entry['quantity'] == '':
        draw_alert(widget, window, screen, "Erreur", "Certains champs sont invalides", clear_overbody, [])
    else:
        if 1 <= int(entry['quantity']) <= max:
            commande = [[mat, int(entry['quantity'])]]
            founisseur = get_with_name(window.fournisseurs, fourn)
            total_mat = Fournisseur.coutMateriaux(founisseur, commande)
            dest = window.stocks[0] # bonus
            cout_transp = Fournisseur.coutTransport(fournisseur, dest)
            temps_transp = Fournisseur.tpsTransport(fournisseur, dest)

            path = 'img/icon/left_grayblu_arrow'
            button_arrow = Button_img(0, path, 0, 0, draw_quantity_mat, [mat, fourn, entry['quantity']])

            text = 'Résumé de la commande'
            label_title = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 0, 0, None, None, [])
            label_title.set_direction('horizontal')
            label_title.set_padding(10,0,0,0)
            label_title.resize(870, 80)
            label_title.set_align('center')
            label_title.make_pos()

            frame_head = Frame(330, 40, [button_arrow, label_title], None, [])
            frame_head.set_items_pos('auto')
            frame_head.set_direction('horizontal')
            frame_head.resize('auto', 'auto')
            frame_head.set_bg_color((52,73,94))
            frame_head.make_pos()

            info1, info2 = [], []
            info1.append(['Commande', entry['quantity'] + ' ' + mat ])
            info1.append(['Coût total des matériaux', str(total_mat) + ' €'])
            info1.append(['Coût du transport', str(cout_transp) + ' €'])
            info1.append(['Coût total', str(total_mat + cout_transp) + ' €'])
            info2.append(['Temps transport', str(int(temps_transp))+ ' semaine(s)'])

            infos = [info1, info2]
            frame_labels = []
            for info in infos:
                label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 40, 30, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 385, 'auto')
                frame_tmp = Frame(0, 0, label_tmp, None, [])
                frame_tmp.set_items_pos('auto')
                frame_tmp.set_marge_items(10)
                frame_tmp.set_direction('vertical')
                frame_tmp.resize('auto', 'auto')
                frame_tmp.set_bg_color((236, 240, 241))
                frame_tmp.make_pos()
                frame_labels.append(frame_tmp)

            newt_button = create_button("Passez la commande", 'font/colvetica/colvetica.ttf', 40, (255, 255, 255), (230, 126, 34), 0, 0, 400, 60, make_appro, [fournisseur, commande, total_mat + cout_transp])

            frame_main = Frame(330, 120, frame_labels + [newt_button], None, [])
            frame_main.set_direction('vertical')
            frame_main.set_items_pos('auto')
            frame_main.resize('auto', 'auto')
            frame_main.set_marge_items(20)
            frame_main.set_padding(20,0,20,0)
            frame_main.set_bg_color((236, 240, 241))
            frame_main.make_pos()

            window.set_body_tmp([frame_head, frame_main])
            window.display(screen)
        else:
            draw_alert(widget, window, screen, "Erreur", "Les données entrées sont invalides", clear_overbody, [])

def make_appro(widget, window, screen, fournisseur, commande, cout_total, *arg):
    if cout_total > window.argent:
        draw_alert(widget, window, screen, "Erreur", "Vous n'avez pas assez d'argent", clear_overbody, [])
    else:
        window.argent = Fournisseur.approvisionnement(window.transports, window.couts, fournisseur, window.stocks[0], commande, window.argent)
        title_msg = ''
        msg = 'La commande de ' + str(commande[0][1]) + ' ' + commande[0][0] + ' à ' + fournisseur.nom +  ' a bien été effectuée.'
        draw_prod(widget, window, screen, 0)
        draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])

def draw_quantity_produit(widget, window, screen, produit, quantity, *arg):
    items = []

    product = get_with_name(window.produits, produit)

    text = 'Stock'
    label_stock = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 330, 40, None, None, [])
    label_stock.set_direction('horizontal')
    label_stock.set_padding(20,10,10,10)
    label_stock.resize(475, 80)
    label_stock.set_align('center')
    label_stock.make_pos()

    liste_mat = listeMat(window.stocks[0], product)
    a = []
    for element in liste_mat:
        info = []

        info.append(create_label(str(element[1]) + 'x ' + element[0], 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        # item_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        # item_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
        # item_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        # item_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        frame_item = Frame(0, 0, info, None, [])
        frame_item.set_direction('vertical')
        frame_item.set_items_pos('auto')
        frame_item.resize(455, 'auto')
        frame_item.set_padding(20,0,20,20)
        frame_item.set_bg_color((236, 240, 241))
        frame_item.make_pos()

        a.append(frame_item)

    item_list = Item_list(a, 330, 120, 785, 120, 20, 480, 'stock')
    items.append(item_list)
    items.append(label_stock)

    text = 'Composants du produit'
    label_stock = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 805, 40, None, None, [])
    label_stock.set_direction('horizontal')
    label_stock.set_padding(20,10,10,10)
    label_stock.resize(475, 80)
    label_stock.set_align('center')
    label_stock.make_pos()

    a = []
    for element in product.materiaux:
        info = []

        info.append(create_label(str(element[1]) + 'x ' + element[0], 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        # item_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        # item_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
        # item_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        # item_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        frame_item = Frame(0, 0, info, None, [])
        frame_item.set_direction('vertical')
        frame_item.set_items_pos('auto')
        frame_item.resize(455, 'auto')
        frame_item.set_padding(20,0,20,20)
        frame_item.set_bg_color((236, 240, 241))
        frame_item.make_pos()

        a.append(frame_item)

    item_list = Item_list(a, 805, 120, 1260, 120, 20, 480, 'composant')
    items.append(item_list)
    items.append(label_stock)

    max = Machine.maxMat(liste_mat, product.materiaux)

    if max != 0:
        label = create_label('Quantité à produire: ', 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
        label_scale = create_label('compris entre 1 et '+ str(max), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

        frame_label = Frame(0, 0, [label, label_scale], None, [])
        frame_label.set_direction('vertical')
        frame_label.set_items_pos('auto')
        frame_label.resize(300, 'auto')
        frame_label.set_marge_items(10)
        frame_label.set_padding(0,0,0,20)
        frame_label.set_bg_color((236, 240, 241))
        frame_label.make_pos()

        entry = Entry(0, 0, 200, 40, True, 'quantity', 0, None)
        entry.set_entry(quantity)

        frame_input = Frame(0, 0, [frame_label, entry], None, [])
        frame_input.set_direction('horizontal')
        frame_input.set_items_pos('auto')
        frame_input.resize('auto', 'auto')
        frame_input.set_marge_items(10)
        frame_input.set_bg_color((236, 240, 241))
        frame_input.make_pos()

        newt_button = create_button("Suivant", 'font/colvetica/colvetica.ttf', 30, (255, 255, 255), (230, 126, 34), 0, 0, 200, 40, draw_choose_machine, [produit, max, None])

        frame_main = Frame(330, 600, [frame_input, newt_button], None, [])
        frame_main.set_direction('horizontal')
        frame_main.set_items_pos('auto')
        frame_main.resize('auto', 'auto')
        frame_main.set_marge_items(120)
        frame_main.set_padding(20,0,50,0)
        frame_main.set_align('center')
        frame_main.set_bg_color((236, 240, 241))
        frame_main.make_pos()
        items.append(frame_main)

    else:
        label = create_label('Vous n\'avez pas assez de matériaux pour produire !', 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
        frame_main = Frame(330, 600, [label], None, [])
        frame_main.set_direction('horizontal')
        frame_main.set_items_pos('auto')
        frame_main.resize('auto', 'auto')
        frame_main.set_marge_items(120)
        frame_main.set_padding(20,0,100,0)
        frame_main.set_align('center')
        frame_main.set_bg_color((236, 240, 241))
        frame_main.make_pos()
        items.append(frame_main)

    window.set_body_tmp(items)
    window.display(screen)

def draw_choose_machine(widget, window, screen, produit, max, quantity, *arg):
    if quantity == None:
        entry = get_entry(widget, window, screen, *arg)
    else:
        entry['quantity'] = quantity

    if entry['quantity'] == '':
        draw_alert(widget, window, screen, "Erreur", "Certains champs sont invalides", clear_overbody, [])
    else:
        if 1 <= int(entry['quantity']) <= max:
            product = get_with_name(window.produits, produit)
            lst_machine = Machine.listeMach(window.machines, product)

            items_tmp = []

            path = 'img/icon/left_grayblu_arrow'
            button_arrow = Button_img(0, path, 0, 0, draw_quantity_produit, [produit, entry['quantity']])

            text = 'Choisir une machine'
            label_title = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 0, 0, None, None, [])
            label_title.set_direction('horizontal')
            label_title.set_padding(10,0,0,0)
            label_title.resize(870, 80)
            label_title.set_align('center')
            label_title.make_pos()

            frame_head = Frame(330, 40, [button_arrow, label_title], None, [])
            frame_head.set_items_pos('auto')
            frame_head.set_direction('horizontal')
            frame_head.resize('auto', 'auto')
            frame_head.set_bg_color((52,73,94))
            frame_head.make_pos()


            a = []
            for element in lst_machine:
                info = []

                info.append(create_label(element.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
                info.append(create_label(' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
                if element.utilisateur != None:
                    info.append(create_label('Utilisateur : ' + element.utilisateur.prenom + ' ' + element.utilisateur.nom, 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
                else:
                    info.append(create_label('Utilisateur : Aucun', 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

                frame_item = Frame(0, 0, info, draw_add_machine_user, [produit, entry['quantity'], element.id, max])
                frame_item.set_direction('vertical')
                frame_item.set_items_pos('auto')
                frame_item.resize(920, 'auto')
                frame_item.set_padding(20,0,20,20)
                frame_item.set_bg_color((236, 240, 241))
                frame_item.make_pos()

                a.append(frame_item)

            item_list = Item_list(a, 330, 120, 1260, 120, 20, 640, 'machine')
            items_tmp.append(item_list)
            items_tmp.append(frame_head)

            window.set_body_tmp(items_tmp)
            window.display(screen)
        else:
            draw_alert(widget, window, screen, "Erreur", "Les données entrées sont invalides", clear_overbody, [])

def draw_add_machine_user(widget, window, screen, produit, quantity, machine, max, *arg):
    machine_name = get_with_id(window.machines, machine)

    items_tmp = []
    if not Machine.verifUtilisateur(window.machines, machine):

        path = 'img/icon/left_grayblu_arrow'
        button_arrow = Button_img(0, path, 0, 0, draw_choose_machine, [produit, max, quantity])

        text = 'Choisir un utilisateur à ajouter à la machine ' + machine_name.nom
        label_title = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 0, 0, None, None, [])
        label_title.set_direction('horizontal')
        label_title.set_padding(10,0,0,0)
        label_title.resize(870, 80)
        label_title.set_align('center')
        label_title.make_pos()

        frame_head = Frame(330, 40, [button_arrow, label_title], None, [])
        frame_head.set_items_pos('auto')
        frame_head.set_direction('horizontal')
        frame_head.resize('auto', 'auto')
        frame_head.set_bg_color((52,73,94))
        frame_head.make_pos()

        ind_with_no_role = []
        for ind in window.individus:
            if ind.role == None:
                ind_with_no_role.append(ind)
        a = []
        for element in ind_with_no_role:
            info = []

            info.append(create_label(element.prenom + ' ' + element.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            info.append(create_label(' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            info.append(create_label('Compétence : ' + str(element.competence_production), 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

            frame_item = Frame(0, 0, info, add_machine_user, [produit, quantity, machine, element.id, max])
            frame_item.set_direction('vertical')
            frame_item.set_items_pos('auto')
            frame_item.resize(920, 'auto')
            frame_item.set_padding(20,0,20,20)
            frame_item.set_bg_color((236, 240, 241))
            frame_item.make_pos()

            a.append(frame_item)

        item_list = Item_list(a, 330, 120, 1260, 120, 20, 640, 'employé')
        items_tmp.append(item_list)
        items_tmp.append(frame_head)

        window.set_body_tmp(items_tmp)
        window.display(screen)
    else:
        add_machine_user(widget, window, screen, produit, quantity, machine, None, max)

def add_machine_user(widget, window, screen, produit, quantity, id_machine, ind_id, max, *arg):
    if ind_id != None:
        ind = get_with_id(window.individus, ind_id)
        ind.role = 'prod'
        machine = get_with_id(window.machines, id_machine)
        machine.utilisateur = ind
    draw_summary_prod(widget, window, screen, produit, quantity, id_machine, max)

def draw_summary_prod(widget, window, screen, produit, quantity, machine_id, max, *arg):

    machine = get_with_id(window.machines, machine_id)
    product = get_with_name(window.produits, produit)
    total_mat = Machine.nbrProd_to_NbrMat(product, int(quantity))

    path = 'img/icon/left_grayblu_arrow'
    # TODO draw_choose_machine
    button_arrow = Button_img(0, path, 0, 0, do_nothing, [produit, max, quantity])

    text = 'Résumé de la commande'
    label_title = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 0, 0, None, None, [])
    label_title.set_direction('horizontal')
    label_title.set_padding(10,0,0,0)
    label_title.resize(930, 80)
    label_title.set_align('center')
    label_title.make_pos()

    # button_arrow
    frame_head = Frame(330, 40, [label_title], None, [])
    frame_head.set_items_pos('auto')
    frame_head.set_direction('horizontal')
    frame_head.resize('auto', 'auto')
    frame_head.set_bg_color((52,73,94))
    frame_head.make_pos()

    info1, info2 = [], []
    info1.append(['Produit', produit])
    info1.append(['Machine', machine.nom])
    info1.append(['Quantité', str(quantity)])
    info2.append( ['Temps de production', str(round(Commande(total_mat, window.operations, product).tps_total / Commande.capaciteUtilisateur(machine.utilisateur), 1)) + " semaine(s)"] )

    infos = [info1, info2]
    frame_labels = []
    for info in infos:
        label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 40, 30, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 385, 'auto')
        frame_tmp = Frame(0, 0, label_tmp, None, [])
        frame_tmp.set_items_pos('auto')
        frame_tmp.set_marge_items(10)
        frame_tmp.set_direction('vertical')
        frame_tmp.resize('auto', 'auto')
        frame_tmp.set_bg_color((236, 240, 241))
        frame_tmp.make_pos()
        frame_labels.append(frame_tmp)

    newt_button = create_button("Passez la commande", 'font/colvetica/colvetica.ttf', 40, (255, 255, 255), (230, 126, 34), 0, 0, 400, 60, make_prod, [produit, quantity, machine])

    label_total = create_label('Matériaux consommés :', 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, [])
    list_label = []
    for element in total_mat:
        list_label.append(create_label(str(element[1]) + 'x ' + element[0], 'calibri', 25, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))


    frame_total_mat = Frame(0, 0, list_label, None, [])
    frame_total_mat.set_direction('vertical')
    frame_total_mat.set_items_pos('auto')
    frame_total_mat.resize('auto', 'auto')
    frame_total_mat.set_marge_items(20)
    frame_total_mat.set_padding(40,0,0,0)
    frame_total_mat.set_bg_color((236, 240, 241))
    frame_total_mat.make_pos()

    frame_main = Frame(330, 120, frame_labels + [label_total, frame_total_mat, newt_button], None, [])
    frame_main.set_direction('vertical')
    frame_main.set_items_pos('auto')
    frame_main.resize('auto', 'auto')
    frame_main.set_marge_items(20)
    frame_main.set_padding(20,0,20,0)
    frame_main.set_bg_color((236, 240, 241))
    frame_main.make_pos()

    window.set_body_tmp([frame_head, frame_main])
    window.display(screen)

def make_prod(widget, window, screen, produit, quantity, machine, *arg):
    title_msg = ''
    msg = 'La production de ' + str(quantity) + ' ' + produit + ' a bien été lancée.'

    product = get_with_name(window.produits, produit)
    total_mat = Machine.nbrProd_to_NbrMat(product, int(quantity))
    Machine.genCommande(window.machines, window.operations, total_mat, machine.id, window.stocks[0], product)

    draw_prod(widget, window, screen, 0)
    draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])

def draw_magasin(widget, window, screen, *arg):
    items = []

    path = 'img/icon/left_grayblu_arrow'
    button_arrow = Button_img(0, path, 0, 0, draw_prod, [4])

    text = 'Liste des machines en vente'
    label_title = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 0, 0, None, None, [])
    label_title.set_direction('horizontal')
    label_title.set_padding(10,0,0,0)
    label_title.resize(870, 80)
    label_title.set_align('center')
    label_title.make_pos()

    frame_head = Frame(330, 40, [button_arrow, label_title], None, [])
    frame_head.set_items_pos('auto')
    frame_head.set_direction('horizontal')
    frame_head.resize('auto', 'auto')
    frame_head.set_bg_color((52,73,94))
    frame_head.make_pos()

    a = []
    for element in window.magasin:
        info = []

        info.append(create_label(element.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
        info.append(create_label('Prix : ' + str(element.prix) + '€', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        info.append(create_label('Opérations : ', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        operations_label = []
        for operation in element.operations_realisables:
            operations_label.append(create_label('- ' + operation, 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        frame_operations = Frame(0, 0, operations_label, None, [])
        frame_operations.set_direction('vertical')
        frame_operations.set_items_pos('auto')
        frame_operations.resize('auto', 'auto')
        frame_operations.set_padding(20,0,0,20)
        frame_operations.set_bg_color((236, 240, 241))
        frame_operations.make_pos()
        info.append(frame_operations)

        button_buy = create_button("Acheter", 'font/colvetica/colvetica.ttf', 25, (255, 255, 255), (230, 126, 34), 0, 0, 'auto', 'auto', buy_machine, [element.id])
        button_buy.set_padding(15,15,10,10)
        button_buy.make_pos()
        info.append(button_buy)

        frame_item = Frame(0, 0, info, None, [])
        frame_item.set_direction('vertical')
        frame_item.set_items_pos('auto')
        frame_item.resize(930, 'auto')
        frame_item.set_padding(20,0,20,20)
        frame_item.set_bg_color((236, 240, 241))
        frame_item.make_pos()

        a.append(frame_item)

    item_list = Item_list(a, 330, 120, 1260, 120, 20, 640, 'machine')
    items.append(item_list)
    items.append(frame_head)

    window.set_body_tmp(items)
    window.display(screen)

def buy_machine(widget, window, screen, machine_id):
    machine = get_with_id(window.magasin, machine_id)
    if window.argent < machine.prix:
        draw_alert(widget, window, screen, "Erreur", "Vous n'avez pas assez d'argent", clear_overbody, [])
    else:
        addMachine(window.machines, machine)
        title_msg = ''
        msg = 'La machine ' + machine.nom + ' a bien été achetée.'
        draw_prod(widget, window, screen, 4)
        draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])

def remove_machine_user(widget, window, screen, machine_id, *arg):
    machine = get_with_id(window.machines, machine_id)
    title_msg = ''
    msg = "L'employé " + machine.utilisateur.prenom + ' ' + machine.utilisateur.nom + ' a été retiré de la machine.'

    user = get_with_id(window.individus, machine.utilisateur.id)
    user.role = None
    machine.utilisateur = None

    draw_prod(widget, window, screen, 4)
    draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])

def draw_add_user_to_machine(widget, window, screen, machine_id, *arg):
    items_tmp = []
    machine = get_with_id(window.machines, machine_id)
    text = 'Choisir un utilisateur à ajouter à la machine ' + machine.nom
    label_title = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 0, 0, None, None, [])
    label_title.set_direction('horizontal')
    label_title.set_padding(20,0,0,0)
    label_title.resize(930, 80)
    label_title.set_align('center')
    label_title.make_pos()

    frame_head = Frame(330, 40, [label_title], None, [])
    frame_head.set_items_pos('auto')
    frame_head.set_direction('horizontal')
    frame_head.resize('auto', 'auto')
    frame_head.set_bg_color((52,73,94))
    frame_head.make_pos()

    ind_with_no_role = []
    for ind in window.individus:
        if ind.role == None:
            ind_with_no_role.append(ind)
    a = []
    for element in ind_with_no_role:
        info = []

        info.append(create_label(element.prenom + ' ' + element.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
        info.append(create_label(' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
        info.append(create_label('Compétence : ' + str(element.competence_production), 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

        frame_item = Frame(0, 0, info, add_user_to_machine, [element.id, machine_id])
        frame_item.set_direction('vertical')
        frame_item.set_items_pos('auto')
        frame_item.resize(920, 'auto')
        frame_item.set_padding(20,0,20,20)
        frame_item.set_bg_color((236, 240, 241))
        frame_item.make_pos()

        a.append(frame_item)

    item_list = Item_list(a, 330, 120, 1260, 120, 20, 640, 'employé')
    items_tmp.append(item_list)
    items_tmp.append(frame_head)

    window.set_body_tmp(items_tmp)
    window.display(screen)

def add_user_to_machine(widget, window, screen, ind_id, machine_id, *arg):
    machine = get_with_id(window.magasin, machine_id)
    ind = get_with_id(window.individus, ind_id)
    ind.role = 'prod'
    machine = get_with_id(window.machines, machine_id)
    machine.utilisateur = ind

    title_msg = ''
    msg = "L'employé " + machine.utilisateur.prenom + ' ' + machine.utilisateur.nom + ' a été ajouté de la machine ' + machine.nom + '.'


    draw_prod(widget, window, screen, 4)
    draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])

'''
================================================================================
FINANCE
================================================================================
'''

def draw_finance(widget, window, screen, i, *arg):
    items = []
    items_tmp = []

    button_pret = create_label("Prêt", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_finance, [0])
    button_bilan = create_label("Bilan", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_finance, [1])
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

            content_list = repartitionDepenses(window.depenses, window.listePret)

            content = []

            content.append(create_label('Revenus', 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            content.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            for element in content_list[0]:
                content.append(create_label(element[0] + ' : ' + element[1] + '€', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

            content.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            content.append(create_label('Dépenses', 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            for element in content_list[1]:
                content.append(create_label(element[0] + ' : ' + element[1] + '€', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

            # item_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            # item_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            # item_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            # item_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))


            main_frame = Frame(0, 0, content, None, [])
            main_frame.set_direction('vertical')
            main_frame.set_items_pos('auto')
            main_frame.resize(910, 'auto')
            main_frame.set_padding(50,0,50,0)
            main_frame.set_marge_items(30)
            main_frame.set_bg_color((236, 240, 241))
            main_frame.make_pos()

            item_list = Item_list([main_frame], 330, 40, 1260, 40, 20, 680, 'salut')
            item_list.bg_color = (236, 240, 241)
            items_tmp.append(item_list)
        elif i == 0.1:
            button_lst_pret = create_label("     Liste des prêts", 'calibri', 20, (255,255,255), (52, 152, 219), 0, 0, None, draw_finance, [0.1])

            prets = []

            for pret in window.listePret:
                pret_info = []

                # pret_info.append(create_label('Nom du pret', 'font/colvetica/colvetica.ttf', 50, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))

                info1, info2 = [], []
                info1.append(['Capital emprunté', str(pret.capital)+'€'])
                info1.append(['Total', str(pret.montantPret)+'€'])
                info1.append(['Début', str(pret.dateDebut.strftime('%d-%m-%Y'))])
                info2.append(['Intérêt', str(pret.tauxInteret)+'%'])
                info2.append(['Mensualité', str(pret.parMois)+'€'])
                info2.append(['Fin', str(pret.dateFin.strftime('%d-%m-%Y'))])

                infos1 = [info1]
                infos2 = [info2]
                frame_labels1, frame_labels2 = [], []
                for info in infos1:
                    label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 30, 30, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 200, 'auto')
                    frame_tmp = Frame(0, 0, label_tmp, None, [])
                    frame_tmp.set_items_pos('auto')
                    frame_tmp.set_marge_items(10)
                    frame_tmp.set_direction('vertical')
                    frame_tmp.resize(465, 'auto')
                    frame_tmp.set_bg_color((236, 240, 241))
                    frame_tmp.make_pos()
                    frame_labels1.append(frame_tmp)

                for info in infos2:
                    label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 30, 30, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 200, 'auto')
                    frame_tmp = Frame(0, 0, label_tmp, None, [])
                    frame_tmp.set_items_pos('auto')
                    frame_tmp.set_marge_items(10)
                    frame_tmp.set_direction('vertical')
                    frame_tmp.resize('auto', 'auto')
                    frame_tmp.set_bg_color((236, 240, 241))
                    frame_tmp.make_pos()
                    frame_labels2.append(frame_tmp)

                frame_tmp1 = Frame(0, 0, frame_labels1 + frame_labels2, None, [])
                frame_tmp1.set_direction('horizontal')
                frame_tmp1.set_items_pos('auto')
                frame_tmp1.resize('auto', 'auto')
                # frame_tmp1.set_align('center')
                frame_tmp1.set_marge_items(0)
                frame_tmp1.set_bg_color((236, 240, 241))
                frame_tmp1.make_pos()
                pret_info.append(frame_tmp1)


                label_avancement = create_label("Avancement :", 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
                label_avancement.resize(200, 'auto')
                label_avancement.set_items_pos('auto')
                label_avancement.make_pos()

                duree = (pret.dateFin - pret.dateDebut)/7
                ecoule = (window.temps - pret.dateDebut)/7
                value = ecoule
                value_max = duree
                pourcentage = str(int(value*100 / value_max))
                label_pourcentage = create_label(pourcentage+'%', 'calibri', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
                progress_bar = Progress_bar(0, 0, 600, 30, None, [], value, value_max, (46, 204, 113), (255, 255, 255))

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
                pret_info.append(frame_tmp2)


                frame_pret = Frame(0, 0, pret_info, None, [])
                frame_pret.set_direction('vertical')
                frame_pret.set_items_pos('auto')
                frame_pret.resize(930, 'auto')
                frame_pret.set_marge_items(20)
                frame_pret.set_padding(20,0,20,20)
                frame_pret.set_bg_color((236, 240, 241))
                frame_pret.make_pos()

                prets.append(frame_pret)

            item_list_pret = Item_list(prets, 330, 40, 1260, 40, 20, 680, 'prêt')

            items.append(item_list_pret)
        elif i == 0.2:
            button_ask_pret = create_label("     Contracter un prêt", 'calibri', 20, (255,255,255), (52, 152, 219), 0, 0, None, draw_finance, [0.2])


            if int(((window.temps - datetime.datetime(2018,1,1)).days)/7) < 4:
                variationInteret = 0
            else:
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
        button_bilan = create_label("Bilan", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_finance, [1])
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

    montant_max = montantPret(dureePretMois(type_pret.lower(), int(duree_entry)),window)

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

    button_ok = create_button("Ok", 'font/colvetica/colvetica.ttf', 40, (255, 255, 255), (230, 126, 34), 0, 0, 400, 60, create_pret, [[montant_entry, taux_interet, interet, total, totalMois, assurance, assuranceMois, dureePretMois(type_pret, int(duree_entry)), type_pret]])

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

    if entry['duree'] == '' or entry['montant'] == '':
        draw_alert(widget, window, screen, "Erreur", "Certains champs sont invalides", clear_overbody, [])
    else:
        montant_max = montantPret(dureePretMois(type_pret.lower() ,int(entry['duree'])),window)
        if duree[0] <= int(entry['duree']) <= duree[1] and 0 <= int(entry['montant']) <= montant_max:
            draw_get_pret(widget, window, screen, type_pret, taux_interet, entry['duree'], entry['montant'])
        else:
            draw_alert(widget, window, screen, "Erreur", "Les données entrées sont invalides", clear_overbody, [])

def create_pret(widget, window, screen, donnees, *arg):
    data = {
        'capital': donnees[0],
        'taux interet': donnees[1],
        'interet': donnees[2],
        'montantPret': donnees[3],
        'montantMois': donnees[4],
        'assurance': donnees[5],
        'assuranceMois': donnees[6],
        'duree': donnees[7],
        'type': donnees[8],
    }
    window.listePret.append(Pret(window.temps,data))
    draw_finance(widget, window, screen, 0.1, *arg)
    draw_alert(widget, window, screen, "Bravo! ", "Votre prêt a bien été contracté.", clear_overbody, [])



'''
================================================================================
VENTES
================================================================================
'''

def inMarket(market, stock, produits, produit_nom, quantite) :
    """
    FONCTION       : Mettre un produit sur le marché
    ENTREES        : Le marché (Stock), le stock (Stock), la liste des produits (Produit list), le nom du produit (string) et une quantité (entier)
    SORTIE         : Le marché mis à jour (Stock) et le stock mis à jour (Stock)
    """

    produit = get_with_name(produits, produit_nom)
    retire([produit_nom, quantite], stock.produits)

    if produit.marche == False :
        produit.marche = True
        market.produits.append([produit, quantite])
    else :
        ajout([produit.nom, quantite], market.produits)

    return(market, stock)

def outMarket(market, stock, produits, produit_nom) :
    """
    FONCTION       : Retirer un produit sur le marché
    ENTREES        : Le marché (Stock), le stock (Stock), la liste des produits (Produit list) et le nom du produit (string)
    SORTIE         : Le marché mis à jour (Stock)
    """

    for prod in market.produits :
        if prod[0] == produit_nom :
            stock.produits.append([prod])

    produit = get_with_name(produits, produit_nom)
    produit.marche=False
    retireAll(produit, market.produits)

    return(market)

def draw_sales(widget, window, screen, i, *arg):
    items = []
    items_tmp = []

    button_statue = create_label("Status", 'calibri', 29, (255,255,255), (189,195,198), 0, 0, None, draw_sales, [0])
    button_product = create_label("Produits", 'calibri', 29, (255,255,255), (189,195,198), 0, 0, None, draw_sales, [1])


    focus_color = (41,128,185)
    if i == 0:
        button_statue = create_label("Status", 'calibri', 29, (255,255,255), focus_color, 0, 0, None, draw_sales, [0])

        text = 'Produit en vente'
        label_stock = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 805, 40, None, None, [])
        label_stock.set_direction('horizontal')
        label_stock.set_padding(20,10,10,10)
        label_stock.resize(475, 80)
        label_stock.set_align('center')
        label_stock.make_pos()

        product_in_sale = []
        for produit in window.produits:
            if produit.marche:
                product_in_sale.append(produit)

        a = []
        for element in product_in_sale:
            info = []

            info.append(create_label(element.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            info.append(create_label('Prix : ' + str(element.prix) + '€', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            info.append(create_label('Temps passé sur le marché : ' + str(element.age) + ' semaine(s)', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

            # item_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            # item_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            # item_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
            # item_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

            frame_item = Frame(0, 0, info, None, [])
            frame_item.set_direction('vertical')
            frame_item.set_items_pos('auto')
            frame_item.resize(455, 'auto')
            frame_item.set_padding(20,0,20,20)
            frame_item.set_bg_color((236, 240, 241))
            frame_item.make_pos()

            a.append(frame_item)

        item_list = Item_list(a, 805, 120, 1260, 120, 20, 640, 'produit')
        items_tmp.append(item_list)
        items_tmp.append(label_stock)

    elif i == 1:
        button_product = create_label("Produits", 'calibri', 29, (255,255,255), focus_color, 0, 0, None, draw_sales, [1])

        products = []

        for product in window.produits:
            product_info = []

            product_info.append(create_label(product.nom, 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            product_info.append(create_label(' ', 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            if product.marche:
                text_in_sale = 'oui'
            else:
                text_in_sale = 'non'
            product_info.append(create_label('En vente : ' + text_in_sale, 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
            product_info.append(create_label('Temps passé sur le marché : ' + str(product.age) + ' semaine(s)', 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))

            frame_product = Frame(0, 0, product_info, draw_sales_product, [product.nom, 0])
            frame_product.set_direction('vertical')
            frame_product.set_items_pos('auto')
            frame_product.resize(930, 'auto')
            frame_product.set_padding(20,0,20,20)
            frame_product.set_bg_color((236, 240, 241))
            frame_product.make_pos()

            products.append(frame_product)

        item_list_product = Item_list(products, 330, 40, 1260, 40, 20, 680, 'produit')

        items.append(item_list_product)

    list_tmp = [button_statue, button_product]
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
    window.set_body_tmp(items_tmp)
    window.draw_button_info('Aide', '')
    window.display(screen)

'''INCOMPLET'''
def draw_sales_product(widget, window, screen, prod_name, i, *arg):
    # ind = get_with_id(window.individus, ind_id)
    product = get_with_name(window.produits, prod_name)

    items = []
    items_tmp = []

    path = 'img/icon/right_white_arrow'
    button_arrow = Button_img(0, path, 0, 0, None, [])
    text = 'Produit'
    name = create_label(text, 'font/colvetica/colvetica.ttf', 40, (255,255,255), (149,165,166), 0, 0, None, None, [])
    frame_back = Frame(0,0, [button_arrow, name], draw_sales, [1])
    frame_back.set_direction('horizontal')
    frame_back.set_items_pos('auto')
    frame_back.resize(250, 80)
    frame_back.set_align('center')
    frame_back.set_padding(10,0,0,0)
    frame_back.set_marge_items(10)
    frame_back.set_bg_color((149, 165, 166))
    frame_back.make_pos()

    info_market = create_label("Infos marché", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_sales_product, [prod_name, 0])

    if not product.marche:
        text_product_kill = "Mettre en vente"
        callback = draw_start_sale
        arg_tmp = [prod_name]
    else:
        text_product_kill = "Arrêter la distribution"
        f1 = ["Oui", stop_sale, [prod_name]]
        f2 = ["Non", clear_overbody, []]
        callback = draw_alert_option
        arg_tmp = ['', 'Voulez-vous vraiment arrêter de vendre ' + product.nom  + ' ?',[f1, f2]]

    make_sale = create_label(text_product_kill, 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, callback, arg_tmp)

    focus_color = (41,128,185)
    if i == 0:
        info_market = create_label("Infos marché", 'calibri', 30, (255,255,255), focus_color, 0, 0, 250, draw_sales_product, [prod_name,0])

        #Info marché
    
    elif i == 1:
        make_sale = create_label(text_product_kill, 'calibri', 30, (255,255,255), focus_color, 0, 0, 250, callback, [])

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

    window.set_body_tmp(items_tmp)
    window.set_body(items)
    window.display(screen)

def draw_start_sale(widget, window, screen, prod_name, *arg):

    items = []

    text = 'Mettre en vente '+prod_name 
    label_title = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 0, 0, None, None, [])
    label_title.set_direction('horizontal')
    label_title.set_padding(10,0,0,0)
    label_title.resize(870, 80)
    label_title.set_align('center')
    label_title.make_pos()
    items.append(label_title)

    max = maxStock(window.stock[0], prod_name)

    label = create_label('Quantité à vendre : ', 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
    label_scale = create_label('compris entre 1 et '+ str(max), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

    frame_label = Frame(0, 0, [label, label_scale], None, [])
    frame_label.set_direction('vertical')
    frame_label.set_items_pos('auto')
    frame_label.resize(300, 'auto')
    frame_label.set_marge_items(10)
    frame_label.set_padding(0,0,0,20)
    frame_label.set_bg_color((236, 240, 241))
    frame_label.make_pos()

    entry = Entry(0, 0, 200, 40, True, 'quantity', 0, None)
    entry.set_entry('1')

    frame_input = Frame(0, 0, [frame_label, entry], None, [])
    frame_input.set_direction('horizontal')
    frame_input.set_items_pos('auto')
    frame_input.resize('auto', 'auto')
    frame_input.set_marge_items(10)
    frame_input.set_bg_color((236, 240, 241))
    frame_input.make_pos()
    items.append(frame_input)

    label = create_label('Prix de vente : ', 'font/colvetica/colvetica.ttf', 40, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])
    #label_scale = create_label('compris entre 1 et '+ str(max), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, None, None, [])

    frame_label = Frame(0, 0, [label], None, [])
    frame_label.set_direction('vertical')
    frame_label.set_items_pos('auto')
    frame_label.resize(300, 'auto')
    frame_label.set_marge_items(10)
    frame_label.set_padding(0,0,0,20)
    frame_label.set_bg_color((236, 240, 241))
    frame_label.make_pos()

    entry = Entry(0, 0, 200, 40, True, 'price', 0, None)
    entry.set_entry('0')

    frame_input = Frame(0, 0, [frame_label, entry], None, [])
    frame_input.set_direction('horizontal')
    frame_input.set_items_pos('auto')
    frame_input.resize('auto', 'auto')
    frame_input.set_marge_items(10)
    frame_input.set_bg_color((236, 240, 241))
    frame_input.make_pos()
    items.append(frame_input)
    
    newt_button = create_button("Mettre en vente", 'font/colvetica/colvetica.ttf', 30, (255, 255, 255), (230, 126, 34), 0, 0, 200, 40, start_sale, [prod_name, max])
    items.append(newt_button)

    window.set_body_tmp(items)
    window.display(screen)

'''IMCOMPLET'''
def start_sale(widget, window, screen, prod_name, max, *arg):
    entry = get_entry(widget, window, screen, *arg)

    if entry['quantity'] == '' or entry['price'] == '':
        draw_alert(widget, window, screen, "Erreur", "Certains champs sont invalides", clear_overbody, [])
    else:
        if 1 <= int(entry['quantity']) <= max :
            product = get_with_name(window.produits, prod_name)
            title_msg = ''
            msg = 'Vous avez mis en vente le produit ' + product.nom

            Produit.fixePrix(window.produits, prod_name, int(entry['price']))
            window.market[0] = inMarket(window.market[0], window.stock[0], window.produits, prod_name)

            draw_sales(widget, window, screen, 1)
            draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])

        else:
            draw_alert(widget, window, screen, "Erreur", "Les données entrées sont invalides", clear_overbody, [])

'''IMCOMPLET'''
def stop_sale(widget, window, screen, prod_name, *arg):
    product = get_with_name(window.produits, prod_name)
    title_msg = ''
    msg = 'Vous avez arrêté de vendre ' + product.nom

    window.market[0] = outMarket(window.market[0], window.stock, window.produits, prod_name)

    draw_sales(widget, window, screen, 1)
    draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])



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
    f1 = ["Oui", reset_game, [False]]
    f2 = ["Non", clear_overbody, []]
    return_opening = create_button("Retourner au menu principal", 'font/colvetica/colvetica.ttf', 40, (236, 240, 241), (52,73,94), 0, 0, 500, 60, draw_alert_option, ['', 'Voulez-vous vraiment retourner au menu principal?',[f1, f2]])
    f1 = ["Oui", close_game, [False]]
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
    reset_game(widget, window, screen, True, *arg)
