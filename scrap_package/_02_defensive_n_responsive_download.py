import time
import wget


def defensif_n_responsive_ddl(image_url, path_jpg):
    """
        Téléchargement respectueux et défensif des covers des livres.

    :proceedings:

    :param image_url:
        L'url de la cover d'un livre, provenant du site
        'https://books.toscrape.com/.

    :param path_jpg:
        Le chemin, nom de fichier inclus, du .jpg quand il sera téléchargé.

    :type image_url:
         Valeur de la clés 'image_url', du dictionnaire data_desired.

    :type path_jpg:
        Une concanétation de str. spécifiants où, et sous quel nom, sera écrit
        le .jpg
        :example:
            './output/art/cover_art/the_art_book_upc_4b8fa561a1e52d1c.jpg'

    :return:
        Pas vraiment un return, mais pltutot un Load. Téléchargement de l'image
        de cover d'un livre du site 'https://books.toscrape.com/', s'il n'y en a
        pas déjà une au même nom.
    """
    count_attempt = 1

    while count_attempt < 6:

        try:
            time.sleep(0.5 * count_attempt)
            wget.download(image_url, out=path_jpg)
            break

        except:
            print('')
            count_attempt += 1

    if count_attempt == 6:
        print('5 tentatives ont échoués à télécharger la cover '
              '\'{}\' depuis cette url \'{}\'.'.format(path_jpg, image_url))
