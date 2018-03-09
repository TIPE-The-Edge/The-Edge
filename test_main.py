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
from production import *

####################################################
##################| FONCTIONS |#####################
####################################################

def affichage_individu(ind):
    print("id: {} \n\ngenre: {} \nnom: {} {} \nage: {} \n\nsalaire: {} \nbonheur: {} \nstatut: {} \nrole: {} \nprojet: {} \n\nexp_RetD: {} \nexp_startup: {} \n\ncompetence_groupe: {} \ncompetence_recherche: {}".format(
           ind.id, ind.genre, ind.prenom, ind.nom, ind.age, ind.salaire, ind.bonheur, ind.statut, ind.role, ind.projet, ind.exp_RetD, ind.exp_startup, ind.competence_groupe, ind.competence_recherche))

####################################################
##################| VARIABLES |#####################
####################################################

# Initialisation des listes de class
individus    = []
produits     = []
operations   = []
materiaux    = []
formations   = []
populations  = []
fournisseurs = []
machines     = []
transports   = []
stocks       = []

# Initialisation des listes supplémentaires
candidats    = [] # Individus pouvant etre recrutés
departs      = [] # Individus quittant l'entreprise [id, nbr semaine qu'il est parti]
couts        = [] # tous les couts générés

####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :

    ######## INITIALISATION DES OBJETS ########

    preset_prod = 2
    preset_fab = 0
    preset_rh = 3

    # individus # Pour les test uniquement
    for i in range(preset_rh):
        individus.append(Individu())

    # populations
    # populations.append(Population("Les Vieux", 100, 2))
    # populations.append(Population("Les Jeunes", 2000, 99))

    # produits
    for i in range(0):
        produits.append(Produit(produits, None, None, None, None))

    # opérations
    for i in range(0 + preset_prod + preset_fab):
        operations.append(Operation())

    # materiaux
    for i in range(0 + preset_prod + preset_fab):
        materiaux.append(Materiau())

    # formations #BONUS
    # for i in range(0):
    #     formations.append(Formation())

    # fournisseurs
    for i in range(0 + preset_prod):
        fournisseurs.append(Fournisseur())

    # machines
    for i in range(0 + preset_prod + preset_fab):
        machines.append(Machine())

    # commandes # Pour les test uniquement
    # commandes.append(Commande([[materiaux[0], 10], [materiaux[1], 5]], operations, produits[0]))

    # transports # Pour les test uniquement
    # transports.append(Transport("Admin", "The Edge", [[materiaux[0].nom, 10], [materiaux[1].nom, 15]], []))

    # stocks
    for i in range (1):
        stocks.append(Stock())

    # candidats
    for i in range (preset_rh):
        candidats.append(Individu())

    # départs # Pour les test uniquement
    for i in range (0):
        departs.append([i, random.randint(0,10)])

    # RH
    lesRH = RH()
    lesRH.update(individus, departs, 3, 3)


    # Créations d'objets supplémentaires # Pour les test uniquement
        # Tests sur le fonctionnement des Commandes et Machines.
            # Produits
    produits.append(Produit(produits, None, [[materiaux[0].nom, 2], [materiaux[1].nom, 1]], [[operations[0].nom, 1], [operations[1].nom, 1]], None))
    produits.append(Produit(produits, None, [[materiaux[0].nom, 3], [materiaux[1].nom, 5]], [[operations[0].nom, 7]], None))
            # Commandes
    # machines[0].commandes.append(Commande([[materiaux[0].nom, 10000], [materiaux[1].nom, 5000]], operations, produits[0]))
    # machines[0].commandes.append(Commande([[materiaux[1].nom, 5000], [materiaux[0].nom, 3000]], operations, produits[1]))
    #
    # machines[1].commandes.append(Commande([[materiaux[1].nom, 10000], [materiaux[0].nom, 6000]], operations, produits[1]))
    # machines[1].commandes.append(Commande([[materiaux[1].nom, 6000], [materiaux[0].nom, 12000]], operations, produits[0]))
            # Machines
    machines[0].operations_realisables = [ope[0] for ope in produits[0].operations]


    ######## VARIABLES DE JEU ########
    temps = datetime.datetime(2018,1,1) # Temps en semaines
    month = 1

    # init produits
    initProduits(populations, produits)
    initProduits(machines, produits)
    initProduits(stocks, produits)

    # init materiaux
    initMateriaux(populations, materiaux)
    initMateriaux(machines, materiaux)
    initMateriaux(stocks, materiaux)

    # Pour les tests
    stocks[0].materiaux[0][1] = 20000
    stocks[0].materiaux[1][1] = 20000

    on = 1
    while on != 0:

        ######## INIT/UPDATE/EVENTS DES OBJETS ########

        # Individus
        Individu.updateExpStartUp(individus)

        # Transports
        Transport.updateTempsTrajet(transports)
        Transport.arrivees(transports, stocks)

        # Commandes
        Commande.updateCommandes(machines, stocks[0]) # test commandes

        # RH
        lesRH.update(individus, departs, 3, 3)
        RH.updateDeparts(departs)
        if (temps.month != month): # Ajoute les couts de RH tous les mois
            month = temps.month
            RH.coutsRH(couts, lesRH)

        ######## AFFICHAGE ########

        os.system('clear') # works on Linux/Mac

        # Temps
        print("------------------------ |{} {} {}| ------------------------\n".format(temps.day, temps.strftime("%B"), temps.year))

        menu = 1
        while menu != 0: # MENU PRINCIPAL
            menu = int(input("menu? \n  0: Continue \n  1: RH\n  2: Production\n  3: TBD\n  4: TBD\n "))

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

            elif menu == 2: # MENU PRODUCTION
                while menu != 0:
                    os.system('clear') # works on Linux/Mac

                    # commandes
                    print("------ Classe : Commande ------")
                    for mac in machines:
                        if len(mac.commandes) > 0:
                            print("+ " + mac.nom)
                            for com in mac.commandes:
                                print(com)
                    print()

                    # transports
                    print("------ Classe : Transport ------")
                    for trans in transports:
                        print(trans)
                    print()

                    # stocks
                    print("------ Classe : Stock ------")
                    for stock in stocks:
                        print(stock)
                    print()

                    menu = int(input("menu? \n  0: Retour \n  1: Approvisionnement\n  2: Production\n "))

                    if menu == 1: # Approvisionnement
                        while menu != 0:
                            os.system('clear') # works on Linux/Mac

                            # materiaux
                            print("------ Classe : Materiau ------")
                            for mat in materiaux:
                                print(mat)
                            print()

                            # fournisseurs
                            print("------ Classe : Fournisseur ------")
                            for four in fournisseurs:
                                print(four)
                            print()

                            # stocks
                            print("------ Classe : Stock ------")
                            for stock in stocks:
                                print(stock)
                            print()

                            mat = input("mat? ")
                            nbr = int(input("combien? "))
                            four = input("fournisseur? ")
                            commande = [[mat, nbr]]
                            Fournisseur.approvisionnement(transports, materiaux, couts, four, "The Edge", commande)

                            menu = int(input("menu? \n  0: Retour \n  1: Acheter\n "))

                        menu = 1

                    elif menu == 2: # Production
                        while menu != 0:
                            os.system('clear') # works on Linux/Mac

                            # produits
                            print("------ Classe : Produit ------")
                            for prod in produits:
                                print(prod)
                            print()

                            # machines
                            print("------ Classe : Machine ------")
                            for mach in machines:
                                print(mach)
                            print()

                            # stocks
                            print("------ Classe : Stock ------")
                            for stock in stocks:
                                print(stock)
                            print()


                            mat1 = int(input("nbr mat1? "))
                            mat2 = int(input("nbr mat2? "))
                            mat_ajustes = Machine.ajusteCommande(machines, machines[0].nom, stocks[0], produits[0], [[materiaux[0].nom, mat1], [materiaux[1].nom, mat2]])
                            print(mat_ajustes)
                            input("ok? ")
                            Machine.genCommande(machines, machines[0].nom, stocks[0], mat_ajustes, operations, produits[0])

                            menu = int(input("menu? \n  0: Retour \n  1: Produire\n "))

                        menu = 2

                menu = 2

            elif menu == 3: # MENU
                while menu != 0:
                    pass

                menu = 3

            elif menu == 4: # MENU
                while menu != 0:
                    pass

                menu = 4



        # Fin
        on = int(input("next week? (0/1) : "))

        #################################
        ### evenements de fin de tour ###
        #################################

        # variables de jeu
        temps += datetime.timedelta(weeks = 1)
