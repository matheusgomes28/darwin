# This file contains functions that will
# be used to manage files (images) in the
# dataset. Main sorting everything out 
# and putting names in the right
# format.

"""File Management

This file contains functions that will be used
to manage files (images) in the dataset. Functions
in this file should only be related to handling 
files and filenames. Maily sorting everythig out
and putting everything in the right format.

When renaming files, the pattern uses the str NUM
to indicate the number of the image. E.g imgNUM 
will yield img0.jp, img1.jpg...

Usage:
    file_management.py PATH PATTERN [-l TYPE...]

Arguments:
    PATH             Path of images to handle.
    PATTERN          Naming pattern to use (see desc).
    TYPE             An image type (e.g jpg)

Options:
    -l --list        Indicates a list of types to use.
"""

import sys, os, util
from docopt import docopt
from colorama import Fore, Style


def get_extension(f): return f[-3:] # Last 3 chars are the extension


def rename(folder, format):
    """
    This function renames all images in a given
    directory according to the pattern given in 
    the format given, init.

    Format: 
        use NUM for the number of the image.
        imgNUM -> img1, img2, .., img100,..
    """

    # Get list of all files then rename images 
    path = util.abspath(folder)
    names_lis = os.listdir(path)
    os.chdir(path) # cwd to work with OS commands 


    # Scan for images and rename them
    for i in range(0, len(names_lis)):
        f = names_lis[i]
        extension = get_extension(f)
        location = "".join([path, "/", f])

        # Need absolute location
        #print("checking location %s. Is file? %s " % (location, is_image(location)))
        if util.is_image(location):
            new_f = "".join([format.replace("NUM", str(i)), ".", extension])
            util.update_line("Renaming file %s to %s." % (f, new_f))
            os.rename(f, new_f) #Tada, done


if __name__ == "__main__":

    # Parse arguments
    arguments = docopt(__doc__, version="1.0") 


    # Get settings passed from user
    # 
    types = [] # Allowed img types given by user
    if arguments['--list']:
        types = arguments['TYPE']

    # Mandatory arguments
    path = arguments['PATH']
    pattern = arguments['PATTERN']

    # Display message with settings
    print(Fore.BLUE, end="") # Change color to blue     
    print("Renaming Files.... Settings passed:\n")
    print("Allowed types: %s" % types)
    print("Path to images: %s" % path)
    print("Naming pattern: %s%s" % (pattern, Style.RESET_ALL))

    #testing stuff here
    print(Fore.GREEN) # Change colour to green
    rename(path, pattern)
    print(Style.RESET_ALL)
