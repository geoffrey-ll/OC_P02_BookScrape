import requests as rq
from bs4 import BeautifulSoup
# import time


# Fonctions à ajouter.

### Fonction pour vérifier que toutes les clés ont bien la même quantité de
# valeur
# Fonction à effectuer avant l'écriture du .csv Afin d'éviter des décalages dans
# les informations.
# Sinon exemple la description de exemple_book pourrait se retrouvée avec les
# autres infos de other_book.
#
# Première ébauche de la fonction………
# def fonctionControleQuantiteParCle():
#     # Avant d'écrire le fchier on vérifier que chaque clée a bien la même
# quantité de valeurs
#     # Si oui on écrire le .csv, sinon on renvoi un message d'erreur en
# présissant où est l'erreur.
#     quantiteValeurParCle = []
#     erreurQuantiteValeur = []
#     for cleDicoInformationsVoulues in infosAEcrire.keys():
#         quantiteValeurParCle.append(len(cleDicoInformationsVoulues))
#
#     comparaison = quantiteValeurParCle.count(quantiteValeurParCle[0])
#     if comparaison == len(infosAEcrire.keys()):
#         continue
#     else:
#         print('Toutes les clés n\'ont pas la même quantité de valeurs\n')
#         for i in range(len(infosAEcrire.keys()):
#           print('%s \t: %d' % (infosAEcrire.keys(i), quantiteValeurParCle[i]))

### Fonction pour connaître la nature de l'url

# S'il s'agit de l'url d'une categorie, exécuter la
# fonction collect_url_books_by_one_category().
# S'il sagit de l'url d'un livre, exécuter directement la foncion scrap_data()

### Fonction envisagées.
# Mettre toutes les fonctions dans une fonction les réunissant toutes ???
# Ou plutôt une foncion qui puisse toutes les appeler lorsqu'il le faut ???


#docstring à créer pour cette fonction (selon pylint).
# Écriture dans un .csv des informations récoltées de chaque url visités.
def write_data_desired_in_csv(data_desired):
    name_file_data_books = 'data_books_in_'\
                           + data_desired.get('category')[0]\
                           + '_category'\
                           + '.csv'
    quantity_values_by_key = len(data_desired['title'])
    # Même si toutes les valeurs du dictionnaire data_desired{} sont censé être
    # en utf-8, il faut quant même encoder le .csv en utf-8, car j'ai eu une
    # erreur pour la catégorie christian à cause d'un espace insécable dans la
    # description du livre "Blue Like[…]", présent juste après
    # "[_]passion in[_]". L'espace insécable est afficher par "\xà0", ce qui
    # n'est pas du utf-8.
    # Préciser encodaging='utf-8' paramètre du .csv m'a levée cette erreur.
    with open(name_file_data_books, 'w', encoding='utf-8') as file_data_books:
        # Le noms des clés de data_desired servent comme nom de colonnes.
        for key_data_desired in data_desired.keys():
            file_data_books.write(key_data_desired + '|')
        file_data_books.write('\n\n')

    # Écriture des informations.
    # On écrit la iémeValeur de chaque clé sur un ligne, puis un saut deligne.
        for ieme_values in range(quantity_values_by_key):
            for key_data_desired in data_desired.keys():
                file_data_books\
                    .write(data_desired.get(key_data_desired)[ieme_values])
                if key_data_desired != 'image_url':
                    file_data_books.write('|')
            if ieme_values < quantity_values_by_key - 1:
                file_data_books.write('\n')


# docstring à créer pour cette fonction (selon pylint).
# Fonction pour lire le .csv contenant les informations récoltées.
def read_csv_content_data_desired(nam_file_data_books):
    with open(nam_file_data_books, 'r') as file_data_books:
        for row in file_data_books:
            print('row', row)


# docstring à créer pour cette fonction (selon pylint).
# Collecte de toutes les informations pour chaque url contenues dans la liste
# url_books
def scrap_data(url_books):
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
    write_data_desired_in_csv(data_desired)

#  lectureCSV('leFichier')


# docstring à créer pour cette fonction (selon pylint)
# Vérfie que les requêtes sur les url_books renvoi un code 200, puis appel la
# fonction scrap_data(). Le cas échéant renvoi un message indiquant les
# url_books invalides.
def controle_url_books(url_books):
    # Less 4 lignes en commentaires suivantse sont là pour introduires des
    # erreurs dans des url_books et vérifier l'efficacité de la fonccion.
    # url_books.insert(0, url_books[0] + 'l')
    # url_books.pop(1)
    # url_books.insert(1, url_books[1] + 'l')
    # url_books.pop(2)
    quantity_error_url_book = []
    for url_book in url_books:
        request_url_book = rq.get(url_book)
        if request_url_book.ok is False:
            quantity_error_url_book.append(url_books.index(url_book))
        else:
            continue
    if len(quantity_error_url_book) == 0:
        scrap_data(url_books)
    else:
        if len(quantity_error_url_book) == 1:
            print('quantity_error_url_book', len(quantity_error_url_book))
            print('\nL\'url :\n{0}\nest invalide !'
                  .format(url_books[quantity_error_url_book[0]]))
        else:
            print('\nLes url :')
            for index_url_books_error in quantity_error_url_book:
                print(url_books[index_url_books_error])
            print('sont invalides !')


# Collecte de toutes les urls de tous les livres d'une categorie.
def collect_url_books_by_one_category():
    url_category_home = '' \
                        'http://books.toscrape.com/catalogue/category/books/' \
                        'contemporary_38/index.html'

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
    soup_home_category = BeautifulSoup(
        request_home_category.content.decode('utf-8'), 'html.parser')
    quantity_books_in_category = soup_home_category.findAll(
        'form', {'class': 'form-horizontal'})[0].find('strong').text

    # Collecte les urls de toutes les pages d'une categorie et les stockent dans
    # la liste url_all_pages_category.
    url_all_pages_category = []
    if int(quantity_books_in_category) > 20:
        url_other_page_category = []
        litag_numbers_of_pages = soup_home_category.findAll('li')[-2:]
        current_page_of_category = [litag_numbers_of_pages[0].text][0][35]

        total_page_of_category = [litag_numbers_of_pages[0].text][0][40]
        for number_page in range(1, int(total_page_of_category)):
            if int(current_page_of_category) < int(total_page_of_category):
                url_other_page_category.append(url_category_home[:-10] +
                                               'page-' +
                                               str(number_page+1) + '.html')
                current_page_of_category = int(current_page_of_category) + 1

        url_all_pages_category = [url_category_home] + url_other_page_category
    else:
        url_all_pages_category.append(url_category_home)

    # Collecte des url de tous les livres de toutes les pages de la categorie,
    # et les stokent dans la liste url_books_of_category.
    url_books_of_category = []
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

    scrap_data(url_books_of_category)


# Collecte les url_home_categery_book de chaqu'une des catégries de livres du
# site : http://books.toscrape.com/.
def collect_url_home_category():
    url_home_site = 'http://books.toscrape.com/'
    request_url_home_site = rq.get(url_home_site)

    # Controle de l'url à impélementer. Vérification que l'url ne pointe pas
    # vers une page type "Hum, nou ne parvenons pas à trouver ce site".
    # Une telle page ne semble pas retouner code html lors de la requeste.get().
    # Dessous ce qui a été tenté, mais qui ne fut pas fructueux.
    # if request_url_home_site.ok != True:
    #     print('L\'url du site est invalide !\n', url_home_site)

    soup_home_site = BeautifulSoup(request_url_home_site.content
                                   .decode('utf-8'), 'html.parser')
    atag_home_site = soup_home_site.findAll('a')
    url_home_category_book = []
    for href_in_home_site in atag_home_site:
        if href_in_home_site.get('href')[:25] == 'catalogue/category/books/':
            url_home_category_book.append(
                url_home_site + href_in_home_site.get('href'))
    # print(url_home_category_book)









collect_url_home_category()
# collect_url_books_by_one_category()

""" IDÉE

Si class identique pour plussieurs infosARechercher ET si id simmilaire ALORS
ce servir du nom variable dans une
boucle pour recupérer toutes les infos avec la boucle.
cou
ntry = soup.find('tr', {'id': 'placse_' + str(nameRecherche) + '__row'}).
find('td', {'class': 'laClasse})"""
