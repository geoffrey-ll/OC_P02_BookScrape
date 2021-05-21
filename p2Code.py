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
        print('dictionnaire', infosAEcrire)
        for cle,information in infosAEcrire.items():
            if information == '':
                file.write('none' + '|')
            else:
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
        soup = BeautifulSoup(response.text, 'html.parser')
        tds = soup.findAll('td')
        for i in range(len(tds)):
            if i == 0:
                informationVoulues['universal_product_code (upc)'] = tds[i].text
            if i == 2 or i == 3:
                informationVoulues['price_excluding_tax'] = tds[i].text.replace('.', ',').replace('Â', '').replace('\u00A3', '\u00A3 ')
            if i == 3:
                informationVoulues['price_including_tax'] = tds[i].text.replace('.', ',').replace('Â', '').replace('\u00A3', '\u00A3 ')
            elif i == 5:
                if str(tds[i].text[0]) == str('I'):
                    informationVoulues['number_available'] = tds[i].text[10:-11]
                else:
                    informationVoulues['number_available'] = tds[i].txt[11:-11]
            else:
                continue
        ecritureCSV(informationVoulues)



scrapInformationVoulues()
lectureCSV('leFichier')



""" IDÉE

Si class identique pour plussieurs infosARechercher ET si id simmilaire ALORS ce servir du nom variable dans une
boucle pour recupérer toutes les infos avec la boucle.
country = soup.find('tr', {'id': 'placse_' + str(nameRecherche) + '__row'}).find('td', {'class': 'laClasse})
"""