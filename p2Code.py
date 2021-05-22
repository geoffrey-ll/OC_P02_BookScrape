import requests as rq
from bs4 import BeautifulSoup
# import time
import csv

# urlLivre = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
#
# response = rq.get(urlLivre)

enTete = ['product_page_url', 'universal_product_code (upc)', 'title']

### Fonction pour écrire dans un .csv les infortions récoltées ###
def ecritureCSV(infosAEcrire):
    with open('leFichier.csv', 'w') as file:
        file.write('product_page_url|universal_product_code (upc)|title|price_including_tax|'
                   'price_excluding_tax|number_available|product_description|category|'
                   'review_rating|image_url' + '\n\n')
        for cle,information in infosAEcrire.items():
               file.write(information + '|')
        file.write('\n')

### Fonction pour lire le .csv contenant les informations récoltées ###
def lectureCSV(infosALire):
    with open(infosALire + '.csv', 'r') as file:
       for row in file:
           print('row', row)


### Fonction pour récupérer toutes les informations voulues sur l'url d'un livre ###
def scrapInformationVoulues(urlLivre):
    informationVoulues = {
        'product_page_url': [],
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

    for urlATraiter in urlLivre:
        response_urlLivres = rq.get(urlATraiter)


        if response_urlLivres.ok:

        #L'ensemble des soups
            soupLivreHome = BeautifulSoup(response_urlLivres.text, 'html.parser')
            tdsProductInformation = soupLivreHome.findAll('td')
            h1TitreOeuvre = soupLivreHome.find('h1').text
            pDescriptionEtNote = soupLivreHome.findAll('p')
            aCategoryOeuvre = soupLivreHome.findAll('a')[3].text
            img_urlImage = soupLivreHome.findAll('img')[0].attrs.get('src')

        # Ajout de l'url de la page
            informationVoulues['product_page_url'].append(urlATraiter)
        # Ajout des informations issues de balises <td>
            informationVoulues['universal_product_code (upc)'].append(tdsProductInformation[0].text)
            # Le caractère unicode "\u00A3" est celui de la livre Sterling on ajoute un espace après celui-ci
            # Remplacement des séparateur décimaux "." en ","
            informationVoulues['price_excluding_tax'].append(
                        tdsProductInformation[2].text.replace('.', ',').replace('Â', '').replace('\u00A3', '\u00A3 '))
            informationVoulues['price_including_tax'].append(
                        tdsProductInformation[3].text.replace('.', ',').replace('Â', '').replace('\u00A3', '\u00A3 '))
            # Extraction de la quantié disponible dans "In stock (xx available)"
            # Supposition que s'il n'y en a pas en stock alors le texte ne débutera pas par "I"
            # S'il débute par "I" alors on récupére la quantité en stock sinon on indique 0
            if tdsProductInformation[5]:
                if str(tdsProductInformation[5].text[0]) == str('I'):
                    informationVoulues['number_available'].append(tdsProductInformation[5].text[10:-11])
                else:
                    informationVoulues['number_available'].append(0)
        # Ajout de l'information issues de la balise <h1>
            informationVoulues['title'].append(h1TitreOeuvre)
        # Ajout des informationss issues de balises <p>
            informationVoulues['product_description'].append(pDescriptionEtNote[3].text)
            # Dictionnaire pour traduire en français le nombre d'étoiles qu'a un livre
            # Information de forme "xx étoile(s)"
            traduction = {'Zero': 'Zéro étoile',
                          'One': 'Une étoile',
                          'Two': 'Deux étoiles',
                          'Three': 'Trois étoiles',
                          'Four': 'Quatre étoiles',
                          'Five': 'Cinq étoiles'}
            informationVoulues['review_rating'].append(str(traduction.get(str(pDescriptionEtNote[2].attrs.get('class')[1]))))
        # Ajout de l'information issue d'une balise <a>
            informationVoulues['category'].append(aCategoryOeuvre)
        # Ajout de l'information issues d'une balise <img>
        # Il faut reconstruire l'url de l'image
            informationVoulues['image_url'].append(str('https://books.toscrape.com/' + str(img_urlImage[6:])))

    # time.sleep()
    # ecritureCSV(informationVoulues)



#  lectureCSV('leFichier')


#### Fonction pour récupérer les urls de tous les livres d'une category ###
def toutesURLCategory ():
    urlCategoryyHome = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'

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
            h3sLivresAffichésPArPage = soupPagesCategory.findAll('h3')
            for h3Livre in h3sLivresAffichésPArPage:
                aLivre = h3Livre.find('a')
                urlLivresDeLaCategroy.append('http://books.toscrape.com/catalogue/' + aLivre['href'][9:])

    scrapInformationVoulues(urlLivresDeLaCategroy)



toutesURLCategory()

""" IDÉE

Si class identique pour plussieurs infosARechercher ET si id simmilaire ALORS ce servir du nom variable dans une
boucle pour recupérer toutes les infos avec la boucle.
cou
ntry = soup.find('tr', {'id': 'placse_' + str(nameRecherche) + '__row'}).find('td', {'class': 'laClasse})
"""