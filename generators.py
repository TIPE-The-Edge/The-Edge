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

Rajouter les fonctions d'update (s'il en manque).

Individu :
    updateExpProduit (voir avec Adrien si j'incrémente l'exp pour
        les prototypes, projets etc..)
    competence_direction (voir avec Adrien, qui apparemment l'utilise, ce qu'il
        en fait et comment je l'initialise.)

Formation : # BONUS
    competences (Besoin d'une fonction pour rendre cohérent)
    self.prix   (Besoin d'une fonction pour rendre cohérent)
    self.duree  (Besoin d'une fonction pour rendre cohérent)

Population : # de consommateurs
    updateProduits() (voir comment on maj les produits vendus
        et a quelle fréquence) (Adrien quand il sera dans la partie vente)

Fournisseur :
    self.materiaux_vendu (Materiaux et prix) (Besoin d'une fonction) (Lucas)

Usine :
    self.operations_realisables (Opérations et prix)
        (Besoin d'une fonction) (Lucas)

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
        self.age     = self.genAge()

        # Experiences en nombre de semaines
        self.exp_RetD    = self.genExpRole()
        self.exp_startup = 0

        # Compétences
            # R&D
        self.competence_groupe    = self.genCompetence() # Capacité à travailler en groupe
        self.competence_recherche = self.genCompetence() # Efficacité à la recherche

        # Caractéristique RH
        self.bonheur = 5 # De 0 à 10, indicateur du bonheur de l'employé dans
                         # l'entreprise.
        self.statut  = "CDI" # Pour l'instant, un seul statut
        self.role    = "R&D" # Pour l'instant, un seul role
        self.projet  = None  # Projet en cours
        self.salaire = self.genSalaire() # Salaire brut

        # Formations
        self.nbr_formations  = 0 # Nbr de formations effectuées # BONUS
        self.cout_formations = 0 # Cout des formations effectuées # BONUS

        # BONUS
        self.conges  = None # BONUS
        self.horaire = None # temps de travail # BONUS
        self.exp_produit = None # Experience par produit # BONUS
        self.competence_direction = None # Capacité à diriger une équipe # BONUS

    def __repr__(self):
        return "{} - {} {}, {} ans. {}".format(
                self.id, self.prenom, self.nom, self.age, self.exp_RetD)

    def genNom(self, genre):
        """ Retourne un nom en fonction du genre entré.
        """

        if   genre == "femme":
            return random.choice(readNameFile("./Name_Files/girl_names.txt"))
        elif genre == "homme":
            return random.choice(readNameFile("./Name_Files/boy_names.txt"))
        else:
            return random.choice(readNameFile("./Name_Files/family_names.txt"))

    def genAge(self):

        liste = [2,2,2,2,2,2, 3,3,3,3,3, 4,4,4, 5,5, 6]
        dizaine = random.choice(liste)

        if dizaine == 2:
            unite = random.randint(3, 9)
        elif dizaine == 6:
            unite = 0
        else:
            unite = random.randint(0,9)

        nbr = int(str(dizaine) + str(unite))
        return nbr

    def genExpRole(self):
        seuil_bas  = int((self.age - 23)*52/3)
        seuil_haut = (self.age - 23)*52
        return(random.randint(seuil_bas, seuil_haut)) # de 0 à 40 ans d'exp

    def genCompetence(self):
        comp_exp = (self.exp_RetD/52)/7.4 # Compétence tirée de l'experience
        comp_rand = random.randint(1, 5)
        return (int(round(comp_exp + comp_rand, 0)))

    def genSalaire(self):

        # R&D
        if self.role == "R&D":
            if self.exp_RetD >= 1768:
                return(4025)
            elif self.exp_RetD >= 884:
                return(3858)
            elif self.exp_RetD >= 468:
                return(3483)
            elif self.exp_RetD >= 312:
                return(2975)
            elif self.exp_RetD >= 208:
                return(2975)
            else:
                return(2550)
        else:
            return(0)

    def initExpProduit(individus, produits):

        for ind in individus:
            ind.exp_produit = [[prod.nom, 0] for prod in produits]

    def updateExpProduit(individus, produits):
        for ind in individus:
            for prod in produits:
                # On cherche à quel projet est affecté l'individu
                if ind.projet == prod.nom:

                    # Puis on incrémente de 1 le bon projet dans exp_produit
                    for proj in ind.exp_produit:
                        if prod.nom in proj:
                            proj[1] += 1

    def updateExpStartUp(individus):
        for ind in individus:
            ind.exp_startup += 1

    def semaine_to_annee(semaines):
        return(round(semaines/52, 1)) # Arrondi à 1 chiffre après la virgule

class Population(object): # de consommateurs

    # Cette classe sera majoritairement paramétrée à la main

    def __init__(self, nom, revenu, nombre):
        self.nom = nom # (Adrien)

        self.revenu = revenu # (Adrien)
        self.nombre = nombre # (Adrien)

        self.produits = [[]] # nbr d'utilisateur qui ont déja acheté par produit

    def __repr__(self):
        return "{} - nombre: {} revenu: {}".format(
                self.nom, self.nombre, self.revenu)

    def initProduits(populations, produits):

        for pop in populations:
            pop.produits = [[prod.nom, 0] for prod in produits]

class Produit(object):

    def __init__(self, utilite, materiaux, operations, tps_adoption):
        self.nom = self.genNom()

        self.utilite    = utilite    # Par population (0-100)
        self.materiaux  = materiaux  # materiaux et quantités nécessaires
        self.operations = operations # Opérations nécessaires

        self.prix     = 0 # Prix fixé
        self.tps_adoption  = tps_adoption

        self.marche = False # Le produit est sur le marché ou non
        self.age    = 0     # Temps sur le marché du produit

        self.nbr_ameliorations = 0
        self.concurence = 0 # BONUS

    def __repr__(self):
        return "{} - age : {}".format(self.nom, self.age)

    def genNom(self):

        prefixe = random.choice(readNameFile("./Name_Files/product_prefixes.txt"))
        sufixe  = random.choice(readNameFile("./Name_Files/product_sufixes.txt"))

        while prefixe + " " + sufixe in [prod.nom for prod in produits]:
            prefixe = random.choice(readNameFile("./Name_Files/product_prefixes.txt"))
            sufixe  = random.choice(readNameFile("./Name_Files/product_sufixes.txt"))

        return prefixe + " " + sufixe

    def creeUtilite(self, populations, seuil):

        somme = seuil + 1
        while somme > seuil:

            for pop in populations:
                utilites = [random.randint(1,100) for pop in populations]
                somme = sum(utilites)

        self.utilite = [[populations[i].nom, utilites[i]] for i in range(len(populations))]

    def ageUpdate(produits):

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
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :
    pass
