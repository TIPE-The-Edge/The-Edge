#! /usr/bin/env python
#-*- coding: utf-8 -*-


####################################
#>>> AUTEUR  : LAFAGE Adrien
#>>> SUJET   : R&D / INNOVATION
#>>> DATE    : 21/12/2017
####################################


############| IMPORTS |#############
import os
import sys
import unittest
from math import *
import numpy as np

from random import randint
from test import *
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
CEPENDANT
D'après les recherches effectuées les
chances de succès sont inférieures à
50%, voire la plupart du temps de
l'ordre de 1-10%. Telle sera la probabilité 
que le produit soit rentable.
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

    - Création de l'objet Concept, avec les
      les fonctions qui lui sont associées.

    - Implémentation d'une fonction de
      génération d'entiers en suivant une
      loi normale (alternative à la fonction
      randint).

    - Développement de la phase 1 du projet.

|→ REMARQUES :
    
    - Garder en tête que les fonctions qui
      qui affichent ou demande à l'utilisateur
      une entrée devront être remplacées pour
      l'intégration dans l'application.
"""
####################################


#| Provisoire |#

#-Population
pop_1 = Population("Jeunes", 300, 15)
pop_2 = Population("Actifs", 2000, 40)
pop_3 = Population("Seniors", 1800, 25)
populations = [pop_1, pop_2, pop_3]

#-Chercheurs

chercheurs =[ Individu() for i in range(3)]

####################################
###########| FONCTIONS |############
####################################

def appreciation(ref) :
    """
    FONCTION       :
    ENTREES        :
    SORTIE         :
    REMARQUES      :
    TEST UNITAIRE  : ("OK"/"...")
    """
    #>>> Initialisation des variables locales <<<#
    rep = ""
    #>>> Corps de la fonction <<<#
    if ref <= 50 :
        rep = "indifférents"
    elif 50<ref<=75 :
        rep = "intéressés"
    elif 75<ref<=90 :
        rep = "enthousiastes"
    else :
        rep = "tres enthousiaste"

    #>>> Sortie <<<#
    return((rep,ref))


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
    TEST UNITAIRE  : ("OK"/"...")
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
    return(10*moyenne -50)

def progret(individus) :
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
############| CLASSES |#############
####################################

class Concept(object) :

    def __init__(self) :

        # On initialise l'appréciation du concept
        #| par les clients (différentes populations)
        self.appreciation = []

        # Désignera une population.
        self.orientation = ""


    def sondage(self) : 
        for pop in populations :
            reference = aleaLoiNormale(esperance=50, ecart_type=16.6)
            self.appreciation.append([appreciation(reference),pop.nom])
        return(self)

    def ciblage(self, population) :
        """
        FONCTION       : Defini quelle population le concept cible-
                         t-il.
        ENTREES        : Un concept (Concept) et des populations 
                         (Population list)
        SORTIE         : Le concept avec une orientation définie 
                         (Concept)
        REMARQUES      : Il faudra prendre en compte ici le cout 
                         d'une campagne marketing.
        TEST UNITAIRE  : OK
        """
        # On modifie l'orientation marketing du projet
        self.orientation = population
        return(self)

    def effetMarketing(self) :
        for avis in self.appreciation :
            if avis[1] == self.orientation :
                avis[0] = appreciation(avis[0][1]+aleaLoiNormale(esperance=5, ecart_type=1.6))
        return(self)

    def __repr__(self) :
        return("{} | {}".format(self.appreciation, self.orientation))


class Prototype(object):

    def __init__(self, chercheurs, appreciation, orientation):

        # La liste des chercheurs parcipant au projet
        self.chercheurs = chercheurs

        # L'opinion des consommateurs sur le produit
        self.appreciation = appreciation

        # La population ciblée par le produit
        self.orientation = orientation

        # Les matériaux 
        self.materiaux = []

        # Les opérations
        self.operations = []

        # Le coût de fabrication
        self.cout = 0

    def creation(self) :

    def __repr__(self) :
        return("{} | {} - {} | {} : {}". format(self.appreciation, 
              self.orientation, self.materiaux, self.operation, self.cout))


class Projet(object):

    def __init__(self, chercheurs) :

        # La liste des chercheurs parcipant au projet
        self.chercheurs = chercheurs

        # Génération d'un produit à l'initialisation
        #| du projet.
        self.produit = Concept() 
        self.avancement = 0
        self.phase = 1

    def etude(self) :

        # On initialise l'appétence des consommateurs
        #| vis à vis du concept.
        self.produit = Concept.sondage(self.produit)
        
        print(self.produit)

        # On demande à l'utilisateur de fixer la population
        #| qu'il souhaite cibler avec son produit.
        Concept.ciblage(self.produit, input("Veuillez entrer le nom d'une population : "))

        # On applique l'effet du ciblage sur l'opinion  
        #| des consommateurs vis à vis du concept.
        self.produit = Concept.effetMarketing(self.produit)

        return(self)

    # def development(self) :

    # def testing(self) :


    def niveau(self, liste) :
        if self.phase == 1 :
            if self.avancement >= liste[0] :
                # Choix de l'orientation/ciblage
                self = Projet.etude(self)
                # On réinitialise l'avancement
                self.avancement = self.avancement-60
                # On passe à la phase suivante du projet
                self.phase += 1
            else :
                # On fait avancer le projet.
                self.avancement += progret(chercheurs)

        elif self.phase == 2 :
            if self.avancement >= liste[1] :

                # On change le concept en prototype
                self.produit = Prototype(self.chercheurs, (self.produit.appreciation), 
                               (self.produit.orientation))
                
                # On passe à la phase suivante du projet
                self.phase += 1
            else :
                # On fait avancer le projet.
                self.avancement += progret(chercheurs)

        elif self.phase == 3 :

            if self.avancement >= liste[2] :

                # On passe à la phase suivante du projet
                self.phase += 1

            else :
                # On fait avancer le projet.
                self.avancement += progret(chercheurs)

        return(self)


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

class Test(unittest.TestCase) :

    def test_appreciation(self) :

        #>>> Test 1 <<<#

        reponse = ("indifférents",40)
        test = appreciation(40)
        self.assertEqual(test, reponse)

    def test_ciblage(self) :

        #>>> Test 1 <<<#

        reponse = "Jeunes"
        test = Concept()
        test = Concept.ciblage(test, "Jeunes")
        self.assertEqual(test.orientation, reponse)


####################################
###########| PROGRAMME |############
####################################

if __name__=="__main__" :
    # On effectue les tests unitaires.
    # unittest.main()

    for cherch in chercheurs :
        print(cherch) 

    print(compRecherche(chercheurs))

    test = Projet(chercheurs)
    compt = 0
    
    while test.phase == 1 :
        test = Projet.niveau(test, [60, 100, 50])
        print(test.avancement)
        compt+=1

    print(test.produit)
    print(compt)