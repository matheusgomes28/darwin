""" Dataset Conversion

This script contains code to convert image format 
given the directory.


Usage:
    image_conversion.py ROOT OUTPUT FORMAT

Arguments:
    ROOT                 The root directory of the image dataset.
    OUTPUT               The output directory to save processed images.
    FORMAT               The format for the files to be converted.
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
    format = arguments['FORMAT']

    # For now, just print out settings and  all the images in the root.
    print(Fore.BLUE + "Settings passed: ")
    print("Root directory........ %s" % root_path)
    print("Output directory...... %s\n" % out_path)

    # Check that both directories exist
    if os.path.lexists(root_path):
        pass
    else:
        print(Fore.RED + "Path not found, root directory does not exist.")
        print(Style.RESET_ALL)
        sys.exit(0) # Use system's abort function

    # Create the output if does not exist
    if not os.path.lexists(out_path): os.mkdir(out_path)

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

        # Saving the processed file 
        name = files.get_filename(img_path) + ".{0}".format(format) 
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
