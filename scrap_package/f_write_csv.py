import re
import os
import csv
from pprint import pprint as pp

#docstring à créer pour cette fonction (selon pylint).
# Écriture dans un .csv des informations récoltées de chaque url visités.
def write_data_desired_in_csv_func(data_desired, option):
    # Dans data_desired les noms de catégories sont en .capitalize et avec un
    # espace entre les mots. name_category change cela.
    name_category = data_desired.get('category')[0].lower().replace(' ', '_')

    # Dossier où est exécuté le scrip = './'

    # Vérifie q'il existe un dossier './output'
    # Sinon crée le dossier.
    if os.path.exists('output') == False:
        os.mkdir('output')

    # Vérifie qu'il existe './output/name_category'
    # Sinon crée le dossier.


    # Nom et chemin du fichier .csv
    if option == 'book_option':
        title_adjust = re.sub('[\\\\/<>|]', '', data_desired['title'][0].lower()
                              .replace('?', '¿')
                              .replace('*', '^')
                              .replace(':', '_-')
                              .replace('"', '\'')
                              .replace(' ','_'))
        upc_book = '_upc_' + data_desired['universal_product_code (upc)'][0] + '.csv'
        start_name_file = 'output/zingle/' + title_adjust
        name_file_temp = start_name_file + upc_book
        path_file = os.getcwd() + '/' + start_name_file + upc_book
        if len(path_file) >= 260:
            # gap_over_limit est le nombre de caractères en trop dans le
            # titre du livre. Dans notre cas, la variable title_adjust.
            gap_over_limit = len(name_file_temp) - 260 + len('[…]') + len(upc_book)
            short_name = start_name_file[:-gap_over_limit] + '[…]' + upc_book
            name_file = short_name
        else:
            name_file = start_name_file + upc_book
    else:
        folder = 'output/' + name_category
        if os.path.exists(folder) == False:
            os.mkdir(folder)
        name_file = folder + '/' + \
                    'data_books_in_' + name_category +'_category' + '.csv'

    # Nécessaire pour générer le nombre de row adéquat à l'aide d'une boucle for
    quantity_values_by_key = len(data_desired['title'])

    # Avec un encoding='utf-8', j'ai de nombreux caractères indésirables. Comme
    # le 'Â' avant le symbole de la livre Streling, où le 'â€•' au lieu de '-',
    # pour ne citer que deux exemples.
    #
    # Sans encoding='utf-8', il est impossible d'écrire les informations du
    # livre "Blue like[…]", de la catégorie 'Christian', à cause de l'espace
    # insécable présent dans la descrition du livre, juste après
    # "[…]passion in[…]". Plus d'autre problèmes d'affichages si l'on ouvre le
    # .csv depuis l'IDE Pycharm.
    #
    # Avec encoding='utf-16', les erreurs décrites précédemment sont résolus.
    # Pas d'autres erreur décelées.

    #### Mettre sur la 1ère ligne, au-dessus des en-têtes de colonnes,
    # (dans la 1ère case), la date et l'heure de la création du fichier  + le
    # nombres de livres de la catégories ????
    #### Ou date et heure création du fichier dans le nom du fichier ???
    # (me plaît moins)
    with open(name_file, 'w', encoding='utf-16', newline='') as file_data:
        # Le noms des clés de data_desired servent comme noms de colonnes.
        # Le choix du delimiter '|' est pour éviter un confilt avec les ',' des
        # prix des livres.
        file_data.write('sep=,\n')
        data_writer = csv.writer(file_data, delimiter=',')

        data_writer.writerow(data_desired)
        data_writer.writerow('')
        for idx in range(quantity_values_by_key):
            row = []
            for key in data_desired.keys():
                row.append(data_desired[key][idx])
            data_writer.writerow(row)
