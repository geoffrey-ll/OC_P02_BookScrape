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
# Il n'est pas utile d'indiquer que le .csv doit être traiter en tant que utf-8 car toutes les valeurs du
# dictionnaire informationsVoulues sont en utf-8 (action réalise dans la fonction scrapInformationsVoulues
    with open('leFichier.csv', 'w') as file:
        # En-tête du fichier. Sert comme nom de colonnes
        file.write('product_page_url|universal_product_code (upc)|title|price_including_tax|'
                   'price_excluding_tax|number_available|product_description|category|'
                   'review_rating|image_url' + '\n\n')
    # Écriture des informations
    # On écrit la iémeValeur de chaque clé sur un ligne puis au fais un saut de ligne
        for iemeValeur in range(quantiteValeurParCle):
            for cleDicoInformationsVoulues in infosAEcrire.keys():
                file.write(infosAEcrire.get(cleDicoInformationsVoulues)[iemeValeur] + '|')
            file.write('\n')

### Fonction pour lire le .csv contenant les informations récoltées ###
def lectureCSV(infosALire):
    with open(infosALire + '.csv', 'r') as file:
       for row in file:
           print('row', row)


### Fonction pour récupérer toutes les informations voulues sur l'url d'un livre ###
def scrapInformationsVoulues(urlLivre):
    informationVoulues = {  'product_page_url': [],
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


#### Fonction pour récupérer les urls de tous les livres d'une category ###
def toutesURLCategory ():
    urlCategoryyHome = 'http://books.toscrape.com/catalogue/category/books/contemporary_38/index.html'

    responseHomeCategory = rq.get(urlCategoryyHome)

    if responseHomeCategory.ok:
        soupHomeCategory = BeautifulSoup(responseHomeCategory.text, 'html.parser')
        liIndicationNombrePages = soupHomeCategory.findAll('li')[-2:]
        quantiteLivreCategory = soupHomeCategory.findAll('form', {'class': 'form-horizontal'})[0].find('strong').text

    # Récupération de toutes les pages d'une category
    # Si la category a plus de 20 livres alors elle a plus que la page http://../index.html
        if int(quantiteLivreCategory) > 20:
            urlAutresPages = []
            pageCouranteCategory = [liIndicationNombrePages[0].text][0][35]
            pageTotalCategory = [liIndicationNombrePages[0].text][0][40]
            for i in range(1, int(pageTotalCategory)):
                if int(pageCouranteCategory) < int(pageTotalCategory):
                    urlAutresPages.append(urlCategoryyHome[:-10] + 'page-' + str(i+1) + '.html')
                    pageCouranteCategory = int(pageCouranteCategory) + 1

            urlPagesCategory = [urlCategoryyHome] + urlAutresPages
    #Si la cetegory a moins de 20 livres alors la category n'a que la page http://../index.html
        else:
            urlPagesCategory = [urlCategoryyHome]

    # Récupération des URL de tous les livres de toutes les pages de la  category
        urlLivresDeLaCategroy = []
        for url in urlPagesCategory:
            responsePagesCategory = rq.get(url)
            soupPagesCategory = BeautifulSoup(responsePagesCategory.text, 'html.parser')
            h3sLivresAffichésParPage = soupPagesCategory.findAll('h3')
            for h3Livre in h3sLivresAffichésParPage:
                aLivre = h3Livre.find('a')
                urlLivresDeLaCategroy.append('http://books.toscrape.com/catalogue/' + aLivre['href'][9:])

    scrapInformationsVoulues(urlLivresDeLaCategroy)



toutesURLCategory()

""" IDÉE

Si class identique pour plussieurs infosARechercher ET si id simmilaire ALORS ce servir du nom variable dans une
boucle pour recupérer toutes les infos avec la boucle.
cou
ntry = soup.find('tr', {'id': 'placse_' + str(nameRecherche) + '__row'}).find('td', {'class': 'laClasse})
"""