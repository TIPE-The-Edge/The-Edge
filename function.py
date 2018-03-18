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
from world.function import *
from world.objets import *
from world.outils import *


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

def clear_body(widget, window, screen, *arg):
    window.set_body(arg[0](*arg))
    window.display(screen)

def change_tab(button, window, screen, *arg):
    for icon in window.nav:
        if icon.num == button.num:
            icon.set_focus()

            if icon.num == 0:
                window.set_body([])
            elif icon.num == 1:
                draw_rh(None, window, screen)
            elif icon.num == 2:
                draw_rd(None, window, screen, 0)
            elif icon.num == 3:
                window.set_body([])
            elif icon.num == 4:
                window.set_body([])
            elif icon.num == 5:
                window.set_body([])
            elif icon.num == 6:
                draw_option(None, window, screen)
        else:
            icon.remove_focus()

    window.display(screen)

def draw_rh(widget, window, screen, *arg):
    rh = window.lesRH
    labels = []
    labels.append(create_label( 'Nombre d\'employé : '+str(rh.nbr_employes), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'Bonheur moyen : '+str(rh.bonheur_moy), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'Âge moyen : '+str(rh.age_moy), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( ' ', 'font/colvetica/colvetica.ttf', 10, (255,255,255), (189,195,198), 0, 0, None, None, []))

    labels.append(create_label( 'Expérience moyenne de la start-up : '+str(rh.exp_start_up_moy), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'what : '+str(rh.exp_RetD_moy), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( ' ', 'font/colvetica/colvetica.ttf', 10, (255,255,255), (189,195,198), 0, 0, None, None, []))

    labels.append(create_label( 'what : '+str(rh.nbr_arrivees), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'Taux d\'arrivées : '+str(rh.taux_arrivees), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'what : '+str(rh.nbr_departs), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'Taux de départ : '+str(rh.taux_departs), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'what : '+str(rh.taux_rotation), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( ' ', 'font/colvetica/colvetica.ttf', 10, (255,255,255), (189,195,198), 0, 0, None, None, []))

    labels.append(create_label( 'Coût de formations : '+str(rh.cout_formations), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'Moyenne formations : '+str(rh.moy_formations), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( ' ', 'font/colvetica/colvetica.ttf', 10, (255,255,255), (189,195,198), 0, 0, None, None, []))

    labels.append(create_label( 'Salaire moyen : '+str(rh.salaire_moy), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'what : '+str(rh.masse_sal_brute), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'what : '+str(rh.masse_sal_nette), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'Coût d\'emploi : '+str(rh.cout_emploi), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'Coût moyen d\'emploi : '+str(rh.cout_moy_emploi), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))
    labels.append(create_label( 'what : '+str(rh.part_masse_sal), 'font/colvetica/colvetica.ttf', 25, (255,255,255), (189,195,198), 0, 0, None, None, []))

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

    frame_left = Frame(80, 40, labels + [frame_v], None, [])
    frame_left.set_direction('vertical')
    frame_left.set_items_pos('auto')
    frame_left.resize(600, 680)
    frame_left.set_padding(20,20,20,20)
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
    # project = create_label("Rejoindre un projet", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee, [id_,3])
    fired = create_label("Licencier", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_employee, [id_,3])

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
    # elif i == 3:
    #     project = create_label("Rejoindre un projet", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [id_, 3])
    #     projects = []
    #     item_list_project = Item_list(projects, 330, 40, 1260, 40, 20, 680, 'projet')
    #     items.append(item_list_project)
    elif i == 3:
        fired = create_label("Licencier", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_employee, [id_,3])


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

        button_add_project = Frame(330, 40, [label_add_project, icon_sum], draw_alert, ['Erreur', 'salut, je ne marche pas donc arrête de me cliquer dessus', clear_overbody, []])
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

    window.set_body(items)
    window.display(screen)

def draw_option(widget, window, screen, *arg):
    button_quit = create_label("RETOURNER AU MENU PRINCIPAL", 'font/colvetica/colvetica.ttf', 40, (255,255,255), (255,0,0), 0, 0, None, reset_game, [])
    button_quit.set_direction('horizontal')
    button_quit.set_padding(50,50,20,20)
    button_quit.make_pos()

    frame = Frame(80, 40, [button_quit], None, [])
    frame.set_direction('vertical')
    frame.set_items_pos('auto')
    frame.resize(1200, 680)
    frame.set_align('center')
    frame.set_marge_items(0)
    frame.set_padding(0,0,280,0)
    frame.set_bg_color((236,240,241))
    frame.make_pos()

    window.set_body([frame])
    window.display(screen)

def quit(widget, window, screen, *arg):
    window.quit()

def get_entry(widget, window, screen, *arg):
    entry_values = []
    for item in window.body:
        if item.type == 'entry':
            if item.char_min <= len(item.entry) <= item.char_max:
                entry_values.append([item.id, item.entry])

def draw_alert(widget, window, screen, msg_type, msg, *arg):
    try:
        widget.set_focus()
    except:
        pass

    s = pygame.Surface((1000,750))  # the size of your rect
    s.set_alpha(128)                # alpha level
    s.fill((255,255,255))           # this fills the entire surface
    screen.blit(s, (0,0))

    label_type = create_label(msg_type, 'font/colvetica/colvetica.ttf', 50, (44, 62, 80), (236,240,241), 0, 0, 1280//3, None, [])
    label_type.set_align('center')
    label_type.make_pos()

    label_msg = create_label(msg, 'font/colvetica/colvetica.ttf', 30, (52, 73, 95), (236,240,241), 0, 0, 1280//3, None, [])
    label_msg.set_align('center')
    label_msg.make_pos()

    button_close = create_label("Fermer", 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230,126,34), 0, 0, None, clear_overbody, [])
    button_close.set_direction('horizontal')
    button_close.set_padding(30,30,10,10)
    button_close.make_pos()

    frame = Frame(0, 0, [label_type, label_msg, button_close], None, [])
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

def create_game(widget, window, screen, *arg):
    window.gen_world()
    window.set_body([])
    window.draw_info()
    window.draw_nav_button()
    window.draw_button_info('Aide', 'Il n\'y en a pas')

    window.display(screen)

def reset_game(widget, window, screen, *arg):
    window.empty_window()
    window.unload_world()
    window.draw_opening()
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
    window.draw_button_info('Aide', 'Informe toi sur les ressources humaines et intéragis avec les employées !')
    window.display(screen)

def get_individu(group, ind_id):
    for ind in group:
        if ind.id == ind_id:
            return ind
    return None

def draw_individu(widget, window, screen, ind_id, *arg):
    ind = get_individu(window.candidats, ind_id)

    employee_info = []
    employee_info.append(create_label(ind.prenom + ' ' +  ind.nom, 'font/colvetica/colvetica.ttf', 30, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
    employee_info.append(create_label( ' ', 'calibri', 10, (44, 62, 80), (236, 240, 241), 0, 0, None, None, []))
    employee_info.append(create_label('âge : ' + str(ind.age), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))
    employee_info.append(create_label('expérience : ' + str(ind.exp_RetD), 'calibri', 20, (44, 62, 80), (236, 240, 241), 0, 0, 1260-680, None, []))

    button_hired = create_label('Recruter', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 700, 650, None, recruit, [ind_id])
    button_hired.set_padding(20,20,15,15)
    button_hired.set_direction('vertical')
    button_hired.resize("auto","auto")
    button_hired.set_align('center')
    button_hired.make_pos()

    # frame_v = Frame(0, 0, [button_hired], None, [])
    # frame_v.set_direction('vertical')
    # frame_v.set_items_pos('auto')
    # frame_v.resize(600, 'auto')
    # frame_v.set_align('center')
    # frame_v.set_padding(0,0,20,0)
    # frame_v.set_bg_color((236, 240, 241))
    # frame_v.make_pos()

    frame_employee = Frame(680, 120, employee_info, None, [])
    frame_employee.set_direction('vertical')
    frame_employee.set_items_pos('auto')
    frame_employee.resize(600, 600)
    frame_employee.set_padding(20,0,20,20)
    frame_employee.set_bg_color((236, 240, 241))
    frame_employee.make_pos()

    window.set_body_tmp([frame_employee, button_hired])
    window.display(screen)

def recruit(widget, window, screen, ind_id, *arg):
    RH.recruter(window.individus, window.candidats, ind_id)
    ind = get_individu(window.individus, ind_id)
    title_msg = 'Bravo !'
    msg = 'Vous avez recruté ' + ind.prenom + ' ' + ind.nom
    draw_recruit(widget, window, screen)
    draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])
