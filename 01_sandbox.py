import re
import os

text = "bonjour j'ai 2 velos et 1 voiture et 135 euros"


result = re.findall("[0-9]+",  text)[2]

print(result)

if os.path.exists('../p15') == False:
    os.mkdir('../p15')