import random
import os
import operator
from outils import *



produits = []
populations = []
materiaux = []
individus = []
operations = []

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

        # Compétences # A COMPLETER?
        self.competence_groupe      = aleaLoiNormale(5, 1.6) # Capacité à travailler en groupe
        self.competence_recherche   = aleaLoiNormale(5, 1.6) # Efficacité à la recherche
        self.competence_direction   = aleaLoiNormale(5, 1.6) # Capacité à diriger une équipe

        self.conges  = 0 # BONUS
        self.horaire = 0 # temps de travail # BONUS

        # Ajoute à la liste
        individus.append(self)

    def __repr__(self):
        return "{} - {} {}, {} ans. {}. recherche {}. groupe {}. leader {}".format(
                self.id, self.prenom, self.nom, self.age, self.genre, self.competence_recherche, 
                self.competence_groupe, self.competence_direction)

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
		self.nom = nom

		self.revenu = revenu # (Adrien)
		self.nombre = nombre # (Adrien)

		self.produits = [[]] # nbr d'utilisateur qui ont déja acheté par produit

		# Ajoute à la liste
		populations.append(self)


class Produit(object):

    def __init__(self, utilite, materiaux, operations, cible):
        self.nom = self.genNom()

        self.utilite    = utilite # Par population (0-100)
        self.materiaux  = materiaux # materiaux et quantités nécessaires
        self.operations = operations   # Opérations nécessaires

        self.cible = cible
        self.prix     = 0 # Prix fixé
        self.tps_adoption  = 0 # ADRIEN

        self.marche = False # Le produit est sur le marché ou non
        self.age    = 0     # Temps sur le marché du produit

        self.nbr_ameliorations = 0
        self.concurence = 0 # BONUS

        # Ajoute à la liste
        produits.append(self)

    def __repr__(self):
        return "Nom : {} \n utilite : {} \n materiaux : {} \n operation : {}".format(self.nom, self.utilite, self.materiaux, self.operations)

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

if __name__=="__main__" :

	a = Individu()
	print(a)