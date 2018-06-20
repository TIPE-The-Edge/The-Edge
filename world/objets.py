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
from world.outils import *


""" TO DO LIST ✔✘

Individu :
    exp:
        Mettre à jours les différentes exp quand les individus participent.
            Par exemple, en R&D augmenter d'1 la val de l'exp pour chaque
            semaine passée sur un projet.
"""


""" PROBLEMS
"""


""" NOTES

Pour LC :
    Couts générés :
        "cout materiaux"
        "cout transport"
"""


""" BONUS

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
        self.age     = self.genAge() # Entre 23 et 60 ans

        # Experiences en nombre de semaines
        self.exp_RetD    = self.genExpRD()
        self.exp_startup = 0
        self.exp_prod    = 0

        # Compétences
            # R&D
        self.competence_groupe    = self.genCompetenceRD() # Capacité à travailler en groupe
        self.competence_recherche = self.genCompetenceRD() # Efficacité à la recherche
        self.competence_direction = self.genCompetenceRD() # Capacité à diriger une équipe
            # Production
        self.competence_production = self.genCompetenceProd()

        # Caractéristique RH
        self.statut  = "CDI" # Pour l'instant, un seul statut
        self.role    = None  # Roles disponibles : R&D, prod
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
        return "{} - {} {}, {} ans. comp_prod = {}".format(
                self.id, self.prenom, self.nom, self.age, self.competence_production)

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

    def genCompetenceProd(self):
        """ Génère les valeurs de la compétence Production.
        """

        # Compétence tirée de l'experience
        # Fonction telle qu'au bout de 2 semaines d'exp, la compétence
        # augmente de 1. Et au bout de 3 ans atteint le max possible.
        a = -1/1716
        b = 215/429
        x = self.exp_prod
        comp_exp = int((a*(x**2) + b*x)**0.5)

        # Compétence tirée de l'aleatoire
        comp_rand = random.randint(1, 2) # Que jusqu'à 2 car il y a un gros
                                         # gap entre 2 et 3, ce qui correspond
                                         # à l'importance de l'expérience.

        return (int(round(comp_exp + comp_rand, 0)))

    def genSalaire(self):
        """ Retourne un salaire en fonction de l'experience.
        """
        if   max(self.exp_RetD, self.exp_prod)>= 1768:
            return(4025)
        elif max(self.exp_RetD, self.exp_prod) >= 884:
            return(3858)
        elif max(self.exp_RetD, self.exp_prod) >= 468:
            return(3483)
        elif max(self.exp_RetD, self.exp_prod) >= 312:
            return(2975)
        elif max(self.exp_RetD, self.exp_prod) >= 208:
            return(2975)
        else:
            return(2550)

    def updateExpStartUp(individus):
        """ MàJ le nbr de semaine qu'à passé l'employé dans l'entreprise.
        """
        for ind in individus:
            ind.exp_startup += 1

class Population(object): # de consommateurs

    # Cette classe sera majoritairement paramétrée à la main

    def __init__(self, nom, revenu, nombre, esp, ecart):
        self.nom = nom

        self.revenu = revenu
        self.nombre = nombre
        self.tps_adoption = [esp, ecart]

    def __repr__(self):
        return "{} - nombre: {} revenu: {}.".format(
                self.nom, self.nombre, self.revenu)

    def ajoutProduit(populations, produit):
        """ Ajoute un nouveau produit aux populations.
        """

        for pop in populations:
            pop.produits.append([produit.nom, 0])

class Produit(object):
    id = 0

    def __init__(self, produits, utilite, materiaux, operations, cible):

        self.id = Produit.id
        Produit.id += 1

        self.nom = self.genNom(produits)
        self.utilite    = utilite    # Par population (0-100)
        self.materiaux  = materiaux  # materiaux et quantités nécessaires
        self.operations = operations # Opérations nécessaires (et quantité = 1)

        self.cible      = cible # Population ciblée
        self.prix       = 0     # Prix fixé

        self.marche = False # Le produit est sur le marché ou non
        self.age    = 0     # Temps sur le marché du produit

        self.develop = False # Défini que le produit n'est pas en développement

        self.nbr_ameliorations = 0
        # self.concurence = 0 # BONUS

    def __repr__(self):
        return "{}. {} - {}, {}".format(self.id, self.nom,
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
        """ Donne un prix à un produit donné
        """
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

        self.consommation = 0  #BONUS # Consommation énergétique? -> cout
        self.duree = 1 # en minutes #TODO # Pour le moment à 1. Peut être
                       # changé plus tard.

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
            nom = "Opération "+suffixe
        except IndexError :
            Operation.indice_nom += 1
            nom = "Opération "+str(Operation.indice_nom)

        return nom

class Materiau(object):
    """ Un peu obsolète car il n'y a que le nom des mats.

    Je la garde pour l'instant parce qu'il y a le vérificateur de doublons et
    ça peut etre utile si l'on veut faire des parties sans tous les mats
    (Sinon on pourrait juste transposer la liste des noms en une liste de mats).
    """

    # Liste des noms existants
    noms_dispo = readNameFile("./world/Name_Files/materiaux.txt")
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
