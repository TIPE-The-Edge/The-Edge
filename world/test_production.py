#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.4.2
# Author: Maxence BLANC
# Last modified : 06/2018
# Titre du Fichier : programme test pour la partie production
########################

# IMPORTS
import random
import os
import datetime

# IMPORTS DE FICHIERS
from outils import *
from objets import *
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

    # # produits
    # for i in range(0):
    #     produits.append(Produit(produits, None, None, None, None))

    # individus
    for i in range(3):
        individus.append(Individu())

    # opérations
    for i in range(0 + preset_prod):
        operations.append(Operation())

    # materiaux
    for i in range(29):
        materiaux.append(Materiau())

    # fournisseurs
    for i in range(6):
        fournisseurs.append(Fournisseur())

    # Pour les test uniquement
    produits.append(Produit(produits, None, [[materiaux[0].nom, 2], [materiaux[1].nom, 1]], [[operations[0].nom, 1], [operations[1].nom, 1]], None))
    produits.append(Produit(produits, None, [[materiaux[0].nom, 3], [materiaux[1].nom, 5], [materiaux[2].nom, 2]], [[operations[0].nom, 7]], None))

    # machines
    for i in range(2):
        machines.append(Machine([ope[0] for ope in produits[i].operations]))

    # commandes # Pour les test uniquement
    # commandes.append(Commande([[materiaux[0], 10], [materiaux[1], 5]], operations, produits[0]))

    # transports # Pour les test uniquement
    # transports.append(Transport("Admin", "The Edge", [[materiaux[0].nom, 10], [materiaux[1].nom, 15]], []))

    # stocks
    for i in range (1):
        stocks.append(Stock())


    # Créations d'objets supplémentaires # Pour les test uniquement
        # Tests sur le fonctionnement des Commandes et Machines.
            # Machines




    ######## VARIABLES DE JEU ########
    temps = datetime.datetime(2018,1,1) # Temps en semaines
    month = 1

    # init produits
    initProduits(populations, produits)
    #initProduits(machines, produits) # Pas utile?
    initProduits(stocks, produits)

    # init materiaux
    initMateriaux(populations, materiaux)
    initMateriaux(machines, materiaux)
    initMateriaux(stocks, materiaux)

    # Pour les tests
    argent = 40000
    # stocks[0].materiaux[0][1] = 20000
    # stocks[0].materiaux[1][1] = 20000
    ajout([[materiaux[0].nom, 100000], [materiaux[1].nom, 100000], [materiaux[2].nom, 100000]], stocks[0].materiaux)

    on = "1"
    while on != "0":

        ######## INIT/UPDATE/EVENTS DES OBJETS ########

        # Transports
        Transport.updateTempsTrajet(transports)
        transports = Transport.arrivees(transports, stocks)

        # Commandes
        Commande.updateCommandes(machines, individus, stocks[0])


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

                    liste_fournisseurs = Fournisseur.listeFour(fournisseurs, mat)

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

                    cout_u      = Fournisseur.coutMateriau(four, mat)

                    max_produit = int(argent/cout_u)
                    print("cout/unité de " + mat + " = " + str(cout_u))

                    nbr = int(input("combien? (0-" + str(max_produit) + ")"))

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

                    bool = (argent >= cout_tot)
                    if ok_commande == "ok" and bool:
                        argent = Fournisseur.approvisionnement(transports, couts, four, desti, commande, argent)
                        four     = ""
                        commande = ""
                        mat      = ""
                        menu     = 0

                    elif not bool:
                        print("pas assez d'argent") #TODO (Dorian, pop-up error)

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

                    # Produit à fabriquer
                    prod = input("produit? ")

                    # Transforme le nom du produit en l'objet concerné
                    for prods in produits:
                        if prods.nom == prod:
                            prod = prods


                    os.system('clear') # works on Linux/Mac

                    # Sélection des materiaux correspondants présents dans le stock
                    liste_mat_stock = listeMat(stocks[0], prod)
                    print("Materiaux dispos : ")
                    print(liste_mat_stock)
                    print()

                    # Affichage de la composition du produit
                    print("Composition du produit :")
                    print(prod.materiaux)
                    print()

                    # Nombre de max que tu peux produire
                    max_prod = Machine.maxMat(stocks[0], prod.materiaux)

                    nbr_prod = int(input("nbr de " + prod.nom + "? (0-" + str(max_prod) + ")"))

                    # La liste des nombres de materiaux respectifs pour
                    # la quantité de produits voulue.
                    liste_mats = Machine.nbrProd_to_NbrMat(prod, nbr_prod)
                    print("ce que vous demandez")
                    print(liste_mats)
                    print()

                    mats_ajustes = Machine.ajusteCommande(stocks[0], prod, liste_mats)
                    print("Apres ajustement")
                    print(mats_ajustes)
                    print()

                    # Affiche le nbr de produit que ça fera
                    prod_totaux = prodTotaux(prod, mats_ajustes)
                    print(str(prod_totaux) + " " + str(prod.nom) + " au total")



                    os.system('clear') # works on Linux/Mac

                    # Recherche des machines adéquates
                    liste_machines = Machine.listeMach(machines, prod)
                    print("Machines dispos : ")
                    print(liste_machines)
                    print()

                    id_mach = int(input("id machine? "))



                    if not Machine.verifUtilisateur(machines, id_mach):

                        print("Personnel disponible")
                        for ind in individus:
                            if ind.role == None:
                                print(ind)

                        id_ind = int(input("la machine n'a pas d'utilisateur, veuillez en choisir un : "))

                        for ind in individus:
                            if ind.id == id_ind:

                                # Change le role de l'utilisateur
                                ind.role = "prod"

                                # L'ajoute à la bonne machine
                                for mac in machines:
                                    if mac.id == id_mach:
                                        mac.utilisateur = ind
                                        obj_mach = mac

                    print()
                    print("temps de prod : " + str(round(Commande(mats_ajustes, operations, prod).tps_total / Commande.capaciteUtilisateur(obj_mach.utilisateur), 1)) + " semaines")

                    ok_commande = input("ok/...") #TODO (Dorian Bouton grisé
                                                  # tant qu'un champs est vide)

                    if ok_commande == "ok" and Machine.verifUtilisateur(machines, id_mach):
                        Machine.genCommande(machines, operations, mats_ajustes, id_mach, stocks[0], prod)
                        menu = 0

                    else:
                        menu = 1


                menu = 2

        on = input("quit?")

        #################################
        ### evenements de fin de tour ###
        #################################

        # variables de jeu
        temps += datetime.timedelta(weeks = 1)
