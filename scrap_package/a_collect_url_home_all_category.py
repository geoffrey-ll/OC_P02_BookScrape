from urllib.parse import urljoin
import requests as rq
from bs4 import BeautifulSoup
import sys

# Collecte les url_home_categery_book de chaqu'une des catégries de livres du
# site : http://books.toscrape.com/.
def collect_url_home_all_category_func(url_site):
    # URL_HOME_SITE est la page d'accueil du site scrapper.
    URL_HOME_SITE = 'http://books.toscrape.com/'


    # Si url_site n'est pas ma constante URL_HOME_SITE, c'est que l'url est un input.
    # Alors on redefinit la constante comme input.
    if url_site != 'URL_HOME_SITE':
        URL_HOME_SITE = str(url_site)



    response_url_home_site = rq.get(URL_HOME_SITE)

    # Controle de l'url à impléementer. Vérification que l'url ne pointe pas
    # vers une page type "Hum, nou ne parvenons pas à trouver ce site".
    # Une telle page ne semble pas retouner code html lors de la requeste.get().
    # Dessous ce qui a été tenté, mais qui ne fut pas fructueux.

    # Message d'erreur et renvoi vers une main_p02_scrap.py pour ne pas
    # poursuivre le script avec une url invalide.
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
    soup_home_site = BeautifulSoup(response_url_home_site.content
                                   .decode('utf-8'), 'html.parser')

                                   
    atag_home_site = soup_home_site.findAll('a')
    url_home_all_category_book = []
    for href_in_home_site in atag_home_site:
        if href_in_home_site.get('href').startswith('catalogue/category/books/'):
            url_home_all_category_book.append(urljoin(URL_HOME_SITE, href_in_home_site.get('href')))

    return url_home_all_category_book
