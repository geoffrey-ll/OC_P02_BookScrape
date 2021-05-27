import re

text = "bonjour j'ai 2 velos et 1 voiture et 135 euros"


result = re.findall("[0-9]+",  text)

print(result)