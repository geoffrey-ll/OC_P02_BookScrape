import requests as rq
from bs4 import BeautifulSoup
import csv

url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

response = rq.get(url)

enTete = ['product_page_url', 'universal_product_code (upc)', 'title']

def ecritureCSV(infosAEcrire):
    with open('leFichier.csv', 'w') as file:
        file.write('prdouct_page_url|universal_product_code (upc)|title|price_including_tax|'
                   'price_excluding_tax|number_available|product_description|category|'
                   'review_rating|image_url' + '\n\n')
        for element in infosAEcrire:
            if infosAEcrire[0] == infosAEcrire[0]:
                file.write(element + '|')
            elif infosAEcrire[2] == infosAEcrire[2]:
                file.write(element in file[2])
            else:
                continue



def lectureCSV(infosALire):
    with open(infosALire + '.csv', 'r') as file:
        for row in file:
            print('row', row)


def scrapProductInformation():
    if response.ok:
        pI = []
        for i in range(10):
            pI.append('none')
        soup = BeautifulSoup(response.text, 'html.parser')
        tds = soup.findAll('td')
        for i in range(len(tds)):
            if i == 0:
                #productInformation = tds[i].text
                pI[i] = tds[i].text
            if i == 2 or i == 3:
               # productInformation = tds[i].text.replace('.', ',').replace('Â', '').replace('\u00A3', '\u00A3 ')
                pI[i] = tds[i].text.replace('.', ',').replace('Â', '').replace('\u00A3', '\u00A3 ')
            elif i == 5:
                if str(tds[i].text[0]) == str('I'):
                    pI[i] = tds[i].text[10:-11]
                else:
                    pI[i] = tds[i].txt[11:-11]
            else:
                continue
        print('tds', tds)
        print('pI', pI)
        ecritureCSV(pI)


"""
repartition = {0: '',: .text.replace('.', ',').replace('Â', '').replace('\u00A3', '\u00A3 '),
                    3
                    5In: .text[10:-11], 5Out: .txt[11:-11], entree: tds[i].text, sortie: pI[i]}
    for i in range(len(tds)):
        repartition.get(-1) = repartition.get(-2) + repartition.get(i)
            if i == 0:
                repartition.key[-1] = repartition.get(-2)
"""

scrapProductInformation()
lectureCSV('leFichier')

""""
def test():
    list = ['a', 'b', 'a', 'd']
    for i in range(len(list)):
        if list[0] == list[0]:
            list[1] = str('e')
        else:
            continue
    print(list)

test()
"""


""" IDÉE

Si class identique pour plussieurs infosARechercher ET si id simmilaire ALORS ce servir du nom variable dans une
boucle pour recupérer toutes les infos avec la boucle.
country = soup.find('tr', {'id': 'placse_' + str(nameRecherche) + '__row'}).find('td', {'class': 'laClasse})
"""