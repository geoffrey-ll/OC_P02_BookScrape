from pprint import pprint as pp
import re

import scrap_package as sp
from scrap_package import collect_url_home_all_category_func
from scrap_package.b_selection_category_to_scrap import selection_category_for_scrap_func
from scrap_package.c_scrap_books_urls_in_category import scrap_books_urls_in_category_func
from scrap_package.d_check_url_books import check_url_books_func
from scrap_package.e_scrap_data import scrap_data_func
from scrap_package.f_write_csv import write_data_desired_in_csv_func
from scrap_package.g_cover_download import cover_ddl_func


# Il y a 1260 url de livres collectées, lorsqu'on récupére les url de livres via
# toutes les catégories d'un coup. Sur la home page du site, il est indiqué
# 1000 livres. Plusieurs livres doivent appartenir à plusieurs catégories.
# Est-ce que cela va poser problème ?


# TODO
# # indiqué lorsque sélection de -all, la durée de première éxécution.
#
# # codé quelque part (probablement dans main_p02_scrap.py), la
# catégorie en cours d'éxécution et le nombre de catégories traitées.
#
# # Possiblité de mettre le script en pause ? De l'interrompre ?
#
#
#
# # Dans fonction écriture .csv, vérifier si plusieurs éditions d'une œuvre sont référencés. Si oui
# ajouter une mention après le nom du titre, genre 'édition A'.

def main_with_book(url_input):
    url_book_ok = check_url_books_func([url_input])
    data = scrap_data_func(url_book_ok)
    write_data_desired_in_csv_func(data)
    cover_ddl_func(data)


def main_with_category(url_input):
    category = re.sub('^.+books/|_[0-9]+.+$', '', url_input).capitalize().replace('-', ' ')
    print('\nScrap des données pour la catégorie \'{}\' en cours'.format(category))
    url_books_of_category = scrap_books_urls_in_category_func(url_input)
    url_books_ok = check_url_books_func(url_books_of_category)
    data = scrap_data_func(url_books_ok)
    print('Écriture du .csv pour la catégorie \'{}\' en cours'.format(category))
    write_data_desired_in_csv_func(data)
    print('Téléchargement des couvertures de livres de la catégorie \'{}\' en cours'.format(category))
    cover_ddl_func(data)
    print('\n\nDonnées récupérées')


def check_url_site(arg):
    if arg != 'URL_HOME_SITE':
        all_url_home_pages_category_book = collect_url_home_all_category_func(arg)
        return all_url_home_pages_category_book

    elif arg == 'URL_HOME_SITE':
        all_url_home_pages_category_book = collect_url_home_all_category_func(arg)
        if all_url_home_pages_category_book == 0:
            url_site = input('\n'
                             'Quelle est l\'adresse du site à scrapper ?\n')
            return check_url_site(url_site)
        else:
            return all_url_home_pages_category_book


def main_with_all():
    all_url_home_pages_category_book = check_url_site('URL_HOME_SITE')
    for idx, url_category in enumerate(all_url_home_pages_category_book):
        print('La catégorie {0} ({1}/{2}) est en cours.\n'.format(url_category[51:-13].replace('_', ' ')
                                                                                     .replace('-', ' '),
                                                       idx + 1, len(all_url_home_pages_category_book)))
        url_books_of_category = scrap_books_urls_in_category_func(url_category)
        url_books_ok = check_url_books_func(url_books_of_category)
        data_desired = scrap_data_func(url_books_ok)
        write_data_desired_in_csv_func(data_desired)
        cover_ddl_func(data_desired)


def main_with_input():
    all_url_home_pages_category_book = check_url_site('URL_HOME_SITE')
    url_home_category_to_scrap = selection_category_for_scrap_func(all_url_home_pages_category_book)
    for idx, url_category in enumerate(url_home_category_to_scrap):
        # category = re.findall('[oks/-_[0-9]+', url_category.replace('_', ' '))
        category = url_category[51:-13].replace('_', ' ').replace('-', ' ')
        print('La catégorie {0} ({1}/{2}) est en cours.\n'.format(category,
                                                       idx + 1, len(url_home_category_to_scrap)))
        url_books_to_scrap = scrap_books_urls_in_category_func(url_category)
        url_books_ok = check_url_books_func(url_books_to_scrap)
        data = scrap_data_func(url_books_ok)
        write_data_desired_in_csv_func(data)
        cover_ddl_func(data)
