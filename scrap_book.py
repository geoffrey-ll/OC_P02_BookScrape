from e_scrap_data import scrap_data_func
from pprint import pprint as pp


def scrap_book(book_url):
    book_url = [book_url]
    print('len', len(scrap_data_func(book_url)['title'][0]))




book_url = 'http://books.toscrape.com/catalogue/at-the-existentialist-cafe-freedom-being-and-apricot-cocktails-with-jean-paul-sartre-simone-de-beauvoir-albert-camus-martin-heidegger-edmund-husserl-karl-jaspers-maurice-merleau-ponty-and-others_459/index.html'

scrap_book(book_url)