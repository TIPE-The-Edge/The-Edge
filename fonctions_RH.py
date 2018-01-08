#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.4.2
# Author: Maxence BLANC
# Last modified : 12/2017
# Titre du Fichier : fonctions pour les RH
########################

# IMPORTS

# IMPORTS DE FICHIERS


""" TO DO LIST ✔✘
#randomQuote : "Une personne vivante est admirable." MB

RH :
    update()

"""

""" NOTES

Gérer les formations dans generators.py

RH():

    Listes des Infos RH :

        Couts :
            Coût moyen par emploi permanent
            Masse salariale brute
            Masse salariale nette
            Part de la masse salariale dans le budget de fonctionnement

        Formation :
            Niveau de qualification des employés
            Nombre d’agents bénéficiaires d’au moins une formation
            Fonds investis dans la formation

"""

""" BONUS
Travailleurs handicapés

Abscences :
    Taux d’absence
    Autres absences
    Coût des absences
    Nombre de jours travaillés dans l’année

Salaire :
    Primes
    Part des primes dans la rémunération

Riques :
    Maladie professionnelle
    Fréquence et de gravité
    Coûts financiers des accidents
    Hygiène
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

class RH(object):

    def __repr__(self):
        return "nbr employés: {} \nbonheur moy: {} \nexp moy: {} \nage moy: {} \n\nnbr arrivees: {} \ntaux arrivees: {} \nnbr departs: {} \ntaux departs: {} \ntaux rotation: {} \n\ncout formations: {} \nmoy formations: {} \n\nsalaire moy: {} \nmasse sal brute: {} \nmasse sal nette: {} \ncout emploi: {} \ncout moy emploi: {} \npart masse sal: {}".format(
                self.nbr_employes, self.bonheur_moy, self.exp_moy, self.age_moy, self.nbr_arrivees, self.taux_arrivees, self.nbr_departs, self.taux_departs, self.taux_rotation, self.cout_formations, self.moy_formations, self.salaire_moy, self.masse_sal_brute, self.masse_sal_nette, self.cout_emploi, self.cout_moy_emploi, self.part_masse_sal)

    def update(self, individus, departs, seuil_arrivees, seuil_departs):
        self.nbr_employes = RH.nbr(individus)
        self.bonheur_moy  = RH.bonheurMoyen(individus)
        self.exp_moy      = RH.expStartUpMoyenne(individus)
        self.age_moy      = RH.ageMoyen(individus)

        # Flux
        self.nbr_arrivees  = RH.arrivees(individus, seuil_arrivees)
        self.taux_arrivees = self.nbr_arrivees / self.nbr_employes
        self.nbr_departs   = RH.departs(departs, seuil_departs)
        self.taux_departs  = self.nbr_departs / self.nbr_employes
        self.taux_rotation = (self.nbr_arrivees + self.nbr_departs)/self.nbr_employes # turn over

        # Formation
        self.cout_formations = None # Fonds investis dans la formation
        self.moy_formations  = None # Moyenne de formations par employé

        # Couts
        self.salaire_moy     = RH.salaireMoyen(individus)
        self.masse_sal_brute = RH.masseSalBrute(individus) # Masse salariale brute
        self.masse_sal_nette = RH.masseSalNette(individus) # Masse salariale nette
        self.cout_emploi     = None # Cout total des employés
                               # (salaire net + charges sociales salariales)
                               # + charges patronales
                               # + charges indirectes
        self.cout_moy_emploi = None # Coût moyen par emploi permanent
        self.part_masse_sal  = None # Part de la masse salariale dans le budget de fonctionnement (LC)

    def nbr(individus):
        return len(individus)

    def bonheurMoyen(individus):
        moyenne = 0
        for ind in individus:
            moyenne += ind.bonheur
        return (moyenne/len(individus))

    def expStartUpMoyenne(individus):
        moyenne = 0
        for ind in individus:
            moyenne += ind.exp_startup
        return (moyenne/len(individus))

    def ageMoyen(individus):
        moyenne = 0
        for ind in individus:
            moyenne += ind.age
        return (moyenne/len(individus))

    def arrivees(individus, seuil):
        acc = 0
        for ind in individus:
            if ind.exp_startup <= seuil:
                acc += 1
        return acc

    def updateDeparts(departs):
        for dep in departs:
            dep[1] += 1

    def departs(departs, seuil):
        acc = 0
        for dep in departs:
            if dep[1] <= seuil:
                acc += 1
        return acc

    def salaireMoyen(individus):
        moyenne = 0
        for ind in individus:
            moyenne += ind.salaire
        return (moyenne/len(individus))

    def masseSalBrute(individus):
        somme = 0
        for ind in individus:
            somme += ind.salaire
        return(somme)

    def masseSalNette(individus):
        somme = 0
        for ind in individus:
            somme += (ind.salaire * 0.78)
        return(int(somme))



####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :
    pass
