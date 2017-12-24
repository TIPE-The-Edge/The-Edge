import random
import os
import operator


produits = []
populations = []
materiaux = []
individus = []

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
        return "{} - {} {}, {} ans. {}. recherche : {}. groupe : {}".format(
                self.id, self.prenom, self.nom, self.age, self.genre, self.competence_recherche, self.competence_groupe)

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


###| Création des populations |###
pop_1 = Population("Jeunes", 300, 15)
pop_2 = Population("Actifs", 2000, 40)
pop_3 = Population("Seniors", 1800, 25)

"""
pop_1A = 
pop_2A = 
pop_3A = 

pop_1B = 
pop_2B = 
pop_3B = 
"""




if __name__=="__main__" :

	a = Individu()
	print(a)