from pprint import pprint as pp
from a_collect_url_home_all_category import collect_url_home_all_category_func
from b_selection_category_to_scrap import selection_category_for_scrap_func
from c_scrap_books_urls_in_category import scrap_books_urls_in_category_func
from d_check_url_books import check_url_books_func
from e_scrap_data import scrap_data_func
from f_write_csv import write_data_desired_in_csv_func
from g_cover_download import cover_ddl_func

# Il y a 1260 url de livres collectées, lorsqu'on récupére les url de livres via
# toutes les catégories d'un coup. Sur la home page du site, il est indiqué
# 1000 livres. Plusieurs livres doivent appartenir à plusieurs catégories.
# Est-ce que cela va poser problème ?
def programme():
    all_url_home_pages_category_book = collect_url_home_all_category_func()
    url_home_category_to_scrap = selection_category_for_scrap_func(all_url_home_pages_category_book)
    for category in url_home_category_to_scrap:
        url_books_to_scrap = scrap_books_urls_in_category_func(category)
        url_books_ok = check_url_books_func(url_books_to_scrap)
        data = scrap_data_func(url_books_ok)
        write_data_desired_in_csv_func(data)
        # print('cover : ', data['image_url'], '\nhome_page : ', data['product_page_url'],
        #       '\ntitle', data['title'])
        cover_ddl_func(data)


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

























