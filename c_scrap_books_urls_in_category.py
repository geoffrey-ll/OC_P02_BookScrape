import requests as rq
import re
from bs4 import BeautifulSoup
from pprint import pprint as pp
from e_scrap_data import scrap_data_func
# from write_csv import write_data_desired_in_csv_func
from g_cover_download import cover_ddl_func


def scrap_books_urls_in_category_func(url_category):
    """
    Description:
        Retourne tous les liens des livres de la catégorie url_category
    Input:
        - url_category: le lien d'une catégorie
    Output:
        - urls_of_books: une liste de tous les urls des livre de la categorie
    """
    url_books_of_category = []


    url_category_home = url_category
    # Pour contrôle que l'url est valide. À terme déplacer CECI dans une
    # fonction qui le vérifie avant la collecte des url.
    # Ne détecte des erreurs dans l'url que si l'erreu est après :
    # "http://books.toscrape.com/".
    # Si l'erreur est après, la requête renvoi le code html 404, si elle est
    # dans le nom de domaine, la requête semble ne pas aboutir. (aucun serveur
    # n'est atteint pour renvoiyer un code html 404…)
    request_home_category = rq.get(url_category_home)
    if request_home_category.ok is False:
        return \
            print('L\'url \n{}\nn\'est pas valide.'.format(url_category_home))

    # Utiliser requeste_home_category.text à la place de
    # request_home_category.content.decode('utf-8) donnerais un résultat
    # équivalent. Je laisse le .decode('utf-8) pour assurer d'un encodage
    # en utf-8.
    soup_home_category = BeautifulSoup(request_home_category.content.decode('utf-8'), 'html.parser')
    quantity_books_in_category = soup_home_category.findAll(
        'form', {'class': 'form-horizontal'})[0].find('strong').text

    # Collecte les urls de toutes les pages d'une categorie et les stockent dans
    # la liste url_all_pages_category.
    url_all_pages_category = []
    if int(quantity_books_in_category) > 20:
        url_other_page_category = []
        total_page_of_category = re\
            .findall("[0-9]+", soup_home_category.findAll('li')[-2].text)[1]

        for number_page in range(2, int(total_page_of_category) + 1):
            url_other_page_category\
                .append(url_category_home[:-10] +
                        'page-' + str(number_page) +
                        '.html')
        url_all_pages_category = [url_category_home] + url_other_page_category

    else:
        url_all_pages_category.append(url_category_home)

    # Collecte des url de tous les livres de toutes les pages de la categorie,
    # et les stokent dans la liste url_books_of_category.
    for url_pages in url_all_pages_category:
        request_page_category = rq.get(url_pages)
        soup_page_category = BeautifulSoup(
            request_page_category.content.decode('utf-8'), 'html.parser')
        h3tag_books_show_by_page = soup_page_category.findAll('h3')
        for h3tag_book in h3tag_books_show_by_page:
            atag_book = h3tag_book.find('a')
            url_books_of_category.append(
                'http://books.toscrape.com/catalogue/' +
                atag_book['href'][9:])

    return url_books_of_category
        

    # controle_url_books(url_books_of_category)


def scrap_category(url_category):
    all_urls = scrap_books_urls_in_category(url_category)
    result = scrap_data_func(all_urls)
    write_csv_func(result)
    # cover_ddl_func(result)

# scrap_books_urls_in_category('http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html')