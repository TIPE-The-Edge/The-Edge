#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.4.2
# Author: Maxence BLANC
# Last modified : 11/2017
# Titre du Fichier : generateurs d'entités
########################

# IMPORTS
import random
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
###################| CLASSES |######################
####################################################

class Individu(object):
    """ Class contenant toutes les informations concernant un individu.

    Nom, Prénom
    Salaire
    Bonheur
    Heure de travail ? (rentre dans le bonheur ?)
    Statut (stagiaire?, cdd, cdi)
    Rôle (Inactif, Marketing, production, chercheur, etc.)
    Age (retraite)
    Nombre de jours de congés (maladie, vacances, etc.)*
    Projet en cours

    Expérience (influence sur les compétences):
        Expérience dans la start up elle même.
        Expérience sur un certain produit (bonus s’il travail sur son amélioration etc.)
        Expérience pour une certaine fonction de l’entreprise.

    Compétences :
        Travail de groupe
        Recherche
        Gestion, Management
        Logistique
        Marketing
    """

    def __init__(self):

        self.genre   = random.choice(["homme", "femme"])

        # Nom, Prénom
        if self.genre == "homme" :
            self.prenom  = self.genName("./Name_Files/boy_names.txt")
        else : self.prenom  = self.genName("./Name_Files/girl_names.txt")
        self.nom     = self.genName("./Name_Files/family_names.txt")

        self.age     = 0

        self.salaire = 0
        self.bonheur = 0

        self.statut  = None
        self.role    = None
        self.conges  = 0
        self.horaire = 0 # temps de travail

        self.projet  = None

        # Experiences
        self.exp_startup = 0
        self.exp_produit = []
        self.exp_role    = []

        # Compétences
        self.competence_groupe      = 0
        self.competence_recherche   = 0
        self.competence_gestion     = 0
        self.competence_logistique  = 0
        self.competence_marketing   = 0

        individus.append(self)

    def genName(self, fichier):
        """ Retourne aléatoirement une ligne d'un fichier.
        ENTREE      : un fichier.txt
        VARIABLES   : lignes : la liste des lignes du fichier
        SORTIE      : une string correspondant à une ligne du fichier
        Vérifié par :
        """

        # Lecture du fichier
        entree = open(fichier,"r") # Fichier voulu
        contenu_entree = entree.readlines()
        entree.close()

        # On créé une liste qui contient toutes les lignes du fichier.
        lignes = [ligne.strip('\n') for ligne in contenu_entree]

        return(random.choice(lignes))



####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :

    individus = [] # liste des individus

    os.system('clear') # works on Linux/Mac
    Bob = Individu()
    print(Bob.prenom, Bob.nom, Bob.age)
    print(Bob.genre, Bob.role)

    print(individus)
