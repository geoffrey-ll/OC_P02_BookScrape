import requests as rq
from bs4 import BeautifulSoup
import sys

# Collecte les url_home_categery_book de chaqu'une des catégries de livres du
# site : http://books.toscrape.com/.
def collect_url_home_all_category_func(url_site):
    # url_home_site est la page d'accueil du site scrapper.
    url_home_site = 'http://books.toscrape.com/'


    if url_site != 'url_site_is_good':
        url_home_site = str(url_site)



    response_url_home_site = rq.get(url_home_site)

    # Controle de l'url à impléementer. Vérification que l'url ne pointe pas
    # vers une page type "Hum, nou ne parvenons pas à trouver ce site".
    # Une telle page ne semble pas retouner code html lors de la requeste.get().
    # Dessous ce qui a été tenté, mais qui ne fut pas fructueux.
    if response_url_home_site.ok != True:
        print('\nL\'accès au site \'{}\' est impossible.'.format(url_home_site))
        return 0

    if response_url_home_site.ok == True:
        url_p02 = 'http://books.toscrape.com'
        if url_home_site != url_p02 and url_home_site != url_p02 + '/':
            print('\nCe scrip à été réalisé dans le cadre du deuxième projet du parcours '
                  '\'Développeur d\'application - Python\' d\'OpenClassRooms.\n'
                  'Il n\'est pas adapté pour scraper un site différent de \'http://books.toscrape.com/\'\n\n'
                  'À bientôt sur ce site.'.format(url_home_site))
            sys.exit()


    # Seules les pages d'accueil des catégories de livres contiennent
    # '/category/books/'. Je m'en sert donc pour détecter le noms des catégories
    # puis reconsruction des urls.
    soup_home_site = BeautifulSoup(response_url_home_site.content
                                   .decode('utf-8'), 'html.parser')

                                   
    atag_home_site = soup_home_site.findAll('a')
    url_home_all_category_book = []
    for href_in_home_site in atag_home_site:
        if href_in_home_site.get('href')[:25] == 'catalogue/category/books/':
            url_home_all_category_book.append(
                url_home_site + href_in_home_site.get('href'))

    return url_home_all_category_book
