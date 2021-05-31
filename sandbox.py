import re
import os

text = 'Mon texte de test. Un peu plus de texte'
text2 = 'Ce texte ne commence pas par \'M\''
texts = [text, text2]

print(texts)

for texte in texts:

    method_test = str(texte).startswith('Mon')
    print(method_test)
    if method_test is True:
        print('Ce texte \'' +  texte + '\' commence bien par \'Mon')
    if method_test is False:
        print('Ce texte \'' + texte + '\' ne commence pas par \'Mon')


blabla = 'Beaucoup de blabla pour ne rien blablater'
print(blabla)
blabla = ''
print(blabla)
blabla = 'Qu\'est-il devenu ?'
print(blabla)
