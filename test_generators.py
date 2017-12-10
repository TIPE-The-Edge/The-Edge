from generators import *

os.system('clear') # works on Linux/Mac

######## INITIALISATION DES OBJETS ########

rang = 1
rang2 = 1

# populations
Population("Les Vieux", 100, 2)
Population("Les Jeunes", 2000, 99)

# produits
for i in range(0 + rang):
    Produit()

# opérations
for i in range(0 + rang):
    Operation()

# materiaux
for i in range(0 + rang):
    Materiau()

# formations
for i in range(0 + rang):
    Formation()

# fournisseurs
for i in range(0 + rang2):
    Fournisseur()

# usines
for i in range(0 + rang2):
    Usine()

# individus
for i in range(0 + rang):
    Individu()

# Tri les produits par ordre alphabétique
produits = enhancedSort(produits, "nom", False)

Individu.initExpProduit()

Population.initProduits()

Produit.initUtilites(150)

######## AFFICHAGE ########

# populations
print("------ Classe : Population ------")
for pop in populations:
    print(pop)
print()

# produits
print("------ Classe : Produit ------")
for prod in produits:
    print(prod)
print()

# opérations
print("------ Classe : Operation ------")
for ope in operations:
    print(ope)
print()

# materiaux
print("------ Classe : Materiau ------")
for mat in materiaux:
    print(mat)
print()

# formations
print("------ Classe : Formation ------")
for form in formations:
    print(form)
print()

# fournisseurs
print("------ Classe : Fournisseur ------")
for four in fournisseurs:
    print(four)
print()

# usines
print("------ Classe : Usine ------")
for usi in usines:
    print(usi)
print()

# individus
print("------ Classe : Individu ------")
for ind in individus:
    print(ind)
print()
