import os
import wget
import re


def cover_ddl_func(all_data):
    # Dans all_data les noms de catégories sont en .capitalize et avec un
    # espace entre les mots. name_category change cela.
    name_category = all_data.get('category')[0].lower().replace(' ', '_')

    # Dossier où est exécuté le scrip = './'

    # Vérifie q'il existe un dossier './output'
    # Sinon crée le dossier.
    if os.path.exists('output') == False:
        os.mkdir('output')

    # Vérifie qu'il existe './output/name_category/cover_name_category'
    # Sinon crée le dossier.
    folder_cover = 'output/' + name_category + '/cover_' + name_category
    if os.path.exists(folder_cover) == False:
        os.mkdir(folder_cover)


    # Dans all_data, les noms des titres de livres ont plusieurs majuscules et
    # espaces. De plus de nombreux caractères sont interdits dans les noms de
    # fichiers. title_adjust change cela.
    # Vérifie que la cover 'folder_cover/title_adjust.jpg' n'existe pas.
    # Si absente alors la download.
    for idx in range(len(all_data['image_url'])):
        # text = all_data['title'][idx].lower().replace('"', '\'').replace(' ', '_')
        title_adjust = re.sub('[\\\\/<>|]', '', all_data['title'][idx].lower()
                              .replace('*', '^')
                              .replace(':', '_-_')
                              .replace('"', '\'')
                              .replace(' ','_'))
        name_cover = folder_cover + '/' + title_adjust + '.jpg'
        if os.path.exists(name_cover) == False:
            wget.download(all_data['image_url'][idx], out=name_cover)

# telecharger_images()

#.re.sub([typefont_no], '-')
