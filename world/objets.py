#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.4.2
# Author: Maxence BLANC
# Last modified : 12/2017
# Titre du Fichier : Générateur d'objets
########################

# IMPORTS
import random

# IMPORTS DE FICHIERS
from world.function import *
from world.outils import *


""" TO DO LIST ✔✘

Population : # de consommateurs
    updateProduits() (voir comment on maj les produits vendus
        et a quelle fréquence) (Adrien quand il sera dans la partie vente)

Fournisseur :
    self.materiaux_vendu (Besoin d'une fonction)

    approvisionnement()

Machine :
    self.operations_realisables (Besoin d'une fonction)

"""


""" PROBLEMS
"""

""" NOTES

Pour LC :
    Couts générés :
        "cout materiaux"
        "cout transport"

Formation : # BONUS
    competences (Besoin d'une fonction pour rendre cohérent)
    self.prix   (Besoin d'une fonction pour rendre cohérent)
    self.duree  (Besoin d'une fonction pour rendre cohérent)
"""

####################################################
##################| FONCTIONS |#####################
####################################################

def initProduits(objets, produits):
    """ Initialise le nombre de produits que possède les objets.
    Les objets doivent avoir l'attribut .produits.
    """

    for ob in objets:
        ob.produits = [[prod.nom, 0] for prod in produits]

def initMateriaux(objets, materiaux):
    """ Initialise le nombre de materiaux que possède les objets.
    Les objets doivent avoir l'attribut .materiaux.
    """

    for ob in objets:
        ob.materiaux = [[mat.nom, 0] for mat in materiaux]

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
        self.exp_RetD    = self.genExpRD()
        self.exp_startup = 0

        # Compétences
            # R&D
        self.competence_groupe    = self.genCompetenceRD() # Capacité à travailler en groupe
        self.competence_recherche = self.genCompetenceRD() # Efficacité à la recherche
        self.competence_direction = self.genCompetenceRD() # Capacité à diriger une équipe

        # Caractéristique RH
        self.statut  = "CDI" # Pour l'instant, un seul statut
        self.role    = "R&D" # Pour l'instant, un seul role
        self.projet  = None  # Projet en cours
        self.salaire = self.genSalaire() # Salaire brut

        #BONUS
        # Formations
        # self.nbr_formations  = 0 # Nbr de formations effectuées
        # self.cout_formations = 0 # Cout des formations effectuées
        #
        # Autres
        # self.conges  = None
        # self.horaire = None # temps de travail
        # self.bonheur = None # De 0 à 10, indicateur du bonheur de l'employé dans
                         # l'entreprise.

    def __repr__(self):
        return "{} - {} {}, {} ans. {}".format(
                self.id, self.prenom, self.nom, self.age, self.exp_RetD)

    def genNom(self, genre):
        """ Retourne un nom en fonction du genre entré.
        """

        if   genre == "femme":
            return random.choice(readNameFile("./world/Name_Files/girl_names.txt"))
        elif genre == "homme":
            return random.choice(readNameFile("./world/Name_Files/boy_names.txt"))
        else:
            return random.choice(readNameFile("./world/Name_Files/family_names.txt"))

    def genAge(self):
        """ Génère un age. # AMELIORABLE
        """

        liste = [2,2,2,2,2,2, 3,3,3,3,3, 4,4,4, 5,5, 6] # Détermine les proba des ages.
                                                        # Favorise la jeunesse.
        dizaine = random.choice(liste)

        if dizaine == 2:
            unite = random.randint(3, 9) # Pour commencer à 23 ans.
        elif dizaine == 6:
            unite = 0                    # Pour terminer à 60 ans.
        else:
            unite = random.randint(0,9)

        nbr = int(str(dizaine) + str(unite))
        return nbr

    def genExpRD(self):
        """ Génère l'experience de l'individu en fonction de son age.
        """

        seuil_haut = (self.age - 23)*52 # Experience max que peut avoir
                                        # l'individu en nbr de semaine

        seuil_bas  = int(seuil_haut/3)  # Pour ne pas que les "vieux" n'aient
                                        # aucune exp, ils ont au moins un tier
                                        # de leur vie active en experience.

        return(random.randint(seuil_bas, seuil_haut)) # de 0 à 40 ans d'exp

    def genCompetenceRD(self):
        """ Génère les valeurs des compétences de R&D. # AMELIORABLE
        """

        # Compétence tirée de l'experience
        pas = 37/5 # Tous les "pas", l'individu gagne 1 d'exp.
        comp_exp = (self.exp_RetD/52) / pas
        # Compétence tirée de l'aleatoire
        comp_rand = random.randint(1, 5)

        return (int(round(comp_exp + comp_rand, 0)))

    def genSalaire(self):
        """ Retourne un salaire en fonction du role et de l'experience.
        """

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

    def updateExpStartUp(individus):
        """ MàJ le nbr de semaine qu'à passé l'employé dans l'entreprise.
        """
        for ind in individus:
            ind.exp_startup += 1

class Population(object): # de consommateurs

    # Cette classe sera majoritairement paramétrée à la main

    def __init__(self, nom, revenu, nombre):
        self.nom = nom # (Adrien)

        self.revenu = revenu # (Adrien)
        self.nombre = nombre # (Adrien)

        self.produits = [[]] # nbr d'utilisateur qui ont déja acheté par produit

    def __repr__(self):
        return "{} - nombre: {} revenu: {}. {}".format(
                self.nom, self.nombre, self.revenu, self.materiaux)

    def ajoutProduit(populations, produit):
        """ Ajoute un nouveau produit aux populations.
        """

        for pop in populations:
            pop.produits.append([produit.nom, 0])

class Produit(object):

    def __init__(self, produits, utilite, materiaux, operations, cible):

        self.nom = self.genNom(produits)

        self.utilite    = utilite    # Par population (0-100)
        self.materiaux  = materiaux  # materiaux et quantités nécessaires
        self.operations = operations # Opérations nécessaires (et quantité = 1)

        self.cible      = cible # Population ciblée
        self.prix       = 0     # Prix fixé

        self.marche = False # Le produit est sur le marché ou non
        self.age    = 0     # Temps sur le marché du produit
        self.ventes = 0     # Nombre de ventes
        self.nbr_ameliorations = 0
        # self.concurence = 0 # BONUS

    def __repr__(self):
        return "{} - {}, {}".format(self.nom,
                                    self.materiaux, self.operations)

    def genNom(self, produits):

        prefixe = random.choice(readNameFile("./world/Name_Files/product_prefixes.txt"))
        sufixe  = random.choice(readNameFile("./world/Name_Files/product_sufixes.txt"))

        while prefixe + " " + sufixe in [prod.nom for prod in produits]:
            prefixe = random.choice(readNameFile("./world/Name_Files/product_prefixes.txt"))
            sufixe  = random.choice(readNameFile("./world/Name_Files/product_sufixes.txt"))

        return prefixe + " " + sufixe

    def ageUpdate(produits):
        """ MaJ le temps qu'ont passé les produits sur le marché.
        """

        for prod in produits:
            if prod.marche:
                prod.age += 1

    def fixePrix(produits, produit, valeur) :
        for prod in produits:
            if prod.nom == produit:
                prod.prix = valeur

class Operation(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./world/Name_Files/operations.txt")
    # Indice pour les noms générés automatiquement
    indice_nom = 0

    def __init__(self):

        self.nom = self.genNom()

        self.consommation = 0  # TODO # Consommation énergétique? -> cout
        self.duree = 1 # TODO # en minutes

    def __repr__(self):
        return "{} - {} min(s)".format(
                self.nom, self.duree)

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
    noms_dispo = readNameFile("./world/Name_Files/materiaux.txt")
    # Indice pour les noms générés automatiquement
    indice_nom = 0

    def __init__(self):

        self.nom = self.genNom()

        self.prix = 1 # TODO

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

class Formation(object): # BONUS

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

        prefixe = random.choice(readNameFile("./world/Name_Files/formations_prefixes.txt"))
        sufixe  = random.choice(readNameFile("./world/Name_Files/formations_sufixes.txt"))

        while prefixe + " " + sufixe in [form.nom for form in formations]:
            prefixe = random.choice(readNameFile("./world/Name_Files/formations_prefixes.txt"))
            sufixe  = random.choice(readNameFile("./world/Name_Files/formations_sufixes.txt"))

        return prefixe + " " + sufixe

####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :
    pass
