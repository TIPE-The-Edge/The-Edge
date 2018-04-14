#! /usr/bin/env python
#-*- coding: utf-8 -*-


####################################
#>>> AUTEUR  : LAFAGE Adrien
#>>> SUJET   : MATHS / OUTILS
#>>> DATE    : 30/12/2017
####################################


############| IMPORTS |#############
import unittest
from math import *

import numpy as np
import operator

from world.function import *
from world.objets import *
from world.outils import *
from world.RH import *

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


def readNameFile(fichier):
    """ Lis un fichier .txt et retourne la liste de ses éléments.
    Entrée : le nom du fichier
    Sortie : une liste des lignes du fichier
    Vérifié par :
    """
    # Lecture du fichier
    entree = open(fichier,"r") # Fichier voulu
    contenu_entree = entree.readlines()
    entree.close()
    # On créé une liste qui contient toutes les lignes du fichier.
    liste = [ligne.strip('\n') for ligne in contenu_entree]

    return liste


def enhancedSort(liste, comparateur, ordre):
    """ Trie une liste d'objets selon le comparateur.
    Entree : La liste
             Le/les attributs de l'objet servant de comparateur(s) (str)
             Ordre de tri (True: décroissant / False: croissant)
    Sortie : La liste de dictionnaires triée.
    """

    return sorted(liste, key=operator.attrgetter(comparateur), reverse=ordre)


def semaine_to_annee(semaines):
    """ converti un nombre de semaines en années.
    Entree : Nbr de semaines
    Sortie : Nbr d'années
    """
    return(round(semaines/52, 1)) # Arrondi à 1 chiffre après la virgule



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
