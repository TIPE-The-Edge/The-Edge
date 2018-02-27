#! /usr/bin/env python
#-*- coding: utf-8 -*-


####################################
#>>> AUTEUR  : LAFAGE Adrien
#>>> SUJET   : R&D / INNOVATION
#>>> DATE    : 19/01/2018
####################################


############| IMPORTS |#############
import os
import sys
import unittest
from math import *

from objets import *
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

|→ TÂCHES EFFECTUEES :

    - Terminé

|→ REMARQUES :

    - Garder en tête que les fonctions qui
      qui affichent ou demande à l'utilisateur
      une entrée devront être remplacées pour
      l'intégration dans l'application.
"""
####################################

#| Provisoire |#

#-Population

pop_1 = Population("Jeunes", 300, 15, 15, 5)
pop_2 = Population("Actifs", 2000, 40, 25,10)
pop_3 = Population("Seniors", 1800, 25, )
populations = [pop_1, pop_2, pop_3]

#-Chercheurs

chercheurs =[ Individu() for i in range(3)]

#-Produits 

produits = []

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
        rep = "tres enthousiaste"

    #>>> Sortie <<<#
    return((rep,ref))


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
        for pop in populations :
            reference = aleaLoiNormale(esperance=50, ecart_type=16.6)
            self.appreciation.append([appreciation(reference),pop.nom])
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
        if self.cible in [pop.nom for pop in populations] :
            return(False)
        else :
            return(True)

    def __repr__(self) :

        return("{} | {}".format(self.appreciation, self.cible))


class Prototype(object):

    def __init__(self, chercheurs, appreciation, cible):

        # La liste des chercheurs parcipant au projet
        self.chercheurs = chercheurs
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

    def creaMater(self) :
        """
        FONCTION       : Defini les materiaux necessaires
                         a la creation du prototype
        ENTREES        : Un prototype sans materiaux
        SORTIE         : Le prototype avec des materiaux
                         associes.
        REMARQUES      :
        TEST UNITAIRE  : ...
        """
        for i in range(random.randint(3, 7)):
            self.materiaux.append(Materiau())

        return(self)

    def creaOpera(self) :
        """
        FONCTION       : Defini les operations necessaires
                         a la creation du prototype
        ENTREES        : Un prototype sans operations
        SORTIE         : Le prototype avec des operations
                         associees.
        REMARQUES      :
        TEST UNITAIRE  : ...
        """

        for i in range(random.randint(2, 5)):
            self.operations.append(Operation())

        return(self)

    def develop(self) :
        """
        FONCTION       : Défini les matériaux, les opérations ainsi que
                         le coût d'un prototype.
        ENTREES        : Un prototype
        SORTIE         : Le prototype avec des matériaux et des opérations.
        """
        Prototype.creaMater(self)
        Prototype.creaOpera(self)
        return(self)

    def appr_to_uti(self) :
        """
        FONCTION       : Convertie pour chaque population l'appréciation
                         en utilité.
        ENTREES        : Un prototype (Prototype) et une liste de
                         population (Population list)
        SORTIE         : L'utilité associée à ces appréciations
        REMARQUES      :
        TEST UNITAIRE  : ("OK"/"...")
        """

        utilite = []

        for app in self.appreciation :
            val = ((app[0][1])**2)*(4/500)
            utilite.append([app[1], val])

        return(utilite)

    def __repr__(self) :
        return("{} | {} - {} | {} : {}". format(self.appreciation,
              self.cible, self.materiaux, self.operations, self.cout))


class Projet(object):

    def __init__(self, chercheurs) :

        # La liste des chercheurs parcipant au projet
        self.chercheurs = chercheurs
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
            self.avancement = self.avancement-palier
            # On passe à la phase suivante du projet
            self.phase += 1

        return(self)

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
        if self.avancement >= palier and self.attente==False :
            # On initialise l'appétence des consommateurs
            #| vis à vis du concept.
            Concept.sondage(self.produit)

            # // WARNING : Afficher les résultats du sondage sur l'interface //
            print(self.produit)
            # // WARNING //

            Projet.verifPhase1(self, palier, utilisateur)

        elif self.avancement >= palier and self.attente==True :

            Projet.verifPhase1(self, palier, utilisateur)

        else :
            # On fait avancer le projet.
            self.avancement += progres(chercheurs)

        return(self)

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

        if utilisateur==True :

            # // Warning  : déduire le coût de création du prototype au budjet de l'utilisateur //
            self.attente = False
            # On réinitialise l'avancement
            self.avancement = 0
            # On passe à la phase suivante du projet
            self.phase += 1

        else :
            self.attente = True

        return(self)

    def phase2(self, palier, utilisateur) :
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

        if self.avancement >= palier and self.attente==False :

            # On change le concept en prototype
            self.produit = Prototype(self.chercheurs, (self.produit.appreciation),
                                    (self.produit.cible))

            Prototype.develop(self.produit)

            Projet.verifPhase2(self, utilisateur)

        elif self.avancement >= palier and self.attente==True :

            Projet.verifPhase2(self, utilisateur)

        else :
            # On fait avancer le projet.
            self.avancement += progres(chercheurs)

        return(self)

    def phase3(self, palier, utilisateur) :
        """
        FONCTION       : Modélise le développement du projet à
                         la phase 3.
        ENTREES        : Un projet (Projet), un palier (int),
                         et une entrée utilisateur
        SORTIE         : Le projet mis à jour
        REMARQUES      : Une phase qui va modéliser le temps
                         de construction du prototype.
        """

        if self.avancement >= palier :
            # On réinitialise l'avancement
            self.avancement = self.avancement-palier
            # On passe à la phase suivante du projet
            self.phase += 1

        else :
            # On fait avancer le projet.
            self.avancement += progres(chercheurs)

        return(self)

    def verifPhase4(self, utilisateur) :
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

        if utilisateur==True :
            # Dépot d'un brevet (Warning : frais supplémentaires)

            # Initialisation de l'utilité
            utilite = Prototype.appr_to_uti(self.produit)
            # Transformation en produit
            self.produit = Produit(produits, utilite, self.produit.materiaux,
                                   self.produit.operations, self.produit.cible)
            # Le projet est fini.
            self.phase += 1
        return(self)

    def phase4(self, palier, utilisateur) :
        """
        FONCTION       : Modélise le développement du projet à
                         la phase 4. Proposition de mise à l'essai
                         du prototype.
        ENTREES        : Un projet (Projet), un palier (int),
                         et une entrée utilisateur
        SORTIE         : Le projet mis à jour
        """

        if self.avancement >= palier :
            Projet.verifPhase4(self, utilisateur)

        elif utilisateur==True and self.essai == False :

            # // Warning : diminuer le capital d'une certaine somme //

            # On met le prototype à l'essai
            self.essai = True
            # On fait avancer le projet avec le bonus de la mise
            #| à l'essai du produit.
            self.avancement += progres(chercheurs) + 0.5*progres(chercheurs)

        else :
            # On fait avancer le projet.
            self.avancement += progres(chercheurs)

    def progression(self, liste, utilisateur) :
        """
        FONCTION       : Modélise la progression du projet et
                         selon la phase de développement, appelle
                         les fonctions qui sont associées.
        ENTREES        : Un projet (Projet), une liste des différents
                         paliers (int list) et une entrée utilisateur.
        SORTIE         : Le projet mis à jour.
        """

        if self.phase == 1 :
            Projet.phase1(self, liste[0], utilisateur)

        elif self.phase == 2 :
            Projet.phase2(self, liste[1], utilisateur)

        elif self.phase == 3 :
            Projet.phase3(self, liste[2], utilisateur)

        elif self.phase == 4 :
            Projet.phase4(self, liste[3], utilisateur)

        return(self)

    def __repr__(self) :

        return("Phase : {} | Progression : {}".format(self.phase, self.avancement))


####################################
########| TESTS UNITAIRES |#########
####################################

class Test(unittest.TestCase) :

    def test_appreciation(self) :

        #>>> Test 1 <<<#

        reponse = ("indifférents",40)
        test = appreciation(40)
        self.assertEqual(test, reponse)

    def test_ciblage(self) :

        #>>> Test 1 <<<#

        reponse = "Jeunes"
        test = Concept()
        test = Concept.ciblage(test, "Jeunes")
        self.assertEqual(test.cible, reponse)


####################################
###########| PROGRAMME |############
####################################

if __name__=="__main__" :
    # On effectue les tests unitaires.
    # unittest.main()

    for cherch in chercheurs :
        print(cherch)

    print(compRecherche(chercheurs))

    test = Projet(chercheurs)

    paliers = [80, 100, 100, 100]

    # PHASE 1
    while test.phase == 1 :
        print(test)
        test = Projet.progression(test, paliers, input("Phase 1 : "))

    print(test.produit)

    # PHASE 2
    while test.phase == 2 :
        print(test)
        test = Projet.progression(test, paliers, True)

    print(test.produit)

    # PHASE 3
    while test.phase == 3 :
        print(test)
        test = Projet.progression(test, paliers, True)

    print(test.produit)

    # PHASE 4
    while test.phase == 4 :
        print(test)
        test = Projet.progression(test, paliers, True)

    produit = 0

    if test.phase == 5 :
        produit = test.produit

    print(produit)
    print(produit.utilite)
