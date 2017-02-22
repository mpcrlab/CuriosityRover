import numpy as np
from skimage.util import view_as_windows

class LCADictionary():
	def __init__(self):
		self.ps = np.array([8, 8, 3]) # patch size 8x8x3
		self.num_dict_patches = 200  # number of dictionary patches
		self.threshhold = 0.1
		self.alpha = None  # initialize sparse coefficients 

		# Initializing dictionary with random values
		self.LCADict = np.random.rand(self.ps.size, self.num_dict_patches)


	# Updates dictionary with one 
	# frame at a time

	# Passed in 120,320,3 image
	def update(self, image):

		# get 8x8x3 patches from the video frame
		patches = view_as_windows(image, (self.ps[0], self.ps[1], self.ps[2]))

		#vectorize patches 
		patches=patches.reshape([patches.shape[0]* 
								patches.shape[1]*
								patches.shape[2], -1])

		patches=np.transpose(patches) 

		patches = (patches - np.mean(patches)) / (np.std(patches, axis=0) + 1e-6)

		# Scales dictionary between 0 -> 1 from 0 -> 255
		self.LCADict = np.matmul(self.LCADict, np.diag(1/np.sqrt(np.sum(self.LCADict**2, 0))))

		# Get sparse coeficients of dictionary to recover patches 
		self.alpha = np.matmul(np.transpose(self.LCADict), patches)

		# Normalizes dictionary between 0 -> 1
		self.alpha = np.matmul(self.alpha, np.diag(1/np.sqrt(np.reduce_sum(self.alpha**2, 0))))

		# Cubic sparsity function
		self.alpha=0.3 * self.alpha**3

		# Dictionary update step
		self.LCADict = self.LCADict+np.matmul((patches-np.matmul(self.LCADict, self.alpha)), np.transpose(self.alpha))


	def isImageRepresented(self, image):
		''' Determines if the objects in the frame are represented well in the short-term dictionary by
			taking the l1-norm of each sparse coefficient vector. The one with the lowest activations 
			is not represented well by the dictionary, and is a novel object. '''

		if self.alpha is None:
			return False
        
		# Get l1-norm of each sparse coefficient vector
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
