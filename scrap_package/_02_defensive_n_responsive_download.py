import time
import wget


def defensif_n_responsive_ddl(image_url, path_jpg):

    count_attempt = 1

    while count_attempt < 6:

        try:
            time.sleep(0.5 * count_attempt)
            wget.download(image_url, out=path_jpg)
            break

        except:
            print('')
            count_attempt += 1

    if count_attempt == 6:
        print('6 tentatives ont échoués à télécharger la cover {} depuis cette url {}'.format(path_jpg, image_url))
