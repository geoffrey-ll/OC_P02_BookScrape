from pprint import pprint as pp
import sys

from scrap_package.c_scrap_books_urls_in_category import scrap_books_urls_in_category_func
from scrap_package.e_scrap_data import scrap_data_func
from scrap_package.main_p02_scrap import main_with_all
from scrap_package.main_p02_scrap import main_with_input
from scrap_package.main_p02_scrap import main_with_book
from scrap_package.main_p02_scrap import main_with_category


user_args = sys.argv


def description():
    print('\n> python scrap.py book http://book_url'
          '\n> python scrap.py category http://category_url/index.html'
          '\n> python scrap.py all'
          '\n> python scrap.py input')


def main(user_args):
    try:
        if user_args[1] == 'book':
            main_with_book(user_args[2])

        elif user_args[1] == 'category':
            main_with_category(user_args[2])
            # pp(url_books_of_category)

        elif user_args[1] == 'all':
            main_with_all()

        elif user_args[1] == 'input':
            main_with_input()
        else:
            description()
    except Exception as e:
        pass
        print(str(e))
        description()


main(user_args)
