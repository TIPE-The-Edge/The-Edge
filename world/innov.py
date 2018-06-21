#! /usr/bin/env python
#-*- coding: utf-8 -*-


####################################
#>>> AUTEUR  : LAFAGE Adrien
#>>> SUJET   : R&D / INNOVATION
#>>> DATE    : 15/06/2018
####################################


############| IMPORTS |#############
import os
import sys
import unittest
from math import *

from world.objets import *
from world.outils import *
from world.lecture import *
from world.production import *
####################################


##########| DESCRIPTION |###########
"""
Fichier rassemblant les différentes
fonctions permettant de modéliser le
processus d'innovation d'un produit :

I/   Phase 1 :
      - Création d'un objet Concept
      - Analyse du marché
      - Ciblage d'une population /
        cible du projet
      - Génération de coûts par rapport
        à une campagne marketing.

II/  Phase 2 :
      - A la fin de cette phase l'utilisateur
        doit décider s'il veut commencer la
        construction d'un prototype ou non.
      - Génération de coûts

III/ Phase 3 :
      - Développement du prototype. (génération
        des matériaux et des opérations)

IV/ Phase 4 :
      - Développement du produit (fixation de
        l'utilité).
      - Option de mise à l'essai.
      - Génération des coûts pour le brevet.

Une fois ces 4 étapes validées les
produit est prêt à être vendu.
CEPENDANT
D'après les recherches effectuées les
chances de succès sont inférieures à
50%, voire la plupart du temps de
l'ordre de 1-10%. Telle devra être la
probabilité que le produit soit rentable.
A TESTER.
"""
####################################


#############| NOTES |##############
"""
|→ HYPOTHESE :
    On considère que nos chercheurs
    ne sont jamais à cours d'idées. Seuls
    les temps relatifs à l'élaboration du
    projet, au développement technique et
    aux tests de validation pourront être
    extrêmement différents en fonction des
    projets.

|→ REMARQUES :

    - Garder en tête que les fonctions qui
      qui affichent ou demande à l'utilisateur
      une entrée devront être remplacées pour
      l'intégration dans l'application.
"""
####################################


####################################
###########| FONCTIONS |############
####################################

def appreciation(ref) :
    """
    FONCTION       : Retourne un couple avec d'une
                     part le résultat du sondage et
                     d'autre part l'indice de l'appreciation
    ENTREES        : Une référence (int)
    SORTIE         : Un couple (appréciation(string), référence(int))
    TEST UNITAIRE  : OK
    """
    #>>> Initialisation des variables locales <<<#
    rep = ""
    #>>> Corps de la fonction <<<#
    if ref <= 50 :
        rep = "indifférents"
    elif 50<ref<=75 :
        rep = "intéressés"
    elif 75<ref<=90 :
        rep = "enthousiastes"
    else :
        rep = "tres enthousiastes"

    #>>> Sortie <<<#
    return((rep,ref))

def delProject(projets, employes, identifiant) :
    """
    FONCTION       : Supprime un projet à la liste des projets
                     en cours.
    ENTREES        : La liste de projets (Projet/Ameliore list) et un identifiant
                     (int).
    SORTIE         : La liste des projets mise à jour (Projet/Ameliore list).
    TEST UNITAIRE  : ...
    """

    for i in range(len(projets)) :
        if projets[i].id==identifiant :
            index = i

    for emp in employes :
        if emp.projet == projets[i].nom :
            emp.projet = None
            emp.role = None

    del projets[index]

def addChercheurs(projet, employes, identifiant) :
    """
    FONCTION       : Ajoute un chercheur libre au Projet.
    ENTREES        : Un projet (Projet/Ameliore), les chercheurs libres
                     (Individu list) et identifiant (int).
    SORTIE         : Le projet avec un chercheur en plus et la liste
                     des chercheurs mis à jour (Individu list)
    TEST UNITAIRE  : ...
    """

    for i in range(len(employes)) :
        if employes[i].id==identifiant :
            employes[i].projet = projet.nom
            employes[i].role = "R&D"

    return(projet, employes)

def delChercheurs(projet, employes, identifiant) :
    """
    FONCTION       : Supprime un chercheur d'un Projet.
    ENTREES        : Un projet (Projet), les chercheurs libres
                     (Individu list) et identifiant (int).
    SORTIE         : Le projet avec un chercheur en moins et la liste
                     des chercheurs mis à jour (Individu list)
    TEST UNITAIRE  : ...
    """
    for i in range(len(employes)) :
        if employes[i].id==identifiant :
            employes[i].projet = None
            employes[i].role = None

    return(projet, employes)

def allProgression(projets, employes, paliers, produits, materiaux, operations, argent) :
    """
    FONCTION       : Fait progresser tous les projets de la liste de projets.
    ENTREES        : Une liste de projets (Projet/Ameliore list).
    SORTIE         : La liste des projets mise à jour (Projet/Ameliore list).
    """
    # Initialisation de la liste des dépenses
    depenses = []
    # Initialisation des couts
    couts=['', 0]

    for proj in projets :
        if proj.id < 0 :
            couts = Ameliore.progression(proj, False)
        else :
            if proj.phase == 1 :
                if proj.avancement<paliers[0] :
                    couts, argent = Projet.progression(proj, employes, paliers, "", produits, materiaux, operations, argent)

                else  :
                    if proj.produit.appreciation==[] :
                        couts, argent = Projet.progression(proj, employes, paliers, "", produits, materiaux, operations, argent)
                        depenses.append(couts)

                    couts, argent = Projet.progression(proj, employes, paliers, "", produits, materiaux, operations, argent)

            elif proj.phase == 2 :
                if proj.avancement<paliers[1] :
                    couts, argent = Projet.progression(proj, employes, paliers, False, produits, materiaux, operations, argent)
                else :
                    couts, argent = Projet.progression(proj, employes, paliers, False, produits, materiaux, operations, argent)

            elif proj.phase == 3 :
                couts, argent = Projet.progression(proj, employes, paliers, None, produits, materiaux, operations, argent)

            elif proj.phase == 4 :
                if proj.avancement<paliers[3] :
                    if proj.essai==False :
                        couts, argent = Projet.progression(proj, employes, paliers, False, produits, materiaux, operations, argent)
                    else :
                        couts, argent = Projet.progression(proj, employes, paliers, None, produits, materiaux, operations, argent)

                else :
                    couts, argent = Projet.progression(proj, employes, paliers, False, produits, materiaux, operations, argent)

        # On ajoute les frais à notre liste de dépense
        if couts[1]!=0 :
            depenses.append(couts)

    return(projets, depenses, argent)

def genNotif(projets, paliers) :
    """
    FONCTION       : Génère les notifications de la partie R&D
    ENTREES        : La liste des projets et la liste des paliers
    SORTIE         : Une liste des notifications.
    """
    notifications = []

    for proj in projets :
        if proj.id >= 0 :
            if proj.phase == 1 :
                if proj.avancement>=paliers[0] :
                    # print("Le projet "+str(proj.nom)+" requiert votre attention !")
                    notification = [0, "Projet : Phase terminée", "Le projet "+str(proj.nom)+" a achevé la phase "+nomPhase(proj.phase, proj.id)+".", proj.id]
                    notifications.append(notification)

            elif proj.phase == 2 :
                if proj.avancement>=paliers[1] :
                    # print("Le projet : "+str(proj.nom)+" requiert votre attention !")
                    notification = [0, "Projet : Phase terminée", "Le projet "+str(proj.nom)+" a achevé la phase "+nomPhase(proj.phase, proj.id)+".", proj.id]
                    notifications.append(notification)

            elif proj.phase == 4 :
                if proj.avancement<paliers[3] :
                    if proj.essai==False :
                        # print("Le projet : "+str(proj.nom)+" requiert votre attention !")
                        notification = [0, "Projet : Phase terminée", "Le projet "+str(proj.nom)+" a achevé la phase "+nomPhase(proj.phase, proj.id)+".", proj.id]
                        notifications.append(notification)

                else :
                    # print("Le projet : "+str(proj.nom)+" requiert votre attention !")
                    notification = [0, "Projet : Phase terminée", "Le projet "+str(proj.nom)+ " a achevé la phase "+nomPhase(proj.phase, proj.id)+".", proj.id]
                    notifications.append(notification)
        else :

            if proj.avancement>=proj.palier and proj.phase != 5 :
                notification = [0, "Projet : Amélioration terminée", "Le projet "+str(proj.nom)+" a été achevé.", proj.id]
                notifications.append(notification)

    return(notifications)

def selectProject(projets, identifiant) :
    """
    FONCTION       :
    ENTREES        :
    SORTIE         :
    TEST UNITAIRE  : ...
    """
    for proj in projets :
        if proj.id == identifiant :
            return(proj)
    return(None)

def avance(projets, paliers, employes) :
    """
    FONCTION       : Fait progresser l'avancement de tous les projets.
    ENTREES        : La liste des projets, la liste des paliers 
    SORTIE         : La liste des projets mise à jour.
    """
    for proj in projets :
        # On fait avancer le projet.
        proj.avancement += progres(employes, proj.nom)
        if proj.id < 0 :
            if proj.avancement > proj.palier :
                proj.avancement = proj.palier
        else :
            if proj.avancement > paliers[proj.phase -1] :
                proj.avancement = paliers[proj.phase -1]

    return(projets)

def completedProject(projets, produits, employes, magasin, stock) :
    """
    FONCTION       :
    ENTREES        :
    SORTIE         :
    TEST UNITAIRE  : ...
    """
    for proj in projets :
        # On ajoute les produits finis à notre liste de produit
        if proj.phase == 5 :
            if proj.id > 0 :
                produits.append(proj.produit)
                ope = [op[0] for op in proj.produit.operations]
                magasin.append(Machine(ope))
            
            if proj.id < 0 :
                # TODO : Il faudra retirer l'ancien produit des stocks.
                pass
            stock.produits.append([proj.produit.nom, 0])
            delProject(projets, employes, proj.id)

def genAutoProduit(population, produits, materiaux, operations, magasin, argent, stock) :
    """
    FONCTION       : Créé un produit automatiquement
    ENTREES        : La population cible (string), la liste des produits,
                     la liste des matériaux et des opération.
    SORTIE         : La liste des produits avec un produit en plus
    """
    #>>> Initialisation des variables locales <<<#

    # On initialise une liste vide d'employés
    employes = []
    # On initialise la liste des paliers
    paliers=[1,1,1,1]
    # On crée un projet nommé "proje"
    projet = Projet("projet")
    # On ajoute ce projet à la liste des projets
    projets = [projet]

    #>>> Corps de la fonction <<<#
    projet.avancement = 1
    cout, argent = Projet.progression(projet, employes, paliers, population, produits, materiaux, operations, argent)
    cout, argent = Projet.progression(projet, employes, paliers, population, produits, materiaux, operations, argent)
    for i in range(3):
        projet.avancement = 1
        cout, argent = Projet.progression(projet, employes, paliers, True, produits, materiaux, operations, argent)

    # On ajoute le produit à la liste des produits
    completedProject(projets, produits, employes, magasin, stock)


####################################
############| CLASSES |#############
####################################

class Concept(object) :

    def __init__(self) :

        # On initialise l'appréciation du concept
        #| par les clients (différentes populations)
        self.appreciation = []
        # Désignera une population.
        self.cible = ""

    def sondage(self) :
        """
        FONCTION       : Crée une appréciation sur le concept pour chaque
                         population.
        ENTREES        : Un concept
        SORTIE         : Un concept avec une appréciation.
        REMARQUES      : Utilisation de la loi normale pour la
                         génération de l'appréciation.
        """
        for pop in ["Jeunes","Actifs","Seniors"] :
            reference = aleaLoiNormale(esperance=50, ecart_type=16.6)
            self.appreciation.append([appreciation(reference),pop])

        return(self)

    def ciblage(self, population) :
        """
        FONCTION       : Defini quelle population le concept cible-
                         t-il.
        ENTREES        : Un concept (Concept) et des populations
                         (Population list)
        SORTIE         : Le concept avec une cible définie
                         (Concept)
        REMARQUES      : Il faudra prendre en compte ici le cout
                         d'une campagne marketing.
        TEST UNITAIRE  : OK
        """
        # On modifie la cible marketing du projet
        self.cible = population
        return(self)

    def effetMarketing(self) :
        """
        FONCTION       : Applique sur l'appréciation de la population
                         cible l'effet de la campagne marketing.
        ENTREES        : Un concept
        SORTIE         : Le concept avec une nouvelle appréciation
                         de la population cible.
        """
        for avis in self.appreciation :
            if avis[1] == self.cible :
                avis[0] = appreciation(avis[0][1]+aleaLoiNormale(esperance=5, ecart_type=1.6))
        return(self)

    def verif(self) :
        """
        FONCTION       : Vérifie si la population cible est à définir
        ENTREES        : Un concept
        SORTIE         : Le booléen indiquant si la population cible
                         est à définir.
        """
        if self.cible in ["Jeunes","Actifs","Seniors"] :
            return(False)
        else :
            return(True)

    def __repr__(self) :

        return("{} | {}".format(self.appreciation, self.cible))


class Prototype(object):

    def __init__(self, appreciation, cible):

        # L'opinion des consommateurs sur le produit
        self.appreciation = appreciation
        # La population ciblée par le produit
        self.cible = cible
        # Les matériaux
        self.materiaux = []
        # Les opérations
        self.operations = []
        # Le coût de fabrication
        self.cout = 0

    def creaMater(self, materiaux) :
        """
        FONCTION       : Défini les materiaux necessaires à la creation du prototype.
        ENTREES        : Un prototype sans materiaux.
        SORTIE         : Le prototype avec des materiaux associés.
        REMARQUES      : Nombre de matériaux créés entre 3 et 5.
        """

        for i in range(random.randint(3, 5)):
            # On récupère aléatoirement un matériaux
            new = materiaux[random.randint(0, (len(materiaux)-1))]
            # Tant que le matériaux qu'on récupère existe dans la liste
            # des matériaux du prototype, on en récupère un autre
            while new.nom in [ m[0] for m in self.materiaux] :
                new = materiaux[random.randint(0, (len(materiaux)-1))]

            # On ajoute le matériaux ainsi trouvé à la liste des matériaux
            # du prototype
            self.materiaux.append([new.nom, random.randint(1, 5)])

    def creaOpera(self, operations) :
        """
        FONCTION       : Defini les operations necessaires
                         a la creation du prototype
        ENTREES        : Un prototype sans operations
        SORTIE         : Le prototype avec des operations
                         associees.
        REMARQUES      : nb opérations entre 2 et 4.
        TEST UNITAIRE  : ...
        """

        for i in range(random.randint(2, 3)):
            # On récupère aléatoirement une opération
            new = operations[random.randint(0, (len(operations)-1))]
            # Tant que l'opérations qu'on récupère existe dans la liste
            # des opérations du prototype, on en récupère une autre
            while new.nom in [o[0] for o in self.operations] :
                new = operations[random.randint(0, (len(operations)-1))]

            # On ajoute l'opération ainsi trouvée à la liste des opérations
            # du prototype
            self.operations.append([new.nom, random.randint(3, 5)])

    def creaCout(self) :
        """
        FONCTION       : Defini les coûts générés pour la
                         création d'un prototype.
        ENTREES        : Un prototype (Prototype)
        SORTIE         : Le prototype avec un cout de production
        TEST UNITAIRE  : ...
        """

        for mat in self.materiaux :
            # Initialise le cout moyen du matériaux
            couts=0
            # On récupère les données concernant les prix
            recup = readLineCSV("materiaux.csv", "materiaux", mat[0], ["cout unitaire"])
            # On fait une moyenne de ces prix
            for prix in recup :
                couts += float(prix[0])*mat[1]
            couts = couts/(len(recup))
            # On ajoute le cout moyen du matériaux au cout total
            #| du prototype.
            self.cout += couts

    def develop(self, materiaux, operations) :
        """
        FONCTION       : Défini les matériaux, les opérations ainsi que
                         le coût d'un prototype.
        ENTREES        : Un prototype
        SORTIE         : Le prototype avec des matériaux et des opérations.
        """
        Prototype.creaMater(self, materiaux)
        Prototype.creaOpera(self, operations)
        Prototype.creaCout(self)

    def apprToUti(self) :
        """
        FONCTION       : Convertie pour chaque population l'appréciation
                         en utilité.
        ENTREES        : Un prototype (Prototype) et une liste de
                         population (Population list)
        SORTIE         : L'utilité associée à ces appréciations
        TEST UNITAIRE  : OK
        """

        utilite = []

        for app in self.appreciation :
            val = ((app[0][1])**2)*(1/125)
            utilite.append([app[1], val])

        return(utilite)

    def __repr__(self) :
        return("{} | {} - {} | {} : {}". format(self.appreciation,
              self.cible, self.materiaux, self.operations, self.cout))


class Projet(object):

    # Initialisation des identifiants
    id=1

    def __init__(self, nom) :

        # Initialise l'identifiant du Projet
        self.id = Projet.id
        Projet.id += 1
        # Initialise le nom du Projet
        self.nom = nom
        # Génération d'un produit à l'initialisation
        #| du projet.
        self.produit = Concept()
        self.avancement = 0
        self.phase = 1
        self.attente = False
        self.essai = False

    def verifPhase1(self, palier, utilisateur) :
        """
        FONCTION       : Récupère une entrée utilisateur, si
                         celle-ci permet de fixer une population
                         cible alors on applique l'effet du ciblage
                         et on passe à la phase 2
        ENTREES        : Un projet (Projet) et une entrée utilisateur
                         (string)
        SORTIE         : Le projet qui tient compte de l'entrée
                         utilisateur.
        """

        # On fixe la population cible à l'aide de l'entrée
        #| utilisateur.
        Concept.ciblage(self.produit, utilisateur)

        # On vérifie que l'utilisateur a entré la population cible
        self.attente = Concept.verif(self.produit)

        # Passage phase 2 ?
        if self.attente==False :
            # On applique l'effet du ciblage sur l'opinion
            #| des consommateurs vis à vis du concept.
            Concept.effetMarketing(self.produit)
            # On réinitialise l'avancement
            self.avancement = 0
            # On passe à la phase suivante du projet
            self.phase += 1

    def phase1(self, palier, utilisateur) :
        """
        FONCTION       : Modélise le développement du projet à
                         la phase 1.
        ENTREES        : Un projet (Projet), un palier (int),
                         et une entrée utilisateur
        SORTIE         : Le projet mis à jour
        REMARQUES      : La progression du projet s'arrête si
                         l'utilisateur ne donne pas de population
                         cible quand l'avancement du projet est
                         supérieur au palier.
        """
        # Initialisation des coûts
        couts = [self.nom, 0]

        if self.avancement == palier and self.attente==False :
            # On initialise l'appétence des consommateurs
            #| vis à vis du concept.
            Concept.sondage(self.produit)

            Projet.verifPhase1(self, palier, utilisateur)

        elif self.avancement == palier and self.attente==True :

            Projet.verifPhase1(self, palier, utilisateur)

        return(couts)

    def verifPhase2(self, utilisateur) :
        """
        FONCTION       : Récupère une entrée utilisateur, si
                         celle-ci est True alors on déduit du
                         capital le coût de production d'un
                         prototype et on passe à la phase 3.
        ENTREES        : Un projet, une entrée utilisateur.
        SORTIE         : Si l'entrée est valide (True), retourne
                         le projet initialisé pour la phase suivante.
                         Sinon met le projet en attente.
        """
        # Initialisation des coûts
        couts = [self.nom, 0]

        if utilisateur==True :

            # Coût de création du prototype
            couts=[self.nom+" : Création du prototype" , self.produit.cout]

            self.attente = False
            # On réinitialise l'avancement
            self.avancement = 0
            # On passe à la phase suivante du projet
            self.phase += 1

        else :
            self.attente = True

        return(couts)

    def phase2(self, palier, utilisateur, materiaux, operations) :
        """
        FONCTION       : Modélise le développement du projet à
                         la phase 2.
        ENTREES        : Un projet (Projet), un palier (int),
                         et une entrée utilisateur
        SORTIE         : Le projet mis à jour
        REMARQUES      : La progression du projet s'arrête si
                         l'utilisateur ne donne pas son accord
                         pour le lancement de la construction
                         du prototype.
        """
        couts = [self.nom, 0]

        if self.avancement == palier and self.attente==False :

            # On change le concept en prototype
            self.produit = Prototype(self.produit.appreciation,
                                     self.produit.cible)

            Prototype.develop(self.produit, materiaux, operations)

            couts = Projet.verifPhase2(self, utilisateur)

        elif self.avancement == palier and self.attente==True :

            couts = Projet.verifPhase2(self, utilisateur)

        return(couts)

    def phase3(self, palier) :
        """
        FONCTION       : Modélise le développement du projet à
                         la phase 3.
        ENTREES        : Un projet (Projet), un palier (int),
                         et une entrée utilisateur
        SORTIE         : Le projet mis à jour
        REMARQUES      : Une phase qui va modéliser le temps
                         de construction du prototype.
        """

        # Initialisation des couts
        couts = [self.nom, 0]

        if self.avancement == palier :

            # On réinitialise l'avancement
            self.avancement = self.avancement-palier
            # On passe à la phase suivante du projet
            self.phase += 1

        return(couts)

    def verifPhase4(self, utilisateur, produits) :
        """
        FONCTION       : Récupère une entrée utilisateur, si
                         celle-ci est True alors on déduit les
                         frais de brevet et le prototype devient
                         un produit. Sinon rien.
        ENTREES        : Un projet et une entrée utilisateur.
        SORTIE         : Le projet mis à jour.
        REMARQUES      : Si l'entrée est True cela marque la fin
                         du projet.
        """

        # Initialisation des couts
        couts = [self.nom, 0]

        if utilisateur==True :
            # Dépot d'un brevet (Warning : frais supplémentaires)
            couts = [self.nom+" : Brevet",50]
            # Initialisation de l'utilité
            utilite = Prototype.apprToUti(self.produit)
            # Transformation en produit
            self.produit = Produit(produits, utilite, self.produit.materiaux,
                                   self.produit.operations, self.produit.cible)
            # Le projet est fini.
            self.phase += 1
        else :
            self.attente=True

        return(couts)

    def phase4(self, employes, palier, utilisateur, produits) :
        """
        FONCTION       : Modélise le développement du projet à
                         la phase 4. Proposition de mise à l'essai
                         du prototype.
        ENTREES        : Un projet (Projet), un palier (int),
                         et une entrée utilisateur
        SORTIE         : Le projet mis à jour
        """
        couts = [self.nom, 0]
        if self.avancement == palier :
            couts = Projet.verifPhase4(self, utilisateur, produits)

        elif utilisateur==True and self.essai == False :

            # // Warning : diminuer le capital d'une certaine somme //
            couts = [self.nom+" : Mise à l'essai", 50]
            # On met le prototype à l'essai
            self.essai = True
            # On fait avancer le projet avec le bonus de la mise
            #| à l'essai du produit.
            self.avancement += 0.5*progres(employes, self.nom)
            # A COMMENTER
            if self.avancement > palier :
                self.avancement = palier

        return(couts)

    def progression(self, individus, paliers, utilisateur, produits, materiaux, operations, argent) :
        """
        FONCTION       : Modélise la progression du projet et
                         selon la phase de développement, appelle
                         les fonctions qui sont associées.
        ENTREES        : Un projet (Projet), une liste des différents
                         paliers (int list) et une entrée utilisateur.
        SORTIE         : Le projet mis à jour.
        """
        # Initialisation des couts
        couts = [self.nom, 0]

        if self.phase == 1 :
            couts = Projet.phase1(self, paliers[0], utilisateur)
        elif self.phase == 2 :
            couts = Projet.phase2(self, paliers[1], utilisateur, materiaux, operations)

        elif self.phase == 3 :
            couts = Projet.phase3(self, paliers[2])

        elif self.phase == 4 :
            couts = Projet.phase4(self, individus, paliers[3], utilisateur, produits)
        
        # On met à jour l'argent de l'utilisateur
        argent -= couts[1]

        return(couts, argent)

    def __repr__(self) :

        return("{}.{} // Phase : {} | Progression : {}".format(self.id,self.nom,self.phase, self.avancement))


class Ameliore() :

    id = -1

    def __init__(self, produit, nom) :

        # Initialise l'identifiant du Projet
        self.id = Ameliore.id
        Ameliore.id -= 1

        # Initialise le nom de l'amélioration
        self.nom = nom

        self.produit = produit
        self.avancement = 0
        self.palier = Ameliore.fixePalier(self)
        self.phase = 1
        self.attente = False

    def changeMateriaux(self) :
        """
        FONCTION       : Supprime un élément de la liste des matériaux.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : Une amélioration dont la liste des matériaux
                         du produit est diminué de 1.
        """

        if sum([mat[1] for mat in self.produit.materiaux])>len(self.produit.materiaux) :

            mat = self.produit.materiaux[random.randint(0, (len(self.produit.materiaux)-1))]

            while mat[1] < 2 :
                mat = self.produit.materiaux[random.randint(0, (len(self.produit.materiaux)-1))]

            mat[1] -= 1


        return(self)

    def changeOperations(self) :
        """
        FONCTION       : Supprime un élément de la liste des opérations.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : Une amélioration dont la liste des opérations
                         du produit est diminué de 1.
        """
        if sum([ope[1] for ope in self.produit.operations])>len(self.produit.operations) :

            ope = self.produit.operations[random.randint(0, (len(self.produit.operations)-1))]

            while ope[1] < 2 :
                ope = self.produit.operations[random.randint(0, (len(self.produit.operations)-1))]

            ope[1] -= 1

        return(self)

    def changeUtilite(self) :
        """
        FONCTION       : Augmente l'utilité de la population ciblée.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : Une amélioration dont l'utilité de la
                         population ciblée a augmenté.
        REMARQUES      : L'augmentation est inversement
                         proportionnelle au nombre d'améliorations.
        """

        bonus = aleaLoiNormale(10, 1.6)-(self.produit.nbr_ameliorations)
        if bonus < 0 :
            bonus = 0

        for uti in self.produit.utilite :
            if uti[0] == self.produit.cible :
                uti[1]+=bonus

        return(self)

    def update(self) :
        """
        FONCTION       : Procède à l'amélioration du produit en fonction
                         du résultat obtenu aléatoirement.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : L'amélioration dont le produit est amélioré.
        """

        valeur = aleaLoiNormale(50, (16/1+(self.produit.nbr_ameliorations)))

        if valeur < 34 and len(self.produit.materiaux)>1 :
            Ameliore.changeMateriaux(self)

        elif 66<valeur and len(self.produit.operations)>1:
            Ameliore.changeOperations(self)

        else :
            Ameliore.changeUtilite(self)

        self.produit.nbr_ameliorations += 1
        return(self)

    def fixePalier(self) :
        """
        FONCTION       : Fixe le nombre de points d'avancement
                         requis pour procéder à l'amélioration
                         du produit.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : Une amélioration dont le palier est fixé.
        """

        return(100)

    def verif(self, utilisateur) :
        """
        FONCTION       :
        ENTREES        :
        SORTIE         :
        """
        # Initialisation des coûts
        couts = [self.nom, 0]

        if utilisateur==True :
            # Dépot d'un brevet (Warning : frais supplémentaires)
            couts = [self.nom+" : Brevet",50]
            # On améliore une caractéristique de notre produit
            self = Ameliore.update(self)
            if self.produit.nbr_ameliorations > 1 :
                self.produit.nom = self.produit.nom[:-1] + str(self.produit.nbr_ameliorations+1)
            else :
                self.produit.nom = self.produit.nom+" v"+str(self.produit.nbr_ameliorations+1)
            self.phase = 5
            self.produit.develop = False
        else :

            self.attente=True

        return(couts)

    def progression(self, utilisateur) :
        """
        FONCTION       : Modélise le développement de l'amélioration
                         d'un produit.
        ENTREES        : Une amélioration (Ameliore)
        SORTIE         : L'amélioration mise à jour.
        """
        # Initialisation des coûts
        couts = [self.nom, 0]

        if self.avancement >= self.palier :
            couts = Ameliore.verif(self, utilisateur)

        return(couts)

    def __repr__(self) :
        return("{}. {} // Produit en développement : {} | Progression : {}".format(self.id, self.nom, self.produit.nom, self.avancement))

####################################
########| TESTS UNITAIRES |#########
####################################

class Test(unittest.TestCase) :

    def test_appreciation(self) :

        #>>> Test 1 <<<#

        reponse = ("indifférents", 40)
        test = appreciation(40)
        self.assertEqual(test, reponse)

    def test_ciblage(self) :

        #>>> Test 1 <<<#

        reponse = "Jeunes"
        test = Concept()
        test = Concept.ciblage(test, "Jeunes")
        self.assertEqual(test.cible, reponse)

    def test_apprToUti(self) :

        #>>> Test 1 <<<#

        reponse = [["Jeunes",80],["Actifs",80], ["Seniors",80]]
        appreciation = [ [["tres enthousiastes", 100], "Jeunes"], [["tres enthousiastes", 100], "Actifs"], [["tres enthousiastes", 100], "Seniors"]]
        test = Prototype(appreciation, "")
        test = Prototype.apprToUti(test)
        self.assertEqual(test, reponse)


####################################
###########| PROGRAMME |############
####################################

if __name__=="__main__" :
    unittest.main()
