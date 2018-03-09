#! /usr/bin/env python
#-*- coding: utf-8 -*-


####################################
#>>> AUTEUR  : LAFAGE Adrien
#>>> SUJET   : VENTES
#>>> DATE    : 09/03/2018
####################################


############| IMPORTS |#############
import os
import sys
import unittest
from math import *

from objets import *
from outils import *
from lecture import *
####################################


##########| DESCRIPTION |###########
"""
Fichier rassemblant les différentes
fonctions permettant de modéliser la
vente d'un produit.

I/ Choix du distributeur :

    - Imposé comme le type de contrat.
      (contrat de distribution exclusif)

L'objectif est de créer une fonction
que l'on appelera à chaque tour pour
effectuer les ventes d'un produit.

Jeunes :

tps_adoption = (15, 5)

Actifs :
tps_adoption = (25, 10)
(le produit dure un an)

Seniors :

tps_adoption = (35, 5)

"""
####################################


#############| NOTES |##############
"""
Actuellement le nombre d'acheteurs est
déterminé par l'utilité qui représente
le pourcentage de la population qui est
prête à acheter le produit.
>>> le nombre d'acheteurs par mois est trop
    élevé.
    (Sol° : retirer les personnes n'ayant
    pas d'accès à internet.)
    En effet seuls 85% de la population à
    accès à internet en 2017.

____________________________________

2,5% du budget d'un ménage est consacré à
l'information et à la communication.
On déduit de ce budget 30€ qui représente
les frais moyens d'une connexion internet.


FAIRE LES COMMENTAIRES DES FONCTIONS

"""
####################################

####################################


####################################
###########| FONCTIONS |############
####################################

def budget(revenus, periode) :
    """
    FONCTION       :
    ENTREES        :
    SORTIE         :
    REMARQUES      :
    TEST UNITAIRE  : ("OK"/"...")
    """
    # Liste des revenus
    rep = []

    # Pourcentage de ménage ayant accès à internet
    acces = (5.4*int(periode)-10765.9)/100

    # Frais d'internet
    internet = 30

    for r in range(len(revenus[0])) :

        if r > int(len(revenus[0])*acces) :
            rep.append((float(revenus[0][r])*(5/2400))-internet)
        else :
            rep.append(float(revenus[0][r])*(5/2400))

    return(rep)


#>>> Création des différentes populations de consommateurs

def consommateurs(periode) :
    """
    FONCTION       : Crée la liste des consommateurs pour une période
                     donnée.
    ENTREES        : Une période (string)
    SORTIE         : Une liste de consommateurs
    REMARQUES      : Possibilité d'augmenter le nombre de types
                     de consommateurs.
    TEST UNITAIRE  : ("OK"/"...")
    """
    #>>> Initialisation des variables locales <<<#

    # Liste des différents types de consommateurs
    rep = []

    # Budget moyens des 3 types de population
    revenus = budget(readLineCSV("revenus.csv", "periode", periode, ["jeunes", "actifs", "seniors"]), periode)

    # Nombre de ménage par type de population
    demo = []
    demographie = readLineCSV("demographie.csv", "periode", periode, ["jeunes", "actifs", "seniors"])
    for d in demographie[0] :
        demo.append(float(d))
    demographie = demo

    # Budget des jeunes
    jeunes = np.random.normal(loc=revenus[0], scale=20, size=100)
    jeunes = np.array(jeunes, int)
    # print("Budget max jeunes : ", max(jeunes))

    # Budget des actifs
    actifs = np.random.normal(loc=revenus[1], scale=30, size=100)
    actifs = np.array(actifs, int)
    # print("Budget max actifs : ", max(actifs))

    # Budget des seniors
    seniors = np.random.normal(loc=revenus[2], scale=30, size=100)
    seniors = np.array(seniors, int)
    # print("Budget max Seniors : ", max(seniors))

    #>>> Corps de la fonction <<<#

    for i in range(100) :
        rep.append(Population("Jeunes", jeunes[i], int(demographie[0]/100), 15, 5))

    for i in range(100) :
        rep.append(Population("Actifs", actifs[i], int(demographie[1]/100), 25, 10))

    for i in range(100) :
        rep.append(Population("Seniors", seniors[i], int(demographie[2]/100), 35, 5))

    #>>> Sortie <<<#
    return(rep)


def nb_acheteur(population, produit) :
    """
    FONCTION       : Retourne pour une population le nombre d'acheteur
    ENTREES        :
    SORTIE         :
    REMARQUES      :
    TEST UNITAIRE  : ("OK"/"...")
    """
    #>>> Initialisation des variables locales <<<#
    acheteurs = 0
    utilite  = 0
    for pop in produit.utilite :
        if pop[0] == population.nom :
            utilite = pop[1]

    #
    acheteurs_potentiels = int((population.nombre)*(utilite/100))

    #>>> Corps de la fonction <<<#
    if population.revenu >= produit.prix :
        acheteurs = acheteurs_potentiels
    #>>> Sortie <<<#
    return(acheteurs)


def demande(acheteurs, produit, esp, ecart) :
    """
    FONCTION       : Détermine la demande d'un produit sur
                     le marché.
    ENTREES        : Le nombre d'acheteurs 
    SORTIE         :
    REMARQUES      :
    TEST UNITAIRE  : ("OK"/"...")
    """
    #>>> Initialisation des variables locales <<<#
    demandes = 0
    num_tour = produit.age
    #>>> Corps de la fonction <<<#
    if abs(esp-num_tour)>=2*ecart:
        demandes = int(acheteurs*(0.025)/(esp-2*ecart))
    elif abs(esp-num_tour)>=ecart:
        demandes = int(acheteurs*(0.135)/(ecart))
    else :
        demandes=int(acheteurs*(0.34)/(ecart))

    #>>> Sortie <<<#
    return(demandes)


def profit(nbr_ventes, produit) :
    """
    FONCTION       :
    ENTREES        :
    SORTIE         :
    REMARQUES      :
    TEST UNITAIRE  : ("OK"/"...")
    """
    # On initialise la marge faite par le distributeur.
    marge = 21/100

    total = nbr_ventes*produit.prix

    gain = total*(1-marge)

    return(gain)


def ventes(market, populations) :
    """
    FONCTION       : Fonction principale que l'on exécutera tous
                     les mois.
    ENTREES        : 
    SORTIE         :
    REMARQUES      :
    TEST UNITAIRE  : ("OK"/"...")
    """
    #>>> Initialisation des variables locales <<<#
    demandes = 0
    gain = []

    #>>> Corps de la fonction <<<#
    for offre in market.produits :
        for pop in populations :
            acheteurs = nb_acheteur(pop, offre[0])
            demandes += demande(acheteurs, offre[0], pop.tps_adoption[0], pop.tps_adoption[1])

        # On définit le nombre de vente du produit qui est
        #| la plus petite valeur entre l'offre et la demande.
        nbr_ventes = min(demandes, offre[1])

        offre[1]-= nbr_ventes

        # On calcule le profit des ventes
        gain.append(( "Chiffre d'affaire : "+offre[0].nom, profit(nbr_ventes, offre[0])))

    #>>> Sortie <<<#
    return(market, gain)

def inMarket(market, produits, produit, quantite) :
    """
    FONCTION       : Mettre un produit sur le marché
    ENTREES        : 
    SORTIE         :
    REMARQUES      :
    TEST UNITAIRE  : ("OK"/"...")
    """

    for prod in produits :
        if prod.nom == produit :
            if prod.marche == False :
                prod.marche = True
                market.produits.append([prod, quantite])
            else :
                ajout([prod.nom, quantite], market.produits)

    return(market, produits)

def outMarket(market, produits, produit) :
    """
    FONCTION       : Retirer un produit sur le marché
    ENTREES        : 
    SORTIE         :
    REMARQUES      :
    TEST UNITAIRE  : ("OK"/"...")
    """

    for prod in produits :
        if prod.nom == produit :
            prod.marche=False
            retireAll(produit, market.produits)

    return(market, produits)

####################################
########| TESTS UNITAIRES |#########
####################################
'''
class Test(unittest.TestCase) :

    """
     def test_fonction(self) :

        #>>> Test 1 <<<#
        # On fait les tests de la fonction en utilisant les self.assert...
    """
'''
####################################
###########| PROGRAMME |############
####################################

if __name__=="__main__" :
    # On effectue les tests unitaires.
    # unittest.main()

    populations = consommateurs(input("Entrez une année : "))

    produit1 = Produit([], [["Jeunes", 15.488], ["Actifs", 45.0], ["Seniors", 11.552]], ["Puce", "Metal", "Diode", "Transistor"], ["Opération_brève", "Opération_silencieuse", "Opération_avancée", "Opération_lente"], "Actifs")
    produit2 = Produit([], [["Jeunes", 15.488], ["Actifs", 45.0], ["Seniors", 11.552]], ["Puce", "Metal", "Diode", "Transistor"], ["Opération_brève", "Opération_silencieuse", "Opération_avancée", "Opération_lente"], "Actifs")
    
    produits=[produit1, produit2]

    market=Stock()
    print(market)
    compteur = 1

    for prod in produits :
        print(str(compteur)+" : ",prod)
        compteur += 1

    choix = input("Choisir un produit : ")
    quantite = input("Choisir une quantité : ")

    # On fixe le prix unitaire du produit.
    Produit.fixePrix(produits, produits[int(choix)-1].nom, int(input("Fixez un prix : ")))

    # On met le produit en vente.
    market, produits = inMarket(market, produits, produits[int(choix)-1].nom, int(quantite))

    print(market)

    gain = ventes(market, populations)

    print(gain)