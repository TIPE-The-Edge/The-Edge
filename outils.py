#! /usr/bin/env python
#-*- coding: utf-8 -*-


####################################
#>>> AUTEUR  : LAFAGE Adrien
#>>> SUJET   : MATHS / OUTILS
#>>> DATE    : 30/12/2017
####################################


############| IMPORTS |#############
import os
import sys
import unittest
from math import *

import numpy as np
####################################


##########| DESCRIPTION |###########
"""
Ce fichier rassemblera des fonctions
qui peuvent être utilisées dans diverses
parties de notre programme. En quelque
sorte, ce fichier constitura notre
boite à outils.
"""
####################################


#############| NOTES |##############
"""
Actuellement il n'y a que la fonction
qui va nous permettre d'obtenir des
valeurs aléatoirement selon une loi
normale.
"""
####################################


####################################
###########| FONCTIONS |############
####################################

def aleaLoiNormale(esperance, ecart_type) :
    """
    FONCTION       : Génère une valeur dont la fréquence
                     d'apparition respecte la loi normale
                     N(esperance, ecart_type²)
    ENTREES        : Une espérance (float) et un écart-type
                     (float)
    SORTIE         : Un entier (int)
    REMARQUES      : On utilise la librairie numpy pour la
                     génération d'une variable aléatoire.
                     Voir le fichier notes.txt pour des 
                     précisions.
    TEST UNITAIRE  : OK
    """
    #>>> Initialisation des variables locales <<<#

    # On définit la taille de la matrice qui contiendra la valeur
    #| aléatoire.
    taille = 1

    #>>> Corps de la fonction <<<#

    # On génère d'abord une valeur (float) dans une matrice.
    matrice = np.random.normal(loc=esperance, scale=ecart_type, size = taille)
    # On convertit notre valeur en entier.
    matrice = np.array(matrice, int)
    # On récupère la valeur contenue dans notre matrice
    valeur = abs(matrice[0])

    #>>> Sortie <<<#
    return(valeur)


# Fonction Compétence "Recherche"
def compRecherche(individus) :
    return(sum([individu.competence_recherche for individu in individus]))

# Fonction Compétence "Groupe"
def compGroupe(individus) :
    # On fait la moyenne des capacités de travail de groupe des chercheurs
    moyenne = sum([individu.competence_groupe for individu in individus])//len(individus)
    leader = max([individu.competence_direction for individu in individus])
    if leader >= 8 :
        moyenne += (int(leader/8))+(leader-8)
    return(10*moyenne -50)

def progres(individus) :
    return(compRecherche(individus)+(compGroupe(individus)/100)*compRecherche(individus))


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
########| TESTS UNITAIRES |#########
####################################

class Test(unittest.TestCase) :

     def test_aleaLoiNormale(self) :

        #>>> Test 1 <<<#
        test = aleaLoiNormale(5, 1.6)>=0
        self.assertTrue(test)


####################################
###########| PROGRAMME |############
####################################

if __name__=="__main__" :
    # On effectue les tests unitaires.
    unittest.main()
