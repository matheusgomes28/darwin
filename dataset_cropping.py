""" Dataset Cropping/Resizing Script

This script will go throght all the images in the given 
dataset and it will identify the bounding box in the 
retinal images, crop the said bounding box containing
the eye, resize if chosen and then save the images
to the output directory.


Usage:
    dataset_cropping.py ROOT OUTPUT 
    dataset_cropping.py ROOT OUTPUT -x WID -y HEI

Arguments:
    ROOT                 The root directory of the image dataset.
    OUTPUT               The output directory to save processed images.
    WID                  The resizing width of the image.
    HEI                  The resizing height of the image.

Options:
	-x WID --width=WID    Indicates resize image with given width.
	-y HEI --height=HEI   Indicates resize image with given height.
"""

import files, cv2 # For the file management stuff
import os, sys # For directory changing, sys stuff
import utilities as ut
import analysis as an
import numpy as np
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

	# Check for the resizing args
	resize = False
	if arguments['-x']:
		# Flag to resize images
		resize = True

		# Get the width and height
		width = int(arguments['WID'])
		height = int(arguments['HEI'])

	# Print the resizing settings
	print("Resizing set to {0}{1}{2}.".format(Fore.GREEN, resize, Fore.BLUE))
	if resize:
		print("Width: {0}{1}px{2}".format(Fore.WHITE, width, Fore.BLUE))
		print("Height: {0}{1}px{2}".format(Fore.WHITE, height, Fore.BLUE))

	# Reset colour
	print(Style.RESET_ALL)

	images = files.get_images(root_path) # Note line below resets the blue 
	print(Style.RESET_ALL + Fore.GREEN + "Number of images in the path: {:d}".format(len(images)))
	
	size = 20 # Length of the loading bar in chars
	for i, img_path in enumerate(images):
		image = ut.read_image(img_path, "BGR2RGB") #grayscale

		# Do the image cropping and save to the output
		rect = an.get_rect(image) # Ruple with bounding rect coords
		cropped = image[rect[1]:rect[3],rect[0]:rect[2]] # Simple cropping

		# This is the resizing stuff. Here I am assuming we
		# will be decimating the image (reducing size), hence
		# the interpolation used is the AREA relation.
		if resize:
			inter = cv2.INTER_AREA # OpenCV const for such interpolation
			cropped = cv2.resize(cropped, (width, height), interpolation=inter)


		# Saving the processed file 
		name = files.get_filename(img_path) + ".jpg"
		save_path = files.append_path(out_path, name)
		ut.save_image(save_path, ut.convert_spaces(cropped, "RGB2BGR"))

		# Progress bar stuff
		perc = (i+1)/len(images)
		bar = int(np.round(perc*size))
		line = "Processing ["
		line += "="*bar + " "*(size-bar)
		line += "] {:d}%".format(int(np.round(perc*100)))
		ut.update_line(line) # Thins func will use carriage return

	print("\nFinished processing.")
	print(Style.RESET_ALL)
