import os
import numpy as np
import math
import librosa
import matplotlib.image as img
import matplotlib.pyplot as plt

import img_processing
import audio_processing
from settings import settings

from PIL import Image

import warnings
warnings.filterwarnings('ignore')


"""
LOADINGS
"""

in_fol = 'input/'
out_fol = 'output/'
im_filename = None
au_filename = None
k = settings['colours']
width = settings['width']
height = settings['height']
pooling_size = [3, 3]

print('\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359')
print('Nice to see you!')
print('\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\U0001F359\n')

for file in os.listdir(in_fol):
	if file.endswith('.jpg'):
		im_filename = file
	elif file.endswith('.m4a') or file.endswith('.mp3') :
		au_filename = file

im_name = im_filename[:-4]
au_name = au_filename[:-4]

print('🖼', '\tfound', im_filename, 'as image')
print('🎙', '\tfound', au_filename, 'as audio')
print('🏟', '\tfound settings: width =', width, '\theight =', height,'\n')

mod_0 = np.genfromtxt(in_fol + 'p_0.dat', delimiter=',')
print('🌒', '\tfound pattern 0')
mod_1 = np.genfromtxt(in_fol + 'p_1.dat', delimiter=',')
print('🌓', '\tfound pattern 1')
mod_2 = np.genfromtxt(in_fol + 'p_2.dat', delimiter=',')
print('🌔', '\tfound pattern 2')
mod_3 = np.genfromtxt(in_fol + 'p_3.dat', delimiter=',')
print('🌕', '\tfound pattern 3\n')

pooling_size_audio = (mod_0.shape[0], mod_0.shape[1])
stride_audio = (mod_0.shape[0], mod_0.shape[1])


"""
IMAGE PREPROCESSING
"""

image = Image.open(in_fol + im_filename)

image = image.resize((width, height))

im = np.asarray(image)
dominants = img_processing.get_cols(im, k)


print('🌈', '\tdominant colours found:', dominants)

pooled = img_processing.poolingOverlap(
			im, 
			pooling_size,
			stride = None,
			method = 'avg',
			pad = False
			)

print('🏊‍♂️', '\tcreated pooled image of shape', pooled.shape)

pooled_dom = img_processing.transform_in_dominant(pooled, dominants)
pooled_dom = img_processing.resize(pooled_dom, width, height)
plt.imsave((out_fol + im_name + '_pooled.png'), pooled_dom/255)

print('🎨', '\ttransformed pooled image to only dominants\n')

"""
AUDIO PREPROCESSING
"""
y, sr = librosa.load(in_fol + au_filename)
chroma = audio_processing.chroma(y, sr, au_name)
if chroma.shape[1] > 198:
	chroma = chroma[:, :198]
print('📯', '\tcreated chromagram for', au_name)

"""
TEXTILE GENERATION
"""

chroma = Image.fromarray((chroma))
chroma = chroma.resize((width, height))
plt.imsave(out_fol + 'chroma_' + au_name + '.png', chroma, cmap='gray')
chroma = np.array(chroma)

chromapool = img_processing.poolingOverlap(
			chroma,
			pooling_size_audio,
			stride = (stride_audio),
			method='mean',
			pad=False)

chrim = Image.fromarray((chromapool)*255)
chrim = np.asarray(chrim)
print('🎹', '\tpooled chromagram of size', chromapool.shape)

remapped = audio_processing.remap(chrim)
mask = audio_processing.create_mask(remapped, [mod_0, mod_1, mod_2, mod_3])
print('👺', '\tcreated mask')

plt.imsave(out_fol + 'mask_' + im_name + '.png', mask, cmap='binary')
plt.imsave(out_fol + 'mask_' + im_name + '.svg', mask, cmap='binary')

mask = np.array([mask.T, mask.T, mask.T]).T

textile = img_processing.apply_mask(pooled_dom, mask)
plt.imsave(out_fol + 'textile_' + im_name + '.png', textile/255)
plt.imsave(out_fol + 'textile_' + im_name + '.svg', textile/255)
gridded = img_processing.apply_grid(textile)
plt.imsave(out_fol + 'textile_grid_' + im_name + '.svg', gridded/255)
print('🧵', '\tcreated textile\n')
print('🐏', '\tfinished')