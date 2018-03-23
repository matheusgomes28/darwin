""" Image Dataset Pre Processing

This script contains funtions to preprocess a dataset
of image with the techniques described in the Jupyter 
Notebooks. Note that this is still being developed...



Usage:
    img_preprocessing.py ROOT OUTPUT

Arguments:
    ROOT            The root directory of the image dataset.
    OUTPUT          The output directory to save processed images.
"""

import files # For the file management stuff
import os # For directory changing
import utilities as ut
import analysis as an
import numpy as np
import filtering as fil
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
	out_path = files.abspath(arguments['ROOT'])

	# For now, just print out settings and  all the images in the root.
	print(Fore.BLUE + "Settings passed: ")
	print("Root directory........ %s" % root_path)
	print("Output directory...... %s\n" % out_path)

	images = files.get_images(root_path) # Note line below resets the blue 
	print(Style.RESET_ALL + Fore.GREEN + "Number of images in the path: {:d}".format(len(images)))

	# CALCULATE THE QUALITIES OF THE IMAGES
	hist_size = 256
	histograms = np.zeros((len(images), hist_size))  # Define matrix for storing histograms
	stats = np.zeros((len(images), 2))				 # Define matrix for storing laplacian variance and ERR

	for i, img_path in enumerate(images):
		image_gray = ut.read_image(img_path, "BGR2GRAY") #grayscale
		lp = an.get_laplacian(image_gray)  # Laplacian

		err = an.get_err(image_gray)

		# Fill the matrices
		histograms[i,:] = an.get_histogram(image_gray).ravel()
		stats[i,0] = np.var(lp)
		stats[i,1] = err

	print(Style.RESET_ALL)

	# Calculate the mean histogram of images and save
	mean_hist = np.mean(histograms, axis=0) 
	np.savetxt("histogram_model.txt", mean_hist)
	np.savetxt("stats.txt", stats)

	# Saving the figure 
	fig = plt.figure(figsize=(10, 5))
	ax = plt.gca()
	ax.set_title("Average Histogram of the Dataset")
	ax.plot(mean_hist)
	plt.show()
	plt.savefig("histogram.jpg")

	# Plot the laplacian variance as a histogram 
	fig = plt.figure(figsize=(10, 5))
	ax = plt.gca()
	ax.set_title("Laplacian Variance Histogram")
	ax.hist(stats[:,0])
	fig.tight_layout()
	plt.show()
	plt.savefig("lv_histogram.jpg")

	# Plot the ERR as a histogram
	fig = plt.figure(figsize=(10, 5))
	ax = plt.gca()
	ax.set_title("Equivalent Rectangle Resolution Histogram")
	ax.hist(stats[:,1])
	fig.tight_layout()
	plt.show()
	plt.savefig("err_histogram.jpg")