#! /usr/bin/env python
#-*- coding: utf-8 -*-


####################################
#>>> AUTEUR  : LAFAGE Adrien
#>>> SUJET   : R&D / AMELIORATION
#>>> DATE    : 31/12/2017
####################################


############| IMPORTS |#############
import os
import sys
import unittest
from math import *

from test import *
####################################


##########| DESCRIPTION |###########
"""
Fichier rassemblant les différentes 
fonctions permettant de modéliser le 
processus d'amélioration d'un produit.
"""
####################################


#############| NOTES |##############
"""
Partons du principe que les chances 
de succès pour une amélioration soient
de l'ordre de 30% (quelque soit le nombre
d'améliorations déjà effectuées)
"""
####################################

#| Provisoire |#

#-Populations

pop_1 = Population("Jeunes", 300, 15)
pop_2 = Population("Actifs", 2000, 40)
pop_3 = Population("Seniors", 1800, 25)
populations = [pop_1, pop_2, pop_3]

#-Chercheurs

chercheurs =[ Individu() for i in range(3)]

#-Produit

produit = Produit([["Jeunes", 50], ["Actifs", 20], ["Seniors", 10]], ["materiaux_1", "materiaux_2"], ["operation_1", "operation_2"], "Jeunes")

####################################
############| CLASSES |#############
####################################

class Ameliore() :

    def __init__(self, produit, chercheurs) :

        self.produit = produit
        self.chercheurs = chercheurs
        self.avancement = 0
        self.palier = 0
        self.phase = 0

    def changeMateriaux(self) : 

        del self.produit.materiaux[-1]
        return(self)

    def changeOperations(self) :

        del self.produit.operations[-1]
        return(self)

    def changeUtilite(self) :
        """
        FONCTION       : Augmente l'utilité de la population ciblée.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : Une amélioration dont l'utilité de la 
                         population ciblée 
        REMARQUES      : L'augmentation est inversement 
                         proportionnelle au nombre d'améliorations.
        TEST UNITAIRE  : ...
        """

        bonus = aleaLoiNormale(10, 1.6)-(self.produit.nbr_ameliorations)
        if bonus < 0 :
            bonus = 0

        for uti in self.produit.utilite :
            if uti[0] == self.produit.cible :
                uti[1]+=bonus
        
        return(self)

    def update(self) : 
        valeur = aleaLoiNormale(50, (16/1+(self.produit.nbr_ameliorations)))

        if valeur < 34 and len(self.produit.materiaux)>1 :
            Ameliore.changeMateriaux(self)

        elif 66<valeur and len(self.produit.operations)>1:
            Ameliore.changeOperations(self)

        else :
            Ameliore.changeUtilite(self)

        self.produit.nbr_ameliorations += 1
        return(self)

    def fixePalier(self) :

        self.palier = 80
        return(self)

    def progression(self) :
        
        if self.avancement >= Ameliore.fixePalier(self).palier :
            # On améliore une caractéristique de notre produit
            self = Ameliore.update(self)
            self.phase += 1

        else : 
            # On fait avancer le projet.
            self.avancement += progres(chercheurs)

        return(self)

    def __repr__(self) : 
        return("Phase {} |Cible : {} | Utilité : {} | Matériaux : {} | Opérations : {} | Avancement : {}".format(
               self.phase,self.produit.cible, self.produit.utilite, self.produit.materiaux, self.produit.operations, self.avancement))

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

    test = Ameliore(produit, chercheurs)
    print(test)
    while test.phase == 0 :
        test=Ameliore.progression(test)
        print(test)

    print(test.produit)

    test = Ameliore(test.produit, chercheurs)
    print(test)
    while test.phase == 0 :
        test=Ameliore.progression(test)
        print(test)

    print(test.produit)