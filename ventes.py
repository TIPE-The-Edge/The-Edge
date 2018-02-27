#! /usr/bin/env python
#-*- coding: utf-8 -*-


####################################
#>>> AUTEUR  : LAFAGE Adrien
#>>> SUJET   : VENTES
#>>> DATE    : 31/01/2018
####################################


############| IMPORTS |#############
import os
import sys
import unittest
from math import *

from objets import *
from outils import *
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








"""
####################################

####################################

# Variables globales :
jeunes = Population("Jeunes", )




####################################
############| CLASSES |#############
####################################
'''
class nom_classe() :
    """
    On crée une nouvelle classe.
    """
    def __init__(self, arg1, arg2) :
        """
        On initialise notre classe.
        """
'''

####################################
###########| FONCTIONS |############
####################################

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
        if pop[0] = population.nom :
            utilite = pop[1]

    acheteurs_potentiels = (population.nombre)*(utilite/100)

    #>>> Corps de la fonction <<<#
    if population.revenu > produit.prix :
        acheteurs = acheteurs_potentiels
    #>>> Sortie <<<#
    return(acheteurs)


def ventes(acheteurs, produit, num_tour, esp, ecart) :
    """
    FONCTION       :
    ENTREES        :
    SORTIE         :
    REMARQUES      :
    TEST UNITAIRE  : ("OK"/"...")
    """
    #>>> Initialisation des variables locales <<<#
    nbr_ventes = 0
    #>>> Corps de la fonction <<<#
    if abs(esp-num_tour)>=2*ecart:
        nbr_ventes = int(acheteurs*(0.025)/(esp-2*ecart))
    elif abs(esp-num_tour)>=ecart:
        nbr_ventes = int(acheteurs*(0.135)/(ecart))
    else :
        nbr_ventes=int(acheteurs*(0.34)/(ecart))

    #>>> Sortie <<<#
    return(nbr_ventes)

'''
def nom_fontion() :
    """
    FONCTION       :
    ENTREES        :
    SORTIE         :
    REMARQUES      :
    TEST UNITAIRE  : ("OK"/"...")
    """
    #>>> Initialisation des variables locales <<<#

    #>>> Corps de la fonction <<<#

    #>>> Sortie <<<#
    return()
'''

####################################
###########| PROCEDURES |###########
####################################
'''
def nom_procedure() :
    """
    FONCTION       :
    ENTREES        :
    SORTIE         :
    REMARQUES      :
    """
    #>>> Initialisation des variables locales <<<#

    #>>> Corps de la procédure <<<#
'''

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
    
