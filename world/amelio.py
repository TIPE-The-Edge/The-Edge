#! /usr/bin/env python
#-*- coding: utf-8 -*-


####################################
#>>> AUTEUR  : LAFAGE Adrien
#>>> SUJET   : R&D / AMELIORATION
#>>> DATE    : 19/01/2018
####################################


############| IMPORTS |#############
import os
import sys
import unittest
from math import *

from world.objets import *
from world.outils import *
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
de 100% (quelque soit le nombre
d'améliorations déjà effectuées)
"""
####################################


####################################
############| CLASSES |#############
####################################

class Ameliore() :

    id = -1

    def __init__(self, produit, nom) :

        # Initialise l'identifiant du Projet
        self.id = Ameliore.id
        Ameliore.id -= 1

        # Initialise le nom de l'amélioration
        self.nom = nom

        self.produit = produit
        self.avancement = 0
        self.palier = Ameliore.fixePalier(self)
        self.phase = 1
        self.attente = False

    def changeMateriaux(self) :
        """
        FONCTION       : Supprime un élément de la liste des matériaux.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : Une amélioration dont la liste des matériaux
                         du produit est diminué de 1.
        """
        del self.produit.materiaux[-1]
        return(self)

    def changeOperations(self) :
        """
        FONCTION       : Supprime un élément de la liste des opérations.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : Une amélioration dont la liste des opérations
                         du produit est diminué de 1.
        """
        del self.produit.operations[-1]
        return(self)

    def changeUtilite(self) :
        """
        FONCTION       : Augmente l'utilité de la population ciblée.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : Une amélioration dont l'utilité de la
                         population ciblée a augmenté.
        REMARQUES      : L'augmentation est inversement
                         proportionnelle au nombre d'améliorations.
        """

        bonus = aleaLoiNormale(10, 1.6)-(self.produit.nbr_ameliorations)
        if bonus < 0 :
            bonus = 0

        for uti in self.produit.utilite :
            if uti[0] == self.produit.cible :
                uti[1]+=bonus

        return(self)

    def update(self) :
        """
        FONCTION       : Procède à l'amélioration du produit en fonction
                         du résultat obtenu aléatoirement.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : L'amélioration dont le produit est amélioré.
        """

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
        """
        FONCTION       : Fixe le nombre de points d'avancement
                         requis pour procéder à l'amélioration
                         du produit.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : Une amélioration dont le palier est fixé.
        """

        return(80)

    def progression(self) :
        """
        FONCTION       : Modélise le développement de l'amélioration
                         d'un produit.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : L'amélioration mise à jour.
        """
        # Initialisation des coûts
        couts = [self.nom, 0]

        if self.avancement >= self.palier :
            # On améliore une caractéristique de notre produit
            self = Ameliore.update(self)
            if self.produit.nbr_ameliorations > 1 :
                self.produit.nom = self.produit.nom[:-1] + str(self.produit.nbr_ameliorations+1)
            else :
                self.produit.nom = self.produit.nom+" v"+str(self.produit.nbr_ameliorations+1)
            self.phase = 5
            self.produit.develop = False

        return(couts)

    def __repr__(self) :
        return("{}. {} // Produit en développement : {} | Progression : {}".format(self.id, self.nom, self.produit.nom, self.avancement))

####################################
###########| PROGRAMME |############
####################################

if __name__=="__main__" :

    pass
