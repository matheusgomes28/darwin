""" Selecting Data - Making Samples

This script provides code to help select
samples for training out cascade classifier.


Usage:
    selecting_data.py ROOT OUTPUT -l FEAT... [-t NUM] 
    selecting_data.py ROOT OUTPUT SIZE LOW HIGH
    selecting_data.py ROOT OUTPUT SIZE LOW HIGH [-f FUNC] [-t NUM] 

Arguments:
    ROOT            The root directory of samples.
    OUTPUT          The output folder to put selected samples.
    FEAT            Feature numbers.
    LOW             Lower index for feature selection.
    HIGH            Upper index for feature selection.
    SIZE            Size of feature array to be selected.
    
Options:
    -f --function         Function to use for selecting.
    -l --list             Indicates a list of features.
    -t NUM --test=NUM      Number of images to use as test.
"""


import sys, os, util, cv2
import numpy as np
from docopt import docopt
from colorama import Style, Fore #Coloured stuff
import util # Utilities functions
from random import randint # For feature selection

def select_folder_sample(root, features, output, test=False, test_num=0, test_out=""):
    """
    This method will select samples from a
    directory-sample structure. This means
    structure where each directory is a sample
    under different conditions (i.e each
    directory is a person's face).

    root - the path of the root folder.
    features - list with numbered features to get.
    """
    
    # Holds the images
    data = []

    # Get all the directories (i.e samples)
    dirs = util.get_directories(root)

    # Now go through every directory and
    # pick the desired features from each folder
    for d in dirs:
        # use numpy to get the partial samples
        images = np.array(util.get_images(d))
        samples = images[features]
        data.extend(list(samples)) # adds to the list
        util.update_line("Getting imgs in folder: %s." % d)

    # Get the testing stuff if chosen
    if test: select_test(data, test_num, test_out)

    # Save all remaining images to the output dir
    print(Fore.GREEN) # Change colour to RED
    for i in range(len(data)):
        sample = data[i]
        percent = ((i+1)/len(data))*100
        util.update_line("Copying samples progess: %.1f%%" % percent)
        dts = "/".join([util.abspath(output), os.path.basename(sample)])
        util.copy_image(sample, dts)
    print(Style.RESET_ALL)   


def select_test(images, num, output):
    """ 
    This function will select the test data
    randomly from a given array of images.
    """

    # Holds the testing data
    samples = []

    # Use get_random to select test samples
    indexes = get_random([i for i in range(len(images))], num)
    indexes.reverse() # So we can pop safely

    # Make output dir if not exists
    if not os.path.exists(output):
        os.makedirs(output)

    # Now get each sample and pop them
    print(Fore.GREEN)
    for i in range(len(indexes)):
        percent = ((i+1)/len(indexes))*100
        util.update_line("Test selection progress: %.1f%%" % percent)
        image = images[indexes[i]]
        util.copy_image(image, os.path.join(output, os.path.basename(image)))
        images.pop(indexes[i])
    print(Style.RESET_ALL)
         
##
## ADD fUNCTION TO SELECT FEATURES HERE
##
def get_random(all_features, size):
    """
    This function will return a list of
    random integers representing the
    random features to be selected.

    note that for any feature f,
    low <= f < high.

    low - lower bound for index.
    high - upper bound for index.
    """
    
    # List to hold the selected features
    selected = []

    # Loop to get unique features (no  repeats)
    for i in range(size):

        # Get a random index rom features list
        index = randint(0, len(all_features)-1)
        
        # Add item to selected and remove from original
        selected.append(all_features[index])
        all_features.pop(index)
    
    selected.sort()
    return selected # voila


def leave_one(all_features, size):
    """
    This function will get half of the features
    by leaving the next one out. Make sure
    the features for each sample is big enough.
    """

    # Holds the selected features
    selected = []

    # Get all even features
    for i in range(size):
        selected.append(all_features[i*2])

    return selected # voila
           
    

if __name__ == "__main__":
    
    # Change cwd to current file's folder
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Change colout of usage to RED
    __doc__ = Fore.RED + __doc__ 
    # Use new __doc__ to parse arguments
    arguments = docopt(__doc__, version="1.0")


    # Check how user input features
    if arguments['--list']: #Here features are given as list
        features = [int(i) for i in arguments['FEAT']]

    elif arguments['--function']: # User defined function to select
        func  = eval(arguments['FUNC'])
        low   = int(arguments['LOW'])
        high  = int(arguments['HIGH'])
        size  = int(arguments['SIZE'])
        features = func(list(range(low, high)), size)

    else:  # Here use default function to select (random)
        low   = int(arguments['LOW'])
        high  = int(arguments['HIGH'])
        size  = int(arguments['SIZE'])
        features = get_random(list(range(low, high)), size)

    # Get the mandatory arguments
    root_path = arguments['ROOT']
    out_path  = arguments['OUTPUT']


    # Print out info to user
    print(Fore.BLUE + "Setting passed: ")
    print("Root directory..... %s." % root_path)
    print("Output directory... %s." % out_path)
    print("Features passed.... %s." % list(features))
    print(Style.RESET_ALL)

    # Finally save the data 
    if arguments['--test']:
        num = int(arguments['--test'])
        test_out = util.abspath(os.path.join(out_path, "test"))
        select_folder_sample(root_path, features, out_path, True, num, test_out)
    else:
        select_folder_sample(root_path, features, out_path)
