#! /usr/bin/env python
#-*- coding: utf-8 -*-

######################
# Python 3.5.2
# Author: Maxence BLANC
# Last modified : 09/2017
######################

# IMPORTS
import os
import sys

################################################
############ BIBLIOTHEQUE HIGHSCORE ############
################################################

""" TO DO LIST ✔✘

"""


""" PROBLEMS
"""


""" NOTES

On ne peut pas garantir l'ordre des clés du dico
càd, un dico peut etre affiché {'nom': 'Jo', 'score': '0'}
                            ou {'score': '0', 'nom': 'Jo'}

Les fonction à changer en fonction du format de fichier sont :
 - readMode()
 - writeMode()
 - nouveauJoueur()

Fichier type :
Nom1 Score1
Nom2 Score2
...
"""

####################################################
### CONSTANTES ###
####################################################

FICHIER_HIGHSCORE = "highscore.txt"
SEPARATEUR = " "

####################################################
### /// CONSTANTES ###
####################################################



####################################################
### FONCTIONS ###
####################################################

def readMode():
    """ Ouvre un fichier de type : "nom score .." et en extrait les données.
    Entree : rien, on connait deja le nom du fichier.
    Sortie : une liste de dictionnaires
             -> [{"nom":le_nom, "score": le_score, ..}, ..]
             ou
             une liste vide
    """
    if os.path.exists(FICHIER_HIGHSCORE): # Le fichier existe

        # Récupération des données
        entree = open(FICHIER_HIGHSCORE,"r") # Fichier de score voulu
        contenu_entree = entree.readlines()
        entree.close()

        # On transforme l'entrée en liste d'élément pour chaque ligne.
        # .strip('\n') retire tout les \n de fin de ligne.
        fichier = [ligne.strip('\n').split(SEPARATEUR) for ligne in contenu_entree]

        # On créé le dico à partir du fichier en donnant à chaque élément
        # une clé. C'est ici que l'on établi le format du fichier d'entrée,
        # par exemple le premier élément sera le nom et le 2eme le score.
        dico = [{"nom":ligne[0],"score":ligne[1]} for ligne in fichier]

        return(dico)

    else:
        return([])

def writeMode(dicos):
    """ Créé ou écrase le fichier existant de scores et y écrit la liste des
    scores.
    Entree : la liste de dicos
    """
    sortie = open(FICHIER_HIGHSCORE,"w")

    for dico in dicos:

        # Pour chaque dico, on écrit une ligne avec le format correspondant.
        # Par exemple le premier élément sera le nom et le 2eme le score.
        # A noter que pour que les données doivent etre des str()
        sortie.write(SEPARATEUR.join([str(dico["nom"]), str(dico["score"])]) +"\n")
    sortie.close()

def changeDico(dicos, nom_utilisateur, type_valeur, valeur):
    """ Change la valeur d'un type de valeur pour un utilisateur.
    Entree : la liste de dicos
             le nom de l'utilisateur
             le type de score que l'on veut changer
             la nouvelle valeur
    """
    for utilisateur in dicos:
        if utilisateur["nom"] == nom_utilisateur:
            utilisateur[type_valeur] = valeur
            continue

def modDico(dicos, nom_utilisateur, type_valeur, valeur):
    """ Modifie relativement la valeur d'un type de valeur pour un utilisateur.
    Entree : la liste de dicos
             le nom de l'utilisateur
             le type de score que l'on veut modifier
             la valeur relative
    """
    for utilisateur in dicos:
        if utilisateur["nom"] == nom_utilisateur:
            utilisateur[type_valeur] = int(utilisateur[type_valeur]) + valeur
            continue

def verifUser(dicos, nom_utilisateur):
    """
    Vérifie si un joueur est déjà dans le fichier.
    Entrée : le nom du joueur
    Sortie : un booléen qui est vrai quand le joueur existe dans le fichier.
    """
    for utilisateur in dicos:
        if utilisateur["nom"] == nom_utilisateur:
            return True
    return False

def newUser(dicos, nom_utilisateur):
    """ Ajoute un joueur à la liste des dicos. Dépend du format.
    Entrée : le nom du joueur
    """
    dicos.append({"nom" : nom_utilisateur, "score" : "0"})

def removeUser(dicos, nom_utilisateur):
    for utilisateur in dicos:
        if utilisateur["nom"] == nom_utilisateur:
            scores.remove(utilisateur)
            continue

def triScores(dicos, comparateur, ordre):
    """ Trie le dictionnaire dans l'ordre décroissant.
    Entree : La liste de dictionnaires.
             Le comparateur (c'est le critère de tri, par exemple le score)
    Sortie : La liste de dictionnaires triée.
    """
    # On trie le dico par le score des joueurs.
    # reverse=True permet d'avoir le trie dans l'ordre décroissant.
    scores_triés = sorted(dicos,
                          key=lambda player: player[comparateur],
                          reverse=ordre)
    return(scores_triés)

def affichage(dicos):
    """ Affichage console pour le dev.
    Entree : La liste de dictionnaires.
    """
    print("\n##### AFFICHAGE #####")
    for ligne in dicos:
        print(ligne)
    print("#####################\n")

def affichageAlt(dicos, comparateur, ordre):
    """ Affichage console pour le dev.
    Entree : La liste de dictionnaires.
    """
    print("\n########## " + comparateur.upper() + " ##########")
    for ligne in triScores(dicos, comparateur, ordre):
        print(ligne)
    print("#####################\n")

def effacer():
    """ Efface le Fichier de Highscores.
    """
    with open(FICHIER_HIGHSCORE, "w"):
        pass



def testFunction():
    while input("0/1? ") != "0":
        nom = input("nom : ")
        #score = int(input("score : "))
        #addLine([nom,score])
        newUser(nom)
        score = input("score : ")
        changeDico(scores, nom, "score", score)
        affichageAlt(scores, "nom", False)

####################################################
### /// FONCTIONS ###
####################################################

if __name__ == "__main__" :

    scores = readMode()

    affichage(scores)

    #testFunction()
    writeMode(scores)
    affichage(scores)
