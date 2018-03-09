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
import os

# IMPORTS DE FICHIERS
from outils import *


""" TO DO LIST ✔✘

Population : # de consommateurs
    updateProduits() (voir comment on maj les produits vendus
        et a quelle fréquence) (Adrien quand il sera dans la partie vente)

Fournisseur :
    self.materiaux_vendu (Materiaux et prix) (Besoin d'une fonction) (Lucas)

    approvisionnement()

Machine :
    self.operations_realisables (Opérations et prix)
        (Besoin d'une fonction)

"""


""" PROBLEMS
"""

""" NOTES

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
        self.exp_RetD    = self.genExpRetD()
        self.exp_startup = 0

        # Compétences
            # R&D
        self.competence_groupe    = self.genCompetenceRH() # Capacité à travailler en groupe
        self.competence_recherche = self.genCompetenceRH() # Efficacité à la recherche
        self.competence_direction = self.genCompetenceRH() # Capacité à diriger une équipe

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

    def genExpRetD(self):
        """ Génère l'experience de l'individu en fonction de son age.
        """

        exp_max = (self.age - 23)*52# Experience max que peut avoir l'individu en nbr de semaine

        seuil_bas  = int(exp_max/3) # pour ne pas que les "vieux" n'aient aucune exp.
        seuil_haut = exp_max

        return(random.randint(seuil_bas, seuil_haut)) # de 0 à 40 ans d'exp

    def genCompetenceRH(self):
        """ Génère les valeurs des compétences de RH. # AMELIORABLE
        """
        pas = 37/5 # Tous les "pas", l'individu gagne 1 d'exp.

        # Compétence tirée de l'experience
        comp_exp = (self.exp_RetD/52) / pas
        # Compétence tirée de l'aleatoire
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

    def updateExpStartUp(individus):
        """ MàJ le nbr de semaine qu'à passé l'employé dans l'entreprise.
        """
        for ind in individus:
            ind.exp_startup += 1

    def licencie(individus, departs, id):
        """ Place un individu dans la liste departs et le supprime de
        individus.
        """
        for ind in individus:
            if ind.id == id:
                departs.append([ind.id, 0])
                individus.remove(ind)

class Population(object): # de consommateurs

    # Cette classe sera majoritairement paramétrée à la main

    def __init__(self, nom, revenu, nombre, esp, ecart):
        self.nom = nom 

        self.revenu = revenu 
        self.nombre = nombre 
        self.tps_adoption = [esp, ecart]

        self.produits = [[]] # nbr d'utilisateur qui ont déja acheté par produit

    def __repr__(self):
        return "{} - nombre: {} revenu: {}.".format(
                self.nom, self.nombre, self.revenu)

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
        self.operations = operations # Opérations nécessaires

        self.cible        = cible # Population ciblée
        self.prix         = 0     # Prix fixé

        self.marche = False # Le produit est sur le marché ou non
        self.age    = 0     # Temps sur le marché du produit

        self.nbr_ameliorations = 0
        self.concurence = 0 # BONUS

    def fixePrix(produits, produit, valeur) :
        for prod in produits :
            if prod.nom == produit :
                prod.prix = valeur

    def __repr__(self):
        return "{} - age : {}".format(self.nom, self.age)

    def genNom(self, produits):

        prefixe = random.choice(readNameFile("./Name_Files/product_prefixes.txt"))
        sufixe  = random.choice(readNameFile("./Name_Files/product_sufixes.txt"))

        while prefixe + " " + sufixe in [prod.nom for prod in produits]:
            prefixe = random.choice(readNameFile("./Name_Files/product_prefixes.txt"))
            sufixe  = random.choice(readNameFile("./Name_Files/product_sufixes.txt"))

        return prefixe + " " + sufixe

    def ageUpdate(produits):
        """ MaJ le temps qu'ont passé les produits sur le marché.
        """

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

        self.prix = 0  # TODO
        self.duree = 0 # TODO

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

        self.prix = 0 # TODO

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

        self.nom = self.genNom()
        self.localisation = self.genLocalistation()

        self.materiaux_vendu = [] # TODO

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
        """ Etabli la localisation du Fournisseur
        """

        loc = random.choice(Fournisseur.localisations)
        # On efface la localisation de la liste car elles sont uniques.
        Fournisseur.localisations.remove(loc)

        return loc

    def approvisionnement(fournisseur, destination, commande):
        """ Créé un cout et créé un objet transport à partir des données d'une
        commande de materiaux.
        Entrée : le nom du fournisseur
                 le nom de la destination
                 la commande [[mat1, nbr_mat1], [mat2, nbr_mat2]..]
        """
        pass
        # TODO

class Machine(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./Name_Files/machine.txt")

    def __init__(self):

        # Infos basiques
        self.nom = self.genNom()

        # Production
        self.operations_realisables = [] # TODO
        self.commandes = [[]]

        # Stockage/Mat réservés pour la machine
        self.materiaux = [[]]

    def __repr__(self):
        return "{} : {}, {}".format(
                self.nom, self.operations_realisables, self.materiaux)

    def genNom(self):
        nom = random.choice(Machine.noms_dispo)
        # On efface le nom de la liste pour éviter les doublons
        # de noms de machines
        Machine.noms_dispo.remove(nom)

        return nom

class Transport(object):

    def __init__(self, depart, arrivee, materiaux, produits):

        self.materiaux = materiaux
        self.produits  = produits

        self.depart  = depart  # Fournisseur de départ
        self.arrivee = arrivee # Stock d'arrivée
        self.tps_trajet = 1    #TODO fontion calcul tps trajet

    def __repr__(self):
        return "{} -> {} : {} et {}".format(
                self.depart, self.arrivee, self.materiaux, self.produits)

    def updateTempsTrajet(transports):
        for trans in transports:
            trans.tps_trajet -= 1

    def arrivees(transports, stocks):
        """ Si un transport est terminé, ses materiaux et produits sont
        transférés dans le stock de destination.
        """
        for trans in transports:
            if trans.tps_trajet == 0:

                for stock in stocks:
                    if stock.nom == trans.arrivee:
                        Transport.ajout(trans.materiaux, stock.materiaux)
                        Transport.ajout(trans.produits, stock.produits)

                transports.remove(trans) # Retire le transport de la liste

    def ajout(liste_depart, liste_arrivee):
        """ Ajoute les valeur d'une liste à la 2e, au bon endroit.
        Entree : une liste [["nom", val], ..]
                 une liste [["nom", val], ..]
        """

        for couple_depart in liste_depart:
            for couple_arrivee in liste_arrivee:
                if couple_depart[0] == couple_arrivee[0]:
                    couple_arrivee[1] += couple_depart[1]

class Stock(object):

    # Localisations
    localisations = ["Paris"]

    def __init__(self):

        self.nom = "The Edge" #TODO
        self.localisation = self.genLocalistation()

        self.capacite  = 0 #TODO
        self.cout      = 0 # Cout par unite #TODO

        self.materiaux = [[]]
        self.produits  = []

    def __repr__(self):
        return "{} - {}, {}".format(
                self.nom, self.materiaux, self.produits)

    def genLocalistation(self):
        """ Etabli la localisation du Fournisseur
        """

        loc = random.choice(Stock.localisations)

        # On efface la localisation de la liste car elles sont uniques.
        Stock.localisations.remove(loc)

        return loc


####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :
    pass
