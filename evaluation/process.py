""" Evaluation Data Processing Tool

This script processes evaluation data (CSV) derived from the
Evaluation GUI Tool and produces graphs

Usage:
    main.py EVALUATION_DATA
    main.py --help 

Arguments:
    EVALUATION_DATA       The path to the evaluation data directory
"""

import sys, os, csv
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

    data = []
    paths = files.get_files(directory, ['csv'])

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

    response_count = Counter([r for _, r, _ in data])
    return [response_count['0'], response_count['1'], response_count['2']]

def gather_response_times(data):
    """ Gathers response times of each response from supplied data

    Arguments:
        data        data in format [(filename, response, response_time)]
    """

    averages = {}
    response_times = [(r, t) for _, r, t in data]
    for r, t in response_times:
        if r not in averages:
            averages[r] = t
        else:
            averages[r] += t
    return averages
    

def plot_responses(responses):
    """ Plots responses in a bar chart

    Arguments:
        responses       list containing response counts
    """
    fig = plt.figure(figsize=(8, 5))
    x = ['Incorrect', 'Correct', 'Near/Close']
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
    print(Fore.BLUE + "Evaluation directory..... %s" % eval_path)

    if os.path.lexists(eval_path):
        pass
    else:
        print(Fore.RED + "Path not found, evaluation directory does not exist.")
        print(Style.RESET_ALL)
        sys.exit(0) # Use system's abort function
    
    # Reset colour
    print(Style.RESET_ALL)

    data = gather_data(eval_path)
    responses = gather_responses(data)
    response_times = gather_response_times(data)

    total_responses = sum(responses)
    i_responses = (responses[0] / total_responses) * 100.0
    c_responses = (responses[1] / total_responses) * 100.0
    n_responses = (responses[2] / total_responses) * 100.0
    i_time = response_times['0'] if '0' in response_times else 0.0
    c_time = response_times['1'] if '1' in response_times else 0.0
    n_time = response_times['2'] if '2' in response_times else 0.0

    print('Incorrect: {}%, Av. Response: {}s'.format(i_responses, i_time))
    print('Correct: {}%, Av. Response: {}s'.format(c_responses, c_time))
    print('Near/Close: {}%, Av. Response: {}s'.format(n_responses, n_time))

    plot_responses(responses)
    # plot_response_times(data)
