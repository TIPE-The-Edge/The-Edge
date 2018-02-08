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

    preset_prod = 0

    # individus # Pour les test uniquement
    for i in range(1):
        individus.append(Individu())

    # populations
    # populations.append(Population("Les Vieux", 100, 2))
    # populations.append(Population("Les Jeunes", 2000, 99))

    # produits
    for i in range(0 + preset_prod):
        produits.append(Produit(produits, None, None, None, None))

    # opérations
    for i in range(0 + preset_prod):
        operations.append(Operation())

    # materiaux
    for i in range(0 + preset_prod):
        materiaux.append(Materiau())

    # formations #BONUS
    # for i in range(0):
    #     formations.append(Formation())

    # fournisseurs
    for i in range(0 + preset_prod):
        fournisseurs.append(Fournisseur())

    # machines
    for i in range(0 + preset_prod):
        machines.append(Machine())

    # transports
    # transports.append(Transport("Admin", "The Edge", [[materiaux[0].nom, 10], [materiaux[1].nom, 15]], []))

    # stocks
    for i in range (1):
        stocks.append(Stock())

    # candidats
    for i in range (5):
        candidats.append(Individu())

    # départs # Pour les test uniquement
    for i in range (0):
        departs.append([i, random.randint(0,10)])

    # RH
    lesRH = RH()
    #lesRH.update(individus, departs, 3, 3)

    ######## VARIABLES DE JEU ########
    temps = datetime.datetime(2018,1,1) # Temps en semaines
    month = 1

    on = 0
    while on != " ": # Boucle de jeu

        os.system('clear') # works on Linux/Mac

        ######## INIT/UPDATE/EVENTS DES OBJETS ########

        # Tri les produits par ordre alphabétique
        # produits     = enhancedSort(produits,     "nom", False)
        # individus    = enhancedSort(individus,    "id",  False)
        # operations   = enhancedSort(operations,   "nom", False)
        # materiaux    = enhancedSort(materiaux,    "nom", False)
        # formations   = enhancedSort(formations,   "nom", False)
        # populations  = enhancedSort(populations,  "nom", False)
        # fournisseurs = enhancedSort(fournisseurs, "nom", False)
        # machines     = enhancedSort(machines,     "nom", False)

        # init produits
        initProduits(populations, produits)
        initProduits(machines, produits)
        initProduits(stocks, produits)

        # init materiaux
        initMateriaux(populations, materiaux)
        initMateriaux(machines, materiaux)
        initMateriaux(stocks, materiaux)

        # Individus
        Individu.updateExpStartUp(individus)

        # Transports
        Transport.arrivees(transports, stocks)
        Transport.updateTempsTrajet(transports)

        # RH
        #lesRH.update(individus, departs, 3, 3)
        RH.updateDeparts(departs)
        if (temps.month != month): # Ajoute les couts de RH tous les mois
            month = temps.month
            RH.coutsRH(couts, lesRH)


        ######## AFFICHAGE ########

        # Temps
        print("------------------------ |{} {} {}| ------------------------\n".format(temps.day, temps.strftime("%B"), temps.year))

        # individus
        print("------ Classe : Individu ------")
        for ind in individus:
            print(ind)
        print()

        # populations
        print("------ Classe : Population ------")
        for pop in populations:
            print(pop)
        print()

        # produits
        print("------ Classe : Produit ------")
        for prod in produits:
            print(prod)
        print()

        # opérations
        print("------ Classe : Operation ------")
        for ope in operations:
            print(ope)
        print()

        # materiaux
        print("------ Classe : Materiau ------")
        for mat in materiaux:
            print(mat)
        print()

        # formations #BONUS
        # print("------ Classe : Formation ------")
        # for form in formations:
        #     print(form)
        # print()

        # fournisseurs
        print("------ Classe : Fournisseur ------")
        for four in fournisseurs:
            print(four)
        print()

        # machines
        print("------ Classe : Machine ------")
        for mach in machines:
            print(mach)
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

        # couts
        print("------ liste : Coûts ------")
        for cou in couts:
            print(cou)
        print()

        ####################
        ### espace tests ###
        ####################
        print("------------------------ ESPACE TESTS ------------------------\n")

        lesRH.update(individus, departs, 3, 3)
        print(lesRH)

        # idt = int(input("recruter ? "))
        # RH.recruter(individus, candidats, idt)
        #
        # idt = int(input("virer ? "))
        # RH.licencier(individus, departs, idt)
        #
        # candidats.append(Individu())
        #
        # mat = input("mat? ")
        # nbr = int(input("combien? "))
        # commande = [[mat, nbr]]
        # Fournisseur.approvisionnement(transports, materiaux, couts, fournisseurs[0].nom, "The Edge", commande)

        # Fin
        on = input("on? : ")

        #################################
        ### evenements de fin de tour ###
        #################################

        # variables de jeu
        temps += datetime.timedelta(weeks = 1)
