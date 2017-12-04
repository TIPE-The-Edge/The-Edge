#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.4.2
# Author: Maxence BLANC
# Last modified : 12/2017
# Titre du Fichier : generateurs d'entités
########################

# IMPORTS
import random
import os

# IMPORTS DE FICHIERS



""" TO DO LIST ✔✘

(voir CDC.txt)


Rajouter les fonctions genName pour plus de lisibilité.

On pourrait faire de l'optimisation en important le contenu des fichiers noms
    au début pour ne pas avoir à les rouvrir.

Individu :
    self.bonheur (à définir)
    compétences (à redefinir)
    Experiences (à définir)
    horaire

Produit :
    self.utilite (aleatoire 0-100) (avec seuil de la somme des utilites)
    self.materiaux (aleatoire)
    self.operations (aleatoire)
    self.tps_adoption (Adrien)
    self.age (créer la fonction modificatrice)

Operation :
    rajouter un rapport avec les materiaux?
        Càd l'opération "découpage" se fait toujours sur un materiau "bois"
        et pas sur "eau".

Materiau :

Formation :
    self.nom
    competences (à redéfinir)
    self.prix   (Besoin d'une fonction pour rendre cohérent)
    self.duree  (Besoin d'une fonction pour rendre cohérent)

Population : # de consommateurs
    self

Fournisseur :
    self.localisation (Lucas)
    self.materiaux_vendu (Materiaux et prix) (Besoin d'une fonction)

Usine :
    self.localisation (Lucas)
    self.operations_realisables (Opérations et prix) (Besoin d'une fonction)
"""


""" PROBLEMS
"""
""" NOTES
"""

####################################################
##################| FONCTIONS |#####################
####################################################

""" A quoi sert la fonction. Comment elle marche
Entrée :
Variables :
Sortie :
Vérifié par :
"""

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


####################################################
###################| CLASSES |######################
####################################################

class Individu(object):

    id = 0
    def __init__(self):

        # Identifiant pour le repérer rapidement dans la liste des individus
        self.id = Individu.id
        Individu.id += 1

        self.genre   = random.choice(["homme", "femme"])

        # Prénom
        if self.genre == "homme" :
            self.prenom = random.choice(readNameFile("./Name_Files/boy_names.txt"))
        else :
            self.prenom = random.choice(readNameFile("./Name_Files/girl_names.txt"))

        self.nom     = random.choice(readNameFile("./Name_Files/family_names.txt"))
        self.age     = random.randint(23,50)

        self.salaire = 0
        self.bonheur = 0 # A DEFINIR

        self.statut  = None
        self.role    = None
        self.conges  = 0 # BONUS
        self.horaire = 0 # temps de travail # BONUS

        self.projet  = None

        # Experiences # A DEFINIR
        self.exp_startup = 0
        self.exp_produit = [[]] # Experience par produit
        self.exp_role    = [[]] # Esperience par role

        # Compétences # A REDEFINIR
        self.competence_groupe      = 0
        self.competence_recherche   = 0
        self.competence_gestion     = 0
        self.competence_logistique  = 0
        self.competence_marketing   = 0

        # Ajoute à la liste
        individus.append(self)

class Produit(object):

    def __init__(self):
        self.nom = random.choice(readNameFile("./Name_Files/product_prefixes.txt")) + " " + random.choice(readNameFile("./Name_Files/product_sufixes.txt"))
        self.utilite    = [] # Par population
        self.materiaux  = [] # materiaux et quantités nécessaires
        self.operations = [] # Opérations nécessaires
        self.valeur     = 0  # Prix fixé

        self.tps_adoption  = 0
        self.age = 0 # Temps sur le marché du produit

        self.nbr_ameliorations = 0
        self.concurence = 0 # BONUS

        # Ajoute à la liste
        produits.append(self)

class Operation(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./Name_Files/operations.txt")
    # Indice pour les noms générés automatiquement
    indice_nom = 0

    def __init__(self):

        # Si l'on peut, on utilise un nom de la liste,
        # Sinon on génère un nom automatiquement avec indice_nom.
        try:
            self.nom = random.choice(Operation.noms_dispo)
            Operation.noms_dispo.remove(self.nom)
        except IndexError :
            self.nom = "Opération_"+str(Operation.indice_nom)
            Operation.indice_nom += 1

        # Ajoute à la liste
        operations.append(self)

class Materiau(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./Name_Files/materiaux.txt")
    # Indice pour les noms générés automatiquement
    indice_nom = 0

    def __init__(self):

        # Si l'on peut, on utilise un nom de la liste,
        # Sinon on génère un nom automatiquement avec indice_nom.
        try:
            self.nom = random.choice(Materiau.noms_dispo)
            Materiau.noms_dispo.remove(self.nom)
        except IndexError :
            self.nom = "Materieau_"+str(Materiau.indice_nom)
            Materiau.indice_nom += 1

        # Ajoute à la liste
        materiaux.append(self)

class Formation(object):

    competences = []

    def __init__(self):

        self.nom = "" # préfixe + sufixe aléatoires

        self.competences = [[]] # liste des compétences améliorées
        self.prix  = 0 # Besoin d'une fonction
        self.duree = 0 # Besoin d'une fonction

class Population(object): # de consommateurs

    # Cette classe sera majoritairement paramétrée à la main

    def __init__(self):
        self.nom = ""

class Fournisseur(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./Name_Files/fournisseurs.txt")

    # Localisation

    def __init__(self):

        self.nom = random.choice(Fournisseur.noms_dispo)
        Fournisseur.noms_dispo.remove(self.nom)

        self.localisation = None
        self.materiaux_vendu = [[]] # Materiaux et prix

        # Ajoute à la liste
        fournisseurs.append(self)

class Usine(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./Name_Files/usines.txt")

    def __init__(self):

        self.nom = random.choice(Usine.noms_dispo)
        Usine.noms_dispo.remove(self.nom)

        self.localisation = None
        self.operations_realisables = [[]] # Opérations et prix

        # Ajoute à la liste
        usines.append(self)

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
    for i in range(5):
        Bob = Individu()
        print(Bob.id, Bob.prenom, Bob.nom, Bob.age)
        print(Bob.genre, Bob.role)
        print()

    # produits
    print("------ Classe : Produit ------")
    for i in range(0):
        print(Produit().nom)
    print()

    # opérations
    print("------ Classe : Operation ------")
    for i in range(0):
        print(Operation().nom)
    print()

    # materiaux
    print("------ Classe : Materiau ------")
    for i in range(0):
        print(Materiau().nom)
    print()

    # formations
    print("------ Classe : Formation ------")
    for i in range(0):
        print(Formation().nom)
    print()

    # populations
    print("------ Classe : Population ------")
    for i in range(1):
        print(Population().nom)
    print()

    # fournisseurs
    print("------ Classe : Fournisseur ------")
    for i in range(1):
        print(Fournisseur().nom)
    print()

    # usines
    print("------ Classe : Usine ------")
    for i in range(1):
        print(Usine().nom)
    print()
