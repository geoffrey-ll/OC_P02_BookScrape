import requests as rq
from bs4 import BeautifulSoup

# Collecte les url_home_categery_book de chaqu'une des catégries de livres du
# site : http://books.toscrape.com/.
def collect_url_home_all_category_func():
    # url_home_site est la page d'accueil du site scrapper.
    url_home_site = 'http://books.toscrape.com/'
    request_url_home_site = rq.get(url_home_site)

    # Controle de l'url à impélementer. Vérification que l'url ne pointe pas
    # vers une page type "Hum, nou ne parvenons pas à trouver ce site".
    # Une telle page ne semble pas retouner code html lors de la requeste.get().
    # Dessous ce qui a été tenté, mais qui ne fut pas fructueux.
    # if request_url_home_site.ok != True:
    #     print('L\'url du site est invalide !\n', url_home_site)

    # Seules les pages d'accueil des catégories de livres contiennent
    # '/category/books/'. Je m'en sert donc pour détecter le noms des catégories
    # puis reconsruction des urls.
    soup_home_site = BeautifulSoup(request_url_home_site.content
                                   .decode('utf-8'), 'html.parser')
    atag_home_site = soup_home_site.findAll('a')
    url_home_all_category_book = []
    for href_in_home_site in atag_home_site:
        if href_in_home_site.get('href')[:25] == 'catalogue/category/books/':
            url_home_all_category_book.append(
                url_home_site + href_in_home_site.get('href'))

    return url_home_all_category_book


collect_url_home_all_category_func()