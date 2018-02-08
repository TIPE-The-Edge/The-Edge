#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.5.2
# Author : Maxence BLANC
# Last modified : 01/18
# Title : Fonctions et classes de production
########################

# IMPORTS
import random

# IMPORTS DE FICHIERS
from outils import *


""" TO DO LIST
"""

""" PROBLEMS
"""

""" NOTES
"""

####################################################
##################| FONCTIONS |#####################
####################################################
def fonction():
    """ A quoi sert la fonction. Comment elle marche
    Entrée :
    Variables :
    Sortie :
    Vérifié par :
    """

####################################################
###################| CLASSES |######################
####################################################

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

    def approvisionnement(transports, materiaux, couts, fournisseur, destination, commande):
        """ Créé un cout et créé un objet transport à partir des données d'une
        commande de materiaux.
        Entrée : le nom du fournisseur
                 le nom de la destination
                 la commande [[mat1, nbr_mat1], [mat2, nbr_mat2]..]
        """

        cout_mat       = Fournisseur.coutMateriaux(materiaux, commande)
        cout_transport = Fournisseur.coutTransport(fournisseur, destination)
        tps_transport  = Fournisseur.tpsTransport(fournisseur, destination)

        transports.append(Transport(fournisseur,
                                    destination,
                                    commande,       # liste de materiaux (& valeur)
                                    [],             # liste de produits
                                    tps_transport))

        couts.append(["cout materiaux", cout_mat])
        couts.append(["cout transport", cout_transport])

    def coutMateriaux(materiaux, commande):
        somme = 0
        for com in commande:
            for mat in materiaux:
                if com[0] == mat.nom:
                    somme += com[1] * mat.prix

        return(somme)

    def coutTransport(fournisseur, destination): #TODO
        return(1)

    def tpsTransport(fournisseur, destination): #TODO
        return(1)

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

    def __init__(self, depart, arrivee, materiaux, produits, tps_trajet):

        self.materiaux = materiaux
        self.produits  = produits

        self.depart  = depart  # Nom du Fournisseur de départ
        self.arrivee = arrivee # Nom du Stock d'arrivée

        self.tps_trajet = tps_trajet #TODO fontion calcul tps trajet

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
        self.produits  = [[]]

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
