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
    print("id: {} \n\ngenre: {} \nnom: {} {} \nage: {} \n\nsalaire: {} \nstatut: {} \nrole: {} \nprojet: {} \n\nexp_RetD: {} \nexp_startup: {} \n\ncompetence_groupe: {} \ncompetence_recherche: {}".format(
           ind.id, ind.genre, ind.prenom, ind.nom, ind.age, ind.salaire, ind.statut, ind.role, ind.projet, ind.exp_RetD, ind.exp_startup, ind.competence_groupe, ind.competence_recherche))

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

    # produits
    for i in range(0):
        produits.append(Produit(produits, None, None, None, None))

    # opérations
    for i in range(0 + preset_prod + preset_fab):
        operations.append(Operation())

    # materiaux
    for i in range(29):
        materiaux.append(Materiau())

    # fournisseurs
    for i in range(6):
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
    argent = 10000 #TODO

    # stocks[0].materiaux[0][1] = 20000
    # stocks[0].materiaux[1][1] = 20000

    on = "1"
    while on != "0":

        ######## INIT/UPDATE/EVENTS DES OBJETS ########

        # Transports
        Transport.updateTempsTrajet(transports)
        Transport.arrivees(transports, stocks)

        # Commandes
        Commande.updateCommandes(machines, stocks[0]) # test commandes


        ######## AFFICHAGE ########

        os.system('clear') # works on Linux/Mac

        # Temps
        print("------------------------ |{} {} {}| ------------------------\n".format(temps.day, temps.strftime("%B"), temps.year))

        menu = 1
        while menu != 0: # MENU PRINCIPAL

            # commandes
            print("------ Commande en cours ------")
            for mac in machines:
                if len(mac.commandes) > 0:
                    print("+ " + mac.nom)
                    for com in mac.commandes:
                        print(com)
            print()

            # transports
            print("------ Transports en cours ------")
            for trans in transports:
                print(trans)
            print()

            # stocks
            print("------ Etat des Stocks ------")
            for stock in stocks:
                print(stock)
            print()

            # couts générés
            print("------ couts ------(dev)")
            print(couts)

            # argent
            print("------ argent ------")
            print(argent)

            menu = int(input("menu? \n  0: Next \n  1: Approvisionnement\n  2: Production\n "))

            if menu == 1: # Approvisionnement
                while menu != 0:
                    os.system('clear') # works on Linux/Mac

                    # materiaux
                    print("------ Classe : Materiau ------ (dev)") # (dev) = pour le programme console uniquement
                                                                   # L'interface graphique aura une liste déroulante à la place.
                    for mater in materiaux:
                        print(mater)
                    print()

                    # stocks
                    print("------ Classe : Stock ------ (dev)")
                    for stock in stocks:
                        print(stock)
                    print()

                    # argent
                    print("------ argent ------")
                    print(argent)

                    mat = input("materiau? ")

                    liste_fournisseurs = Fournisseur.checkMat(fournisseurs, mat)

                    os.system('clear') # works on Linux/Mac

                    # fournisseurs
                    print("------ Fournisseurs de "+ mat +" ------")
                    for fourn in liste_fournisseurs:
                        print(fourn)
                    print()

                    four = input("fournisseur? ")

                    for fou in fournisseurs:
                        if fou.nom == four:
                            four = fou

                    cout_u     = Fournisseur.coutMateriau(four, mat)
                    print("cout/unité de " + mat + " = " + str(cout_u))

                    nbr = int(input("combien? "))

                    commande = [[mat, nbr]]

                    desti = stocks[0] # The Edge


                    print("cout/unité de " + mat + " = " + str(cout_u))

                    cout_mat   = Fournisseur.coutMateriaux(four, commande)
                    print("cout total mat = " + str(cout_mat))
                    print()

                    cout_trans = Fournisseur.coutTransport(four, desti)
                    tps_trans  = Fournisseur.tpsTransport(four, desti)
                    print("cout transport = " + str(cout_trans))
                    print("tps transport = " + str(tps_trans))
                    print()

                    cout_tot   = cout_mat + cout_trans
                    print("cout total = " + str(cout_tot))
                    print()

                    ok_commande = input("ok/...") #TODO (Dorian Bouton grisé
                                                  # tant qu'un champs est vide)

                    if ok_commande == "ok" and Fournisseur.verifCommande(four, desti, commande, argent):
                        argent = Fournisseur.approvisionnement(transports, couts, four, desti, commande, argent)
                        four     = ""
                        commande = ""
                        mat      = ""
                        menu     = 0

                    else:
                        menu = 1

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

                    prod = input("produit? "    )


                    mat1 = int(input("nbr mat1? "))
                    mat2 = int(input("nbr mat2? "))
                    mat_ajustes = Machine.ajusteCommande(machines, machines[0].nom, stocks[0], produits[0], [[materiaux[0].nom, mat1], [materiaux[1].nom, mat2]])
                    print(mat_ajustes)
                    input("ok? ")
                    Machine.genCommande(machines, machines[0].nom, stocks[0], mat_ajustes, operations, produits[0])

                    menu = int(input("menu? \n  0: Retour \n  1: Produire\n "))

                menu = 2

        on = input("quit?")

        #################################
        ### evenements de fin de tour ###
        #################################

        # variables de jeu
        temps += datetime.timedelta(weeks = 1)
