from bs4 import BeautifulSoup

import re

import scrap_package as sp

# docstring à créer pour cette fonction (selon pylint).
# Collecte de toutes les informations pour chaque url contenues dans la liste
# url_books
def scrap_data_func(url_books):
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
                    'image_url': []}

    for url_book in url_books:
        response_url_book = sp.rq_resp(url_book)
        soup_book_home = BeautifulSoup(response_url_book.content, 'html.parser')

        tdstag_content_product_information = soup_book_home.findAll('td')
        h1_title_book = soup_book_home.find('h1').text
        ptag_description_and_rating = soup_book_home.findAll('p')
        a_category_book = soup_book_home.findAll('a')[3].text
        img_url_cover_book = soup_book_home.findAll('img')[0].attrs.get('src')

        # Ajout des différentes informations dans le dictionnaire data_desired.
        data_desired['product_page_url'].append(url_book)
        data_desired['universal_product_code (upc)'] \
            .append(tdstag_content_product_information[0].text)
        # Ajout d'un espace après le symbole de la livre Sterling (\u00A3)
        # Remplacement du séparateur décimaux "." en ",".
        data_desired['price_excluding_tax'] \
            .append(tdstag_content_product_information[2].text
                    .replace('.', ',')
                    .replace('\u00A3', '\u00A3 '))
        data_desired['price_including_tax'] \
            .append(tdstag_content_product_information[3].text
                    .replace('.', ',')
                    .replace('\u00A3', '\u00A3 '))
        # Collecte de la quantité d'unité en stock  dans :
        # "In stock (xx available)" à l'aide d'une expression régulière.
        # Rq : l'expression régulière est une liste l'un seule élèment.
        # Du coup on prend l'index [0] de l'expression régulière,
        # .re.findall()[0] pour éviter que la quantité n'apparaisse sous forme
        # de liste dans le .csv.
        data_desired['number_available'].append(re\
            .findall(str("[0-9]+"), tdstag_content_product_information[5].text)[0])
        # Collecte du titre présent dans la balise h1
        data_desired['title'].append(h1_title_book)
        # Collecte des informations présentent dans des ptag
        data_desired['product_description'] \
            .append(ptag_description_and_rating[3].text)
        # Dictionnaire pour traduire en français le nombre d'étoiles qu'a un
        # livre. data_desired['review_rating'] = "xx étoile(s)"
        traduction = {'Zero': 'Zéro étoile',
                      'One': 'Une étoile',
                      'Two': 'Deux étoiles',
                      'Three': 'Trois étoiles',
                      'Four': 'Quatre étoiles',
                      'Five': 'Cinq étoiles'}
        data_desired['review_rating'] \
            .append(str(traduction
                        .get(str(ptag_description_and_rating[2].attrs
                                 .get('class')[1]))))
        # Collecte de la catégorie du livre.
        data_desired['category'].append(a_category_book)
        # Recontruction de l'url de l'image de la couverture du livre.
        data_desired['image_url'] \
            .append(
            str('https://books.toscrape.com/' + str(img_url_cover_book[6:])))
    return data_desired
