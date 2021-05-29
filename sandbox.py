import re
import os

text = "bonjour j'ai 2 velos et 1 voiture et 135 euros"


result = re.sub("[0-9]+", 'nope', text)

print(result)
