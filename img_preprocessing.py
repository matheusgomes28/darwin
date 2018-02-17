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
from colorama import Style, Fore, init # Colouring CLI stuff
from docopt import docopt # CLI argument parser 


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
	print(Style.RESET_ALL + Fore.GREEN + "Available images in the path: ")
	for i in images: print(i)
	print(Style.RESET_ALL)


