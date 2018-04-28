""" Optic Disk Connection 

This script will open images in a dataset and 
detect the OD in each image. The resulting fitted
OD images will be saved in the OUTPUT directory.

Note: The input images must be normalised beforehand.

Usage:
    dtect_od.py ROOT OUTPUT PCA

Arguments:
    ROOT            The root directory of the image dataset.
    OUTPUT          The output directory to save the analysis files.
    PCA 			The path to the PCA file
"""

import files # For the file management stuff
import os, sys # For directory changing, sys stuff
import utilities as ut
import analysis as an
import numpy as np
from colorama import Style, Fore, init # Colouring CLI stuff
from docopt import docopt # CLI argument parser 
from matplotlib import pyplot as plt


# Main program here 
if __name__== "__main__":

	# Change cwd to the current file's directory
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	# init colourama to filter ANSI chars in windows/linux
	init() 

	# Change colour of usage to RED (help text)
	__doc__ = Fore.RED + __doc__ + Style.RESET_ALL

	# Use __doc__ string to parse cmd arguments
	arguments = docopt(__doc__, version="1.0")


	################################################
	## PARSING THE CLI STUFF AND MAIN PROGRAM FLOW #
	################################################


	# Get the root and output dirs absolute paths
	root_path = files.abspath(arguments['ROOT'])
	out_path = files.abspath(arguments['OUTPUT'])
	pca_path = files.abspath(arguments['PCA'])

	# For now, just print out settings and  all the images in the root.
	print(Fore.BLUE + "Settings passed: ")
	print("Root directory........ %s" % root_path)
	print("Output directory...... %s\n" % out_path)

	# Check that both directories exist
	if os.path.lexists(out_path) and os.path.lexists(root_path):
		pass
	else:
		print(Fore.RED + "Path not found, one of the directories does not exist.")
		print(Style.RESET_ALL)
		sys.exit(0) # Use system's abort function

	# Reset colour
	print(Style.RESET_ALL)

	# Load PCA
	PCA = np.loadtxt(pca_path)

	# Loading a list of image paths
	images = files.get_images(root_path) # Note line below resets the blue 
	print(Style.RESET_ALL + Fore.GREEN + "Number of images in the path: {:d}".format(len(images)))

	size = 20 # Length of the loading bar in chars

	# Create the correlation array
	corr_array = np.zeros(image.shape)

	# Settings (window size)
	width, height = 30, 30

	# Create the circular mask (from the center) to remove
	# the iamge circular boarders.
	Xs = np.ones((N,N))*np.arange(N)
	Ys = Xs.T
	r = 180 # Radius (from center) in pixels
	s = np.floor(N/2) # Displacement
	Xs, Ys = Xs - s, Ys - s
	Dist = Xs*Xs + Ys*Ys
	mask = Dist < r**2

	# Loading all the images in the path and detecting the OD in them
	for i, img_path in enumerate(images):
		img = ut.read_image(img_path, "BGR2GRAY")
		img = cv2.resize(image, (450,450), cv2.INTER_AREA)

		# Sliding algorithm (y,x is the center pixel)
		offset = np.max([width, height])//2 + 2 # The offset from the boarders
		for y in range(offset, N-offset, 5):
		    for x in range(offset, N-offset, 5):
		        
		        # Tuples to represent the window box
		        starts = np.array([y-height/2, x-width/2], dtype=int)
		        stops = np.array([starts[0]+height, starts[1]+width], dtype=int)
		        
		        window = img[starts[0]:stops[0], starts[1]:stops[1]]

		        # PCA reconstruction
		        weights = np.dot(np.ravel(window), PCA)
		        recons = np.sum(weights*PCA, axis=1).astype("uint8")
		        
		        # Set the value of the comparing matrix
		        corr_array[y,x] = cv2.matchTemplate(recons.reshape(height,width), window, cv2.TM_CCOEFF)

		# Normalise the array
		corr_array[corr_array < 0] = 0 # Threshold by 0
		cv2.normalize(corr_array, corr_array, 0, 255, cv2.NORM_MINMAX)

		# Apply mask
		corr_array *= mask
	print("\nFinished processing.")
