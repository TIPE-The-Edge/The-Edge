#! /usr/bin/env python
#-*- coding: utf-8 -*-


####################################
#>>> AUTEUR  : LAFAGE Adrien
#>>> SUJET   : Gestion Banque/ Lecture
#>>> DATE    : 30/12/17
####################################


############| IMPORTS |#############
import os
import sys
import unittest
from math import *

# Chargement des données.
import pandas as pd
####################################


##########| DESCRIPTION |###########
"""
Voici le fichier contenant les différentes
fonctions permettant de récupérer les
données de notre base de données.
"""
####################################


#############| NOTES |##############
"""
Pour récupérer une information précise,
il faudra utiliser la fonction
readLineCSV. Pour comprendre mieux
le fonctionnement de cette fonction
il est conseillé d'étudier les tests
unitaires qui lui sont associés.
"""
####################################


####################################
###########| FONCTIONS |############
####################################


#-------------- Outils ------------#

def nettoie(double_liste) :
    """
    FONCTION       : Supprime d'une liste de listes les chaines de
                     caractères suivantes : "\r\n","nan" ; ainsi
                     que les listes vides.
    ENTREES        : Une  liste de listes (list list).
    SORTIE         : Une liste de listes ne contenant pas de listes
                     vides et dont les éléments diffèrent de :
                     "\r\n" et "nan" (list list)
    REMARQUES      : 
    TEST UNITAIRE  : OK
    """
    #>>> Initialisation des variables locales <<<#

    #>>> Corps de la fonction <<<#

    for liste in double_liste :
        while "nan" in liste :
            liste.remove("nan")
        while "\r\n" in liste :
            liste.remove("\r\n")

    while [] in double_liste :
        double_liste.remove([])

    #>>> Sortie <<<#
    return(double_liste)

def normalise(chaine) :
    """
    FONCTION       : Retourne sous forme de flottant une chaine 
                     de caractères si cela est possible sinon 
                     retourne la chaine.
    ENTREES        : Une chaine de caractères (string).
    SORTIE         : Un flottant (float) OU la chaine d'entrée
                     (string)
    REMARQUES      :
    TEST UNITAIRE  : OK
    """
    #>>> Initialisation des variables locales <<<#

    #>>> Corps de la fonction <<<#

    try :
        chaine = float(chaine)
    except :
        chaine = chaine

    #>>> Sortie <<<#

    return(chaine)

#------------- Lecture ------------#

def readFileCSV(nom_fichier) :
    """
    FONCTION       : Retourne le contenu d'un fichier.csv sous
                     forme d'une liste de ses lignes.
    ENTREES        : Un nom de fichier .csv (string).
    SORTIE         : Les lignes du fichier sous une forme de liste.
                     (string list) et la liste des paramètres que
                     les données décrivent.
    REMARQUES      : Le fichier se trouve dans le dossier "Banque"
    TEST UNITAIRE  : ...
    """
    #>>> Initialisation des variables locales <<<#

    # On charge le dataset que l'utilisateur entre.
    fichier_donnees = pd.read_csv("./Banque/"+nom_fichier)
    # On récupère les paramètres du graphique
    parametres=[ligne for ligne in fichier_donnees]
    del parametres[-1]
    # On initialise une liste des lignes du fichier.
    lignes = []

    #>>> Corps de la fonction <<<#

    for numligne in range(len(fichier_donnees)) :
        # On initialise la liste qui contiendra les différents
        #| éléments d'une ligne du fichier csv.
        ligne  = []
        for parametre in parametres :
            ligne.append(str(fichier_donnees[parametre][numligne]))
        lignes.append(ligne)

    lignes = nettoie(lignes)
    #>>> Sortie <<<#

    return(lignes, parametres)


def readLineCSV(nom_fichier, parametreEntree, element, parametreSortie) :
    """
    FONCTION       : Trouve dans un fichier de données csv,
                     les éléments décrivant les paramètres de sortie en
                     fonction d'un élément du paramètre d'entrée associé.
    ENTREES        : Un nom de fichier csv (string), un paramètre
                     d'entrée (string) et son élément associé (string),
                     et des paramètres de sortie (string list).
    SORTIE         : Les éléments décrivant les paramètres de sortie associés
                     à l'élément du paramètre d'entrée (string list list).
    REMARQUES      :
    TEST UNITAIRE  : OK
    """
    #>>> Initialisation des variables locales <<<#

    # On initialise une liste des lignes et des paramètres du fichier.
    lignes, parametres = readFileCSV(nom_fichier)
    # On normalise notre élément d'entrée pour pouvoir le comparer.
    element = normalise(element)
    # On initialise notre sortie finale
    res = []

    #>>> Corps de la fonction <<<#

    # Pour chaque ligne du fichier.
    for ligne in lignes :

        # Si l'élément de la liste (ligne) relatif au paramètre
        #| d'entrée est égale à l'élément d'entrée. Alors on
        #| ajoute à notre liste réponse (res) les éléments décrivant
        #| les paramètres contenus dans la liste parametreSortie.
        if normalise(ligne[parametres.index(parametreEntree)]) == element :
            # Une liste qui contiendra les éléments des paramètres de sortie 
            #| d'une ligne dans laquelle la condition ci-dessus est vérifiée.
            mem = []
            for parametre in parametreSortie :
                mem.append(ligne[parametres.index(parametre)])
            res.append(mem)
    #>>> Sortie <<<#
    # On retourne notre liste réponse (res).
    return(res)


####################################
########| TESTS UNITAIRES |#########
####################################


class Test(unittest.TestCase) :

    
    def test_nettoie(self) :

        #>>> Test 1 <<<#
        
        reponse = [["Je","suis"],["Aydens"]]
        test = nettoie([["nan","Je","nan","suis","\r\n"],["\r\n","Aydens","nan"],["\r\n","nan"]])
        self.assertEqual(test, reponse)

    def test_normalise(self) :

        #>>> Test 1 <<<#

        reponse = "une chaine"
        test = normalise("une chaine")
        self.assertEqual(test, reponse)

        #>>> Test 2 <<<#

        reponse = 2015.0
        test = normalise("2015")
        self.assertEqual(test, reponse)

    def test_readLineCSV(self) :

        #>>> Test 1 <<<#

        reponse = [["3859168","10324453"]]
        test = readLineCSV("demographie.csv", "periode", "2010", ["jeunes","seniors"])
        self.assertEqual(test, reponse)

        #>>> Test 2 <<<#

        reponse = [["New York","25.0"],["Hong Kong","23.0"],["Berlin","26.0"]]
        test = readLineCSV("materiaux.csv", "materiaux", "clef usb", ["pays","cout unitaire"])
        self.assertEqual(test, reponse)

        #>>> Test 3 <<<#

        reponse = [["diode","0.41"],["vis","5.0"],["cable","26.0"],["gros bouton rouge","15.0"],
                  ["graveur blueray","170.0"],["port audio","12.0"],["circuit imprime","25.0"],
                  ["radiateur","150.0"]]
        test = readLineCSV("materiaux.csv","pays","Paris",["materiaux","cout unitaire"])
        self.assertEqual(test, reponse)

        #>>> Test 4 <<<#

        reponse=[["25.0"],["26.0"],["22.0"]]
        test = readLineCSV("materiaux.csv", "materiaux", "cable", ["cout unitaire"])
        self.assertEqual(test, reponse)

####################################
###########| PROGRAMME |############
####################################


if __name__=="__main__" :

    # On effectue les tests unitaires.
    unittest.main()