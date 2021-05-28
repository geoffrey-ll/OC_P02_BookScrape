import re
from pprint import pprint as pp
import csv


#docstring à créer pour cette fonction (selon pylint).
# Écriture dans un .csv des informations récoltées de chaque url visités.
def write_data_desired_in_csv_func(data_desired):

#### Code mis dans detection_category_scrap.
    # category_select = [data_desired['category'][0]]
    #
    # for category in data_desired.get('category'):
    #     count = 0
    #     for elmt in category_select:
    #         if re.findall(category, elmt) == [category]:
    #             count += 1
    #     if count == 0:
    #         category_select.append(category)
    # print('category_select', category_select)
####



    # for category in category_select:

    # name_file_data_books = 'data_books_in_'\
    #                        + data_desired.get('category')[0]\
    #                        + '_category'\
    #                        + '.csv'
    # quantity_values_by_key = len(data_desired['title'])
    # # Même si toutes les valeurs du dictionnaire data_desired{} sont censé être
    # # en utf-8, il faut quant même encoder le .csv en utf-8, car j'ai eu une
    # # erreur pour la catégorie christian à cause d'un espace insécable dans la
    # # description du livre "Blue Like[…]", présent juste après
    # # "[_]passion in[_]". L'espace insécable est afficher par "\xà0", ce qui
    # # n'est pas du utf-8.
    # # Préciser encodaging='utf-8' paramètre du .csv m'a levée cette erreur.
    #
    # #### Mettre sur la 1ère ligne, au-dessus des en-têtes de colonnes,
    # # (dans la 1ère case), la date et l'heure de la création du fichier  + le
    # # nombres de livres de la catégories ????
    # #### Ou date et heure création du fichier dans le nom du fichier ???
    # # (me plaît moins)
    # with open(name_file_data_books, 'w', encoding='utf-8') as file_data_books:
    #     # Le noms des clés de data_desired servent comme nom de colonnes.
    #     for key_data_desired in data_desired.keys():
    #         file_data_books.write(key_data_desired + '|')
    #     file_data_books.write('\n\n')
    #
    # # Écriture des informations.
    # # On écrit la iémeValeur de chaque clé sur un ligne, puis un saut deligne.
    #     for ieme_values in range(quantity_values_by_key):
    #         for key_data_desired in data_desired.keys():
    #             file_data_books\
    #                 .write(data_desired.get(key_data_desired)[ieme_values])
    #             if key_data_desired != 'image_url':
    #                 file_data_books.write('|')
    #         if ieme_values < quantity_values_by_key - 1:
    #             file_data_books.write('\n')

def write_csv_func(category_dict):
    pass
