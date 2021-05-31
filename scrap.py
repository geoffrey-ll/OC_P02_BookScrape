from pprint import pprint as pp
import sys

from scrap_package.c_scrap_books_urls_in_category import scrap_books_urls_in_category_func
from scrap_package.e_scrap_data import scrap_data_func
from scrap_package.main_p02_scrap import main_without_selection
from scrap_package.main_p02_scrap import main_with_selection


user_args = sys.argv


def description():
    print('\n> python scrap.py book http://book_url'
          '\n> python scrap.py category http://category_url'
          '\n> python scrap.py all'
          '\n> python scrap.py input')


def main(user_args):
    try:
        if user_args[1] == 'book':
            data_desired = scrap_data_func([user_args[2]])
            pp(data_desired)

        elif user_args[1] == 'category':
            url_books_of_category = scrap_books_urls_in_category_func(user_args[2])
            pp(url_books_of_category)

        elif user_args[1] == 'all':
            main_without_selection()

        elif user_args[1] == 'input':
            main_with_selection()
        else:
            description()
    except Exception as e:
        print(str(e))
        description()


main(user_args)
