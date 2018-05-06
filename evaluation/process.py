""" Evaluation Data Processing Tool

This script processes evaluation data (CSV) derived from the
Evaluation GUI Tool and produces graphs

Usage:
    process.py EVALUATION_DATA INPUT OUTPUT
    process.py --help 

Arguments:
    EVALUATION_DATA       The path to the evaluation data directory
    INPUT                 The directory where the response images are located.
    OUTPUT                The directory to copy images to (response extraction).
"""

import sys, os, csv
import shutil # For ccopying files
from collections import Counter
from docopt import docopt
from colorama import Style, Fore, init 
import matplotlib.pyplot as plt

# For loading the main helper scripts
sys.path.append(os.path.abspath('../'))
import files

def gather_data(directory):
    """ Gathers evaluation data from all csv files in a given
    directory.

    Arguments:
        directory       Directory the csv files are stored in
    """

    # Get all the csv files
    data = []
    paths = files.get_files(directory, ['csv'])

    # Open each csv and dum all the responses to a list
    for p in paths:
        with open(p, 'r') as f:
            reader = csv.reader(f)
            data.extend(list(map(tuple, reader))[1:])
    
    return data

def gather_responses(data):
    """ Gathers response counts from supplied data

    Arguments:
        data        data in format [(filename, response, response_time)]
    """

    # Counter object (basically a dict with (key:counts))
    response_count = Counter([int(r) for _, r, _ in data])

    # Returns counts of (0, 1, 2) corresponding to (invalid, correct, near)
    return response_count[0], response_count[1], response_count[2]

def gather_response_times(data):
    """ Gathers response times of each response from supplied data

    Arguments:
        data        data in format [(filename, response, response_time)]
    """

    # sums is the sum of response times (dict with key=response, val=sum_times)
    # divisor is a dict counting the number of responses for a key
    sums, divisor = {}, {}

    # list with all the response times (label, times as float)
    response_times = [(r, t) for _, r, t in data]

    # update the dicts as loop through the response list
    for r, t in response_times:

        # if respnse not in the dicts, add them
        if r not in sums:
            sums[r] = float(t)
            divisor[r] = 1

        # if already in the dicts, simply update the values
        else:
            sums[r] += float(t)
            divisor[r] += 1

    # return a dictionary containing {key=response, val=average times}
    return {x : sums[x] / float(divisor[x]) for x in sums}

def get_responsefiles(response, data):
    """
    Given a response value i (i=0,1,2), this function will
    return a list with all the file names associated with 
    the i response.

    Args:
        response - the reponse in the csv file.
        data     - list containing the read csv responses [(name, response, time)]
    Returns:
        list of string containing file names ()
    """

    # List to hod the filenames corresponsing to the reponse
    response_names = [] 

    # Loop through the data adding the response names
    # to our output list
    for n, r, _ in data: 

        # Check if correct response
        if int(r)==int(response): response_names.append(files.get_filename(n)) 

    # Return the list containing the filenames, note that the 'set'
    # operator gets rid of duplications
    return list(set(response_names))

    

def plot_responses(responses):
    """ Plots responses in a bar chart

    Arguments:
        responses       list containing response counts
    """
    fig = plt.figure(figsize=(8, 5))
    x = [0, 1, 2]
    y = responses
    plt.bar(x, y, 1, color='red')
    plt.xlabel('Response Types')
    plt.ylabel('# Responses')
    plt.title('Evaluation Responses')
    plt.show()

def plot_response_times(data):
    pass

if __name__ == '__main__':
    # Change cwd to the current file's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # init colourama to filter ANSI chars in windows/linux
    init() 

    # Change colour of usage to RED (help text)
    __doc__ = Fore.RED + __doc__ + Style.RESET_ALL

    # Use __doc__ string to parse cmd arguments
    arguments = docopt(__doc__, version="1.0")

    eval_path = files.abspath(arguments['EVALUATION_DATA'])
    input_path = files.abspath(arguments['INPUT'])
    output_path = files.abspath(arguments['OUTPUT'])
    print(Fore.BLUE + "Evaluation directory..... %s" % eval_path)
    print(Fore.BLUE + "Image input directory.... %s" % input_path)
    print(Fore.BLUE + "Image output directory... %s" % output_path)

    if os.path.lexists(eval_path) and os.path.lexists(input_path):
        pass
    else:
        print(Fore.RED + "Path not found, evaluation/input directory does not exist.")
        print(Style.RESET_ALL)
        sys.exit(0) # Use system's abort function
    
    # Reset colour
    print(Style.RESET_ALL)

    # Gather the data
    data = gather_data(eval_path)
    responses = gather_responses(data)
    response_times = gather_response_times(data)


    ##########################################
    ## Extracting the response images stuff ##
    #########################################

    # Get all the images in the dataset
    image_paths = files.get_images(input_path)

    # Get the list of JUST the file names from all the images
    dataset_names = list(map(files.get_filename, image_paths))

    # Get the response file names
    response_names = get_responsefiles(1, data)
    print("response is: {}".format(response_names))

    # Make sure output path exists
    if not os.path.exists(output_path):
        os.mkdir(output_path) #mode = 777

    # Loop to go trhough the response_times and copy the
    # images to the output directory
    for name in response_names:

        # find location in the 'dataset_names'
        loc = dataset_names.index(name)

        # use shutil to copy this image to the output
        extension = files.get_fileext(image_paths[loc])

        # copying the file here
        shutil.copy2(image_paths[loc], output_path)


    total_responses = sum(responses)
    i_responses = (responses[0] / total_responses) * 100.0
    c_responses = (responses[1] / total_responses) * 100.0
    n_responses = (responses[2] / total_responses) * 100.0
    i_time = response_times['0'] if '0' in response_times else 0.0
    c_time = response_times['1'] if '1' in response_times else 0.0
    n_time = response_times['2'] if '2' in response_times else 0.0

    print('Incorrect: {:.3f}%, Av. Response: {:.3f}s'.format(i_responses, i_time))
    print('Correct: {:.3f}%, Av. Response: {:.3f}s'.format(c_responses, c_time))
    print('Near/Close: {:.3f}%, Av. Response: {:.3f}s'.format(n_responses, n_time))

    plot_responses(responses)
    plot_response_times(data)
