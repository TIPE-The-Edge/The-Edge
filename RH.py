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


""" TO DO LIST

RH :
    update()
        self.cout_emploi : changer le 0 par la valeur des charges indirectes
            (voir NOTES)

        self.part_masse_sal : récupérer le budget total (LC)

    Etablir le cout des locaux (location de locaux)

Rajouter les couts dans la liste des couts pour LC.

"""

""" NOTES
Pour LC :
    Couts générés :
        "cout RH"

Cout de l'emploi :
    Les charges indirectes :
        - Le coût des locaux / le nombre d’employés
        - Ses coûts de formation # Bonus
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
        return "nbr employés: {} \nbonheur moy: {} \nage moy: {} \n\nexp start up moy: {} \nexp R&D moy: {} \n\nnbr arrivees: {} \ntaux arrivees: {} \nnbr departs: {} \ntaux departs: {} \ntaux rotation: {} \n\ncout formations: {} \nmoy formations: {} \n\nsalaire moy: {} \nmasse sal brute: {} \nmasse sal nette: {} \ncout emploi: {} \ncout moy emploi: {} \npart masse sal: {}".format(
                self.nbr_employes, self.bonheur_moy, self.age_moy, self.exp_start_up_moy, self.exp_RetD_moy, self.nbr_arrivees, self.taux_arrivees, self.nbr_departs, self.taux_departs, self.taux_rotation, self.cout_formations, self.moy_formations, self.salaire_moy, self.masse_sal_brute, self.masse_sal_nette, self.cout_emploi, self.cout_moy_emploi, self.part_masse_sal)

    def __init__(self):
        self.nbr_employes     = None
        self.bonheur_moy      = None
        self.age_moy          = None

        # Experience
        self.exp_start_up_moy = None
        self.exp_RetD_moy     = None

        # Flux
        self.nbr_arrivees  = None
        self.taux_arrivees = None
        self.nbr_departs   = None
        self.taux_departs  = None
        self.taux_rotation = None

        # Formation
        self.cout_formations = None # BONUS
        self.moy_formations  = None # BONUS

        # Couts
        self.salaire_moy     = None
        self.masse_sal_brute = None
        self.masse_sal_nette = None
        self.cout_emploi     = None
        self.cout_moy_emploi = None
        self.part_masse_sal  = None

    def update(self, individus, departs, seuil_arrivees, seuil_departs):
        self.nbr_employes     = RH.nbr(individus)
        # self.bonheur_moy      = RH.bonheurMoyen(individus) #BONUS
        self.age_moy          = RH.ageMoyen(individus)

        # Experience
        self.exp_start_up_moy = RH.expStartUpMoyenne(individus)
        self.exp_RetD_moy     = RH.expRetDMoyenne(individus)

        # Flux
        self.nbr_arrivees  = RH.arrivees(individus, seuil_arrivees)
        self.taux_arrivees = round(self.nbr_arrivees / self.nbr_employes, 1)
        self.nbr_departs   = RH.departs(departs, seuil_departs)
        self.taux_departs  = round(self.nbr_departs / self.nbr_employes, 1)
        self.taux_rotation = round((self.nbr_arrivees + self.nbr_departs)/self.nbr_employes, 1) # turn over

        # Formation
        self.cout_formations = None # Fonds investis dans la formation # BONUS
        self.moy_formations  = None # Moyenne de formations par employé # BONUS

        # Couts
        self.salaire_moy     = RH.salaireMoyen(individus)
        self.masse_sal_brute = RH.masseSalBrute(individus) # Masse salariale brute
        self.masse_sal_nette = RH.masseSalNette(individus) # Masse salariale nette
        self.cout_emploi     = round(self.masse_sal_brute + (self.masse_sal_brute*0.42) + 0, 2)
                                # Cout total des employés
                                # (salaire net + charges sociales salariales)
                                # + charges patronales
                                # + charges indirectes
        self.cout_moy_emploi = round(self.cout_emploi/self.nbr_employes, 2) # Coût moyen par emploi
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

    def expRetDMoyenne(individus):
        moyenne = 0
        for ind in individus:
            moyenne += ind.exp_RetD
        return (round(moyenne/len(individus), 2))

    def ageMoyen(individus):
        moyenne = 0
        for ind in individus:
            moyenne += ind.age
        return (round(moyenne/len(individus), 2))

    def arrivees(individus, seuil):
        """ Nombre d'employé arrivés pendant les "seuil" dernières semaines.
        Entrée    : la liste des individus
                    le nombre de semaine. (ex: "2" permettra de trouver les
                        employés arrivés pendant les 2 dernières semaines.)
        Variables : acc : compte les individus correspondants aux critères.
        Sortie    : le nombre d'individus correspondants aux critères.
        """
        acc = 0
        for ind in individus:
            if ind.exp_startup <= seuil:
                acc += 1
        return acc

    def licencier(individus, departs, id):
        """ Place un individu dans la liste departs et le supprime de
        individus.
        """
        for ind in individus:
            if ind.id == id:
                departs.append([ind.id, 0])
                individus.remove(ind)

    def recruter(individus, candidats, id):
        for cand in candidats:
            if cand.id == id:
                individus.append(cand)
                candidats.remove(cand)

    def updateDeparts(departs):
        """ Met à jour le temps de départ des individus dans la liste departs.
        """
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
        return (round(moyenne/len(individus), 2))

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

    def coutsRH(couts, lesRH):
        couts.append(["cout RH", lesRH.cout_emploi])



####################################################
##################| PROGRAMME |#####################
####################################################

if __name__ == "__main__" :
    pass
