# Fonction Compétence "Recherche"
def compRecherche(individus) :
	return(sum([individu.competence_recherche for individu in individus]))


# Fonction Compétence "Groupe"
def compGroupe(individus) :
	# On fait la moyenne des capacités de travail de groupe des chercheurs
	moyenne = sum([individu.competence_groupe for individu in individus])/len(individus)
	return(10*moyenne -50)

