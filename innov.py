#! /usr/bin/env python
#-*- coding: utf-8 -*-


####################################
#>>> AUTEUR  : LAFAGE Adrien
#>>> SUJET   : R&D / INNOVATION
#>>> DATE    : 08/12/2017
####################################


############| IMPORTS |#############
import os
import sys
import unittest
from math import *
####################################


##########| DESCRIPTION |###########
"""
Fichier rassemblant les différentes
fonctions permettant de modéliser le
processus d'innovation d'un produit :

I/   Génération d'idées :
      - Définition d'une classe Projet

II/  Analyse du marché :
      - Génération d'un retour client
        sur un objet de classe Projet
      - Ciblage d'une population /
        orientation du projet

III/ Développement/Test de validation :
(Se présente en deux étapes)
      1. Une première ébauche qui va
         donner une idée des matériaux
         à utiliser, et donc des coûts.
      -----| Avis client |-----
      2. Développement, ajustement des
         matériaux nécessaires et fixation
         du prix minimum pour être rentable
         (Phase de test : si le prix minimum
         est trop élevé alors cela échoue)

Une fois ces 3 étapes validées les
produit est prêt à être vendu.

D'après les recherches effectuées les
chances de succès sont inférieures à
50%, voire la plupart du temps de
l'ordre de 1-10%.
"""
####################################


#############| NOTES |##############
"""
|→ HYPOTHESE :
    On considère que nos chercheurs
    ne sont jamais à cours d'idées. Seuls
    les temps relatifs à l'élaboration du
    projet, au développement technique et
    aux tests de validation pourront être
    extrêmement différents en fonction des
    projets.

|→ TÂCHES EFFECTUEES :

"""
####################################


####################################
############| CLASSES |#############
####################################

class Projet() :

    def __init__(self, arg1, arg2) :
        """
        On initialise notre classe.
        """


####################################
###########| FONCTIONS |############
####################################

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


####################################
###########| PROCEDURES |###########
####################################

def nom_procedure() :
    """
    FONCTION       :
    ENTREES        :
    SORTIE         :
    REMARQUES      :
    """
    #>>> Initialisation des variables locales <<<#

    #>>> Corps de la procédure <<<#


####################################
########| TESTS UNITAIRES |#########
####################################

class Test(unittest.TestCase) :

    """
     def test_fonction(self) :

        #>>> Test 1 <<<#
        # On fait les tests de la fonction en utilisant les self.assert...
    """

####################################
###########| PROGRAMME |############
####################################

if __name__=="__main__" :
    # On effectue les tests unitaires.
    unittest.main()
