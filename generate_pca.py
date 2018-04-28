""" Image Principal Component Generator

This script will run PCA on the given image
folder, and return the N principal components.

Usage:
    dtect_od.py ROOT OUTPUT N

Arguments:
    ROOT            The root directory of the image dataset.
    OUTPUT          The output directory to save the analysis files.
    N               The number of principal components to be returned.
"""

import files # For the file management stuff
import os, sys, cv2 # For directory changing, sys stuff
import utilities as ut
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
	N = int(arguments['N'])

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

	images = files.get_images(root_path) # Note line below resets the blue 
	print(Style.RESET_ALL + Fore.GREEN + "Number of images in the path: {:d}".format(len(images)))

	# Create the image matrix here
	height, width = 30, 30
	img_matrix = np.zeros((len(images), height*width)) # (num_imgs x dim)


	# Going through all the images and polutating the img_matrix
	size = 20 # Length of the loading bar in chars
	for i, img_path in enumerate(images):

		# Open each image
		img = ut.read_image(img_path, "BGR2GRAY")
		resized = cv2.resize(img, (height, width), cv2.INTER_AREA)

		reshaped = resized.reshape(width*height) # So we have it as a vector

		# populate the matrix
		img_matrix[i,:] = reshaped

		# Progress bar stuff
		perc = (i+1)/len(images)	
		bar = int(np.round(perc*size))
		line = "Opening images ["
		line += "="*bar + " "*(size-bar)
		line += "] {:d}%".format(int(np.round(perc*100)))
		ut.update_line(line) # This func will use carriage return
	print("\nFinding the principal components.")


	##############################
	####### PCA stuff here #######
	##############################
	from numpy.linalg import eigh as eig
	covariance = np.cov(img_matrix, rowvar=False)

	# Get the eigenvectors with eigh. This function
	# gets eigenvalues and eigenvectors of symmetric 
	# matrices and is a lot faster than linalg.eig.
	w, v = eig(covariance)

	# Ony use the first N principal components. 
	# Note that eigh returns the vectors in ascending
	# order of eigenvalue, hence why the flip.
	v_order = np.fliplr(v)[:,:N]
	print("Completed... Saving and showing the figure.")
	np.savetxt(files.append_path(out_path, "pca.txt"), v_order)

	# Plot all the PCAs
	fig = plt.figure(figsize=(10,7))
	for i in range(10): # Go throught 10 PCAs
	    pca = v_order[:,i]
	    pca_img = pca.reshape((height,width))
	    
	    ax = plt.subplot(2,5,i+1)
	    ax.set_axis_off()
	    ax.imshow(pca_img, cmap="gray")
	plt.suptitle("The first 10 PCAs")
	fig.tight_layout(); plt.show();