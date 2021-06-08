import requests as rq
import wget

import time


def requests_respectful(url):
    time.sleep(0.1)
    response = rq.get(url)
    return response



# wget.download(data_desired['image_url'][idx], out=short_name)
#
# def ddl_respectful(url, name):
#     time.sleep(0.1)
#     wget.download(url, out=name)