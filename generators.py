#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.4.2
# Author: Maxence BLANC
# Last modified : 11/2017
# Titre du Fichier : generateurs d'entités
########################

# IMPORTS
from random import *
import os

# IMPORTS DE FICHIERS



""" TO DO LIST ✔✘

(voir CDC.txt)

Rendre possible la lecture de fichier.txt situés dans des dossiers. ✘

"""

""" PROBLEMS
python ne comprend pas les path que je lui donne.
"""

""" NOTES
"""

''' Commentaires

""" A quoi sert la fonction. Comment elle marche
Entrée :
Variables :
Sortie :
Vérifié par :
"""

'''



####################################################
##################| FONCTIONS |#####################
####################################################

def genName(fichier_prenom, fichier_nom):
    """ Retourne aléatoirement un prénom avec son nom de famille
    a partir d'un fichier de noms.
    Entrée :
    Variables :
    Sortie :
    Vérifié par :
    """

    # Names
    entree = open(fichier_prenom,"r") # Fichier de score voulu
    contenu_entree = entree.readlines()
    entree.close()

    NAMES = [ligne.strip('\n') for ligne in contenu_entree]

    # Family names
    entree = open(fichier_nom,"r") # Fichier de score voulu
    contenu_entree = entree.readlines()
    entree.close()

    FAMILY_NAMES = [ligne.strip('\n') for ligne in contenu_entree]

    # Corps de la fonction

    ran1 = randint(0, len(NAMES)-1)
    ran2 = randint(0, len(FAMILY_NAMES)-1)
    return(NAMES[ran1]+" "+FAMILY_NAMES[ran2])



####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :

    os.system('clear') # works on Linux/Mac
    print(genName("./Name_Files/boy_names.txt", "./Name_Files/family_names.txt"))
    print(genName("./Name_Files/girl_names.txt", "./Name_Files/family_names.txt"))
