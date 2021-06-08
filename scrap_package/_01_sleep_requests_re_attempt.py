import requests as rq
import wget

import time


def requests_respectful(url):
    count_attempt = 0
    time.sleep(0.1)
    response = rq.get(url)
    if response.ok != True:
        while response.ok != True and count_attempt != 9:
            count_attempt += 1
            response = rq.get(url)
        return response
    else:
        return response


# wget.download(data_desired['image_url'][idx], out=short_name)
#
# def ddl_respectful(url, name):
#     time.sleep(0.1)
#     wget.download(url, out=name)
