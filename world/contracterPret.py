#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.4.2
# Author:
# Last modified :
# Titre du Fichier :
########################

# IMPORTS
import pickle

####################################################
##################| FONCTIONS |#####################
####################################################

##################| VARIATION INTERET |#####################

def evolutionChiffreAff(chiffreAff,chiffreAffM2,chiffreAffM3):
    """
    Entrée : Les chiffres d'affaires des trois derniers mois
    Variables : chiffreAff: mois précédent
                chiffreAffM2: il y a 2 mois
                chiffreAffM3: il y a 3 mois
    Sortie : la croissance du chiffre d'affaire
    """
    moyenne = (chiffreAffM2 + chiffreAffM3)/2
    croissance = ((chiffreAff - moyenne)/moyenne)*100
    return croissance

def ptChiffreAff(evChiffreAff):
    """
    Entrée : l'evolution du chiffre d'affaire
    Variables : evChiffreAff: l'évolution du chiffre d'affaire
    Sortie : le nb de point par rapport au chiffre d'affaire
            (compris entre -4 et 4)
    """
    pt = (4*evChiffreAff)/100
    return min(4,max(-4,pt))

def evolutionResultatEx(resultatExercice,resultatExerciceM2,resultatExerciceM3):
    """
    Entrée : Le résultat de l'exercice du mois (disponible dans le bilan)
    Variables : resultatExercice: ce résultat
                resultatExerciceM2: il y a 2 mois
                resultatExerciceM3: il y a 3 mois
    Sortie : la croissance du résultat de l'exercice
    """
    moyenne = (resultatExerciceM2 + resultatExerciceM3)/2
    croissance = ((resultatExercice - moyenne)/moyenne)*100
    return croissance

def ptResultat(evResultatExercice):
    """
    Entrée : Le résultat de l'exercice du mois (disponible dans le bilan)
    Variables : evResultatExercice: l'évolution du résultat de l'exercice
    Sortie : le résultat de l'exercice en point
            (compris entre -4 et 4)
    """
    pt = (4*evResultatExercice)/100
    return min(4,max(-4,pt))

def rentabilite(evChiffreAff,evResultatExercice):
    """
    Entrée : L'évolution du chiffre d'affaire et du résultat
    Variables : evChiffreAff: sorti de evolutionChiffreAff
                evResultatExercice: sorti de evolutionResultatEx
    Sortie : la rentabilite en point
    """
    rentabilite = evResultatExercice/evChiffreAff
    if rentabilite >= 1: pt = 2
    else: pt = -2
    return pt

def solvabilite(actif,dispo,dette):
    """
    Entrée : Des éléments du bilan
    Variables : actif: total des actifs (bilan)
                dispo: disponibilité(bilan)
                dette: total dette
    Sortie : la solvabilité en point (compris entre -4 et 4)
    """
    solvabilite = (actif-dispo)/dette
    pt = (8*solvabilite - 32)/3
    return min(4,max(-4,pt))

def poidsRemboursement(dette, chiffreAff):
    """
    Entrée : Le chiffre d'affaire et le montant de la dette
    Variables : chiffreAff: chiffre d'affaire du mois (bilan)
                dette: total dette
    Sortie : le poids en point (compris entre -4 et 4)
    """
    poids = dette/chiffreAff
    if poids >= 1: pt = 2
    else: pt = -2
    return pt

def variationInteretTotal(donneesF):
    """
    Entrée : Toutes les données de la partie finance
    Variables : donneesF: dictonnaire comportant ces données
                i de 1 à 5: les pt d'interet selon les 5 méthodes
    Sortie : le taux d'intéret final du pret
    """
    listeChiffreAff = donneesF['chiffreAff']
    i11 = evolutionChiffreAff(listeChiffreAff[-1],listeChiffreAff[-2],listeChiffreAff[-3])
    i12 = ptChiffreAff(i11)

    listeResultatEx = donneesF['resultatEx']
    i21 = evolutionResultatEx(listeResultatEx[-1],listeResultatEx[-2],listeResultatEx[-3])
    i22 = ptResultat(i21)

    i3 = rentabilite(i11,i12)
    i4 = solvabilite(donneesF['actif'],donneesF['disponibilité'],donneesF['dette'])
    i5 = poidsRemboursement(donneesF['dette'],listeChiffreAff[-1])

    total = i12 + i22 + i3 + i4 + i5
    variationPt = min(4,max(-4,total))
    variationPourcentage = variationPt/10
    return variationPourcentage


##################| AFFICHAGE |#####################

# A appeler lors du click sur "Contracter un prêt"
def affichageInteret():
    """
    Variables : donneesF: les données récupérées
                variationInteret: la variation du taux d'interet calculer selon
                                  la situation de l'entreprise
    Sortie : Le texte à afficher
    """
    #Lecture des données finance
    with open('donneesFinance', 'rb') as fichierFinance:
        depickler = pickle.Unpickler(fichierFinance)
        donneesF = depickler.load()

    variationInteret = variationInteretTotal(donneesF)

    #Texte à trous
    if variationInteret < (-2):
        texte1 = "nous pouvons vous faire confiance"
        texte2 = "bas"
    elif variationInteret > 2:
        texte1 = "nous sommes méfiants en votre capacité à rembourser vos prêts"
        texte2 = "élevé"
    else:
        texte1 = "nous sommes assez confiants en votre capacité à rembourser vos prêts"
        texte2 = "correct"

    print("Après une analyse de la situation de votre start-up, nous avons conclu "+
    "que "+ texte1 +". Nous vous proposons donc un prêt à taux d'intérêt correct "+ texte2 +".")
    print("                     Votre Banque.")

    #Affichage taux d'intérêt selon la durée du prêt
    interetCourt = round(1.5 + (variationInteret/2),1)
    interetMoyen = round(1.6 + variationInteret,1)
    interetLong = round(2.1 + variationInteret,1)
    print("Taux d'intérêt: "+str(interetCourt)+"%")
    print("Taux d'intérêt: "+str(interetMoyen)+"%")
    print("Taux d'intérêt: "+str(interetLong)+"%")

#On détermine les bornes de la durée du prêt en fonction du type de prêt
def dureePret(typePret):
    if typePret == "court":
        debut = "1 mois"
        fin = "12 mois"
    elif typePret == "moyen":
        debut = "2 ans"
        fin = "4 ans"
    elif typePret == "long":
        debut = "5 ans"
        fin = "10 ans"

    return [debut,fin]

#Donne la durée en mois, et non en année
def dureePretMois(typePret,duree):
    #La durée pour un pret court est déjà récupérée en mois
    if typePret == 'court':
        return duree
    else:
        return (duree*12)

#On determine le montant maximal du pret en fonction de la durée du pret
def montantPret(duree):
    #On récupère les données finance
    with open('donneesFinance', 'rb') as fichierFinance:
        depickler = pickle.Unpickler(fichierFinance)
        donneesF = depickler.load()

    montantAnnee = round((donneesF['capital'] + donneesF['report à nouveau'])/10,2)
    montant = round(montantAnnee*(duree/12),2)

    return montant

# A appeler après avoir choisi entre pr^t à court/moyen/long terme
def affichageTypePret(typePret,tauxInteret):
    """
    Entrée : typePret: en fonction où click l'utilisateur à la page précédente
             tauxInteret: à récupérer de la page précédente
    Sortie : l'affichage des données
    """
    #On détermine les bornes de la durée du prêt en fonction du type de prêt
    debutFin = dureePret(typePret)

    #Affichage
    print("Vous avez choisi un prêt à "+typePret+" terme.\n")
    print("Taux d'intêret: "+str(tauxInteret)+"%")
    print("Assurance: 2%\n")

    #A traiter les erreurs
    duree = dureePretMois(typePret,int(input("Durée du prêt: (compris entre "+debutFin[0]+" et "+debutFin[1]+")")))

    #On determine le montant maximal du pret en fonction de la durée du pret
    montantMax = montantPret(duree)

    montant = input("Montant du prêt: (compris entre 1€ et "+str(montantMax)+"€)")

# A appeler avec le bouton "GENERER"
def affichageFinal(tauxInteret,capitalPret,duree,tauxAssurance):
    """
    Entrée : les données récupérées de l'utilisateur
    Sortie : l'affichage des données
    """
    assurance = round(capitalPret*(tauxAssurance/100),2)
    assuranceMois = round(assurance/duree,2)

    interet = round(capitalPret*(tauxInteret/100),2)
    total = capitalPret+interet
    totalMois = round(total/duree,2)

    print("Prix de l'assurance: "+str(assurance)+"€")
    print("Prix de l'assurance par mois: "+str(assuranceMois)+"€\n")

    print("Montant du prêt: "+str(capitalPret)+"€")
    print("Montant de l'intérêt: "+str(interet)+"€")
    print("Total: "+str(total)+"€")
    print("Prix du prêt par mois: "+str(totalMois)+"€")


####################################################
################| TESTS UNITAIRES |#################
####################################################

def testUnitaire():
    donneesF = {
    "chiffreAff": [3000,4000,5000],
    "resultatEx": [500,600,800],
    "actif": 30000,
    "disponibilité": 300,
    "dette": 10000,
    "capital": 30000,
    "report à nouveau": 15000
    }
    with open('donneesFinance', 'wb') as fichierFinance:
        pickler = pickle.Pickler(fichierFinance)
        pickler.dump(donneesF)

    affichageInteret();
    print("\n\n\n")
    affichageTypePret('moyen',2.2);
    print("\n\n\n")
    affichageFinal(2.2,30000,24,2);
