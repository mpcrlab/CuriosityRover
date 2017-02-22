import tensorflow as tf
import numpy as np
from skimage.util import view_as_windows

class LCADictionary():
	def __init__(self):
		self.patch_size = 64 * 3 # patch size 8x8x3
		self.num_dict_patches = 200 # number of dictionary patches
		self.threshhold = 0.1
		self.ps = np.sqrt(self.patch_size / 3)
		self.alpha = None
		# Initializing random dictionary
		self.LCADict = np.random.rand(self.patch_size, self.num_dict_patches)


	# Updates dictionary with one 
	# frame at a time

	# Passed in 120,320,3 image
	def update(self, image):
		patches = view_as_windows(image, (self.ps, self.ps, 3))

		patches=patches.reshape([patches.shape[0]* 
								patches.shape[1]*
								patches.shape[2], -1])

		patches=np.transpose(patches) 

		patches = (patches - np.mean(patches)) / (np.std(patches, axis=0) + 1e-6)

		# Scales dictionary between 0 -> 1 from 0 -> 255
		self.LCADict = np.matmul(self.LCADict, np.diag(1/tf.sqrt(np.sum(self.LCADict**2, 0))))

		# Get sparse coeficients of dictionary to recover patches 
		self.alpha = np.matmul(tf.transpose(self.LCADict), patches)

		# Scales dictionary between 0 -> 1
		self.alpha = np.matmul(self.alpha, np.diag(1/np.sqrt(np.reduce_sum(self.alpha**2, 0))))

		# Cubic sparsity function
		self.alpha=0.3 * self.alpha**3

		# Updates dictionary
		self.LCADict = self.LCADict+np.matmul((patches-np.matmul(self.LCADict, self.alpha)), np.transpose(self.alpha))


	def isImageRepresented(self, image):
		if self.alpha is None:
			return False
        
		# Get sum along zero axis in LCADict
		l1_norm = np.sum(self.alpha, axis=0)

		#get minimum l1 norm index
		min_l1_norm = np.where(l1_norm == l1_norm.min())
		print ("l1 norm:", l1_norm)
		

		if min_l1_norm > self.threshold:
			return True
		else:
			return False



	def clear(self):
	    pass