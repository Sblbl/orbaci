import pandas as pd
import numpy as np
from scipy.cluster.vq import kmeans
from PIL import Image
import math

def get_cols(im, k):

	r = []
	g = []
	b = []
	
	# store color in separated channels
	for row in im:
		for temp_r, temp_g, temp_b in row:
			# normalise to make it faster
			r.append(temp_r/255)
			g.append(temp_g/255)
			b.append(temp_b/255)
			
	im_df = pd.DataFrame({'red' : r, 'green' : g, 'blue' : b})
	im_df = im_df.astype('float64')
	#print(im_df.info())
	
	centers, _ = kmeans(im_df[['red', 'green', 'blue']], k)
	colours = []
	
	for center in centers:
		red_scaled, green_scaled, blue_scaled = center
		#print(red_scaled, green_scaled, blue_scaled)
		colours.append([
			# restore values 0 - 255
			int(red_scaled*255), 
			int(green_scaled*255), 
			int(blue_scaled*255)
		])

	return colours


# from https://stackoverflow.com/questions/42463172/how-to-perform-max-mean-pooling-on-a-2d-array-using-numpy
def asStride(arr,sub_shape,stride):
	'''
	Get a strided sub-matrices view of an ndarray.
	See also skimage.util.shape.view_as_windows()
	'''
	s0,s1=arr.strides[:2]
	m1,n1=arr.shape[:2]
	m2,n2=sub_shape
	view_shape=(1+(m1-m2)//stride[0],1+(n1-n2)//stride[1],m2,n2)+arr.shape[2:]
	strides=(stride[0]*s0,stride[1]*s1,s0,s1)+arr.strides[2:]
	subs=np.lib.stride_tricks.as_strided(arr,view_shape,strides=strides)
	return subs

def poolingOverlap(mat,ksize,stride=None,method='max',pad=False):
	'''
	Overlapping pooling on 2D or 3D data.
	<mat>: ndarray, input array to pool.
	<ksize>: tuple of 2, kernel size in (ky, kx).
	<stride>: tuple of 2 or None, stride of pooling window.
			  If None, same as <ksize> (non-overlapping pooling).
	<method>: str, 'max for max-pooling,
				   'mean' for mean-pooling.
	<pad>: bool, pad <mat> or not. If no pad, output has size
		   (n-f)//s+1, n being <mat> size, f being kernel size, s stride.
		   if pad, output has size ceil(n/s).
	Return <result>: pooled matrix.
	'''

	m, n = mat.shape[:2]
	ky,kx=ksize
	if stride is None:
		stride=(ky,kx)
	sy,sx=stride

	_ceil=lambda x,y: int(np.ceil(x/float(y)))

	if pad:
		ny=_ceil(m,sy)
		nx=_ceil(n,sx)
		size=((ny-1)*sy+ky, (nx-1)*sx+kx) + mat.shape[2:]
		mat_pad=np.full(size,np.nan)
		mat_pad[:m,:n,...]=mat
	else:
		mat_pad=mat[:(m-ky)//sy*sy+ky, :(n-kx)//sx*sx+kx, ...]

	view=asStride(mat_pad,ksize,stride)

	if method=='max':
		result=np.nanmax(view,axis=(2,3))
	else:
		result=np.nanmean(view,axis=(2,3))

	return result

def colour_similarity(col_1, col_2):
	r_mean = math.ceil((col_1[0] + col_2[0]) / 2)
	r = math.ceil(col_1[0]) - math.ceil(col_2[0])
	g = math.ceil(col_1[1]) - math.ceil(col_2[1])
	b = math.ceil(col_1[2]) - math.ceil(col_2[2])
	
	distance = math.ceil(math.sqrt( (((512+r_mean)*r*r)>>8) + 4*g*g + (((767-r_mean)*b*b)>>8) ))
	similarity = float('{:.2f}'.format((765 - distance)/765))
	
	#print('distance: '+ str(distance) + ' - similarity: '+ str(similarity))
	return(similarity)

def transform_in_dominant(im, dominants):
	new_im = []
	for i in range(len(im)):
		new_im.append([])
		for j in range(len(im[0])):
			in_col = [im[i][j][0], im[i][j][1], im[i][j][2]]
			similarities = []
			#compute distance between each pixel and each dominant col
			for dominant in dominants:
				similarities.append(colour_similarity(in_col, dominant))
			#get the most similar
			out_col = dominants[similarities.index(max(similarities))]
			new_im[i].append(out_col)
	return np.array(new_im)

def resize(image, w, h):
	im = Image.fromarray(np.uint8(image))
	im = im.resize((w, h), Image.NEAREST)	
	im = np.asarray(im)
	return im

def apply_mask(im, mask):
	textile = []
	for i in range(im.shape[0]):
		row = []
		for j in range(im.shape[1]):
			if mask[i][j][0] == 0:
				row.append(np.array([255, 255, 255]))
			else:
				row.append(im[i][j])
		textile.append(row)
		
	return np.array(textile)

def apply_grid(ar, reps=8):
	result = []
	for x in range(ar.shape[0]):
		for repx in range(reps):
			row = []
			for y in range(ar.shape[1]):
				for repy in range(reps):
					row.append(ar[x][y])
				row.append([0, 255, 255])
			result.append(row)
			g_row = []
		for i in range(len(row)):
			g_row.append([0, 255, 255])
		result.append(g_row)
	result = np.array(result)
	return(np.array(result))