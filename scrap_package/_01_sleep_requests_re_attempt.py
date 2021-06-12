import requests as rq

import time


def requests_respectful(url):
    """
        Ajoute un délai avant une requeste.

    Pour éviter de submerger les serveurs interrogés.
    Pour éviter d'être bloquer par le site.

    :proceedings:

    :param url:
        Une url provenant du site 'https://books.toscrape.com/'
        :example:
            'https://books.toscrape.com/catalogue/olio_984/index.html'

    :type url:
        La valeur d'une list en str.
        :example:
            'https://books.toscrape.com/catalogue/olio_984/index.html'

    :returns:
        Une response exploitable
        ou
        un message indiquant l'url défaillante.
    """
    count_attempt = 0

    time.sleep(0.5)
    response = rq.get(url)

    if response.ok != True:

        while response.ok != True or count_attempt != 9:
            count_attempt += 1
            time.sleep(0.5 + 1 * count_attempt)
            response = rq.get(url)

        if response.ok == True:
            return response

        else:
            mess_fail = print('10 requests à cette url {} ont échouées'
                              .format(url)) +\
                        print('Si elle n\'est pas érronée, veuillez réitérer'
                              'votre reqetsts plus tard.')
            return mess_fail

    else:
        return response
