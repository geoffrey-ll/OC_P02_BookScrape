from urllib.parse import urljoin
from bs4 import BeautifulSoup

import sys

import scrap_package as sp


def collect_url_home_all_category_func(url_site):
    """
        Collecte la home page de toutes les catégories de livre du site
        'https://books.toscrape.com/'.

    Ce module n'est appelé qu'avec les options 'all' et 'input'. La collecte ce
    fait par scraping de la home page du site.
    :example:
        'https://books.toscrape.com/catalogue/category/books/mystery_3/index.html'

    :proceedings:

    :param url_site: Une constante URL_SITE_HOME
        Une CONSTANTE permettant de vériféier que l'url du site est exploitable.

    :type url_site:
        list de str.

    :return:
        url_home_all_category_book, contenant la home page de toutes les
        catégories de livre.
    """

    # URL_HOME_SITE est la page d'accueil du site scrapper.
    URL_HOME_SITE = 'http://books.toscrape.com/'


    # Si url_site n'est pas ma constante URL_HOME_SITE, c'est que l'url est un input.
    # Alors on redefinit la constante comme input.
    if url_site != 'URL_HOME_SITE':
        URL_HOME_SITE = str(url_site)

    response_url_home_site = sp.rq_resp(URL_HOME_SITE)

    if response_url_home_site.ok != True:
        print('\nL\'accès au site \'{}\' est impossible.'.format(URL_HOME_SITE))
        return 0

    # Si la requête renvoi un code 200. Si l'url est la constante, alors
    # poursuite du script, sinon c'est que l'url valide est un input et dans ce
    # cas un message informe que le script n'est pas utilisable puis
    # l'interrompt.
    if response_url_home_site.ok == True:
        URL_P02 = 'http://books.toscrape.com'

        if URL_HOME_SITE != URL_P02 and URL_HOME_SITE != URL_P02 + '/':
            print('\nCe scrip à été réalisé dans le cadre du deuxième projet du parcours '
                  '\'Développeur d\'application - Python\' d\'OpenClassRooms.\n'
                  'Il n\'est pas adapté pour scraper un site différent de \'http://books.toscrape.com/\'\n\n'
                  'À bientôt sur ce site.'.format(URL_HOME_SITE))

            sys.exit()

    # Seules les pages d'accueil des catégories de livres contiennent
    # '/category/books/'. Je m'en sert donc pour détecter le noms des catégories
    # puis reconsruction des urls.
    soup_home_site = BeautifulSoup(response_url_home_site.content, 'html.parser')

    atag_home_site = soup_home_site.findAll('a')
    url_home_all_category_book = []
    for href_in_home_site in atag_home_site:
        if href_in_home_site.get('href').startswith('catalogue/category/books/'):
            url_home_all_category_book.append(urljoin(URL_HOME_SITE, href_in_home_site.get('href')))

    return url_home_all_category_book
