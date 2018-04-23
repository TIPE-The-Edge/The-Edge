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


def create_label(text, police, fontsize, msg_color, bg_color, x, y, size, action, *arg):
    if size == None:
        label =  Label(text, police, fontsize, msg_color, bg_color, x, y, action, *arg)

        frame = Frame(x, y, [label], action, *arg)

    else:
        words = text.split(' ')
        lines = []

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

def clear_body(widget, window, screen, *arg):
    window.set_body(arg[0](*arg))
    window.display(screen)

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

def draw_home(widget, window, screen, *arg):
    button_next = create_label('Tour suivant', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, None, [])
    button_next.set_padding(20,20,15,15)
    button_next.make_pos()
    button_next.set_pos(1280-10-button_next.width, 720-10-button_next.height)
    button_next.make_pos()

    window.set_body([button_next])
    window.draw_button_info('Aide', 'Salut')
    window.display(screen)

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
    ind = get_individu(window.individus, ind_id)

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
    fired = create_label("Licencier", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, None, draw_alert_option, ['', 'Voulez-vous vraiment licencier ' + ind.prenom + ' ' + ind.nom + ' ?',f1, f2])

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
        individus = window.individus
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

    list_tmp = [attribute, upgrade]
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
    entry_values = {}
    for item in window.items:
        if item.type == 'entry':
            entry_values.update({item.id: item.entry})
    return entry_values

def draw_alert(widget, window, screen, msg_type, msg, *arg):
    items = []
    try:
        widget.set_focus()
    except:
        pass

    s = pygame.Surface((1000,750))  # the size of your rect
    s.set_alpha(128)                # alpha level
    s.fill((255,255,255))           # this fills the entire surface
    screen.blit(s, (0,0))

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

def draw_alert_option(widget, window, screen, msg_type, msg, *arg):
    items = []
    try:
        widget.set_focus()
    except:
        pass

    s = pygame.Surface((1000,750))  # the size of your rect
    s.set_alpha(128)                # alpha level
    s.fill((255,255,255))           # this fills the entire surface
    screen.blit(s, (0,0))

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
    for element in arg:
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

    window.body = [frame]
    window.display(screen)

def set_name(widget, window, screen, *arg):
    entry = get_entry(widget, window, screen, *arg)
    if check_string(widget, window, screen, r"^[a-zA-Z]+", entry['user_name'], "Des caractères ne sont pas acceptés"):
        window.user_name = entry['user_name']
        create_game(widget, window, screen, *arg)

def create_game(widget, window, screen, *arg):
    window.gen_world()

    window.draw_info()
    window.draw_nav_button()
    window.draw_button_info('Aide', 'Il n\'y en a pas')
    draw_home(None, window, screen)

def reset_game(widget, window, screen, *arg):
    window.empty_window()
    window.unload_world()
    window.draw_opening()
    window.display(screen)

'''INCOMPLET'''
def load_game(widget, window, screen, *arg):
    text = 'Sauvegardes'
    label = create_label(text, 'font/colvetica/colvetica.ttf', 45, (255,255,255), (52,73,94), 64, 48 , None, None, [])
    label.set_direction('horizontal')
    label.set_padding(20,10,10,10)
    label.resize(512, 80)
    label.set_align('center')
    label.make_pos()

    a = []
    # for ind in window.candidats:
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

    button_load = create_label( 'Charger', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, None, [])
    button_load.set_direction('vertical')
    button_load.resize(514,'auto')
    button_load.set_align('center')
    button_load.make_pos()

    frame_v1 = Frame(704, 605, [button_load], None, [])
    frame_v1.set_direction('horizontal')
    frame_v1.set_items_pos('auto')
    frame_v1.resize('auto', 68)
    frame_v1.set_align('center')
    frame_v1.set_bg_color((230, 126, 34))
    frame_v1.make_pos()

    rect0 = Rectangle(0, 0, 640, 720, (44,62,80), None, None, [])
    rect1 = Rectangle(64, 0, 512, 48, (44,62,80), None, None, [])
    rect2 = Rectangle(64, 576, 512, 145, (44,62,80), None, None, [])

    window.body = [rect0, item_list_save, rect1, rect2, label, label_save, frame_right, frame_v, frame_v1]
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

def get_individu(group, ind_id):
    for ind in group:
        if ind.id == ind_id:
            return ind
    return None

def create_label_value(labels, font1, font2, size1, size2, color1, color2, color_bg1, color_bg2, width1, width):
    items = []
    for element in labels:
        label = create_label(element[0] + ' : ', font1, size1, color1, color_bg1, 0, 0, 400, None, [])
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

def draw_individu(widget, window, screen, ind_id, *arg):
    ind = get_individu(window.candidats, ind_id)

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
        label_tmp = create_label_value(info, 'font/colvetica/colvetica.ttf', 'calibri', 30, 20, (44, 62, 80), (44, 62, 80), (236, 240, 241), (236, 240, 241), 300, 520)
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

def recruit(widget, window, screen, ind_id, *arg):
    RH.recruter(window.individus, window.candidats, ind_id)
    ind = get_individu(window.individus, ind_id)
    title_msg = 'Bravo !'
    msg = 'Vous avez recruté ' + ind.prenom + ' ' + ind.nom
    draw_recruit(widget, window, screen)
    draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])

def fired_ind(widget, window, screen, ind_id, *arg):
    ind = get_individu(window.individus, ind_id)
    title_msg = ''
    msg = 'Vous avez licencié ' + ind.prenom + ' ' + ind.nom
    RH.licencier(window.individus, window.departs, ind_id)
    draw_rh(widget, window, screen)
    draw_alert(widget, window, screen, title_msg, msg, clear_overbody, [])

def get_uppest_item(items, mouse_pos):
    uppest_item = None
    for item in items:
        if item.rect.collidepoint(mouse_pos):
            if uppest_item == None:
                uppest_item = item
            elif uppest_item.level <= item.level:
                uppest_item = item

    return uppest_item

# def draw_shadow(window, screen, item):
#     rectangle = Rectangle(item.rect.x, item.rect.y, item.rect.width, item.rect.height, (0,0,0), 128, None, [])
#     window.set_overbody([rectangle])
#     window.display(screen)

'''INCOMPLET'''
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

    button_submit = create_label('Ajouter le projet', 'font/colvetica/colvetica.ttf', 30, (255,255,255), (230, 126, 34), 0, 0, None, None, [])
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
    window.display(screen)

'''INCOMPLET'''
def draw_sales(widget, window, screen, *arg):
    pass

'''INCOMPLET'''
def draw_sales_product(widget, window, screen, prod_id, i, *arg):
    # ind = get_individu(window.individus, ind_id)

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

def draw_finance(widget, window, screen, i, *arg):
    items = []

    button_pret = create_label("Prêt", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_finance, [0])
    button_bilan = create_label("Produit", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_finance, [1])
    button_compte = create_label("Compte de résultat", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_finance, [2])
    button_macro = create_label("Macroéconomie", 'calibri', 30, (255,255,255), (189,195,198), 0, 0, 250, draw_finance, [3])

    lst_button_pret = [button_pret]

    focus_color = (41,128,185)

    if 0 <= i < 1:
        button_pret = create_label("Prêt", 'calibri', 30, (255,255,255), focus_color, 0, 0, None, draw_finance, [0])
        lst_button_pret = [button_pret]

        button_resume_pret = create_label("Résumé", 'calibri', 25, (255,255,255), (127, 140, 141), 0, 0, None, draw_finance, [0])
        button_lst_pret = create_label("Liste des prêts", 'calibri', 25, (255,255,255), (127, 140, 141), 0, 0, None, draw_finance, [0.1])
        button_ask_pret = create_label("Contracter un prêt", 'calibri', 25, (255,255,255), (127, 140, 141), 0, 0, None, draw_finance, [0.2])

        if i == 0:
            button_resume_pret = create_label("Résumé", 'calibri', 25, (255,255,255), (149, 165, 166), 0, 0, None, draw_finance, [0])
        elif i == 0.1:
            button_lst_pret = create_label("Liste des prêts", 'calibri', 25, (255,255,255), (149, 165, 166), 0, 0, None, draw_finance, [0.1])
        elif i == 0.2:
            button_ask_pret = create_label("Contracter un prêt", 'calibri', 25, (255,255,255), (149, 165, 166), 0, 0, None, draw_finance, [0.2])

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
