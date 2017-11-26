"""
This file will contain some utility code
that will be useful when processing images.

Most of the functions here will be used in 
Jupyter notebook in order to load, show and 
analyse images in the correct format 
(Matplotlib), and convert between colour 
spaces (E.g BGR -> RGB).
"""
# Version 0.1 - Python 3.x

import cv2, sys, os
import numpy as np
import cv2

# This holds the strings for the conversion
# for the conversion codes. Feel free to add 
# more strings if you need a different space
# for analysis (format = "{SPACE1}2{SPACE2})
convert_strs = {
				 "BGR2RGB" : cv2.COLOR_BGR2RGB,
				 "BGR2GRAY": cv2.COLOR_BGR2GRAY,
				 "RGB2BGR" : cv2.COLOR_RGB2BGR,
				 "RGG2GRAY": cv2.COLOR_RGB2GRAY,
			   }

def get_dir(path:str):
	"""
	Thiis function will be used to parse
	path string into directory objects in
	Python. Very useful for cross platform 
	(as Windows and Unix paths are not 
	compatible).
	"""

	# Change to proper OS directory
	return path

def convert_spaces(img:np.ndarray, key:str) -> np.ndarray:

	# Return a new image in the converted space
	return cv2.cvtColor(img, convert_strs[key])


def read_image(path:str, key:str="COLOR_BGR2RGB") -> np.ndarray:
	"""
	This funtion will use OpenCV to load an image. 
	Note that the default colour space is BGR. To 
	convert between spcaes, just change the default 
	'key' argument (see convert_strs). 

	path - string representing the path of the image
	key - string representing key in the convert_dir
	"""

	# Load image (BGR)
	img = cv2.imread(get_dir(path))

	# Returns the converted image 
	return convert_spaces(img, convert_strs[key]) 