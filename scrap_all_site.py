

def scrap_categories_urls(url_site):
    pass



def scrap_all(url_site):
    all_categories_urls = scrap_categories_urls(url_site)
    for category_url in all_categories_urls:
        scrap_category(category_url)
