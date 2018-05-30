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
"""
####################################


#############| NOTES |##############
"""
FAIRE LES COMMENTAIRES DES FONCTIONS
"""
####################################

####################################


####################################
###########| FONCTIONS |############
####################################


#>>> Création des différentes populations de consommateurs


def budget(revenus, periode) :
    """
    FONCTION       : Fonction calculant le budjet mensuel moyen des
                     trois classes de population (jeunes/actifs/seniors)
    ENTREES        : Les données du fichier.csv (string list list) sur les
                     revenus sous forme d'une liste contenant une seule
                     liste où se trouve les trois revenus des classes de
                     populations à la "période" indiquée (string).
    SORTIE         : La liste des trois budjets moyens associés aux classes
                     de population (float list).
    TEST UNITAIRE  : ...
    """
    # Liste des revenus (Initialisation)
    rep = []

    # Pourcentage de ménage ayant accès à internet
    #| Cette fonction d'écoule d'une régression
    #| linéaire sur les quelques données concernat
    acces = (5.4*int(periode)-10765.9)/100

    # Frais d'internet (donnée approximative)
    internet = 30

    for r in range(len(revenus[0])) :

        if r > int(len(revenus[0])*acces) :
            rep.append((float(revenus[0][r])*(5/2400))-internet)
        else :
            rep.append(float(revenus[0][r])*(5/2400))

    return(rep)


def consommateurs(periode) :
    """
    FONCTION       : Crée la liste des consommateurs pour une période
                     donnée.
    ENTREES        : Une période (string)
    SORTIE         : Une liste de consommateurs
    REMARQUES      : Possibilité d'augmenter le nombre de types
                     de consommateurs.
    TEST UNITAIRE  : ...
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


#>>> Système de vente


def nb_acheteur(population, produit) :
    """
    FONCTION       : Retourne pour une population le nombre d'acheteurs.
    ENTREES        : Un population (Population) et un produit (Produit)
    SORTIE         : Le nombre total d'acheteurs pour le produit dans
                     l'état actuel des choses (int).
    REMARQUES      : On peut jouer sur le nombre d'acheteur en modifiant
                     le nombre d'acheteurs potentiels par le biais de
                     l'utilité.
    TEST UNITAIRE  : ("OK"/"...")
    """
    #>>> Initialisation des variables locales <<<#
    acheteurs = 0
    utilite  = 0
    for pop in produit.utilite :
        if pop[0] == population.nom :
            utilite = pop[1]

    # Le nombre d'acheteur potentiels
    #| L'utilité représente le pourcentage d'acheteurs potentiels
    #| au sein d'une population.
    acheteurs_potentiels = int((population.nombre)*(utilite/1000))

    #>>> Corps de la fonction <<<#

    # Résolution du problème du consommateur
    #| "le budjet des clients potentiels est-il
    #| suffisamment élevé ?"
    if population.revenu >= produit.prix :
        acheteurs = acheteurs_potentiels

    #>>> Sortie <<<#
    #| Ce résultat peut être modifié si le prix du produit change.
    #| Sinon pour un même prix chaque population aura toujours le
    #| résultat.
    return(acheteurs)


def demande(acheteurs, produit, tps_adoption) :
    """
    FONCTION       : Détermine la demande d'un produit sur
                     le marché en fonction du temps de
                     celui-ci sur le marché, du nombre d'acheteur
                     et du temps d'adoption de la population.
    ENTREES        : Le nombre d'acheteurs (int), produit (Produit),
                     un couple représentant le temps d'adoption
                     (int list)
    SORTIE         : Le nombre de demandes (int)
    REMARQUES      : A MODIFIER (Mettre de la documentation pour
                     expliquer cette fonction)
    TEST UNITAIRE  : ...
    """
    #>>> Initialisation des variables locales <<<#

    # Nombre de demandes (Initialisation)
    demandes = 0
    # Le temps du produit sur le marché
    num_tour = int(produit.age/4)
    # Le temps d'adoption de la population
    [esp, ecart] = tps_adoption

    #>>> Corps de la fonction <<<#

    if abs(esp-num_tour)>=2*ecart:
        demandes = int(acheteurs*(0.025)/(esp-2*ecart))
    elif abs(esp-num_tour)>=ecart:
        demandes = int(acheteurs*(0.135)/(ecart))
    else :
        demandes=int(acheteurs*(0.34)/(ecart))

    # On passe la demande au mois à une demande en semaine
    demandes = int(demandes/4)

    #>>> Sortie <<<#
    return(demandes)


def profit(nbr_ventes, produit) :
    """
    FONCTION       : Retourne le chiffre d'affaire en fonction
                     d'un nombre de vente et du prix du produit.
    ENTREES        : Nombre de ventes (int) et un produit (Produit)
    SORTIE         : Le chiffre d'affaire (float)
    TEST UNITAIRE  : ...
    """
    # Variable représentant les frais du à la vente
    #| que ce soit la marge des distributeurs ou
    #| les frais liés à l'acheminement des produits
    #| au consommateur.
    frais = 21/100

    # Calcule le chiffre d'affaire brut
    total = nbr_ventes*produit.prix

    # Calcule les gains réalisés en tenant compte
    #| des frais éventuels.
    gain = total*(1-frais)

    #>>> Sortie <<<#
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
            demandes += demande(acheteurs, offre[0], pop.tps_adoption)

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
