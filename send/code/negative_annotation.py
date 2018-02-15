
""" Annotations

This script was designed to facilitate the creation
of annotations for opencv_trainclassifier function.
Furthermore, it also provides simple methods for
path related operations necessary for the creation
of annotations. For more info read docstrings.


Usage:  
    negative_annotations.py  INFOPATH SAMPLEPATH [-r]  

Arguments:
    INFOPATH         Path for info.dat.
    SAMPLEPATH       Path for samples folder.

Option:
    -r --relative    Use relative path instead of absolute.
"""


import cv2
import os, sys
from colorama import Fore, Style 
from docopt import docopt
from util import get_images
from util import abspath
from util import get_relative_dir
from util import update_line


def save_bg_info(img_path, bg_file, func=abspath):
    """
    This function will create the background file
    for a given folder.

    img_path - path to the negative images.
    bg_file  - background path file.
    func     - path finder function.
    """

    # Config stuff needed 
    path_to_use = func(img_path)
    
    line  = "".join([path_to_use, "\n"])
    bg_file.write(line)


if __name__ == "__main__":
    
    # Get the arguments
    arguments = docopt(__doc__, version="1.0")

    # Now create the bg info.dat file
    bg_info_path = arguments['INFOPATH']
    images_path =  arguments['SAMPLEPATH']
    
    # Get the path finder function 
    if arguments['--relative']:
        func = lambda x : get_relative_dir(bg_info_path, x)
    else: func = abspath

    
    # Print erlcome text
    print(Fore.BLUE)
    print("Negative Annotation... Settings passed:")
    print("Background file path: %s" % bg_info_path)
    print("Background images sample %s" % images_path)
    print("Use relative path: %s" % arguments['--relative'])
    print(Style.RESET_ALL)


    # Open/create background file
    open(bg_info_path, "w").close()
    bg_file = open(bg_info_path, "a")
    print("file opened successfully, retrieving imags (might take a while)") 
    
    # Go through all images and save them
    images = get_images(abspath(images_path))
    print("Starting to save images")
    print(Fore.GREEN)
    for i in range(len(images)):

        # Print progress here
        percent = ((i+1)/len(images))*100
        update_line("Progress: %.2f" % percent)
        
        # Save the info to the file
        save_bg_info(images[i], bg_file, func)
    print(Style.RESET_ALL)

    # Finally close the file
    bg_file.close()
