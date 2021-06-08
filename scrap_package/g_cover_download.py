import wget

import os
import re
import time


def cover_ddl_func(data_desired, option):
    # Dans all_data les noms de catégories sont en .capitalize et avec un
    # espace entre les mots. name_category change cela.
    name_category = data_desired.get('category')[0].lower().replace(' ', '_')

    # Dossier où est exécuté le scrip = './'

    # Vérifie q'il existe un dossier './output'
    # Sinon crée le dossier.
    if os.path.exists('output') == False:
        os.mkdir('output')

    # Vérifie qu'il existe './output/name_category/cover_name_category'
    # Sinon crée le dossier.
    folder_cover = ''
    if option == 'book_option':
        folder_cover = 'output/zingle/'
        pass
    else:
        folder_cover = 'output/' + name_category + '/cover_' + name_category
        if os.path.exists(folder_cover) == False:
            os.mkdir(folder_cover)


    # Dans all_data, les noms des titres de livres ont plusieurs majuscules et
    # espaces. De plus de nombreux caractères sont interdits dans les noms de
    # fichiers. title_adjust change cela.
    # Vérifie que la cover 'folder_cover/title_adjust.jpg' n'existe pas.
    # Si absente alors la download.
    for idx in range(len(data_desired['image_url'])):
        title_adjust = re.sub('[\\\\/<>|]', '', data_desired['title'][idx].lower()
                              .replace('?', '¿')
                              .replace('*', '^')
                              .replace(':', '_-')
                              .replace('"', '\'')
                              .replace(' ','_'))

        upc_book = '_upc_' + data_desired['universal_product_code (upc)'][idx] + '.jpg'
        start_name_cover = folder_cover + '/' + title_adjust
        name_cover = start_name_cover + upc_book
        if os.path.exists(name_cover) == False:
            # La longueur de chemin complet du fichier de la cover et nécessaire
            # pour gérer l'exception des noms trop long.
            path = os.getcwd() + '/' + name_cover

            # Gére l'exception des noms trop long. La limite d'un nom, chemin
            # inclus, pour win 7 et 10 (par défault), est de 260 caractères.
            #
            # Dans ce total de caractères, il faut en préserver 15 pour le
            # module gwet. En effet, en fin de process, gwet recherche le chemin
            # '.\\le_chemin_indiqué_en_out_(extension_inclus)str_gwet.tmp' où
            # 'str_gwet' est un string de type : '[0-9][a-z]*8'
            # (ex : 'xza0gat5.tmp'). Soit '.\\' en début de chemin +
            # 'xza0gat5.tmp' en fin de chemin, ce qui porte bien à 15 le nombre
            # de caractère dans l'expression du fichier, à réservé au module
            # gwet.
            # Example de nom trop long : 'At the Existantialist […] and others'
            # de la catégorie 'Philosophy'.
            #
            # Une fois la cover download, son chemin à pour longueur 244
            # caractères, soit 14 caractères libres. En effet, l'un des
            # caractère vital pour le module gwet, (l'un des '\' en début de
            # chemin) est aussi rajouté par windows, car out=short_name exclu
            # le caractère '\' entre le répertoire courrant '.' et le
            # short_name, dans notre cas, la '\' avant le dossier 'output'.
            # De fait, à la fin du process, seul 14 emplacements de caractères
            # sont libres et non 15.
            if len(path) >= 245:
                vital_module_gwet = 15
                # gap_over_limit est le nombre de caractères en trop dans le
                # titre du livre. Dans notre cas, la variable title_adjust.
                gap_over_limit = len(name_cover) - 260 + vital_module_gwet + len('[…]') + len(upc_book)
                short_name = start_name_cover[:-gap_over_limit] + '[…]' + upc_book
                # On vérifie qu'il n'existe pas déjà une cover du même nom, pour
                # éviter les download inutile et réduire la durée du script.
                if os.path.exists(short_name) == False:
                    time.sleep(0.1)
                    wget.download(data_desired['image_url'][idx], out=short_name)
            else:
                wget.download(data_desired['image_url'][idx], out=name_cover)
