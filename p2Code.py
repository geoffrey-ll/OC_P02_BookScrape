import requests as rq
from bs4 import BeautifulSoup
# import time

# urlLivre = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
#
# response = rq.get(urlLivre)

enTete = ['product_page_url', 'universal_product_code (upc)', 'title']


##### Deux fonction a ajouter
### Fonction pour vérifier que toutes les clés est bien la même quantité de valeur ###
    # Foncion a effectuer avant l'écriture du .csv
    # Afin d'éviter des décalages dans les informations.
    # Sinon exemple la description de exempleLivre pourrait se retrouver avec les autres infos de autreLivre
# def fonctionControleQuantiteParCle():
#     # Avant d'écrire le fchier on vérifier que chaque clée a bien la même qunatité de valeurs
#     # Si oui on écrire le .csv si non on renvoi un message d'erreur en présissant  ou est l'erreur
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
#             print('%s \t: %d' % (infosAEcrire.keys(i), quantiteValeurParCle[i]))

### Fonction pour connaître la nature de l'url ###
    # S'il s'agit de l'url d'une category, exécuter la fonction toutesURLCategory
    # S'il sagit de l'url d'un livre, exécuter directement la foncion scrapInformationsVoulus

# Mettre toutes les fonctions dans une fonction les réunissant toutes ???
# Ou plutôt une foncion qui puisse toutes les appeler lorsqu'il le faut



### Fonction pour écrire dans un .csv les infortions récoltées ###
def ecritureCSV(infosAEcrire):
    quantiteValeurParCle = len(infosAEcrire['title'])
# Même si toutes les valeurs du dictionnaire informationsVoulues{} sont censé être en utf-8
# il faut quant même encoder le .csv en utf-8 car j'ai eu une erreur pour la catégorie christian à cause d'un espace
# insécable (\xà0) qui n'était pas utf-8.
# Présicer encodage du .csv m'a levée cette erreur.
    with open('leFichier.csv', 'w', encoding='utf-8') as file:
        # En-tête du fichier. Sert comme nom de colonnes
        file.write('product_page_url|universal_product_code (upc)|title|price_including_tax|'
                   'price_excluding_tax|number_available|product_description|category|'
                   'review_rating|image_url' + '\n\n')
    # Écriture des informations
    # On écrit la iémeValeur de chaque clé sur un ligne puis au fais un saut de ligne
        for iemeValeur in range(quantiteValeurParCle):
            for cleDicoInformationsVoulues in infosAEcrire.keys():
                file.write(infosAEcrire.get(cleDicoInformationsVoulues)[iemeValeur] + '|')
            if iemeValeur < quantiteValeurParCle - 1:
                file.write('\n')

### Fonction pour lire le .csv contenant les informations récoltées ###
def lectureCSV(infosALire):
    with open(infosALire + '.csv', 'r') as file:
       for row in file:
           print('row', row)


### Fonction pour récupérer toutes les informations voulues sur l'url d'un livre ###
def scrap_data(urlLivre):
    informationVoulues = { 'product_page_url': [],
                            'universal_product_code (upc)': [],
                            'title': [],
                            'price_including_tax': [],
                            'price_excluding_tax': [],
                            'number_available': [],
                            'product_description': [],
                            'category': [],
                            'review_rating': [],
                            'image_url': []}

    for urlATraiter in urlLivre:
        response_urlLivres = rq.get(urlATraiter)

        if response_urlLivres.ok:

        # L'ensemble des soups
            # Nécessaire de préciser a BeautifulSoup que le contenu de respons_urlLivre doit être lu en tant que utf-8
            # Cela permet la compréhension de tous les caractères (utile pour caractères particulier présent en description)
            # En revanche cela marche uniquement parce que la page à été encoder en utf-8
            # Cela implique que soupLivreHome est transformé en str() donc la méthode .text() ne doit pas être appliquée
            soupLivreHome = BeautifulSoup(response_urlLivres.content.decode('utf-8'), 'html.parser')
            tdsTagProductInformation = soupLivreHome.findAll('td')
            h1StrTitreOeuvre = soupLivreHome.find('h1').text
            pTagDescriptionEtNote = soupLivreHome.findAll('p')
            aStrCategoryOeuvre = soupLivreHome.findAll('a')[3].text
            img_urlImage = soupLivreHome.findAll('img')[0].attrs.get('src')

        # Ajout de l'url de la page
            informationVoulues['product_page_url'].append(urlATraiter)
        # Ajout des informations issues de balises <td>
            informationVoulues['universal_product_code (upc)'].append(tdsTagProductInformation[0].text)
            # Le caractère unicode "\u00A3" est celui de la livre Sterling on ajoute un espace après celui-ci
            # Remplacement des séparateur décimaux "." en ","
            informationVoulues['price_excluding_tax'].append(
                    tdsTagProductInformation[2].text.replace('.', ',').replace('Â', '').replace('\u00A3', '\u00A3 '))
            informationVoulues['price_including_tax'].append(
                    tdsTagProductInformation[3].text.replace('.', ',').replace('Â', '').replace('\u00A3', '\u00A3 '))
            # Extraction de la quantié disponible dans "In stock (xx available)"
            # Supposition que s'il n'y en a pas en stock alors le texte ne débutera pas par "I"
            # S'il débute par "I" alors on récupére la quantité en stock sinon on indique 0
            if tdsTagProductInformation[5]:
                if str(tdsTagProductInformation[5].text[0]) == str('I'):
                    informationVoulues['number_available'].append(tdsTagProductInformation[5].text[10:-11])
                else:
                    informationVoulues['number_available'].append(0)
        # Ajout de l'information issues de la balise <h1>
            informationVoulues['title'].append(h1StrTitreOeuvre)
        # Ajout des informationss issues de balises <p>
            # On a un bon affichage des caractères particuliers (tel "…" "'")
            # parce que soupLivreHome est decoder en utf-8
            # informationVoulues['product_description'].append(DU UTF-8)
            informationVoulues['product_description'].append(pTagDescriptionEtNote[3].text)
            # Dictionnaire pour traduire en français le nombre d'étoiles qu'a un livre
            # Information de forme "xx étoile(s)"
            traduction = {'Zero': 'Zéro étoile',
                          'One': 'Une étoile',
                          'Two': 'Deux étoiles',
                          'Three': 'Trois étoiles',
                          'Four': 'Quatre étoiles',
                          'Five': 'Cinq étoiles'}
            informationVoulues['review_rating'].append(str(traduction.get(str(pTagDescriptionEtNote[2].attrs.get('class')[1]))))
        # Ajout de l'information issue d'une balise <a>
            informationVoulues['category'].append(aStrCategoryOeuvre)
        # Ajout de l'information issues d'une balise <img>
        # Il faut reconstruire l'url de l'image
            informationVoulues['image_url'].append(str('https://books.toscrape.com/' + str(img_urlImage[6:])))
    # time.sleep()
    ecritureCSV(informationVoulues)

#  lectureCSV('leFichier')


# Collecte de toutes les urls de tous les livres d'une categorie.
def collect_url_books_by_one_category():
    url_category_home = '' \
                        'http://books.toscrape.com/catalogue/category/books/' \
                        'christian_43/index.html'

    # Pour contrôle que l'url est valide. À terme déplacer CECI dans une
    # fonction qui le vérifie avant la collecte des url.
    request_home_category = rq.get(url_category_home)
    if request_home_category.ok is False:
        return print('L\'url n\'est pas valide.')

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


collect_url_books_by_one_category()

""" IDÉE

Si class identique pour plussieurs infosARechercher ET si id simmilaire ALORS
ce servir du nom variable dans une
boucle pour recupérer toutes les infos avec la boucle.
cou
ntry = soup.find('tr', {'id': 'placse_' + str(nameRecherche) + '__row'}).
find('td', {'class': 'laClasse})
"""