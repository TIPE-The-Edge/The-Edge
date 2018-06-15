import datetime
import calendar

def add_months(sourcedate, months):

     month = sourcedate.month - 1 + months
     year = sourcedate.year + month // 12
     month = month % 12 + 1
     day = min(sourcedate.day, calendar.monthrange(year, month)[1])
     return datetime.datetime(year, month, day)

class Pret:

    def __init__(self, temps, donnees):
        self.type = donnees['type']
        self.tauxInteret = donnees['taux interet']
        self.dureePret = donnees['duree']
        self.capital = donnees['capital']
        self.montantPret = donnees['montantPret']
        self.montantPaye = 0
        self.interet = donnees['interet']
        self.dateDebut = temps  # Variable de la date
        self.dateFin = add_months(temps, self.dureePret)
        self.assurance = donnees['assurance']
        self.assuranceMois = donnees['assuranceMois']
        self.parMois = donnees['montantMois']

    def setMontantPaye(self, montant):
        self.montantPaye = montant
