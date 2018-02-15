#  This file contain functions necessary to
#  generate the info.dat file for positive
#  imags in the dataset.


""" Annotations

This script was designed to facilitate the creation
of annotations for opencv_trainclassifier function.
Furthermore, it also provides simple methods for
path related operations necessary for the creation
of annotations. For more info read docstrings.

Functions available to save info:
    save_info - Automatically detect faces using default openCV's haar cascade.
    save_null - Uses whole image as the face (x,y,w,h) = (0, 0, width, height) 


Usage:  
    annotations.py  INFOPATH SAMPLEPATH [-c XMLPATH] [-f FUNC] 
    annotations.py  --help 
Arguments:
    INFOPATH         Rel path for info.dat.
    SAMPLEPATH       Rel path for samples folder.

Options:
    -c XMLPATH --cascade=XMLPATH     Path for xml cascade file.
    -f FUNC --function=FUNC          Function to use to save info.
    --help                           Print verbose usage info.
"""

import numpy as np
from docopt import docopt
from colorama import init, Fore, Style
from util import get_images, is_image
from util import get_relative_dir
from util import abspath
from util import update_line
import cv2, sys, os


def open_image(name, output="cv"):
    """
    This function will attempt to open an image
    from a given path. If an exception is caught,
    None will be returned.
    """
    file_path = IMG_PATH + "/" + name 
    
    if output=="cv": return cv2.imread(file_path)
    try: 
        file = open(file_path, "rb") 
        image = file.read()
        file.close()
    except FileNotFoundError:
        print("Image file not found.")
        image = None # We know where it comes from
        
    
    
    return image

# Convert RGB image to use on pyplot
def show_image(img):
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb_image)

def printf(text, cmd=sys.stdout):
    """
    This function is for printing formatted text
    onto the stdout without new line char.
    """

    print(text, end='')


def detect_faces(img, face_cascade, args=[(1.3, 3), ()]):
    
    # Get image in Gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, *args[0])
    
    # Drawing the rectangles
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 4)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
    return img # Return images with rectangles drawn on them




### USER DEFINED FUNCTIONS TO SAVE INFO ABOUT FACES IN 
### EACH PICTURE.

def save_info(image_path, info_file, face_cascade): 
    """
    This function will run face detecton with 
    default parameters on an image file and 
    save all the instances of faces to the 
    file in the format wanted by openCV.
    """
    # Load image file by name
    img = cv2.imread(image_path)

    
    # Get image in Gray (only if not in gray scale)
    if len(img.shape) > 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else: gray = img

    faces = face_cascade.detectMultiScale(gray) #No args here
    
    
    # Drawing the rectangles
    count = len(faces)
    info_file.write("%s  %s  " % (image_path, count))
    
    # Write all instances
    line = ""
    for (x,y,w,h) in faces:
        line += "%s %s %s %s   " % (x, y, w, h)
        #cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 4)
        
    info_file.write(line.strip() + "\n")
    
    return img


def save_null(image_path, info_file, face_cascade):
    """
    This function will save a line to the info file
    where the whole image is the face. Use this 
    when no face detection is needed to create info
    file.
    """
    
    # Load image to get file info
    img = cv2.imread(image_path)
    
    # Get width adn height
    height, width = img.shape[:2]

    # Now just save the info to the file
    line = "%s  1  0 0 %s %s" % (image_path, width, height)
    info_file.write(line.strip() + "\n")



if __name__ == "__main__":

    # Change cwd to current file's folder
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Init ANSI convertion for windows.
    init(convert=True)
    print("Ansi conversion initialised.")

    # Change color of usage to red
    __doc__ = Fore.RED + __doc__ 
    # Use new __doc__ to parse arguments
    arguments = docopt(__doc__, version="1.0")
    # Print full usage if help selected
    if arguments['--help']: print(__doc__)

    # Retrieving location of the files
    img_path = arguments['SAMPLEPATH']
    positive_info_file = arguments['INFOPATH']
    images = get_images(img_path)
    
    # Gets what function to use as saving info func
    save_func = save_info # default function uses haar cascade
    if arguments['--function']:
        save_func = eval(arguments['--function'])


    # Finally get the face cascade obj
    if arguments['--cascade']: 
        xml_file = arguments['--cascade']
        printf(Fore.GREEN) # Change colour to red
        print("Cascade file was provided: %s" % xml_file)
        printf(Style.RESET_ALL, flush=True) # Change back colours and flush
    else: # Use default
        xml_file = "classifiers/haarcascade_frontalface_default.xml"
        printf(Fore.RED) # Change colour to green
        printf("Cascade not provided, default: %s" % xml_file)
        print(Style.RESET_ALL) # Again reset style for further.
    
    # Create the obj 
    face_cascade = cv2.CascadeClassifier(xml_file)


    # Now open/create the file
    if not os.path.isfile(positive_info_file):
        # Doesn't exist so create file beforehand
        open(positive_info_file, "w").close()

    # Now open in append mode for writing the lines
    info_file = open(positive_info_file, "w").close()
    info_file = open(positive_info_file, "a") # append mode

    # Get relative path of img folders to info file
    #os.chdir(os.path.dirname(positive_info_file))
    #img_rel_path = get_relative_dir(positive_info_file, img_path)
    img_path = abspath(img_path)
    
    # Not just save faces for every image
    printf(Fore.GREEN) # Change colour 
    for path in images:
        save_func(path, info_file, face_cascade)
        
        # Use ansi to update line (FIX FOR WINDOWS)
        update_line("Image processed: %s     " % path)

    # Set things back to normal (colors and style)
    print(Style.RESET_ALL)

    info_file.close() # Close as function doesnt'do it

    print(Fore.GREEN+"Finished"+Style.RESET_ALL)
