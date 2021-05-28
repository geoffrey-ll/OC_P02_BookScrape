import re


def detection_category_scrap_func(data_desired):
    category_select = [data_desired['category'][0]]

    for category in data_desired.get('category'):
        count = 0
        for elmt in category_select:
            if re.findall(category, elmt) == [category]:
                count += 1
        if count == 0:
            category_select.append(category)
    # print(category_select)
