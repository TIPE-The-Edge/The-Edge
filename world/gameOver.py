"""
Fonction qui retourne un booleen qui vérifie si l'on a perdu
A vérifier à chaque debut de tour
"""
def faillite(argent,droitAuPret):
    if argent < 0 and droitAuPret == False:
        return True
    else:
        return False
