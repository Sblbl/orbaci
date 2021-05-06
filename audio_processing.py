import librosa
import numpy as np

def chroma(y, sr, title='plot'):
	y_harmonic, y_percussive = librosa.effects.hpss(y)
	# We'll use a CQT-based chromagram with 36 bins-per-octave in the CQT analysis.  An STFT-based implementation also exists in chroma_stft()
	# We'll use the harmonic component to avoid pollution from transients
	#C = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, bins_per_octave=36)
	C = librosa.feature.chroma_stft(y=y_harmonic, sr=sr)
	#print(C)
	
	return C

def create_mask(pooled_chroma, modules):
	pooled_chroma = pooled_chroma.astype(int)
	result = []
	for row in pooled_chroma:
		expanded_row = []
		for el in row:
			if len(expanded_row) == 0:
				expanded_row = modules[int(el)]
			else:
				expanded_row = np.concatenate((expanded_row, modules[el]), axis=1)
		result.append(expanded_row)
	final_result = result[0]
	for i, el in enumerate(result):
		if i == 0:
			pass
		else:
			final_result =  np.concatenate((final_result, el), axis=0)
	return final_result

def remap(chroma):
	return np.floor(chroma/63.75)