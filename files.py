""" File Management Python Cript

This script is supposed to contain all the necessary functions
to manage files and paths in the OS. Note that this code was
only tested in Windows and Linux environments.
"""

import sys, os, cv2
from colorama import Fore, Style


def abspath(path):
    """
    This function is designed to fix cross platform 
    errors with os's abspath function (windows uses
    \ while linux / ).

	Params:
    path - the path stirng of the file/directory.

    returns -> str representing absolute path in curr os.
    """

    return os.path.abspath(path).replace("\\","/")

def relpath(path):
    """
    This function is design to fix cross platform 
    errors with os's relpath function (windows uses 
	\ while linux uses /).

	Params:
	path - the path stirng of fie/folder.

	returns -> str representing relative path.
    """

    return os.path.relpath(path).replace("\\", "/")

def get_images(path):
    """
    This function will return a list with all the
    images names in a given path.

    Params:
    path - the path string (rel or abs) representing folder path.

    returns -> list of string containing all the images.
    """
    
    # Cast path to absolute path
    absolute = abspath(path)

    img_lis = [] # Holds images in a folder
    file_lis = get_files(absolute)

    # Now get the images within file list
    img_lis = [f for f in file_lis if is_image(f)]

    return img_lis


def get_files(path):
    """
    This function will return a list of all files in 
    the given directory.

    Params:
    path - the path (rel or abs) of the directory to get files.

    returns -> list of strings containing all the files in a dir.
    """
    
    # Uses abs path as the directory
    absolute = abspath(path)
    all_files = os.listdir(absolute) 

    # Get the absolute path of each file
    absolute_files = ["/".join([absolute, i]) for i in all_files]

    # Filter out non-files and return
    return [f for f in absolute_files if os.path.isfile(f)]

def get_directories(path):
    """
    This function will return all folders in
    a given path. Only returns directorie*

    Params:
    path - string representing directory to search.

    returns -> list of strings containing all directories.
    """

    # Uses abspath as the directory
    absolute = abspath(path)
    all_files = os.listdir(abspath(absolute))
    
    # Get the absolute path of each file
    absolute_files = ["/".join([absolute, d]) for d in all_files]

    # Here we filter all non-directires out and return
    return [i for i in absolute_files if os.path.isdir(i)]



def get_relative_dir(path1, path2):
    """
    This function will return the relative location 
    (wihout filenames) of the second file to the 
    first file.

    Examples: 
    get_relative_dir("parent/file.txt", "parent/child/pic.jpg") -> "child/"
    get_relative_dir("parent/child/file.txt", "parent/pic.jpg") -> "../"

    Params: 
    path1 - string representing the first dir (absolute dir)
    path2 - string representing the second dir.

    returns -> string representing path2 relative to path1.
    """

    originalwd = os.getcwd() # Get original working directory


    # Get directories if files given
    if os.path.isdir(path1): dir1 = path1
    else:dir1 = os.path.dirname(path1)
    
    if os.path.isdir(path2): dir2 = path2
    else: dir2 = os.path.dirname(path2)
    

    # Change working dir
    os.chdir(dir1)
    rel_dir = relpath(dir2)

    os.chdir(originalwd) # switch back to wd

    # return the relative path
    return "/".join([rel_dir, os.path.basename(path2)])


def is_image(img_path, formats=["jpg", "png", "gif", "pgm"]):
    """
    Determines whether or not a
    given file is an image.

    Params:
    img_path - string representing path of image.
    formats - list os formats (strings).

    returns -> True if file is image, False if not.
    """
    #formats = ["jpg", "png", "gif", "pgm"]
    end = img_path[-3:]
    return os.path.isfile(img_path) and (end in formats)


def copy_image(source, dest):
    """
    This function will simply copy the image in
    the source location to the destinatio
    location.

    Params:
    source - image source string.
    dest - image destinationq string.

    returns -> Null.
    """

    # Cast to abs path 
    abs_src = abspath(source)
    abs_dst = abspath(dest)

    # OpenCV to open and save image
    img = cv2.imread(abs_src)
    cv2.imwrite(abs_dst, img)


def update_line(text, chars=["\033[F","\r"]): 
    """
    This function will output text on the same line.
    I.e update the line with the new text using 
    ANSII.

    Params:
    text - string of text to update line with.
    chars - list containing reset character (os dependent).

    returns -> Null.
    """
    
    if os.name == 'nt':
        # Print text and update cursor
        sys.stdout.write(text)
        sys.stdout.flush()

        sys.stdout.write(chars[1])
        sys.stdout.flush()

    else:
        sys.stdout.write(text + "\n")
        sys.stdout.write(chars[0])
        
if __name__ == "__main__": #testing code here
    print(os.getcwd())
    print(get_files(os.getcwd()))