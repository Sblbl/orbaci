import os
import numpy as np
import math
import librosa
import matplotlib.image as img
import matplotlib.pyplot as plt

import img_processing
import audio_processing

from PIL import Image
from patterns import mod_0, mod_1, mod_2, mod_3

import warnings
warnings.filterwarnings('ignore')


in_fol = 'input/'
out_fol = 'output/'
im_filename = None
au_filename = None
k = 3
pooling_size = [3, 3]

for file in os.listdir(in_fol):
	if file.endswith('.jpg'):
		im_filename = file
	elif file.endswith('.m4a') or file.endswith('.mp3') :
		au_filename = file

im_name = im_filename[:-4]
au_name = au_filename[:-4]

print('\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359')
print('Nice to see you!')
print('\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359')


"""
IMAGE PREPROCESSING
"""

print('\U0001F303', '\tfound', im_filename, 'as image')
print('\U0001F3A7', '\tfound', au_filename, 'as audio')

image = Image.open(in_fol + im_filename)
 
horizontal = False

if image.size[0] > image.size[1]:
	image = image.resize((225, 150))
	horizontal = True
else: 
	image = image.resize((150,225))
	
im = np.asarray(image)

dominants = img_processing.get_cols(im, k)
# TODO: add possibility to choose n° of clusters

print('\U0001F3A8', '\tdominant colours found:', dominants)

# TODO: add possibility to set the pooling size
pooled = img_processing.poolingOverlap(im, pooling_size,stride=None,method='avg',pad=False)
print('\U0001F3CA', '\tcreated pooled image with pooling =', pooling_size)

pooled_dom = img_processing.transform_in_dominant(pooled, dominants)
print('\U0001F308', '\ttransformed pooled image to only dominants')

np.save(out_fol + im_name + '.npy', pooled_dom)

"""
AUDIO PREPROCESSING
"""
y, sr = librosa.load(in_fol + au_filename)
chroma = audio_processing.chroma(y, sr, au_name)
if chroma.shape[1] > 198:
	chroma = chroma[:, :198]
print('\U0001F3BC', '\tcreated chromagram for', au_name)

np.save(out_fol + 'chroma_' + au_name + '.npy', chroma)

"""
TEXTILE GENERATION
"""

pooled_dom = img_processing.resize(pooled_dom)
plt.imsave((out_fol + im_name + '_pooled.png'), pooled_dom/255)

chromapool = img_processing.poolingOverlap(chroma,(3, 5),stride=(1, 8),method='mean',pad=False)
chrim = Image.fromarray((chromapool)*255)
chrim = np.asarray(chrim)
print('\U0001F3B9', '\tpooled chromagram')

remapped = audio_processing.remap(chrim)
mask = audio_processing.create_mask(remapped, [mod_0, mod_1, mod_2, mod_3])
print('\U0001F47A', '\tcreated mask')

plt.imsave(out_fol + 'mask_' + im_name + '.png', mask, cmap='binary')
plt.imsave(out_fol + 'mask_' + im_name + '.svg', mask, cmap='binary')

mask = np.array([mask.T, mask.T, mask.T]).T

textile = img_processing.apply_mask(pooled_dom, mask)
plt.imsave(out_fol + 'textile_' + im_name + '.png', textile/255)
plt.imsave(out_fol + 'textile_' + im_name + '.svg', textile/255)
print('\U0001F458', '\tcreated textile')
print('\U0001F411', '\tfinished')