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
    data = []
    paths = files.get_files(directory, ['csv'])

    for p in paths:
        with open(p, 'r') as f:
            reader = csv.reader(f)
            data.extend(list(map(tuple, reader))[1:])
    
    return data

def plot_responses(data):
    # Gather response data
    response_count = Counter([r for _, r, _ in data])
    responses = [response_count['0'], response_count['1'], response_count['2']]

    fig = plt.figure(figsize=(8, 5))
    x = ['Incorrect', 'Correct', 'Near/Close']
    y = responses
    plt.bar(x, y, 1, color='red')
    plt.xlabel('Response Types')
    plt.ylabel('# Responses')
    plt.title('Evaluation Responses')
    plt.show()

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
    plot_responses(data)
