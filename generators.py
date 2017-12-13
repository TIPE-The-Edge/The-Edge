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

Rajouter les fonctions d'update.
Rajouter les fonctions de recherche.

Individu :

Produit :
    self.materiaux    (aleatoire) (Adrien)
    self.operations   (aleatoire) (Adrien)
    self.tps_adoption (Adrien)

Operation :

Materiau :

Formation :
    competences (Besoin d'une fonction pour rendre cohérent)
    self.prix   (Besoin d'une fonction pour rendre cohérent)
    self.duree  (Besoin d'une fonction pour rendre cohérent)

Population : # de consommateurs
    updateProduits() (voir comment on maj les produits vendus et a quelle fréquence) (Adrien quand il sera dans la partie vente)

Fournisseur :
    self.materiaux_vendu (Materiaux et prix) (Besoin d'une fonction) (Lucas)

Usine :
    self.operations_realisables (Opérations et prix) (Besoin d'une fonction) (Lucas)

Faire les BONUS.
"""


""" PROBLEMS
"""

""" NOTES

On pourrait faire de l'optimisation en important le contenu des fichiers noms
    au début pour ne pas avoir à les rouvrir ?

POUR ADRIEN : Produit materiaux population

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

    # Initialisation des identifiants
    id = 0

    def __init__(self):

        # Identifiant pour le repérer rapidement dans la liste des individus
        self.id = Individu.id
        Individu.id += 1

        # Caractéristiques de l'individu
        self.genre   = random.choice(["homme", "femme"])
        self.prenom  = self.genNom(self.genre) # Prénom (en fonction du genre)
        self.nom     = self.genNom("family")
        self.age     = random.randint(23,50)

        self.salaire = 0
        self.bonheur = random.randint(3, 10)
        self.statut  = None
        self.role    = None
        self.projet  = None

        # Experiences # A DEFINIR
        self.exp_startup = 0
        self.exp_produit = [[]] # Experience par produit
        #self.exp_role    = [[]] # Experience par role # To be removed

        # Compétences # A COMPLETER?
        self.competence_groupe      = random.randint(1, 10) # Capacité à travailler en groupe
        self.competence_recherche   = random.randint(1, 10) # Efficacité à la recherche
        self.competence_direction   = random.randint(1, 10) # Capacité à diriger une équipe

        self.conges  = 0 # BONUS
        self.horaire = 0 # temps de travail # BONUS

        # Ajoute à la liste
        individus.append(self)

    def __repr__(self):
        return "{} - {} {}, {} ans. {}.".format(
                self.id, self.prenom, self.nom, self.age, self.genre)

    def genNom(self, genre):
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
        self.nom = nom # (Adrien)

        self.revenu = revenu # (Adrien)
        self.nombre = nombre # (Adrien)

        self.produits = [[]] # nbr d'utilisateur qui ont déja acheté par produit

        # Ajoute à la liste
        populations.append(self)

    def __repr__(self):
        return "{} - nombre: {} revenu: {}".format(
                self.nom, self.nombre, self.revenu)

    def initProduits():

        for pop in populations:
            pop.produits = [[prod.nom, 0] for prod in produits]

class Produit(object):

    def __init__(self):
        self.nom = self.genNom()

        self.utilite    = [[]] # Par population (0-100)
        self.materiaux  = [[]] # materiaux et quantités nécessaires
        self.operations = []   # Opérations nécessaires

        self.prix     = 0 # Prix fixé
        self.tps_adoption  = 0 # ADRIEN

        self.marche = False # Le produit est sur le marché ou non
        self.age    = 0     # Temps sur le marché du produit

        self.nbr_ameliorations = 0
        self.concurence = 0 # BONUS

        # Ajoute à la liste
        produits.append(self)

    def __repr__(self):
        return "{} - age : {}".format(self.nom, self.age)

    def genNom(self):

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

        self.nom = self.genNom()

        # Ajoute à la liste
        operations.append(self)

    def __repr__(self):
        return "{}".format(
                self.nom)

    def genNom(self):

        # Si l'on peut, on utilise un nom de la liste,
        # Sinon on génère un nom automatiquement avec indice_nom.
        try:
            suffixe = random.choice(Operation.noms_dispo)
            # On efface le nom de la liste pour éviter les doublons
            # de noms d'opérations
            Operation.noms_dispo.remove(suffixe)
            nom = "Opération_"+suffixe
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

        self.nom = self.genNom()

        # Ajoute à la liste
        materiaux.append(self)

    def __repr__(self):
        return "{}".format(
                self.nom)

    def genNom(self):

        # Si l'on peut, on utilise un nom de la liste,
        # Sinon on génère un nom automatiquement avec indice_nom.
        try:
            nom = random.choice(Materiau.noms_dispo)
            # On efface le nom de la liste pour éviter les doublons
            # de noms de materiaux
            Materiau.noms_dispo.remove(nom)
        except IndexError :
            Materiau.indice_nom += 1
            nom = "Materieau_"+str(Materiau.indice_nom)

        return nom

class Formation(object):

    competences = ["competence_groupe", "competence_recherche", "competence_direction"]

    def __init__(self):

        self.nom = self.genNom() # préfixe + sufixe aléatoires

        self.competences = [[]] # liste des compétences améliorées # Besoin d'une fonction
        self.prix  = 0 # Besoin d'une fonction
        self.duree = 0 # Besoin d'une fonction

        formations.append(self)

    def __repr__(self):
        return "{} - prix: {} duree: {}".format(
                self.nom, self.prix, self.duree)

    def genNom(self):

        prefixe = random.choice(readNameFile("./Name_Files/formations_prefixes.txt"))
        sufixe  = random.choice(readNameFile("./Name_Files/formations_sufixes.txt"))

        while prefixe + " " + sufixe in [form.nom for form in formations]:
            prefixe = random.choice(readNameFile("./Name_Files/formations_prefixes.txt"))
            sufixe  = random.choice(readNameFile("./Name_Files/formations_sufixes.txt"))

        return prefixe + " " + sufixe

class Fournisseur(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./Name_Files/fournisseurs.txt")

    # Localisations
    localisations = ["Paris",
                    "New York",
                    "Los Angeles",
                    "Hong Kong",
                    "Allemagne",
                    "Pays-Bas"]

    def __init__(self):

        self.localisation = self.genLocalistation()

        self.nom = self.genNom()

        self.materiaux_vendu = [[]] # Materiaux et prix

        # Ajoute à la liste
        fournisseurs.append(self)

    def __repr__(self):
        return "{} - {} : {}".format(
                self.nom, self.localisation, self.materiaux_vendu)

    def genNom(self):

        nom = random.choice(Fournisseur.noms_dispo)
        # On efface le nom de la liste pour éviter les doublons
        # de noms de fournisseurs
        Fournisseur.noms_dispo.remove(nom)

        return nom

    def genLocalistation(self):

        loc = random.choice(Fournisseur.localisations)
        # On efface la localisation de la liste car elles sont uniques.
        Fournisseur.localisations.remove(loc)

        return loc

class Usine(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./Name_Files/usines.txt")

    # Localisations
    localisations = ["Paris",
                    "New York",
                    "Los Angeles",
                    "Hong Kong",
                    "Allemagne",
                    "Pays-Bas"]

    def __init__(self):

        self.nom = self.genNom()

        self.localisation = self.genLocalistation()
        self.operations_realisables = [[]] # Opérations et prix

        # Ajoute à la liste
        usines.append(self)

    def __repr__(self):
        return "{} - {} : {}".format(
                self.nom, self.localisation, self.operations_realisables)

    def genNom(self):
        nom = random.choice(Usine.noms_dispo)
        # On efface le nom de la liste pour éviter les doublons
        # de noms d'usines
        Usine.noms_dispo.remove(nom)

        return nom

    def genLocalistation(self):

        loc = random.choice(Usine.localisations)
        # On efface la localisation de la liste car elles sont uniques.
        Usine.localisations.remove(loc)

        return loc

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
    pass
