import requests as rq
from bs4 import BeautifulSoup
import csv

url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

response = rq.get(url)

enTete = ['product_page_url', 'universal_product_code (upc)', 'title']

def ecritureCSV(infosAEcrire):
    with open('leFichier.csv', 'w') as file:
        file.write('product_page_url|universal_product_code (upc)|title|price_including_tax|'
                   'price_excluding_tax|number_available|product_description|category|'
                   'review_rating|image_url' + '\n\n')
        for cle,information in infosAEcrire.items():
               file.write(information + '|')
        file.write('\n')


def lectureCSV(infosALire):
    with open(infosALire + '.csv', 'r') as file:
       for row in file:
           print('row', row)


def scrapInformationVoulues():
    if response.ok:
        informationVoulues = {
            'product_page_url': '',
            'universal_product_code (upc)': '',
            'title': '',
            'price_including_tax': '',
            'price_excluding_tax': '',
            'number_available': '',
            'product_description': '',
            'category': '',
            'review_rating': '',
            'image_url': ''
        }

    #L'ensemble des soups
        soup = BeautifulSoup(response.text, 'html.parser')
        tds = soup.findAll('td')
        titreOeuvre = soup.find('h1').text
        paragraphes = soup.findAll('p')
        categoryOeuvre = soup.findAll('a')[3].text
        image = soup.findAll('img')[0].attrs.get('src')

    # Ajout de l'url de la page
        informationVoulues['product_page_url'] = url
    # Ajout des informations issues de tds
        informationVoulues['universal_product_code (upc)'] = tds[0].text
        informationVoulues['price_excluding_tax'] = tds[2].text.replace('.', ',').replace('Â', '').replace('\u00A3',
                                                                                                           '\u00A3 ')
        informationVoulues['price_including_tax'] = tds[3].text.replace('.', ',').replace('Â', '').replace('\u00A3',
                                                                                                           '\u00A3 ')
        if tds[5]:
            if str(tds[5].text[0]) == str('I'):
                informationVoulues['number_available'] = tds[5].text[10:-11]
            else:
                informationVoulues['number_available'] = tds[5].txt[11:-11]
    # Ajout des infos issues de titreOeuvre
        informationVoulues['title'] = titreOeuvre
    # Ajout des infos issues des paragraphes
        informationVoulues['product_description'] = paragraphes[3].text
        traduction = {'Zero': 'Zéro étoile',
                      'One': 'Une étoile',
                      'Two': 'Deux étoiles',
                      'Three': 'Trois étoiles',
                      'Four': 'Quatre étoiles',
                      'Five': 'Cinq étoiles'
                      }
        informationVoulues['review_rating'] = str(traduction.get(str(paragraphes[2].attrs.get('class')[1])))
    # Ajout de la categorie de l'oeuvre
        informationVoulues['category'] = categoryOeuvre
    # Ajout de l'url de l'image de l'oeuvre
        informationVoulues['image_url'] = str('https://books.toscrape.com/' + str(image[6:]))

        ecritureCSV(informationVoulues)



scrapInformationVoulues()
# lectureCSV('leFichier')



""" IDÉE

Si class identique pour plussieurs infosARechercher ET si id simmilaire ALORS ce servir du nom variable dans une
boucle pour recupérer toutes les infos avec la boucle.
country = soup.find('tr', {'id': 'placse_' + str(nameRecherche) + '__row'}).find('td', {'class': 'laClasse})
"""