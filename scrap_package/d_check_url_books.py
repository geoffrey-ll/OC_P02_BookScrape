import scrap_package as sp

# docstring à créer pour cette fonction (selon pylint)
# Vérfie que les requêtes sur les url_books renvoi un code 200, puis appel la
# fonction scrap_data(). Le cas échéant renvoi un message indiquant les
# url_books invalides.
def check_url_books_func(url_books):
    # Less 4 lignes en commentaires suivantse sont là pour introduires des
    # erreurs dans des url_books et vérifier l'efficacité de la fonccion.
    # url_books.insert(0, url_books[0] + 'l')
    # url_books.pop(1)
    # url_books.insert(1, url_books[1] + 'l')
    # url_books.pop(2)
    quantity_error_url_book = []
    for url_book in url_books:
        response_url_book = sp.rq_resp(url_book)
        if response_url_book.ok != True:
            quantity_error_url_book.append(url_books.index(url_book))
        else:
            continue
    if len(quantity_error_url_book) == 0:
        return url_books
    else:
        if len(quantity_error_url_book) == 1:
            print('quantity_error_url_book', len(quantity_error_url_book))
            print('\nL\'url :\n{0}\nest invalide !'
                  .format(url_books[quantity_error_url_book[0]]))
        else:
            print('\nLes url :')
            for index_url_books_error in quantity_error_url_book:
                print(url_books[index_url_books_error])
            print('sont invalides !')
