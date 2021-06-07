![open_class_rooms](https://img.shields.io/badge/OpenClassRooms-Project02-limegreen?labelColor=blueviolet&style=plastic)
![built_by](https://img.shields.io/badge/Built%20by-Developers%20%3Cgeoffrey_ll%3E-black?labelColor=orange&style=plastic)

![made_with_python](https://img.shields.io/badge/Made%20With-Python-darkgreen?logo=python&labelColor=red&style=plastic)
![IDE use](https://img.shields.io/badge/IDE%20use-PyCharm-darkgreen?logo=pycharm&labelColor=red&style=plastic)
![OS_use](https://img.shields.io/badge/OS%20use-Windows-blue?labelColor=red&style=plastic&logo=windows)

![open_source](https://img.shields.io/badge/licence-libre-darkkhaki?labelColor=red&style=plastic)

# scrap.py #

## Description. ##

Ce script à été réalisé dans le cadre d'un projet du parcours 'Développeur d'application - Python' d'OpenClassROoms.

scrap.py est un outil de scraping utilisable uniquement sur le site [books to scrape](http://books.toscrape.com/), une simulation de librairie en ligne. Il permet de recueillir diverses informations sur les livres, et de les écrire dans un .csv, ainsi que de télécharger les images de couverture des livres.

Pour illustrer, voici le .csv de la catégorie 'Contemporary' contenant 3 livres,

![csv_contemporary_category](readme/csv_contemporary.jpg)

et les diffentes couvertures récupérées.

![folder_contemporary_covers](readme/folder_contemporary_covers.jpg)

Pour chacune des catégorie scraper, le script crée un dossier au nom de la catégorie contenant le .csv et le dossier de couverture des livres. Chacun de ces dossiers sont rangés dans le dossier 'output' du répertoire du script (dossier crée par le script si inexsistant).

Voici à quoi ressemble le dossier 'output' après le scrap des 50 catégories du site,

![folder_output_all](readme/folder_output_all.jpg)

et le dossier contemporary.

![folder_contemporary](readme/folder_contemporary.jpg)

\
**Attention :**
- Le .csv utilise '|' comme séparateur de colonnes.\
- Les .csv et la couverture des livres ne sont pas mis à jour en direct.\
- Relancer le script réécrira le .csv de la catégorie, mais ne retéléchargera pas les couvertures si celles-ci existent déjà. 


## Utilisation ##

Le script s'utilise à partir d'un terminal, de 4 façons différentes.

![option_scrap.py](readme/option_scrap.py.jpg)
1. L'option 'book' suivit de l'url d'un livre spécifique, pour recueillir les données d'un seul livre.\
Tous les .csv écrits et les couvertures des livres téléchargées via cette option, sont stockés dans le dossier './output/zingle'\
![two_books_of_contemporary_category_in_folder_zingle](readme/two_books_of_contemporary_category_in_folder_zingle.jpg)
2. L'option 'category', suivit le l'url de la page '^.index.html' d'une catégorie, pour recueillir les informations de toutes une catégorie.\
 **Attention**, si la catégorie a plusieurs pages, il faut impérativement renseigner la première page qui finit en '/index.html'\
3. L'option 'all' pour recueillir les données pour tous les livres de toutes les catégorie de livre.
4. L'option input, pour recueillir les données d'une ou plusieurs catégories, via un menu à utiliser dans le terminal. \
![option_input_menu_home](readme/option_input_menu_home.jpg)\
Via cette option, ont peut sélectionner tous les catégories du site, ou n'en sélectionner que quelques unes.\
Les .csv et couvertures de livres sont stockés au même endroit.\
La sélection se fait par demande d'input à l'utilisateur.

## Installation ##

### Environnement virtuel

### Requierements

Une fois l'environnement virtuel activé, entrez la commande 'pip install -r requierements.txt' dans le terminal, pour installer tous les modules requit pour l'utilisation de scrap.py.


### Package
Pour chaqu'un des élèments du package
description
    entrée transformation sortie
structure

### Bugs connus
Indiquer une solution envisagée pour sa réparation

#### Idées d'amélioration (optionnel)
Permettre à l'utilisateur de définir le nombre de caractères à utiliser
pour le nom de cover.










