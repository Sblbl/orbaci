"""
Calculates the padding and the pattern size
to obtain the desired output
hello
"""
import os
import numpy as np
import matplotlib.image as img
from PIL import Image
import json

"""
LOADINGS
"""

in_fol = 'input/'
settings_filename = None
chroma_shape = [12, 198]

for file in os.listdir(in_fol):
	elif file.endswith('.json'):
		settings_filename = file

settings_name = settings_filename[:-5]

print('🤖', '\tfound', settings_name, 'as settings\n')

with open('input/' + settings_filename, 'r') as f:
	settings = json.load(f)

print('🤖', '\tso you want a ', settings['width'], 'x', /
	settings['height'], 'textile.\n\tLet me calculate it for ya.')

"""
CALCULATIONS

In realtà basta regolare il pooling dell'audio 
perché l'immagine sarà già ritrasformata 
nella dimensione adatta.

Quindi il problema sta solo nel trovare 
il giusto pooling del suono. 
Questo possibilmente dando la possibilità 
di scegliere diverse misure di pattern.

Idea: far stabilire all'utente la dimensione 
dei pattern + trattare il suono al pari dell'immagine,
strecciarlo per fargli raggiungere le stesse dimensioni
e applicare lo stesso pooling dell'immagine
"""


