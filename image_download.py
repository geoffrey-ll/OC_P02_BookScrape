import wget


def telecharger_images(category_dict):
    wget.download('http://books.toscrape.com/media/cache/17/db/17db3de71e8217d4277a9328b04f56cf.jpg', out='output/Travel/images/example.jpg')
    pass

# telecharger_images()