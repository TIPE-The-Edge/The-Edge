#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.4.2
# Author: Maxence BLANC
# Last modified : 12/2017
# Titre du Fichier : fonctions pour les RH
########################

# IMPORTS
import random
import os
import datetime

# IMPORTS DE FICHIERS
from outils import *
from objets import *
from RH import *

####################################################
##################| FONCTIONS |#####################
####################################################

def affichage_individu(ind):
    print("id: {} \n\ngenre: {} \nnom: {} {} \nage: {} \n\nsalaire: {} \nstatut: {} \nrole: {} \nprojet: {} \n\nexp_RetD: {} \nexp_startup: {} \n\ncompetence_groupe: {} \ncompetence_recherche: {}".format(
           ind.id, ind.genre, ind.prenom, ind.nom, ind.age, ind.salaire, ind.statut, ind.role, ind.projet, ind.exp_RetD, ind.exp_startup, ind.competence_groupe, ind.competence_recherche))

####################################################
##################| VARIABLES |#####################
####################################################

# Initialisation des listes de class
individus      = []
# produits     = []
# operations   = []
# materiaux    = []
# formations   = []
# populations  = []
# fournisseurs = []
# machines     = []
# transports   = []
# stocks       = []

# Initialisation des listes supplémentaires
candidats    = [] # Individus pouvant etre recrutés
departs      = [] # Individus quittant l'entreprise [id, nbr semaine qu'il est parti]
couts        = [] # tous les couts générés

####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :

    ######## INITIALISATION DES OBJETS ########

    # # individus # Pour les test uniquement
    # for i in range(5):
    #     individus.append(Individu())

    # candidats
    for i in range (5):
        candidats.append(Individu())

    # RH
    print(individus)
    lesRH = RH()


    ######## VARIABLES DE JEU ########
    temps = datetime.datetime(2018,1,1) # Temps en semaines
    month = 1

    argent = 0 #TODO

    on = 1
    while on != 0:

        ######## INIT/UPDATE/EVENTS DES OBJETS ########

        # Individus
        Individu.updateExpStartUp(individus)

        # RH
        lesRH.update(individus, departs, 3, 3)

        RH.updateDeparts(departs)

        if (temps.month != month): # Ajoute les couts de RH tous les mois
            month = temps.month
            argent = RH.coutsRH(couts, lesRH)

            # MaJ des candidats chaque mois
            candidats = []
            for i in range (5):
                candidats.append(Individu())


        ######## AFFICHAGE ########

        os.system('clear') # works on Linux/Mac

        # Temps
        print("------------------------ |{} {} {}| ------------------------\n".format(temps.day, temps.strftime("%B"), temps.year))

        menu = 1
        while menu != 0: # MENU PRINCIPAL

            print("argent")
            print(argent)
            print()

            menu = int(input("menu? \n  0: Continue \n  1: RH\n "))

            if menu == 1: # MENU RH
                while menu != 0:
                    os.system('clear') # works on Linux/Mac

                    # individus
                    print("------ Classe : Individu ------")
                    for ind in individus:
                        print(ind)
                    print()

                    # candidats
                    print("------ Liste : Candidats ------")
                    for cand in candidats:
                        print(cand)
                        #affichage_individu(cand)
                    print()

                    # départs
                    print("------ liste : Départs ------")
                    for dep in departs:
                        print(dep)
                    print()

                    # RH
                    print("------ Classe : RH ------\n")
                    print(lesRH)
                    print()

                    menu = int(input("menu? \n  0: Retour \n  1: Recruter\n  2: Virer\n  3: Infos Employés"))

                    if menu == 1: # RECRUTEMENT
                        while menu != 0:
                            os.system('clear') # works on Linux/Mac

                            # candidats
                            print("------ Liste : Candidats ------")
                            for cand in candidats:
                                print(cand)
                                #affichage_individu(cand)
                            print()

                            # Recrutement
                            idt = int(input("recruter qui? "))
                            RH.recruter(individus, candidats, idt)

                            lesRH.update(individus, departs, 3, 3)

                            menu = int(input("menu? \n  0: Retour \n  1: Recruter\n "))

                        menu = 1

                    elif menu == 2: # LICENCIEMENT
                        while menu != 0:
                            os.system('clear') # works on Linux/Mac

                            # individus
                            print("------ Classe : Individu ------")
                            for ind in individus:
                                print(ind)
                            print()

                            idt = int(input("virer ? "))
                            RH.licencier(individus, departs, idt)

                            lesRH.update(individus, departs, 3, 3)

                            menu = int(input("menu? \n  0: Retour \n  1: Licencier\n "))

                        menu = 2

                    elif menu == 3: # LISTE EMPLOYES

                        os.system('clear') # works on Linux/Mac

                        # individus
                        print("------ Classe : Individu ------")
                        for ind in individus:
                            print(ind)
                        print()

                        idt = int(input("employe ? "))

                        os.system('clear') # works on Linux/Mac

                        for ind in individus:
                            if ind.id == idt:
                                affichage_individu(ind)

                        input("ok?")


                menu = 1

        # Fin
        on = int(input("next week? (0/1) : "))

        #################################
        ### evenements de fin de tour ###
        #################################

        # variables de jeu
        temps += datetime.timedelta(weeks = 1)
