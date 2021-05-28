from pprint import pprint as pp
from collect_url_home_all_category import collect_url_home_all_category_func
from selection_category_to_scrap import selection_category_for_scrap_func
from scrap_books_urls_in_category import scrap_books_urls_in_category_func
from scrap_data import scrap_data_func
from detection_category_scrap import detection_category_scrap_func
from write_csv import write_data_desired_in_csv_func

# Il y a 160 url de livres collectées, lorsqu'on récupére les url de livres via
# toutes les catégories d'un coup. Sur la home page du site, il est indiqué
# 1000 livres. Plusieurs livres doivent appartenir à plusieurs catégories.
# Est-ce que cela va poser problème ?
def programme():
    all_url_home_pages_category_book = collect_url_home_all_category_func()
    url_home_category_to_scrap = selection_category_for_scrap_func(all_url_home_pages_category_book)
    url_books_to_scrap = scrap_books_urls_in_category_func(url_home_category_to_scrap)
    test = scrap_data_func(url_books_to_scrap)
    detection_category_scrap_func(test)


programme()



# def scrap_categories_urls(url_site):
#     pass
#
#
#
# def scrap_all(url_site):
#     all_categories_urls = scrap_categories_urls(url_site)
#     for category_url in all_categories_urls:
#         scrap_category(category_url)

























