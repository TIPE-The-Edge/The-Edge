import datetime
import calendar


def get_with_id(group, identifier):
    for obj in group:
        if obj.id == identifier:
            return obj
    return None


"""
Fonction qui calcule le cout des prets du mois
"""
def coutPret(listePret):
    total = 0
    for pret in listePret:
        total += pret.parMois

    return total


"""
Fonction qui complete la liste des depenses avec les prêts
"""
def listeDepenseFinance(listeDepense,listePret):
    cout = coutPret(listePret)
    if cout == 0:
        return listeDepense
    else:
        return listeDepense.append(['Remboursement des prêts',cout])


"""
Fonction qui sépare les revenues et les dépenses
A utiliser à chaque tour
"""
def repartitionDepenses(listeDepense, listePret):
    listeDepense = listeDepenseFinance(listeDepense,listePret)
    depensesOrdo = [[],[]]

    if listeDepense != None:
        for depense in listeDepense:
            if depense[1] != None and depense[1] != 0:
                if 'Chiffre' in depense[0]:
                    depensesOrdo[0].append(depense)
                else:
                    depensesOrdo[1].append(depense)

    return depensesOrdo

def resetValeur(window):

    window.donneesF['achats matieres premieres'] = 0

    window.donneesF['impot'] = 0


    #Maj liste chiffreAff
    window.donneesF['chiffre affaire'].append(0)
    window.donneesF['chiffre affaire'].pop(0)

    #Maj liste report à nouveau
    window.donneesF["resultat exercice"].append(0)
    window.donneesF["resultat exercice"].pop(0)


def majStock(window):
    listeProduits = window.stocks[0].produits
    total = 0
    for product in listeProduits:
        nomProduit = product[0]
        objet = get_with_id(window.produits,nomProduit)
        if objet != None:
            prix = objet.prix
            total += (prix*product[1])

    return total

#Mise à jour de fin du mois (bilan, compte de résultat)
def majMois(window):

    if int(((window.temps - datetime.datetime(2010,1,1)).days)/7) == 5:
        window.donneesF["capital"] = 40000
        window.bilan['capital'] = 40000

    window.exBilan = (window.bilan).copy()
    window.exCompteResultat = (window.compteResultat).copy()

    #Maj argent
    cout = coutPret(window.listePret)
    window.donneesF["interet et charges"] = cout
    window.donneesF["total resultat financier"] = cout
    window.argent -= cout

    #Maj listePret
    for i in range(len(window.listePret)):
        if window.temps > window.listePret[i].dateFin:
            window.listePret.pop(i)

    #Maj stock
    valeurStock = majStock(window)


    machineDonnees = majBilanCompte(window)
    machineBrut = machineDonnees[0]
    machineNet = machineDonnees[1]
    amortissement = machineDonnees[2]

    #Maj bilan
    donneesF = window.donneesF

    difference = donneesF["total actif"] - donneesF["total passif"]
    if difference != 0 :
        valeurStock -= difference
        donneesF["total actif"] = donneesF["total passif"]

    window.bilan = {
        ### BILAN ###
        "amenagement locaux": donneesF["amenagement locaux"],
        "machinesBrut": machineBrut,
        "machinesAmortissement": amortissement,
        "machinesNet": machineNet,
        "brevets": donneesF["brevets"],
        "total actif immobilise": donneesF["total actif immobilise"],

        "stocks et en-cours": valeurStock,
        "avances et acomptes": donneesF["avances et acomptes"],
        "disponibilites": donneesF["disponibilites"],
        "total actif circulant": donneesF["total actif circulant"],

        "total actif": donneesF["total actif"],

        "capital": donneesF["capital"],
        "reserve legal": donneesF["reserve legal"],
        "report à nouveau": donneesF["report à nouveau"],
        "resultat exercice": [donneesF["resultat exercice"][0]],
        "total capitaux propres": donneesF["total capitaux propres"],

        "emprunts": donneesF["emprunts"],
        "dettes fournisseurs": donneesF["dettes fournisseurs"],
        "dettes sociales": donneesF["dettes sociales"],
        "dettes fiscales": donneesF["dettes fiscales"],
        "total dettes": donneesF["total dettes"],

        "total passif": donneesF["total passif"],
    }

    #Maj compte de résultat
    window.compteResultat = {
        "chiffre affaire": donneesF["chiffre affaire"][0],
        "production stockee": valeurStock,
        "total produits exploitation": donneesF["total produits exploitation"],

        "achats matieres premieres": donneesF["achats matieres premieres"],
        "loyer immobilier": donneesF["loyer immobilier"],
        "impots": donneesF["impots"],
        "salaires": donneesF["salaires"],
        "charges sociales": donneesF["charges sociales"],
        "dotations amortissements": donneesF["dotations amortissements"],
        "total charges exploitation": donneesF["total charges exploitation"],

        "interet et charges": donneesF["interet et charges"],
        "total resultat financier": donneesF["total resultat financier"],

        "resultat exercice compte": donneesF["resultat exercice compte"]
    }

    donneesF["report à nouveau"] += donneesF["resultat exercice"][0]
    resetValeur(window)




#listeDepense = [('chiffreAffaire',10),('coutRH',50)]
#print(repartitionDepenses(listeDepense))

#Fais les modifications nécessaires des données finances de fin de moi, afin de préparer le bilan et le compte de résultat
def majBilanCompte(window):
    donneesF = window.donneesF

    #Locaux
    if donneesF['amenagement locaux'] == 0:
        donneesF['amenagement locaux'] = 500
        window.argent -= 500

    #Amortissement
    amortissement = 0
    machineBrut = 0
    machineNet = 0
    for machine in window.donneesF['machines']:
        machineBrut += machine[0]
        parAnnee = machine[0]/10
        amortissement += parAnnee
        machineNet += (machine[0] - machine[1])
        machine[1] += parAnnee

        if machine[0] == machine[1]:
            window.donneesF['machines'].remove(machine)

    ###COMPTE DE RESULTAT###
    donneesF['total produits exploitation'] = donneesF['chiffre affaire'][0] + donneesF['production stockee']
    donneesF["dettes fiscales"] = window.tva
    donneesF['dotations amortissements'] = amortissement
    donneesF['total charges exploitation'] = donneesF['achats matieres premieres'] + \
        donneesF['loyer immobilier'] + donneesF['impots'] + \
        donneesF['salaires'] + \
        donneesF['charges sociales'] + \
        donneesF['dotations amortissements']


    donneesF['resultat exercice compte'] = donneesF['total produits exploitation'] - \
        donneesF['total charges exploitation'] - donneesF["total resultat financier"]

    #Impot sur le revenus
    if donneesF['resultat exercice compte'] > 0:
        impotBenefice = donneesF['resultat exercice compte'] * 15/100
        donneesF['resultat exercice compte'] -= impotBenefice
        donneesF['impots'] += impotBenefice

    donneesF['total charges exploitation'] = donneesF['achats matieres premieres'] + \
        donneesF['loyer immobilier'] + donneesF['impots'] + \
        donneesF['salaires'] + \
        donneesF['charges sociales'] + \
        donneesF['dotations amortissements']


    ###BILAN###

    #ACTIF
    donneesF['total actif immobilise'] = machineNet + \
        donneesF['amenagement locaux'] + donneesF['brevets']
    donneesF["disponibilites"] = window.argent
    donneesF['total actif circulant'] = donneesF['stocks et en-cours'] + donneesF["disponibilites"]
    donneesF['total actif'] = donneesF['total actif immobilise'] + donneesF['total actif circulant']


    #PASSIF
    resultat = donneesF['resultat exercice compte']
    reserveMax = donneesF['capital'] * 10/100
    reserveLegal = donneesF['reserve legal']
    if resultat > 0:
        if reserveLegal <= reserveMax:
            dotation = resultat * 5/1200
            if dotation + reserveLegal > reserveMax:
                dotation = reserveMax - reserveLegal
                reserveLegal = reserveMax
                resultat -= dotation
            else:
                reserveLegal += dotation
                resultat -= dotation

            donneesF['reserve legal'] = reserveLegal

    donneesF['resultat exercice'][0] = resultat

    donneesF['total capitaux propres'] = donneesF['capital'] + \
        donneesF['reserve legal'] + donneesF['report à nouveau'] + \
        donneesF['resultat exercice'][0]

    totalDette = 0
    for pret in window.listePret:
        totalDette += pret.montantPret

    donneesF['emprunts'] = totalDette
    donneesF['dettes sociales'] = donneesF['charges sociales']
    donneesF['total dettes'] = donneesF['emprunts'] + donneesF['dettes fiscales']
    donneesF['total passif'] = donneesF['total capitaux propres'] + \
        donneesF['total dettes']

    return [machineBrut, machineNet,amortissement]




#Met à jour des données finances chaque semaine en fonction des revenus/dépenses de la semaine
def majDonneesF(window,listeDepense):
    donneesF = window.donneesF
    for depense in listeDepense:
        if 'Chiffre' in depense[0]:
            donneesF['chiffre affaire'] += depense[1]

        elif depense[0] == 'Salaires':
            donneesF['salaires'] = depense[1]

        elif depense[0] == 'Charges salariales et patronales':
            donneesF['charges sociales'] = depense[1]

        elif depense[0] == 'Loyer et charges associées':
            donneesF['loyer immobilier'] = depense[1]

        elif depense[0] == 'Achats des matériaux':
            donneesF['achats matieres premieres'] += depense[1]

        elif depense[0] == 'Achat machine':
            donneesF['machines'].append([depense[1], depense[1]])

        elif 'Création' in depense[0]:
            donneesF['achats matieres premieres'] += depense[1]

        elif 'Brevet' in depense[0]:
            donneesF['brevets'] += depense[1]

        elif 'Mise' in depense[0]:
            donneesF['achats matieres premieres'] += depense[1]


def payerTaxe(window):
    window.donneesF['impots'] += window.tva
    window.argent -= window.tva
    window.tva = 0


#A appeler chaque semaine
#Lance toutes les étapes nécessaires
def majSemaine(window):
    majDonneesF(window,window.couts)

    if int(window.temps.month) in [3,6,9,12]:
        payerTaxe(window)
    if (int(window.temps.day) < 8) and (window.temps != window.tempsDebut):

        majMois(window)

listeDepense = [
    ('Chiffre d\'affaire',0),
    ('Salaires',0),
    ('Charges salariales et patronales',0),
    ('Loyer et charges associées',0),
    ('Coût transports',0),
    ('Achat machine',0),
    ('Achats des matériaux',0),
    ]
