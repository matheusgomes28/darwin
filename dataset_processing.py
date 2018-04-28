""" Dataset Processing Script

This script will process a dataset given. So far, the 
processing image techniques used are deblurring (with
unsharp mask) and histogram manipulation. For more 
information please read the notebook on the Image
Processing directory.


Usage:
    dataset_cropping.py ROOT OUTPUT STATS HIST [-v]


Arguments:
    ROOT                 The root directory of the image dataset.
    OUTPUT               The output directory to save processed images.
    STATS                The path to the stats file (with lap var and err)
    HIST                 The path to the model histogram file.

Options:
    -v --view         Viewing option, no saving.
"""

import files, cv2 # For the file management stuff
import os, sys # For directory changing, sys stuff
import utilities as ut
import filtering as ft
import numpy as np
from colorama import Style, Fore, init # Colouring CLI stuff
from docopt import docopt # CLI argument parser

# For the viewing if enabled 
from matplotlib import pyplot as plt 

# For the data analysis stuff
import analysis as an




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
	stats_path = files.abspath(arguments['STATS'])
	hist_path = files.abspath(arguments['HIST'])

	# For now, just print out settings and  all the images in the root.
	print(Fore.BLUE + "Settings passed: ")
	print("Root directory........ %s" % root_path)
	print("Output directory...... %s\n" % out_path)
	print("Stats file directory........ %s" % stats_path)
	print("Histogram file directory...... %s\n" % hist_path)

	# Check that both directories exist
	if os.path.lexists(out_path) and os.path.lexists(root_path):
		pass
	else:
		print(Fore.RED + "Path not found, one of the directories does not exist.")
		print(Style.RESET_ALL)
		sys.exit(0) # Use system's abort function

	# Reset colour
	print(Style.RESET_ALL)

	# Open the histogram file should be [N,2]
	model_hist = np.loadtxt(hist_path)

	# Now we open the stats and calculate the stuff we want
	stats = np.loadtxt(stats_path)
	means = np.mean(stats, axis=0)
	span = np.max(np.linalg.norm(stats-means, axis=1))
	norm_stats = (stats-means)/span
	covariance = np.cov(norm_stats, rowvar=False)
	stdevs = np.sqrt(np.diag(covariance))

	# Precalculate the deblurring stuff
	a, b = 5, 4 # Weights for the unsharp mask
	gaussian_kernel = ft.gaussian_kernel(7, [0,0], 10) 
	unsharp_mask = a*ft.delta(7) - b*gaussian_kernel # The filter we want

	# Jut for the distribution visualization
	plt.plot(norm_stats[:,0], norm_stats[:,1], "x")
	plt.show()

	# Get the list of images
	images = files.get_images(root_path) # Note line below resets the blue 
	print(Style.RESET_ALL + Fore.GREEN + "Number of images in the path: {:d}".format(len(images)))
	
	size = 20 # Length of the loading bar in chars
	for i, img_path in enumerate(images):

		# Original image
		image = ut.read_image(img_path, "BGR2GRAY")

		# Check if image is in the lower standard deviation
		# (note that the mean should be 0 theoretically)
		if norm_stats[i,0] < -stdevs[0] and norm_stats[i,1]  < -stdevs[1]:

			# Sharpened image
			image = ft.image_conv(image, unsharp_mask)

		# Match the histogram
		final = an.match_histogram(image, model_hist)

		# Save the image to disc
		name = files.get_filename(img_path) + ".jpg"
		save_path = files.append_path(out_path, name)
		ut.save_image(save_path, final)

		if arguments['--view']:
			# Plot the difference here
			fig = plt.figure(figsize=(12, 7))
			ax1 = plt.subplot(1,2,1)
			ax1.set_title("Original Image")
			ax1.imshow(image, cmap="gray")
			ax2 = plt.subplot(1,2,2)
			ax2.set_title("Sharpened Image")
			ax2.imshow(final, cmap="gray") 
			fig.tight_layout()
			plt.show()

		# Progress bar stuff
		perc = (i+1)/len(images)
		bar = int(np.round(perc*size))
		line = "Processing ["
		line += "="*bar + " "*(size-bar)
		line += "] {:d}%".format(int(np.round(perc*100)))
		ut.update_line(line) # Thins func will use carriage return

	print("\nFinished processing.")
	print("Count:  {0}".format(count))
	print(Style.RESET_ALL)
