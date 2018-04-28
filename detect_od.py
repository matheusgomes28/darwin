""" Optic Disk Connection 

This script will open images in a dataset and 
detect the OD in each image. The resulting fitted
OD images will be saved in the OUTPUT directory.

Note: The input images must be normalised beforehand.

Usage:
    dtect_od.py ROOT OUTPUT

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

	
	size = 20 # Length of the loading bar in chars
	for i, img_path in enumerate(images):
		pass
	print("\nFinished processing.")
