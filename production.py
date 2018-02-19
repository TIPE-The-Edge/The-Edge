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

Commande()
    tempsRestant() & updateCommandes()
        On pourra laisser le temps en flottant et faire en sorte que
        les commandes dans les machines s'enchainent meme en pleine
        semaine.
        Actuellement si la machine peut produire 1200 prod par
        semaine, et qu'elle a de quoi en fabriquer 1201, elle va mettre
        2 semaines à terminer (soit une semaine ou elle va produire 1
        et ne sera pas dispo pour une autre commande.)

"""

""" PROBLEMS
"""

""" NOTES
"""
####################################################
###################| CONSTANTES |###################
####################################################

MINS_PAR_SEMAINE = 2400

####################################################
###################| FONCTIONS |####################
####################################################
def fonction():
    """ A quoi sert la fonction. Comment elle marche
    Entrée :
    Variables :
    Sortie :
    Vérifié par :
    """

def ajout(liste_depart, liste_arrivee):
    """ Ajoute les valeur d'une liste à la 2e, au bon endroit.
    Entree : une liste [["nom", val], ..]
             une liste [["nom", val], ..]
    """

    for couple_depart in liste_depart:
        for couple_arrivee in liste_arrivee:
            if couple_depart[0] == couple_arrivee[0]:
                couple_arrivee[1] += couple_depart[1]

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
        self.utilisateur = None

        # Production
        self.operations_realisables = [] # TODO
        self.commandes = []

        # Stockage/Mat réservés pour la machine
        # self.materiaux = [[]] #TOBE REMOVED (les materiaux sont dans les commandes)

    def __repr__(self):
        return "{} : {}, {}".format(
                self.nom, self.operations_realisables, self.materiaux)

    def genNom(self):
        nom = random.choice(Machine.noms_dispo)
        # On efface le nom de la liste pour éviter les doublons
        # de noms de machines
        Machine.noms_dispo.remove(nom)

        return nom

    def genCommande(usines, usine, materiaux, operations, produit):
        for usi in usines:
            if usi.nom == usine:
                usi.commandes.append(Commande(materiaux, operations, produit))

class Commande(object): # Commandes faites aux machines

    def __init__(self, materiaux, operations, produit):

        self.materiaux = materiaux  # Liste de liste [[mat, nbr_mat], ...]
        self.produit   = produit    # Produit final

        # Process
        self.recette          = self.produit.materiaux # Type et nbr de mat par produit
        self.mins_par_produit = Commande.minsParProduit(operations, self.produit) # Tps en minutes pour 1 produit

        # Infos
        self.prodRestants() # Pour savoir combien on peut encore produire.
        self.prod_totaux = self.prod_restants # Pour l'affichage

        self.tps_restant = self.prod_restants * self.mins_par_produit # En minutes
        self.tps_total   = self.tps_restant # Pour affichage

    def __repr__(self):
        return "{} -> {}".format(self.prod_restants, self.produit.nom)
        # return "{} -> {}".format(self.prod_restants, self.tps_restant)

    def minsParProduit(operations, produit):
        """ retourne le nombre de produits qui peuvent être fabriqués
        chaque semaine.
        """
        somme = 0 # Somme des durées des opérations necessaires à
                  # la fabrication d'un produit.
        for ope in produit.operations: # parcours la liste [["ope", nbr_ope], ...]
            for op in operations:      # parcours la liste des operations
                if op.nom == ope[0]:
                    somme += op.duree * ope[1] # Ajoute la duree de l'operation
                                               # multiplié par le nombre de
                                               # fois qu'elle est nécéssaire

        return(somme)

    def prodRestants(self):
        """ Cherche combien le nombre de mat de la machine, lui permettra de
        faire de produits.
        """
        for mat in self.materiaux:
            if mat[0] == self.recette[0][0]:
                self.prod_restants = mat[1] / self.recette[0][1]

    def updateCommandes(machines, stock):
        for mac in machines:
            if len(mac.commandes) > 0: # La machine a au moins une commande.

                Commande.process(mac.commandes, stock)

    def process(commandes, stock):
        mins = MINS_PAR_SEMAINE

        while mins > 0 and len(commandes) > 0:

            if commandes[0].tps_restant == 0: # Supprime les commandes terminées
                commandes.remove(commandes[0])

            if len(commandes) > 0:
                mins = commandes[0].update(stock, mins)

    def update(self, stock, mins):

        mins = self.transforme(stock, mins)
        # new_mins = mins - self.tps_restant

        self.prodRestants() # MàJ le nbr de produits restants
        self.tps_restant = self.prod_restants * self.mins_par_produit

        return(mins)

    def transforme(self, stock, mins):
        """ Met à jour les materiaux.
        Entrée : l'objet stock où seront stockés les produits
                 minutes disponibles

        """
        new_materiaux = []
        temps = min(mins, self.tps_restant) # Temps réel dépensé
        nbr_prod = int(temps / self.mins_par_produit) # Nbr réel de produits fabriqués

        for mat in self.materiaux:
            for mat_r in self.recette:
                if mat[0] == mat_r[0]:
                    new_materiaux.append([mat[0], mat[1] - nbr_prod * mat_r[1]])

        # MàJ des materiaux de la machine
        self.materiaux = new_materiaux

        # Ajout des produits terminés au stock
        ajout([[self.produit.nom, nbr_prod]], stock.produits)

        return(mins-temps)

class Transport(object):

    def __init__(self, depart, arrivee, materiaux, produits, tps_trajet):

        self.materiaux = materiaux
        self.produits  = produits

        self.depart  = depart  # Nom du Fournisseur de départ
        self.arrivee = arrivee # Nom du Stock d'arrivée

        self.tps_trajet = tps_trajet # fontion calcul tps trajet

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
                        ajout(trans.materiaux, stock.materiaux)
                        ajout(trans.produits, stock.produits)

                transports.remove(trans) # Retire le transport de la liste

class Stock(object):

    # Localisations
    localisations = ["Paris"]

    def __init__(self):

        self.nom = "The Edge"
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
