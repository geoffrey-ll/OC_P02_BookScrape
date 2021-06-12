import scrap_package as sp


def check_url_books_func(url_books):
    """
        Vérifie l'exploitabilité d'une reqests avant de la transmettre

    :proceedings:

    :param url_books:
        Une ou des urls de home pages de livres, provenant du site
        'https://books.toscrape.com/'

    :type url_books:
        list de str.

    :return:
         list responses_books_ok avec les response des requests revenues avec un
         code 200.
         list url_books_ok des url correspondante au resquests exploitables.
    """
    responses_books_ok = []
    url_books_ok = []
    quantity_error_url_book = []

    for url_book in url_books:
        response_url_book = sp.rq_resp(url_book)

        if response_url_book.ok != True:
            quantity_error_url_book.append(url_books.index(url_book))
        else:
            responses_books_ok.append(response_url_book)
            url_books_ok.append(url_book)

    if len(quantity_error_url_book) == 1:
        print('\nL\'url :\n{0}\nest invalide !'
              .format(url_books[quantity_error_url_book[0]]))
    elif len(quantity_error_url_book) > 1:
        print('\nLes url :')
        for index_url_books_error in quantity_error_url_book:
            print(url_books[index_url_books_error])
        print('sont invalides !')


    return responses_books_ok, url_books_ok