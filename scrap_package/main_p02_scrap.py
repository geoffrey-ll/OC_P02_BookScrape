from pprint import pprint as pp
import re

import scrap_package as sp


# TODO
# # indiqué lorsque sélection de -all, la durée de première éxécution.
#
#
# # Possiblité de mettre le script en pause ? De l'interrompre ?

def main_with_book(url_input):
    url_book_ok = sp.check_url_books_func([url_input])
    data = sp.scrap_data_func(url_book_ok)
    sp.write_data_desired_in_csv_func(data, 'book_option')
    sp.cover_ddl_func(data, 'book_option')
    print('\nDonnées récupérées pour le livre \'{}\'.'.format(data['title'][0]))


def main_with_category(url_input):
    category = re.sub('^.+books/|_[0-9]+.+$', '', url_input).capitalize().replace('-', ' ')
    print('\nLa catégorie \'{}\' est en cours.'.format(category))
    print('\nScrap des données en cours')
    url_books_of_category = sp.scrap_books_urls_in_category_func(url_input)
    url_books_ok = sp.check_url_books_func(url_books_of_category)
    data = sp.scrap_data_func(url_books_ok)
    sp.write_data_desired_in_csv_func(data, 'category_option')
    print('Écriture du .csv terminé')
    print('Téléchargement des .jpg en cours')
    sp.cover_ddl_func(data, 'category_option')
    print('\n\nDonnées récupérées pour la catégorie \'{}\''.format(category))


def check_url_site(arg):
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
    all_url_home_pages_category_book = check_url_site('URL_HOME_SITE')
    category = []

    for idx, url_category in enumerate(all_url_home_pages_category_book):
        category.append(re.sub('^.+books/|_[0-9]+.+$', '', url_category).replace('-', '').capitalize())
        print('\n')
        print('La catégorie \'{0}\' ({1}/{2}) est en cours.\n'.format(category[idx], idx + 1, len(all_url_home_pages_category_book)))
        print('Scrap en cours.')
        url_books_of_category = sp.scrap_books_urls_in_category_func(url_category)
        url_books_ok = sp.check_url_books_func(url_books_of_category)
        data_desired = sp.scrap_data_func(url_books_ok)
        sp.write_data_desired_in_csv_func(data_desired, 'all_option')
        print('Écriture du .csv terminé')
        print('Téléchargement des .jpg en cours')
        sp.cover_ddl_func(data_desired, 'all_option')

    print('\n\nDonnées récupérées pour TOUTES les catégories.')


def main_with_input():
    all_url_home_pages_category_book = check_url_site('URL_HOME_SITE')
    url_home_category_to_scrap = sp.selection_category_for_scrap_func(all_url_home_pages_category_book)
    category = []

    for idx, url_category in enumerate(url_home_category_to_scrap):
        category.append(re.sub('^.+books/|_[0-9]+.+$', '', url_category).replace('-', ' ').capitalize())
        print('\n')
        print('La catégorie \'{0}\' ({1}/{2}) est en cours.\n'.format(category[idx],
                                                                      idx + 1, len(url_home_category_to_scrap)))
        print('Scrap en cours.')
        url_books_to_scrap = sp.scrap_books_urls_in_category_func(url_category)
        url_books_ok = sp.check_url_books_func(url_books_to_scrap)
        data = sp.scrap_data_func(url_books_ok)
        sp.write_data_desired_in_csv_func(data, 'input_option')
        print('Écriture du .csv terminé')
        print('Téléchargement des .jpg en cours')
        sp.cover_ddl_func(data, 'input_option')

    # Message de fin selon les catégories sélectionnées.
    if len(category) == 0:
        pass

    elif  len(category) != 0 and len(category) <= 10:
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
