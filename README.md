# The Edge

The Edge est un serious game relatif à la gestion d’entreprise. Développé dans le cadre du projet de TIPE, The Edge, a pour but de modéliser sous forme informatique les répercussions de nos choix dans le futur. Devenez dès maintenant le dirigeant d’une petite Start-up de conception de produits High-tech. Gérez vous-même vos produits, de leur conception à leur commercialisation. Engagez des employés qualifiés et attribuez-leur le poste qui convient le mieux. Apprenez à maîtriser vos revenus et vos dépenses ainsi qu’à gérer vos prêts pour faire prospérer votre entreprise.
Ce sont vos choix qui feront évoluer votre Start-up et détermineront son avenir.

## Contenu de l'archive

* doc :
* font : Contient les polices utilisées par l'application;
* img : Contient les images utilisées par l'application;
* lib : Contient le fichier python contenant la "class" gérant la sauvegarde;
* save : Contient les sauvegardes du jeu;
* widget : Contient les fichiers python contenant les "class" gérant les widgets (zone de saisie de texte, barre de défilement, bouton, etc.);
* world : Contient les fichiers python contenant les "class" gérant les différentes branches de l'entreprise;
* function.py : fichier python contenant la desciption des éléments (widgets, menu, barre de navigation) affichés sur la fenêtre et de l'action de ces derniers sur l'entrprise.
* main.py : fichier principale faisant appel à l'ensemble des fichiers pythons cités précedemment et gérant la fenêtre et le jeu.

## Installation & Prérequis

### Windows

* Installer Anaconda avec la version 3.6 de Python : [Lien vers l'installateur](https://www.anaconda.com/download/)
* Ouvrez l'application Anaconda Prompt instalé, puis entez les commandes suivantes dans l'apllication ouverte pour installer les paquets dont dépend notre programme :

```sh
pip install pygame
pip install numpy
pip install panda
```

## Utilisation

* Ouvrez l'application Anaconda Prompt

* Dirigez vous ensuite vers le dossier "program" en entrant la commande dans l'apllication ouverte :
```sh
cd chemin
```
où *chemin* est le chemin ou adresse d'accès menant vers le dossier "program". Vous pouvez le récumpérer dans l'explorateur de fichier. Si ce dernier contient des espaces, veuillez mettre *chemin* entre guillement.

* Éxécuter le programme en entrant la commande :
```sh
python main.py
```

## Historique des versions

* 24/06/2018 : Version 1.0.0
