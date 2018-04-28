""" Optic Disk Connection 

This script will open images in a dataset and 
detect the OD in each image. The resulting fitted
OD images will be saved in the OUTPUT directory.

Note: The input images must be normalised beforehand.

Usage:
    detect_od.py ROOT OUTPUT PCA

Arguments:
    ROOT            The root directory of the image dataset.
    OUTPUT          The output directory to save the analysis files.
    PCA 			The path to the PCA file
"""

import files # For the file management stuff
import os, sys, cv2 # For directory changing, sys stuff
import utilities as ut
import analysis as an
import numpy as np
from colorama import Style, Fore, init # Colouring CLI stuff
from docopt import docopt # CLI argument parser 
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


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
	N = 450 # N is the square size of the image (make sure matches PCA sections)
	corr_array = np.zeros((N,N))

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

	#############################################################
	# Params for fitting the curve to the image and displaying it
	max_weight = 5 # Max weights of points (0-max)
	Xs = np.linspace(0, 450, 2000) # The linspace X for drawing line

	# The hypothesis function 
	def func(x, a, b, c): # So we can fit a parabola 
		return a*x**2 + b*x + c

	# Loading all the images in the path and detecting the OD in them
	for i, img_path in enumerate(images):
		img = ut.read_image(img_path, "BGR2GRAY")
		img = cv2.resize(img, (450,450), cv2.INTER_AREA)
		masked_img = img*mask

		# Sliding algorithm (y,x is the center pixel)
		offset = np.max([width, height])//2 + 2 # The offset from the boarders
		for y in range(offset, N-offset, 5):
		    for x in range(offset, N-offset, 5):
		        
		        # Tuples to represent the window box
		        starts = np.array([y-height/2, x-width/2], dtype=int)
		        stops = np.array([starts[0]+height, starts[1]+width], dtype=int)
		        
		        window = masked_img[starts[0]:stops[0], starts[1]:stops[1]]

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

		##########################
		###### Line Fitting ######
		##########################
		cv2.normalize(corr_array, corr_array, 0, max_weight, cv2.NORM_MINMAX)
		corr_array = np.round(corr_array)
		points = np.empty((2,0), dtype=int)

		for w in range(1, max_weight):
		    # Corresponding layer in depth matrix is bool repr.
		    # corresponding weight locations
		    coords = np.vstack(np.where(corr_array == w))
		    points = np.hstack((points, np.repeat(coords, w, axis=1)))

		# Fit the line parameters and get new Ys (based on the Xs)
		params, ppcov = curve_fit(func, points[0,:], points[1,:])
		b, c, d = params
		Ys = b*Xs**2 + c*Xs + d

		# Clip the lines (so we dont go off the img)
		points = np.vstack((Xs, Ys))
		x_clip = np.logical_or(Xs < 20, Xs > 420)
		y_clip = np.logical_or(Ys < 20, Xs > 420)
		clip = np.logical_not(np.logical_or(x_clip, y_clip))

		# Get the extrema
		ext_x = -c/(2*b)
		ext_y = b*ext_x**2 + c*ext_x + d
		# Draw circle in the od 
		cv2.circle(img,(int(ext_y),int(ext_x)), 10, (255,0,0), -1)


		# Saving the figure and the line
		my_dpi = 96 # DPA of YOUR monitor (for exact size)
		fig = plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
		ax = plt.gca()
		ax.set_axis_off()
		ax.imshow(img, cmap="gray")
		ax.plot(Ys[clip], Xs[clip], color="blue")
		fig.tight_layout(); 
		plt.savefig(files.append_path(out_path, files.get_filename(img_path)+".jpg"), dpi=my_dpi)

		# Progress bar stuff
		perc = (i+1)/len(images)	
		bar = int(np.round(perc*size))
		line = "Processing ["
		line += "="*bar + " "*(size-bar)
		line += "] {:d}%".format(int(np.round(perc*100)))
		ut.update_line(line) # Thins func will use carriage return
	print("\nFinished processing.")
