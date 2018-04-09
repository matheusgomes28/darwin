""" Image Dataset Analysis

This script will analyse and obtain some features from the
dataset given. Note that most of the code used here comes
from the 'analysis.py' file. 

Usage:
    dataset_analysis.py ROOT OUTPUT

Arguments:
    ROOT            The root directory of the image dataset.
    OUTPUT          The output directory to save the analysis files.
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

	# CALCULATE THE QUALITIES OF THE IMAGES
	hist_size = 256
	histograms = np.zeros((len(images), hist_size))  # Define matrix for storing histograms
	stats = np.zeros((len(images), 2))				 # Define matrix for storing laplacian variance and ERR

	
	size = 20 # Length of the loading bar in chars
	for i, img_path in enumerate(images):
		image_gray = ut.read_image(img_path, "BGR2GRAY") #grayscale
		lp = an.get_laplacian(image_gray)  # Laplacian
		err = an.get_err(image_gray) # Err

		# Fill the matrices (Log domain)	
		histograms[i,:] = an.get_histogram(image_gray).ravel()
		stats[i,0] = np.log(np.var(lp))
		stats[i,1] = np.log(err)

		# Progress bar stuff
		perc = (i+1)/len(images)	
		bar = int(np.round(perc*size))
		line = "Processing ["
		line += "="*bar + " "*(size-bar)
		line += "] {:d}%".format(int(np.round(perc*100)))
		ut.update_line(line) # Thins func will use carriage return
	print("\nFinished processing.")

	# Get saving directories
	stats_path = os.path.join(out_path, "stats.txt")
	hist_path = os.path.join(out_path, "hist_model.txt")
	# Calculate the mean histogram of images and save
	# both stats file and the mean histogram
	mean_hist = np.mean(histograms, axis=0) 
	np.savetxt(hist_path, mean_hist)
	np.savetxt(stats_path, stats)


	# Plotting the distributions of the lap, err
	# and plotting the mean histogram 
	fig = plt.figure(figsize=(10, 7))
	ax1 = plt.subplot(2,1,1)
	ax1.set_title("Mean Histogram")
	ax1.plot(mean_hist)

	ax2 = plt.subplot(2,2,3)
	ax2.set_title("Var of Lap Histogram")
	ax2.hist(stats[:,0], bins=25)

	ax3 = plt.subplot(2,2,4)
	ax3.set_title("ERR Histogram")
	ax3.hist(stats[:,1], bins=50)

	fig.tight_layout()
	plt.show()