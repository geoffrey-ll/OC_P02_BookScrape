from bs4 import BeautifulSoup
from urllib.parse import urljoin

import re

import scrap_package as sp


def scrap_books_urls_in_category_func(url_category):
    """
        Collecte toutes les url des livres d'une catégorie.

    :proceedings:

    :param url_category:
        url d'une home page d'une catégorie de livres, provenant du site
        'https://books.toscrape.com/'.

    :type url_category:
        list de str. Plus précisément, des url appartenant au site
        https://books.toscrape.com/.

    :return:
        list de str. Contients toutes les pages url d'un category
    """
    url_books_of_category = []

    url_category_home = url_category
    # Ne détecte des erreurs dans l'url que si l'erreur est après :
    # "http://books.toscrape.com/".
    # Si l'erreur est après, la requête renvoi le code html 404, si elle est
    # dans le nom de domaine, la requête semble ne pas aboutir. (aucun serveur
    # n'est atteint pour renvoiyer un code html 404…)
    response_home_category = sp.rq_resp(url_category_home)
    if response_home_category.ok is False:
        return \
            print('L\'url \n{}\nn\'est pas valide.'.format(url_category_home))

    soup_home_category = BeautifulSoup(response_home_category.content, 'html.parser')
    quantity_books_in_category = soup_home_category.findAll(
        'form', {'class': 'form-horizontal'})[0].find('strong').text

    url_all_pages_category = []
    if int(quantity_books_in_category) > 20:
        url_other_page_category = []
        total_page_of_category = re\
            .findall("[0-9]+", soup_home_category.findAll('li')[-2].text)[1]

        for number_page in range(2, int(total_page_of_category) + 1):

            url_other_page_category\
                .append(url_category_home[:-10] + 'page-' + str(number_page) + '.html')

        url_all_pages_category = [url_category_home] + url_other_page_category

    else:
        url_all_pages_category.append(url_category_home)

    for url_pages in url_all_pages_category:

        request_page_category = sp.rq_resp(url_pages)
        soup_page_category = BeautifulSoup(
            request_page_category.content, 'html.parser')

        h3tag_books_show_by_page = soup_page_category.findAll('h3')
        for h3tag_book in h3tag_books_show_by_page:
            atag_book = h3tag_book.find('a')
            url_books_of_category.append('http://books.toscrape.com/catalogue/'
                                         + atag_book['href'][9:])

    return url_books_of_category
