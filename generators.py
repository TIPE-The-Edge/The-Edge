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

Population

Individu :
    self.bonheur (à définir)
    compétences (à redefinir)
    Experiences
    horaire

Produit :
    self.utilite (aleatoire 0-100)
    self.materiaux (aleatoire)
    self.operations (aleatoire)
    self.tps_adoption (Adrien)
    self.age (créer la fonction modificatrice)

Operation :
    self

Materiau :
    self

Formation :
    self

Population : # de consommateurs
    self

Fournisseur :
    self

Usine :
    self
"""

""" PROBLEMS
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
    """

    def __init__(self):
        # Identifiant pour le repérer rapidement dans la liste des individus
        self.id = len(individus)+1

        self.genre   = random.choice(["homme", "femme"])

        # Nom, Prénom
        if self.genre == "homme" :
            self.prenom  = self.genName("./Name_Files/boy_names.txt")
        else :
            self.prenom  = self.genName("./Name_Files/girl_names.txt")
        self.nom     = self.genName("./Name_Files/family_names.txt")

        self.age     = random.randint(23,50)

        self.salaire = 0
        self.bonheur = 0

        self.statut  = None
        self.role    = None
        self.conges  = 0
        self.horaire = 0 # temps de travail

        self.projet  = None

        # Experiences
        self.exp_startup = 0
        self.exp_produit = [] # Experience par produit
        self.exp_role    = [] # Esperience par role

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

class Produit(object):
    """ Class contenant toutes les informations concernant un produit.
    """

    def __init__(self):
        self.nom = self.genName()
        self.utilite    = [] # Par population
        self.materiaux  = [] # materiaux et quantités nécessaires
        self.operations = [] # Opérations nécessaires
        self.valeur     = 0  # Prix fixé

        self.tps_adoption  = 0
        self.age = 0 # Temps sur le marché du produit

        self.nbr_ameliorations = 0
        self.concurence = 0 # BONUS

        produits.append(self)

    def genName(self):
        """ Générateur de nom pour les produits, un peu de fun.
        VARIABLES   : une liste de nom d'objets
                      une liste d'adjectifs
        SORTIE      : une string représentant un nom de produit
        Vérifié par :
        """
        # Lecture du fichier de préfixes
        entree = open("./Name_Files/product_prefixes.txt","r") # Fichier voulu
        contenu_entree = entree.readlines()
        entree.close()
        # On créé une liste qui contient toutes les lignes du fichier.
        prefixes = [ligne.strip('\n') for ligne in contenu_entree]

        # Lecture du fichier de sufixes
        entree = open("./Name_Files/product_sufixes.txt","r") # Fichier voulu
        contenu_entree = entree.readlines()
        entree.close()
        # On créé une liste qui contient toutes les lignes du fichier.
        sufixes = [ligne.strip('\n') for ligne in contenu_entree]

        return(random.choice(prefixes) + " " + random.choice(sufixes))

class Operation(object):
    """ Class contenant toutes les informations concernant un
    """
    def __init__(self):
        pass

class Materiau(object):
    """ Class contenant toutes les informations concernant un
    """
    def __init__(self):
        pass

class Formation(object):
    """ Class contenant toutes les informations concernant un
    """
    def __init__(self):
        pass

class Population(object): # de consommateurs
    """ Class contenant toutes les informations concernant un
    """
    def __init__(self):
        pass

class Fournisseur(object):
    """ Class contenant toutes les informations concernant un
    """
    def __init__(self):
        pass

class Usine(object):
    """ Class contenant toutes les informations concernant un
    """
    def __init__(self):
        pass

####################################################
##################| VARIABLES |#####################
####################################################

# Initialisation des listes de class
individus    = []
produits     = []
operations   = []
materiaux    = []
formations   = []
populations  = []
fournisseurs = []
usines       = []

####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :



    os.system('clear') # works on Linux/Mac

    # individu
    print("------ Classe : Individu ------")
    for i in range(3):
        Bob = Individu()
        print(Bob.id, Bob.prenom, Bob.nom, Bob.age)
        print(Bob.genre, Bob.role)
        print()

    print(individus)

    # produits
    print("------ Classe : Produit ------")
    Machine = Produit()
    print(Machine.nom)
