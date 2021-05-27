import requests as rq
from bs4 import BeautifulSoup


# docstring à créer pour cette fonction (selon pylint).
# Collecte de toutes les informations pour chaque url contenues dans la liste
# url_books
def scrap_data_func(url_books):
    """
    Description: Cette fonction scrape un livre
    Input:
        - url_books : une liste de urls de livres
    Output:
        - d
        -
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
        request_url_book = rq.get(url_book)
        # Nécessaire de préciser à BeautifulSoup que le contenu de
        # request_url_book doit être lu en tant que utf-8.
        # Cela permet la compréhension de tout les caractères (utile pour
        # caractères particuliers présent dans de nombreuses descriptions).
        # Cela implique que soup_book_home est transformée en str() donc la
        # méthode .text() ne doit pas être appliquée.
        soup_book_home = BeautifulSoup(request_url_book.content
                                       .decode('utf-8'), 'html.parser')
        tdstag_content_product_information = soup_book_home.findAll('td')
        h1_title_book = soup_book_home.find('h1').text
        ptag_description_and_rating = soup_book_home.findAll('p')
        a_category_book = soup_book_home.findAll('a')[3].text
        img_url_cover_book = soup_book_home.findAll('img')[0].attrs.get('src')

        # Ajout des différentes informations dans le dictionnaire data_desired.
        data_desired['product_page_url'].append(url_book)
        data_desired['universal_product_code (upc)']\
            .append(tdstag_content_product_information[0].text)
        # Ajout d'un espace après le symbole de la livre Sterling (\u00A3)
        # Remplacement du séparateur décimaux "." en ",".
        data_desired['price_excluding_tax']\
            .append(tdstag_content_product_information[2].text
                    .replace('.', ',')
                    .replace('\u00A3', '\u00A3 '))
        data_desired['price_including_tax']\
            .append(tdstag_content_product_information[3].text
                    .replace('.', ',')
                    .replace('\u00A3', '\u00A3 '))
        # Collecte de la quantité d'unité en stock "In stock (xx available)"
        # Supposition que s'il n'y en a pas en stock, alors le texte ne débutera
        # pas par "I".
        # S'il débute par "I", on récupére la quantité en stock, sinon on
        # indique 0.
        if tdstag_content_product_information[5]:
            if str(tdstag_content_product_information[5].text[0]) == str('I'):
                data_desired['number_available']\
                    .append(tdstag_content_product_information[5].text[10:-11])
            else:
                data_desired['number_available'].append(0)
        data_desired['title'].append(h1_title_book)
        # Les caractères particuliers (tel "…" "'"), s'affiche correctement
        # parce que soup_book_home est decoder en utf-8.
        # data_desired['product_description'].append(est en utf-8)
        data_desired['product_description']\
            .append(ptag_description_and_rating[3].text)
        # Dictionnaire pour traduire en français le nombre d'étoiles qu'a un
        #  livre. data_desired['review_rating'] = "xx étoile(s)"
        traduction = {'Zero': 'Zéro étoile',
                      'One': 'Une étoile',
                      'Two': 'Deux étoiles',
                      'Three': 'Trois étoiles',
                      'Four': 'Quatre étoiles',
                      'Five': 'Cinq étoiles'}
        data_desired['review_rating']\
            .append(str(traduction
                        .get(str(ptag_description_and_rating[2].attrs
                                 .get('class')[1]))))
        data_desired['category'].append(a_category_book)
        # Il faut reconstruire l'url de l'image de la couverture du livre.
        data_desired['image_url']\
            .append(
            str('https://books.toscrape.com/' + str(img_url_cover_book[6:])))
    # time.sleep()
    # write_data_desired_in_csv(data_desired)
    return data_desired

#  lectureCSV('leFichier')



