import os
import re

import scrap_package as sp


def cover_create_path_func(data_desired, option):
    name_category = data_desired.get('category')[0].lower().replace(' ', '_')

    # Répertoire de travail du script = './'
    if os.path.exists('output') == False:
        os.mkdir('output')

    if option == 'book_option':
        folder_cover = 'output/zingle/'
        pass
    else:
        folder_cover = 'output/' + name_category + '/cover_' + name_category
        if os.path.exists(folder_cover) == False:
            os.mkdir(folder_cover)

    for idx in range(len(data_desired['image_url'])):
        title_adjust = re.sub('[\\\\/<>|]', '', data_desired['title'][idx].lower()
                              .replace('?', '¿')
                              .replace('*', '^')
                              .replace(':', '_-')
                              .replace('"', '\'')
                              .replace(' ','_'))

        start_name_cover = folder_cover + '/' + title_adjust
        end_name_cover = '_upc_' + data_desired['universal_product_code (upc)'][idx] + '.jpg'
        name_cover = start_name_cover + end_name_cover
        path = os.getcwd() + '/' + name_cover

        # Sous Windows, un chemin est limité par défault, à 260 caractères.
        # 15 doivent être réservés pour gwet.
        if len(path) >= 245:
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
            vital_module_gwet = 15
            # gap_over_limit est le nombre de caractères que l'on va enlever au
            # title_adjust du livre pour que le chemin fasse 245 caractères.
            gap_over_limit = len(name_cover) - 260 + vital_module_gwet + len('[…]') + len(end_name_cover)
            short_name = start_name_cover[:-gap_over_limit] + '[…]' + end_name_cover

            if os.path.exists(short_name) == False:
                sp.def_ddl(data_desired['image_url'][idx], short_name)

        else:
            if os.path.exists(name_cover) == False:
                sp.def_ddl(data_desired['image_url'][idx], name_cover)
