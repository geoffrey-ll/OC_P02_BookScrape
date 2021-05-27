from scrap_data import scrap_data_func
from pprint import pprint as pp


def scrap_book(book_url):
    book_url = [book_url]
    pp(scrap_data_func(book_url))



book_url = "http://books.toscrape.com/catalogue/the-last-mile-amos-decker-2_754/index.html"

scrap_book(book_url)