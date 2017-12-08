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
import operator

# IMPORTS DE FICHIERS



""" TO DO LIST ✔✘

(voir CDC.txt)

POUR ADRIEN : Produit materiaux population

rajouter aux classes des __repr__(self): pour plus de lisibilité

On pourrait faire de l'optimisation en important le contenu des fichiers noms
    au début pour ne pas avoir à les rouvrir ?

Rajouter les fonctions d'update.
Rajouter les fonctions de recherche.

Individu :
    Les fonctions d'update
    BONUS

Produit :
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
    competences (à compléter?)
    self.prix   (Besoin d'une fonction pour rendre cohérent)
    self.duree  (Besoin d'une fonction pour rendre cohérent)

Population : # de consommateurs
    self.produits

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

def enhancedSort(liste, comparateur, ordre):
    """ Trie une liste d'objets selon le comparateur.
    Entree : La liste
             Le/les attributs de l'objet servant de comparateur(s) (str)
             Ordre de tri (True: décroissant / False: croissant)
    Sortie : La liste de dictionnaires triée.
    """

    return sorted(liste, key=operator.attrgetter(comparateur), reverse=ordre)

####################################################
###################| CLASSES |######################
####################################################

class Individu(object):

    id = 0

    def __init__(self):

        # Identifiant pour le repérer rapidement dans la liste des individus
        self.id = Individu.id
        Individu.id += 1

        # Caractéristiques de l'individu
        self.genre   = random.choice(["homme", "femme"])

        self.prenom  = self.genName(self.genre) # Prénom (en fonction du genre)
        self.nom     = self.genName("family")
        self.age     = random.randint(23,50)

        self.salaire = 0
        self.bonheur = random.randint(3, 10)

        self.statut  = None
        self.role    = None
        self.conges  = 0 # BONUS
        self.horaire = 0 # temps de travail # BONUS

        self.projet  = None

        # Experiences # A DEFINIR
        self.exp_startup = 0
        self.exp_produit = [[]] # Experience par produit
        #self.exp_role    = [[]] # Experience par role # To be removed

        # Compétences # A COMPLETER?
        self.competence_groupe      = random.randint(1, 10)
        self.competence_recherche   = random.randint(1, 10)

        # Ajoute à la liste
        individus.append(self)

    def genName(self, genre):
        """ Retourne un nom en fonction du genre entré.
        """

        if   genre == "femme":
            return random.choice(readNameFile("./Name_Files/girl_names.txt"))
        elif genre == "homme":
            return random.choice(readNameFile("./Name_Files/boy_names.txt"))
        else:
            return random.choice(readNameFile("./Name_Files/family_names.txt"))

    def initExpProduit():

        for ind in individus:
            ind.exp_produit = [[prod.nom, 0] for prod in produits]

class Population(object): # de consommateurs

    # Cette classe sera majoritairement paramétrée à la main

    def __init__(self, nom, revenu, nombre):
        self.nom = nom

        self.revenu = revenu # (Adrien)
        self.nombre = nombre # (Adrien)

        self.produits = [[]] # nbr d'utilisateur qui ont déja acheté par produit

        # Ajoute à la liste
        populations.append(self)

class Produit(object):

    def __init__(self):
        self.nom = self.genName()
        self.utilite    = [[]] # Par population (0-100)
        self.materiaux  = [[]] # materiaux et quantités nécessaires
        self.operations = [] # Opérations nécessaires
        self.valeur     = 0  # Prix fixé

        self.tps_adoption  = 0

        self.marche = False # Le produit est sur le marché ou non
        self.age    = 0     # Temps sur le marché du produit

        self.nbr_ameliorations = 0
        self.concurence = 0 # BONUS

        # Ajoute à la liste
        produits.append(self)

    def genName(self):

        prefixe = random.choice(readNameFile("./Name_Files/product_prefixes.txt"))
        sufixe  = random.choice(readNameFile("./Name_Files/product_sufixes.txt"))

        while prefixe + " " + sufixe in [prod.nom for prod in produits]:
            prefixe = random.choice(readNameFile("./Name_Files/product_prefixes.txt"))
            sufixe  = random.choice(readNameFile("./Name_Files/product_sufixes.txt"))

        return prefixe + " " + sufixe

    def creeUtilite(self, seuil):
        somme = seuil + 1
        while somme > seuil:

            for pop in populations:
                utilites = [random.randint(1,100) for pop in populations]
                somme = sum(utilites)
                print(utilites)

        self.utilite = [[populations[i].nom, utilites[i]] for i in range(len(populations))]

    def initUtilites(seuil):

        for prod in produits:
            prod.creeUtilite(seuil)

    def ageUpdate():

        for prod in produits:
            if prod.marche:
                prod.age += 1


class Operation(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./Name_Files/operations.txt")
    # Indice pour les noms générés automatiquement
    indice_nom = 0

    def __init__(self):

        self.nom = self.genName()

        # Ajoute à la liste
        operations.append(self)

    def genName(self):

        # Si l'on peut, on utilise un nom de la liste,
        # Sinon on génère un nom automatiquement avec indice_nom.
        try:
            nom = random.choice(Operation.noms_dispo)
            Operation.noms_dispo.remove(nom)
        except IndexError :
            Operation.indice_nom += 1
            nom = "Opération_"+str(Operation.indice_nom)

        return nom

class Materiau(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./Name_Files/materiaux.txt")
    # Indice pour les noms générés automatiquement
    indice_nom = 0

    def __init__(self):

        self.nom = self.genName()

        # Ajoute à la liste
        materiaux.append(self)

    def genName(self):

        # Si l'on peut, on utilise un nom de la liste,
        # Sinon on génère un nom automatiquement avec indice_nom.
        try:
            nom = random.choice(Materiau.noms_dispo)
            Materiau.noms_dispo.remove(nom)
        except IndexError :
            Materiau.indice_nom += 1
            nom = "Materieau_"+str(Materiau.indice_nom)

        return nom

class Formation(object):

    competences = []

    def __init__(self):

        self.nom = "" # préfixe + sufixe aléatoires

        self.competences = [[]] # liste des compétences améliorées
        self.prix  = 0 # Besoin d'une fonction
        self.duree = 0 # Besoin d'une fonction

    def genName(self):
        pass

class Fournisseur(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./Name_Files/fournisseurs.txt")

    # Localisation

    def __init__(self):

        self.nom = self.genName()


        self.localisation = None
        self.materiaux_vendu = [[]] # Materiaux et prix

        # Ajoute à la liste
        fournisseurs.append(self)

    def genName(self):
        nom = random.choice(Fournisseur.noms_dispo)
        Fournisseur.noms_dispo.remove(nom)

        return nom

class Usine(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./Name_Files/usines.txt")

    def __init__(self):

        self.nom = self.genName()

        self.localisation = None
        self.operations_realisables = [[]] # Opérations et prix

        # Ajoute à la liste
        usines.append(self)

    def genName(self):
        nom = random.choice(Usine.noms_dispo)
        Usine.noms_dispo.remove(nom)

        return nom

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

    rang = 3
    rang2 = 6

    # populations
    print("------ Classe : Population ------")
    print(Population("Les Vieux", 100, 2).nom)
    print(Population("Les Jeunes", 2000, 99).nom)
    print()

    # produits
    print("------ Classe : Produit ------")
    for i in range(0 + rang):
        print(Produit().nom)
    print()

    """
    # opérations
    print("------ Classe : Operation ------")
    for i in range(0 + rang):
        print(Operation().nom)
    print()

    # materiaux
    print("------ Classe : Materiau ------")
    for i in range(0 + rang):
        print(Materiau().nom)
    print()

    # formations
    print("------ Classe : Formation ------")
    for i in range(0 + rang):
        print(Formation().nom)
    print()

    # fournisseurs
    print("------ Classe : Fournisseur ------")
    for i in range(0 + rang2):
        print(Fournisseur().nom)
    print()

    # usines
    print("------ Classe : Usine ------")
    for i in range(0 + rang2):
        print(Usine().nom)
    print()

    # individu
    print("------ Classe : Individu ------")
    for i in range(0 + rang):
        Bob = Individu()
        print(Bob.id, Bob.prenom, Bob.nom, Bob.age)
        print(Bob.genre, Bob.role, Bob.competence_groupe, Bob.competence_recherche)
        Individu.initExpProduit()
        print(Bob.bonheur, Bob.exp_produit)
        print()
        """

    produits = enhancedSort(produits, "nom", False)

    Produit.initUtilites(2000)

    for prod in produits:
        print(prod.nom)
        print(prod.utilite)
