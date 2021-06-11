import re

import scrap_package as sp


def main_with_book(url_input):
    """
        Suite d'instructions pour l'option 'book'.

    Pour utiliser l'option 'book', il faut lancer l'application avec deux
    arguments.
    :example:
       llopis_scraper_books_online.py book http://books.toscrape.com/catalogue/
       vagabonding-an-uncommon-guide-to-the-art-of-long-term-world

    :proceedings:
        Vérification de l'url est exploitable.
        Scrap des informations (voir :returns:).
        Écriture du .csv.
        Téléchargement de la cover
        Message de fin d'exécution.

    :param url_input:
        C'est l'url absolu d'un livre du site 'http://books.toscrape.com/'.
        :example:
            http://books.toscrape.com/catalogue/vagabonding-an-uncommon-guide-
            to-the-art-of-long-term-world-travel_552/index.html

    :type url_input:
        str, plus précisément une url provenant du site
        'http://books.toscrape.com/'

    :returns:
        Un .csv contenant les informations collectées sur le livre, et le .jpg
        de la couverture du livre utilisé par le site. Les élèments sont
        enregistrés dans le répertoire './output/zingle/'

        Informations collectées :
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
    """
    response_book_ok, url_book = sp.check_url_books_func([url_input])

    data = sp.scrap_data_func(response_book_ok, url_book)
    sp.write_data_desired_in_csv_func(data, 'book_option')
    sp.cover_ddl_func(data, 'book_option')

    print('\nDonnées récupérées pour le livre \'{}\'.'.format(data['title'][0]))


def main_with_category(url_input):
    """
        Suite d'instructions pour l'option 'category'.

    Pour utiliser l'option 'category', il faut lancer l'application avec deux
    arguments.
    :example:
        llopis_scraper_books_online.py category http://books.toscrape.com/
        catalogue/category/books/crime_51/index.html

    :proceedings:
        On récupére le nom de la catégorie depuis url_input.
        Message de progression de l'application.
        Collecte des url de tous les livres de la catégorie.
        Vérification pour chaque url, qu'elle est exploitable.
        Scrap des informations sur les livres.
        Écriture du .csv contenant les informations de tous les livres.
        Téléchargement des .jpg des covers des livres.
        Message de fin d'exécution.

    :param url_input:
         C'est l'url absolu de la première page d'une catégorie de livre issue
         du site 'http://books.toscrape.com/'.
        :example:
            http://books.toscrape.com/catalogue/category/books/crime_51/index.html

    :type url_input:
        str, plus précisément une url provenant du site
        'http://books.toscrape.com/'

    :returns:
        Un .csv contenant les informations collectées sur tous les livres de la
        catégorie, ainsi que tous les .jpg des couvertures des livres utilisées
        par le site. Les élèments sont enregistrée dans le répertoire
        './output/name_category/'.

        Informations collectées :
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
    """
    category = re.sub('^.+books/|_[0-9]+.+$', '', url_input).capitalize().replace('-', ' ')

    print('\nLa catégorie \'{}\' est en cours.'.format(category))
    print('\nScrap en cours')

    url_books_of_category = sp.scrap_books_urls_in_category_func(url_input)
    response_books_ok, url_books = sp.check_url_books_func(url_books_of_category)
    data = sp.scrap_data_func(response_books_ok, url_books)
    sp.write_data_desired_in_csv_func(data, 'category_option')

    print('Écriture du .csv terminé')
    print('Téléchargement des .jpg en cours')

    sp.cover_ddl_func(data, 'category_option')

    print('\n\nDonnées récupérées pour la catégorie \'{}\''.format(category))


def check_url_site(arg):
    """
        Vérifie que l'url du site est exploitable.

    Pour cette version Bêta, l'url du site est codée en dur, elle est donc pas
    nécessaire, mais cette fonctionnalité le deviendras, lors du passage vers la
    version RC. À ce moment, il faudras adapté cette fonction.

    arg est une constante qui n'est modifiée que si l'url du site à scraper est
    inexploitable.

    arg = 'URL_HOME_SITE'

    :proceedings:
        Si arg est correct.
            Collect de toutes les url de pages d'accueil des catégories du site.
        Sinon demande une nouvelle url via input, puis se relance.

    :param arg:
        Lors de son premier appel, arg = 'URL_HOME_SITE'.
        Si arg != 'URL_HOME_SITE' c'est que l'url du site à scraper n'est pas
        exploitable.

    :type arg:
        str. arg = 'URL_HOME_SITE'. De plus c'est une constante qui n'est
        modifiée que si l'url du site à scraper est inexploitable.

    :return:
        Toutes les url de page d'accueil des catégorie du site
        'http://books.toscrape.com/'

    .. todo::
        Adapter cette fontion lors du passage à la version RC.
    """
    if arg != 'URL_HOME_SITE':
        all_url_home_pages_category_book = sp.collect_url_home_all_category_func(arg)
        return all_url_home_pages_category_book

    elif arg == 'URL_HOME_SITE':
        all_url_home_pages_category_book = sp.collect_url_home_all_category_func(arg)

        if all_url_home_pages_category_book == 0:
            url_site = input('\n'
                             'Quelle est l\'adresse du site à scrapper ?\n')
            return check_url_site(url_site)

        else:
            return all_url_home_pages_category_book


def main_with_all():
    """
        Suite d'instructions pour l'option 'all'.

    Pour utiliser l'option 'all', il faut lancer l'application avec l'argument
    'all'.
    :example:
        llopis_scraper_books_online.py all

    :proceedings:
        Vérification que l'url du site est exploitable et collecte les home page
        de toutes les catégories.
        Pour chaque catégorie.
            Message de progression de l'application.
            Collecte des url de tous les livres de la catégorie.
            Vérification pour chaque url, qu'elle est exploitable.
            Scrap des informations sur les livres.
            Écriture du .csv contenant les informations de tous les livres.
            Téléchargement des .jpg des covers des livres.
        Message de fin d'exécuton.

    :returns:
        Pour chaque catégories du site.
            Un .csv contenant les informations collectées sur tous les livres de
            la catégorie, ainsi que tous les .jpg des couvertures des livres
            utilisées par le site. Les élèments sont enregistrée dans le
            répertoire './output/name_category/'.

        Informations collectées :
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
    """
    all_url_home_pages_category_book = check_url_site('URL_HOME_SITE')
    category = []

    for idx, url_category in enumerate(all_url_home_pages_category_book):
        category.append(re.sub('^.+books/|_[0-9]+.+$', '', url_category)
                        .replace('-', ' ').capitalize())

        print('\n')
        print('La catégorie \'{0}\' ({1}/{2}) est en cours.\n'
              .format(category[idx], idx + 1, len(all_url_home_pages_category_book)))
        print('Scrap en cours.')

        url_books_of_category = sp.scrap_books_urls_in_category_func(url_category)
        response_books_ok, url_books = sp.check_url_books_func(url_books_of_category)
        data_desired = sp.scrap_data_func(response_books_ok, url_books)
        sp.write_data_desired_in_csv_func(data_desired, 'all_option')

        print('Écriture du .csv terminé')
        print('Téléchargement des .jpg en cours')

        sp.cover_ddl_func(data_desired, 'all_option')

    print('\n\nDonnées récupérées pour TOUTES les catégories.')


def main_with_input():
    """
        Suite d'instructions pour l'option 'input'.

    Pour utiliser l'option 'input', il faut lancer l'application avec l'argument
    'input'.
    :example:
        llopis_scraper_books_online.py input

    :proceedings:
        Vérification que l'url du site est exploitable et collecte les home page
        de toutes les catégories.
        Sélection des catégories à scraper, via un menu et input utilisateur.
            Options :
                -nom categorie 1 -nom categorie 2 …
                -all
                -list
                -quit
        Pour chaque catégorie sélectionnées.
            Message de progression de l'application.
            Collecte des url de tous les livres de la catégorie.
            Vérification pour chaque url, qu'elle est exploitable.
            Scrap des informations sur les livres.
            Écriture du .csv contenant les informations de tous les livres.
            Téléchargement des .jpg des covers des livres.
        Message de fin d'exécuton.

    :returns:
        Pour chaque catégories sélectionnées.
            Un .csv contenant les informations collectées sur tous les livres de
            la catégorie, ainsi que tous les .jpg des couvertures des livres
            utilisées par le site. Les élèments sont enregistrée dans le
            répertoire './output/name_category/'.

        Informations collectées :
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
    """
    all_url_home_pages_category_book = check_url_site('URL_HOME_SITE')
    url_home_category_to_scrap = sp.selection_category_for_scrap_func(all_url_home_pages_category_book)
    category = []

    for idx, url_category in enumerate(url_home_category_to_scrap):
        category.append(re.sub('^.+books/|_[0-9]+.+$', '', url_category)
                        .replace('-', ' ').capitalize())

        print('\n')
        print('La catégorie \'{0}\' ({1}/{2}) est en cours.\n'
              .format(category[idx], idx + 1, len(url_home_category_to_scrap)))
        print('Scrap en cours.')

        url_books_to_scrap = sp.scrap_books_urls_in_category_func(url_category)
        response_books_ok, url_books = sp.check_url_books_func(url_books_to_scrap)
        data = sp.scrap_data_func(response_books_ok, url_books)
        sp.write_data_desired_in_csv_func(data, 'input_option')

        print('Écriture du .csv terminé')
        print('Téléchargement des .jpg en cours')

        sp.cover_ddl_func(data, 'input_option')

    # Message de fin selon les catégories sélectionnées.
    if len(category) == 0:
        pass

    elif len(category) != 0 and len(category) <= 10:
        message_end = ['\n\nDonnées récupérées pour les catégories ']
        for idx, cat in enumerate(category):
            if idx != len(category) - 1 and idx != len(category) - 2:
                message_end.append('\'{}\', '.format(cat))
            elif idx == len(category) - 2:
                message_end.append('\'{}\' et '.format(cat))
            elif idx == len(category) - 1:
                message_end.append('\'{}\'.'.format(cat))
        print(''.join(message_end))

    elif len(category) >= 10 and len(category) != 50:
        print('\n\nDonnées récupérées pour l\'ensemble des catégories choisit.')

    else:
        print('\n\nDonnées récupérées pour TOUTES les catégories.')
