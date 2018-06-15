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
from world.outils import *
from world.lecture import *

""" TO DO LIST

"""

""" PROBLEMS

"""

""" NOTES
"""
####################################################
###################| CONSTANTES |###################
####################################################

MINS_PAR_SEMAINE = 2400 # 60 mins * 8 h * 5 jours

####################################################
###################| FONCTIONS |####################
####################################################
def prodTotaux(produit, liste_mat):
    """ Indique le nombre de produit que l'on peut produire avec les
    des materiaux donnés.
    Entrée : un produit (objet)
             la liste de materiaux et leur nombre
    Sortie : le nombre de produit que l'on peut produire avec les
                materiaux donnés.
    """

    for mat in liste_mat:
        if mat[0] == produit.materiaux[0][0]:
            prod_totaux = round(mat[1]/produit.materiaux[0][1])

    return(prod_totaux)

def listeMat(stock, produit):
    """ Renvoie la liste et leur quantité des materiaux du stock concernant un
    certain produit.
    Entrée : un stock (objet)
             un produit (objet)
    """
    liste = []

    for mat in produit.materiaux:
        for mater in stock.materiaux:
            if mat[0] == mater[0]:
                liste.append(mater)

    return(liste)

def addMachine(machines, machine):
    """
    FONCTION       : Ajoute une machine à la liste machines
    ENTREES        : La liste machines et une machine
    SORTIE         : La liste machines à jour
    """

    # On crée une copie de la machine
    engine = Machine(machine.operations_realisables)
    engine.nom = machine.nom
    engine.prix = machine.prix
    # On ajoute la machine aux machines de l'entreprise
    machines.append(engine)

####################################################
###################| CLASSES |######################
####################################################

class Fournisseur(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./world/Name_Files/fournisseurs.txt")

    # Localisations
    localisations = ["Paris",
                    "New York",
                    "Los Angeles",
                    "Hong Kong",
                    "Berlin",
                    "Amsterdam"]

    def __init__(self):

        self.nom = self.genNom()
        self.localisation = self.genLocalistation()

        self.materiaux_vendu = [mat[0] for mat in readLineCSV("materiaux.csv","pays",self.localisation,["materiaux"])]

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

    def approvisionnement(transports, couts, fournisseur, destination, commande, argent):
        """ Créé un cout et créé un objet transport à partir des données d'une
        commande de materiaux. Renvoie l'arfent restant.
        Entrée : le fournisseur (objet)
                 la destination (objet)
                 la commande [[mat1, nbr_mat1], [mat2, nbr_mat2]..]
                 Les fonds disponibles
        Sortie : argent restant
        """

        cout_mat       = Fournisseur.coutMateriaux(fournisseur, commande)
        cout_transport = Fournisseur.coutTransport(fournisseur, destination)
        tps_transport  = Fournisseur.tpsTransport(fournisseur, destination)

        transports.append(Transport(fournisseur.nom,
                                    destination.nom,
                                    commande,       # liste de materiaux (& valeur)
                                    [],             # liste de produits
                                    tps_transport))

        couts.append(["Achats de materiaux", cout_mat])
        couts.append(["Cout transports", cout_transport])

        argent -= (cout_mat+cout_transport)

        return(argent)

    def coutMateriau(fournisseur, materiau):
        """ Retourne le prix du'un materiau, pour un fournisseur donné.
        """
        liste = [mat for mat in readLineCSV("materiaux.csv","materiaux",materiau,["pays", "cout unitaire"])]

        for elt in liste:
            if elt[0] == fournisseur.localisation:
                return float(elt[1])

    def coutMateriaux(fournisseur, commande):
        """ Calcule le cout total des materiaux de la commande.
        Entrée : la commande [[mat1, nbr_mat1], [mat2, nbr_mat2]..]
        """
        somme = 0
        for com in commande:
            prix_mat = Fournisseur.coutMateriau(fournisseur, com[0])
            somme += com[1] * prix_mat

        return(somme)

    def coutTransport(fournisseur, destination):
        """
        FONCTION       : Retourne le coût de transport entre le
                         stock d'un fournisseur et sa destination.
        ENTREES        : un fournisseur (Fournisseur) et une destination
                         (string).
        SORTIE         : Le coût du trajet en ??? (float).
        TEST UNITAIRE  : ...
        """
        fournisseurs = readLineCSV("transport.csv",
                                   "fournisseur",
                                   fournisseur.localisation,
                                   ["fournisseur","destination","cout"])

        for four in fournisseurs :
            if four[1]==destination.localisation :
                return(float(four[2]))

        # Si le trajet n'existe pas dans le fichier de données.
        return(None)

    def tpsTransport(fournisseur, destination):
        """
        FONCTION       : Retourne le temps de transport entre le
                         stock d'un fournisseur et sa destination.
        ENTREES        : Un fournisseur (string) et une destination
                         (string).
        SORTIE         : Le temps du trajet en semaine (float)
        TEST UNITAIRE  : ...
        """

        fournisseurs = readLineCSV("transport.csv", "fournisseur", fournisseur.localisation, ["fournisseur","destination","temps"])

        for four in fournisseurs :
            if four[1]==destination.localisation :
                return(float(four[2]))


        # Si le trajet n'existe pas dans le fichier de données.
        return(None)

    def listeFour(fournisseurs, materiau):
        """ Renvoie la liste des fournisseurs qui vendent le materieau entré.
        Entrée : le nom d'un materiau
        """

        # Vérifie dans la base de données quel pays vend le materiau.
        pays = [four[0] for four in readLineCSV("materiaux.csv","materiaux",materiau,["pays"])]

        # Check dans les fournisseurs ceux qui sont dans les pays vendeurs.
        liste = [four for four in fournisseurs if four.localisation in pays]

        return(liste)

class Machine(object):

    # Liste des noms existants
    noms_dispo = readNameFile("./world/Name_Files/machine.txt")

    # Initialisation des identifiants
    id = 0

    def __init__(self, liste_operations):

        # Identifiant pour le repérer rapidement dans la liste des individus
        self.id = Machine.id
        Machine.id += 1

        # Infos basiques
        self.nom = self.genNom()
        self.utilisateur = None  # (objet)

        # Production
        self.operations_realisables = liste_operations # liste des opérations du produit
        self.commandes = []

        self.materiaux = [[]]

        self.prix = 0 # TODO

    def __repr__(self):
        return "\n {} --> {} {} : \n{}".format(
                self.utilisateur, self.id, self.nom, self.operations_realisables)

    def genNom(self):
        nom = random.choice(Machine.noms_dispo)
        # On efface le nom de la liste pour éviter les doublons
        # de noms de machines
        Machine.noms_dispo.remove(nom)

        return nom

    def verifOperations(machines, id_machine, produit):
        """ Vérifie que les opérations nécessaires sont bien dans la liste
        des opérations réalisables par la machine.

        INUTILE?
        """
        for mac in machines:
            if mac.id == id_machine: # La machine qui nous interresse.

                for ope in produit.operations:
                    if ope[0] not in mac.operations_realisables:
                        return(False)
                return(True)

    def verifUtilisateur(machines, id_machine):
        """ Vérifie si une machine a un utilisateur.
        Entrée : l'id de la machine
        """
        for mac in machines:
            if mac.id == id_machine: # La machine qui nous interresse.

                if mac.utilisateur == None:
                    return(False)
                else:
                    return(True)

    def nbrProd_to_NbrMat(produit, nombre):
        """Retourne la liste avec les nombres de materiaux respectifs pour
        un certain nombre de produits
        Entrée : le produit (objet)
                 le nombre désiré
        Sortie : la liste des nombre de mats [[nom_mat, nbr_mat], ...]
        """

        liste = []

        for mat in produit.materiaux:
            liste.append([mat[0], mat[1] * nombre])

        return(liste)

    def ajusteUnMatStock(stock, materiau):
        """ Ajuste la quantité d'un materiau en fonction de la quantité
        dans le stock.
        """
        for mat_s in stock.materiaux:
            if materiau[0] == mat_s[0]:
                return(min(materiau[1], mat_s[1]))

    def ajusteMatStock(stock, materiaux):
        """ Ajuste les nombres de materiaux en fonction des quantités présentes
        dans le stock.
        """
        new_materiaux = []

        for mat in materiaux:
            for mat_s in stock.materiaux:
                if mat[0] == mat_s[0]:
                    new_materiaux.append([mat[0], min(mat[1], mat_s[1])])

        return(new_materiaux)

    def ajusteMatProd(produit, materiaux):
        """ Ajuste les nombres de materiaux en fonction des proportions à
        respecter pour la fabrication d'un produit.
        """
        new_materiaux = []
        coefs = []

        for mat in materiaux:
            for mat_p in produit.materiaux:
                if mat[0] == mat_p[0]:
                    coefs.append(int(mat[1]/mat_p[1]))

        mult = min(coefs)
        new_materiaux = [[mat_p[0], mat_p[1]*mult] for mat_p in produit.materiaux]

        return(new_materiaux)

    def ajusteCommande(stock, produit, materiaux):
        """ Ajuste les materiaux en fonction du stock,
        ajuste les materiaux donnés dans les bonnes proportions.
        Entree: Liste de machines
                Nom de la machine
                Stock (objet)
                Produit (objet)
                Liste des materiaux entrés [["nom_mat", nbr_mat], ..]
        Sortie: Liste de materiaux ajustée [["nom_mat", nbr_mat], ..]
        """

        new_materiaux = Machine.ajusteMatStock(stock, materiaux)
        new_materiaux = Machine.ajusteMatProd(produit, new_materiaux)

        return(new_materiaux)

    def genCommande(machines, operations, liste_materiaux, id_machine, stock, produit):
        """
        Entrée : la liste des materiaux utilisés et leur nombre
                 l'id de la machine utilisée
                 le stock contenant les materiaux (objet)
                 le produit à créer (objet)
        """
        # Créé la commande.
        for mac in machines:
            if mac.id == id_machine:
                mac.commandes.append(Commande(liste_materiaux, operations, produit))

        # Retire les mat du stock.
        retire(liste_materiaux, stock.materiaux)

    def listeMach(machines, produit):
        """ Renvoie la liste des machines qui réalise les opérations nécessaires à un produit.
        Entrée : Un produit (objet)
        """
        liste = []

        for mach in machines:
            # Verifie que toutes les opérations nécessaires au produit se
            # trouvent dans les opé réalisables de la machine.
            verif_all =  all(ope[0] in mach.operations_realisables for ope in produit.operations)

            if verif_all:
                liste.append(mach)

        return(liste)

    def maxMat(mat_stock, recette):
        """ Retourne le nombre max de fois que l'on peut faire la recette
        à partir des ressources du stock.
        ENTREE: la liste des mat du stock et leur nom (concernés par la recette)
                la recette
        """

        nombre = mat_stock[0][1] # init

        for mat in recette:
            for mater in mat_stock:
                if mat[0] == mater[0]: # Meme nom
                    nombre = min(nombre, int(mater[1]/mat[1]))

        return(nombre)

class Commande(object): # Commandes faites aux machines

    def __init__(self, materiaux, operations, produit):

        self.materiaux = materiaux  # Liste de liste [[mat, nbr_mat], ...]
        self.produit   = produit    # Produit final (objet)

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

    def updateCommandes(machines, individus, stock):
        for mac in machines:
            # Vérifie que la machine a au moins une commande et un utilisateur.
            if len(mac.commandes) > 0 and mac.utilisateur != None:

                Commande.process(mac.commandes, stock, mac.utilisateur)

            # Enlève les utilisateurs des machines qui n'ont pas de commandes.
            if len(mac.commandes) == 0 and mac.utilisateur != None:
                # Reset le role de l'individu
                for ind in individus:
                    if ind.id == mac.utilisateur.id:
                        ind.role = None
                # Eleve l'utilisateur de la machine
                mac.utilisateur = None

    def capaciteUtilisateur(utilisateur):
        """ Renvoie la capacité de travail que peut fournir un utilisateur.
        """

        x = utilisateur.competence_production

        # mins est l'équivalent en minute de travail que peut fournir l'utilisateur
        mins = int((300/9)*(x**2) - (300/9)*x + MINS_PAR_SEMAINE) # Polynome du second degré

        return(mins)

    def process(commandes, stock, utilisateur):

        # mins est l'équivalent en minute de travail que peut fournir l'utilisateur
        mins = capaciteUtilisateur(utilisateur)

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
        Entrée : le Stock (objet) où seront stockés les produits
                 nbr de minutes disponibles

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
        self.temps_total = tps_trajet

    def __repr__(self):
        return "{} -> {}, {} : {} et {}".format(
                self.depart, self.arrivee, self.tps_trajet, self.materiaux, self.produits)

    def updateTempsTrajet(transports):
        for trans in transports:
            trans.tps_trajet -= 1

    def arrivees(transports, stocks, notifications):
        """ Si un transport est terminé, ses materiaux et produits sont
        transférés dans le stock de destination. Et la liste des transports
        restants est retournée.
        """
        copy = []

        for trans in transports:

            if trans.tps_trajet == 0:

                for stock in stocks:
                    if stock.nom == trans.arrivee:
                        ajout(trans.materiaux, stock.materiaux)
                        ajout(trans.produits, stock.produits)

                texte = ""

                mats = trans.materiaux
                for i in range(len(mats)):
                    texte += str(mats[i][1]) + "x " + mats[i][0]
                    if i+1 != len(mats):
                        texte += ", "

                prods = trans.produits

                if len(mats) > 0 and len(prods) > 0:
                    texte += " et "

                for i in range(len(prods)):
                    texte += str(prods[i][1]) + "x " + prods[i][0]
                    if i+1 != len(prods):
                        texte += ", "

                notifications.append([1,"Production : transport terminée", "Le transport de " + texte + " entre " + trans.depart + " et " + trans.arrivee + " est bien arrivé."])

            else:
                copy.append(trans)

        return(copy)

class Stock(object):

    # Localisations
    localisations = ["Paris"]

    def __init__(self):

        self.nom = "The Edge"
        self.localisation = self.genLocalistation()

        self.capacite  = 0 #BONUS
        self.cout      = 0 # Cout par unite #TODO

        self.materiaux = [[]]
        self.produits  = [[]]

    def __repr__(self):
        return "{}:\n\nMat : {}\n\nProd : {}".format(
                self.nom, self.materiaux, self.produits)

    def genLocalistation(self):
        """ Etabli la localisation du Fournisseur
        """

        loc = random.choice(Stock.localisations)

        # On efface la localisation de la liste car elles sont uniques.
        Stock.localisations.remove(loc)

        return loc


####################################
########| TESTS UNITAIRES |#########
####################################


class Test(unittest.TestCase) :


    def test_coutTransport(self) :

        #>>> Test 1 <<<#

        reponse = 500
        test = Fournisseur.coutTransport("Paris", "Amsterdam")
        self.assertEqual(test, reponse)

        #>>> Test 2 <<<#

        reponse = None
        test = Fournisseur.coutTransport("Toulouse", "Paris")
        self.assertEqual(test, reponse)


####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :

    # Tests unitaires
    #unittest.main()
    pass
