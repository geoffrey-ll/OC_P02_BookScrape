import sys
import re
from pprint import pprint as pp
from bs4 import BeautifulSoup
import a_collect_url_home_all_category


#### Si dans l'input manul, le premier caractère n'est pas '-', alors rien ne se passe.
# Identifie les catégories disponibles à scrapper, d'après celles récoltés dans
# la fonction collect_url_home_category(). Puis laisse l'utilisateur définir les
# catégories qui sont à scrapper.
def selection_category_for_scrap_func(all_url_home_page_category_book):
    category_possible = []

    # Collecte les différents noms des catégories du site marchand et les ajoute
    # à la liste nommée category_possible.
    def collect_category_possible(all_url_home_page_category_book):
        for category_book in all_url_home_page_category_book:
            category_possible.append(category_book[51:-13]
                                     .replace('_', '')
                                     .replace('-', ' ')
                                     .capitalize())
        demand_of_user_what_category_to_scrap()

    # Input pour connaître les catégories de livers à scrapper, avec
    # présentations des différentes options possibles.
    # '-quit' plutôt qui '-q' ou 'q' pour éviter les sorties du script
    # accidentelles.
    def demand_of_user_what_category_to_scrap():
        all_input_user = [input(('{0}' * 56
                                 + '\n#{1:^54}#\n'
                                 + '{0}' * 56 + '\n\n' +
                                 '{2:<16} : {3}\n' +
                                 '{4:<16} : {5}\n' +
                                 '{6:<16} : {7}\n' +
                                 '{8:<16} : {9}\n')
                                .format('#',
                                        'Quelles catégories de livres sont à '
                                        'scraper ?',
                                        '-noms categories', 'toutes les entrées'
                                                            ' sur la même ligne'
                                                            '',
                                        '-all', 'TOUTES les catégories',
                                        '-list', 'catégories disponible au '
                                                 'scrap',
                                        '-quit', 'interrompt le script'))]
        analyze_and_collect_input_user(all_input_user)

    # Exécute les options par défaut is présent dans l'input (-list or -quit or
    # -all). Sinon envoi l'input dans la fonction suivant qui déterminera les
    # catégories renseignées.
    def analyze_and_collect_input_user(all_input_user):
        for input_user in all_input_user:
            if input_user == '-list':
                category_possible_sorted = sorted(category_possible)
                # Titre de la liste de catégories.
                print('\n{0:#^100}\n#{1:^98}#\n{0:#^100}\n'
                      .format('',
                              'Catégories disponibles pour le scrapping.'))
                # Affichage des catégories de livres disponibles, rangées par
                # ordre alphabétique et disposées en 5 colonnes (20 caractères
                # par nom de catégories, alignement gauche) sur le nombres de
                # lignes nécessaires.
                number_row_less_one = len(category_possible_sorted) // 5
                number_category_in_last_row = len(category_possible_sorted) % 5
                for start_index_category_by_int_row in \
                        range(0, number_row_less_one * 5, 5):
                    end_index_show_by_int_row = start_index_category_by_int_row \
                                                + 4
                    print('{0:<20}{1:<20}{2:<20}{3:<20}{4:<20}'
                          .format(category_possible_sorted
                                  [start_index_category_by_int_row],
                                  category_possible_sorted
                                  [start_index_category_by_int_row + 1],
                                  category_possible_sorted
                                  [start_index_category_by_int_row + 2],
                                  category_possible_sorted
                                  [start_index_category_by_int_row + 3],
                                  category_possible_sorted
                                  [end_index_show_by_int_row]))
                if number_category_in_last_row == 1:
                    print('{:<20}'
                          .format(category_possible_sorted
                                  [number_row_less_one * 5]))
                elif number_category_in_last_row == 2:
                    print('{0:<20}{1:<20}'
                          .format(category_possible_sorted
                                  [number_row_less_one * 5],
                                  category_possible_sorted
                                  [number_row_less_one * 5 + 1]))
                elif number_category_in_last_row == 3:
                    print('{0:<20}{1:<20}{2:<20}'
                          .format(category_possible_sorted
                                  [number_row_less_one * 5],
                                  category_possible_sorted
                                  [number_row_less_one * 5 + 1],
                                  category_possible_sorted
                                  [number_row_less_one * 5 + 2]))
                elif number_category_in_last_row == 4:
                    print('{0:<20}{1:<20}{2:<20}{3:<20}'
                          .format(category_possible_sorted
                                  [number_row_less_one * 5],
                                  category_possible_sorted
                                  [number_row_less_one * 5 + 1],
                                  category_possible_sorted
                                  [number_row_less_one * 5 + 2],
                                  category_possible_sorted
                                  [number_row_less_one * 5 + 3], ))
                all_input_user.clear()
                all_input_user \
                    .append(input(('\n' +
                                   '{0:<16} : {1}\n' +
                                   '{2:<16} : {3}\n' +
                                   '{4:<16} : {5}\n')
                                  .format('-noms catégories', 'toutes les '
                                                              'entrées sur la '
                                                              'même ligne',
                                          '-all', 'TOUTES les catégories',
                                          '-quit', 'interrompt le scrit')))
                analyze_and_collect_input_user(all_input_user)
            elif input_user == '-all':
                # Utilisation d'un compteur pour quitter aisément la boucle.
                counter_of_confirm = 0
                while counter_of_confirm == 0:
                    print('\nVous avez choisit TOUTES les catégories :')
                    confirmation_select_category = \
                        input(('{0:<5} : {1}\n' +
                               '{2:<5} : {3}\n')
                              .format('y/n', 'confirmer/refaire la sélection',
                                      '-quit', 'interrompt le script'))
                    if confirmation_select_category == 'y':
                        for index_cat, cat in enumerate(category_possible):
                            category_validate_to_scrap \
                                .append(category_possible[index_cat])
                            counter_of_confirm += 1
                    elif confirmation_select_category == 'n':
                        counter_of_confirm += 1
                        demand_of_user_what_category_to_scrap()
                    elif confirmation_select_category == '-quit':
                        sys.exit()
                    elif confirmation_select_category != 'y' \
                            and confirmation_select_category != 'n':
                        print('\nRéponse invalide')
            elif input_user == '-quit':
                sys.exit()
            elif input_user is not '-list' or input_user is not '-all':
                analyze_category_select_by_user(all_input_user)

    def analyze_category_select_by_user(all_input_user):
        all_category_want_by_user = []
        if len(all_input_user) == 1:
            for index_all_input_user, character_all_input_user in enumerate(
                    all_input_user[0]):
                if character_all_input_user == '-':
                    index_start_input_current = index_all_input_user + 1
                    index_end_input_current = index_start_input_current
                    while all_input_user[0][index_end_input_current] != '-':
                        if index_end_input_current < len(all_input_user[0]) - 1:
                            index_end_input_current += 1
                        elif index_end_input_current == len(
                                all_input_user[0]) - 1:
                            break
                    # [:index_end_input_current +1] car la valeur d'index est un stop exclu. Il n'est pas pris en compte
                    input_current = all_input_user[0][
                                    index_start_input_current:index_end_input_current + 1]
                    if input_current[-1] == '-':
                        all_category_want_by_user.append(input_current[:-2])
                    else:
                        all_category_want_by_user.append(input_current)
                else:
                    continue
        comparate_name_ask_with_name_category(all_category_want_by_user)

    def comparate_name_ask_with_name_category(category_to_analyze):
        category_reword = []
        for index_category_want, category_in_analyze in enumerate(
                category_to_analyze):
            count_of_disparity = 0
            for index_category_possible, name_category_possible in enumerate(
                    category_possible):
                if category_in_analyze == name_category_possible.lower():
                    category_validate_temp.append(category_in_analyze)
                    break
                elif category_in_analyze != name_category_possible.lower():
                    count_of_disparity += 1
            if count_of_disparity == len(category_possible):
                reword = input(('\n\'{0}\' {1}\n' +
                                '{2}\n' +
                                '{3:<5} : {4}\n' +
                                '{5:<5} : {6}\n')
                               .format(category_in_analyze,
                                       'n\'est pas reconnue',
                                       'Reformulez sous la forme \'-noms categories\'',
                                       '-pass', 'ne rien ajouter',
                                       '-quit', 'interrompt le script'))
                # .format(category_in_analyze))
                if reword != '-pass':
                    category_reword.append(reword[1:])
                elif reword == '-quit':
                    sys.exit()

        if len(category_reword) != 0:
            comparate_name_ask_with_name_category(category_reword)
        else:
            if len(category_validate_temp) == 1:
                count_of_confirm_error = 0
                while count_of_confirm_error == 0:
                    confirm_category_choose = input('\nVous avez selectionné\n'
                                                    '{}\n'
                                                    '\'y/n\' ?\n'
                                                    .format(
                        category_validate_temp))
                    if confirm_category_choose == 'y':
                        category_validate_to_scrap.append(
                            category_validate_temp[0])
                        count_of_confirm_error += 1
                    # collect_url_home_category(category_validate_to_scrap     LANCER LA SUITE DU SCRIPT
                    elif confirm_category_choose == 'n':
                        #                 QUE FAIRE SI LA SÉLECTION N'EST PAS VALIDER ???
                        print(
                            '\nBon ben… Revenez lorque vous saurez ce que vous souhaitez')
                        count_of_confirm_error += 1
                    elif confirm_category_choose != 'y' and confirm_category_choose != 'n':
                        print('\nRéponse invalide\n\n')
            elif len(category_validate_temp) > 1:
                count_of_confirm_error = 0
                while count_of_confirm_error == 0:
                    # Formater l'affichage en 4 colones avec 20 caractères
                    # alloués pour chaque noms de catégories
                    confirm_category_choose = input('\nVous avez selectionnés\n'
                                                    '{}\n'
                                                    '\'y/n\' ?\n'
                                                    .format(
                        category_validate_temp))
                    if confirm_category_choose == 'y':
                        for index_cat_temp, cat_temp in enumerate(
                                category_validate_temp):
                            category_validate_to_scrap.append(
                                category_validate_temp[index_cat_temp])
                            count_of_confirm_error += 1
                    elif confirm_category_choose == 'n':
                        #                 QUE FAIRE SI LA SÉLECTION N'EST PAS VALIDER ???
                        print(
                            '\nBon ben… Revenez lorque vous saurez ce que vous souhaitez')
                        count_of_confirm_error += 1
                    elif confirm_category_choose != 'y' and confirm_category_choose != 'n':
                        print('\nRéponse invalide')

    category_validate_temp = []
    category_validate_to_scrap = []
    collect_category_possible(all_url_home_page_category_book)


    url_home_category_to_scrap = []
    def category_to_scrap(category_validate_to_scrap):
        if len(category_validate_to_scrap) != 0:
            for category in category_validate_to_scrap:
                temp_for_search = category.replace(' ', '-').lower()
                for idx, url in enumerate(all_url_home_page_category_book):
                    similarity = re.findall(temp_for_search + '_', url)
                    if similarity != []:
                        url_home_category_to_scrap.append(url)
            return url_home_category_to_scrap
        else:
            print('Aucunes catégories de livres n\'a été renseigné')

    category_to_scrap(category_validate_to_scrap)
    return url_home_category_to_scrap