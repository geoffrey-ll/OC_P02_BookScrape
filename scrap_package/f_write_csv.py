import os
import re
import csv


def write_data_desired_in_csv_func(data_desired, option):
    """
        Écrit le .csv avec les données présentes dans data_desired.

    :proceedings:
        Stocke le nom de la catégorie.
        Crée le dossier './output' s'il n'existe pas.
        Si l'option utilisée est 'book'.
            Crée le dossier './output/zingle' s'il n'existe pas.
            Détermine le chemin du fichier, dans la limite des 260 caractères
            imposés par défault par Windows.
        Si l'option utilisées n'est pas 'book'.
            Crée le doissier './output/name_category' s'il n'existe pas.
            Détermine le nom du fichier .csv. (sans gestion de longueur du
            chemin)
        Stocke la quantité de valeur contenu par key.
        Ouverture du .csv.
        Paramètrage du fichier.
        Écriture des en-têtes et saut de ligne.
        Pour chaque index du dictionnaire.
            Écrit les valeurs de keys pour l'index en cours.

    :param data_desired:
        Est le dictionnaire contenant toutes les informations collectées. Ces
        keys sont :
        data_desired.keys =
            {
            'product_page_url': [],
            'universal_product_code (upc)': [],
            'title': [],
            'price_including_tax': [],
            'price_excluding_tax': [],
            'number_available': [],
            'product_description': [],
            'category': [],
            'review_rating': [],
            'image_url': []
            }

    :param option:
        Est l'option utilisée par l'utilisateur.
        Son argument est une constante.

    :type data_desired:
        dict.
        data_desired.keys =
            {
            'product_page_url': [],
            'universal_product_code (upc)': [],
            'title': [],
            'price_including_tax': [],
            'price_excluding_tax': [],
            'number_available': [],
            'product_description': [],
            'category': [],
            'review_rating': [],
            'image_url': []
            }

    :type option:
        str. Son argument est une constante qui dépend de l'option choisie par
        l'utilisateur. option peut être l'une de ces 4 valeurs :
        book_option
        category_option
        all_option
        input_option

    :return:
        Le .csv contenant toutes les informations collectées durant le
        proceedings.
        Le .csv a pour en-têtes :
            {
            'product_page_url': [],
            'universal_product_code (upc)': [],
            'title': [],
            'price_including_tax': [],
            'price_excluding_tax': [],
            'number_available': [],
            'product_description': [],
            'category': [],
            'review_rating': [],
            'image_url': []
            }
        Son delimiter='|' et a pour encoding='utf-16'
        Le chemin du fichier a deux patterns possible :
            ./output/name_category/data_books_in_name_category_category.csv
            s'il contient une catégorie.
            ou
            ./output/zingle/name_book_upc_upc_book.csv
            s'il contient un livre.
    """
    name_category = data_desired.get('category')[0].lower().replace(' ', '_')

    # Répertoire de travail du script = './'
    if os.path.exists('output') == False:
        os.mkdir('output')

    if option == 'book_option':
        if os.path.exists('output/zingle') == False:
            os.mkdir('output/zingle')

        title_adjust = re.sub('[\\\\/<>|]', '', data_desired['title'][0].lower()
                              .replace('?', '¿')
                              .replace('*', '^')
                              .replace(':', '_-')
                              .replace('"', '\'')
                              .replace(' ','_'))
        start_name_file = 'output/zingle/' + title_adjust
        end_name_file = '_upc_' + data_desired['universal_product_code (upc)'][0] + '.csv'
        name_file = start_name_file + end_name_file
        path_file = os.getcwd() + '/' + start_name_file + end_name_file

        # Sous Windows, un chemin est limité par défault, à 260 caractères.
        if len(path_file) >= 260:
            # gap_over_limit est le nombre de caractères que l'on va enlever au
            # title_adjust du livre pour que le chemin fasse 260 caractères.
            gap_over_limit = len(name_file) - 260 + len('[…]') + len(end_name_file)
            short_name = start_name_file[:-gap_over_limit] + '[…]' + end_name_file
            name_file = short_name

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

        file_data.write('sep=|\n')
        data_writer = csv.writer(file_data, delimiter='|')
        # Paramètre pas bon pour The Black Maria catégory Poetry dans description

        data_writer.writerow(data_desired)
        data_writer.writerow('')

        for idx in range(quantity_values_by_key):
            row = []
            for key in data_desired.keys():
                row.append(data_desired[key][idx])
            data_writer.writerow(row)
