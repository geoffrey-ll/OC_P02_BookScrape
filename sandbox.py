import re
import os

text = "bonjour j'ai 2 velos et 1 voiture et 135 euros"
chemin = 'C:\open_class_rooms\p02\output\philosophy\cover_philosophy/at_the_existentialist_café_-__freedom,_being,_and_apricot_cocktails_with_-__jean-paul_sartre,_simone_de_beauvoir,_albert_camus,_martin_heidegger,_edmund_husserl,_karl_jaspers,_mauric'

chemin_max = 'C:\open_class_rooms\p02\output\philosophy\cover_philosophy/at_the_existentialist_café_-__freedom,_being,_and_apricot_cocktails_with_-__jean-paul_sartre,_simone_de_beauvoir,_albert_camus,_martin_heidegger,_edmund_husserl,_karl_jaspers,_mauric (1)vvvvvvvvvv'
result = re.sub("[0-9]+", 'nope', text)

chemin_other = 'C:\open_class_rooms\p02\output\philosophy/at_the_existentialist_café_-__freedom,_being,_and_apricot_cocktails_with_-__jean-paul_sartre,_simone_de_beauvoir,_albert_camus,_martin_heidegger,_edmund_husserl,_karl_jaspers,_mauric (1)vvvvvvvvvvlllllllllllllllll'

print('len chemin', len(chemin), '\nlen chemin_max', len(chemin_max), '\nlen chemin_other', len(chemin_other))

print(len('output\philosophy\cover_philosophy'))




