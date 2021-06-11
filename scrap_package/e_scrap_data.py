from bs4 import BeautifulSoup
from urllib.parse import urljoin

import re


# docstring à créer pour cette fonction (selon pylint).
# Collecte de toutes les informations pour chaque url contenues dans la liste
# url_books
def scrap_data_func(response_books_ok, url_books):
    """Collecte de toutes les informations, pour chaque url de livres, contenues
    dans la liste url_book.

    :param url_books: list Ensemble des urls de livre sur lequelles extraire la
                        data.
    :return: dict data_desired Contenant la data extrait depuis chaqu'une des
            urls de livre.
    """


    data_desired = {'product_page_url': [],
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

    for idx in range(len(response_books_ok)):
        soup_book_home = BeautifulSoup(response_books_ok[idx].content, 'html.parser')

        tdstag_content_product_information = soup_book_home.findAll('td')
        h1_title_book = soup_book_home.find('h1').text
        ptag_description_and_rating = soup_book_home.findAll('p')
        a_category_book = soup_book_home.findAll('a')[3].text
        img_url_cover_book = soup_book_home.findAll('img')[0].attrs.get('src')

        data_desired['product_page_url'].append(url_books[idx])
        data_desired['universal_product_code (upc)'].append(tdstag_content_product_information[0].text)
        # Livre Sterling (\u00A3)
        data_desired['price_excluding_tax'].append(tdstag_content_product_information[2].text
                                                   .replace('.', ',').replace('\u00A3', '\u00A3 '))
        data_desired['price_including_tax'] \
            .append(tdstag_content_product_information[3].text
                    .replace('.', ',').replace('\u00A3', '\u00A3 '))
        # Rq : l'expression régulière est une liste d'un seule élèment.
        # Du coup on prend l'index [0] de l'expression régulière,
        # .re.findall()[0] pour éviter que la quantité n'apparaisse sous forme
        # de liste dans le .csv.
        data_desired['number_available'].append(
            re.findall(str("[0-9]+"), tdstag_content_product_information[5].text)[0])
        data_desired['title'].append(h1_title_book)
        data_desired['product_description'].append(ptag_description_and_rating[3].text)
        # data_desired['review_rating'] = "xx étoile(s)"
        traduction = {'Zero': 'Zéro étoile',
                      'One': 'Une étoile',
                      'Two': 'Deux étoiles',
                      'Three': 'Trois étoiles',
                      'Four': 'Quatre étoiles',
                      'Five': 'Cinq étoiles'}
        data_desired['review_rating']\
            .append(str(traduction
                        .get(str(ptag_description_and_rating[2].attrs.get('class')[1]))))
        data_desired['category'].append(a_category_book)
        data_desired['image_url'].append(str('https://books.toscrape.com/' + str(img_url_cover_book[6:])))                      # todo à remplacer par la méthode join


    return data_desired
