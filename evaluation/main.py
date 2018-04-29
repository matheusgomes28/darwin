""" Evaluation GUI Tool 

This script creates a Qt window with Python which displays
the original and result images from OD analysis.

Usage:
    main.py ORIGINALS RESULTS
    main.py --help 

Arguments:
    ORIGINALS       The path to the original images directory.
    RESULTS         The path to the result images directory.
"""


import sys, os
from random import shuffle 
from PyQt4 import QtGui, QtCore, uic
import csv

# For the CLI stuff
from docopt import docopt
from colorama import Style, Fore, init 

# For loading the main helper scripts
sys.path.append(os.path.abspath('../'))
import files

class MyWindow(QtGui.QMainWindow):
    def __init__(self, original_path, result_path):
        super(MyWindow, self).__init__()
        uic.loadUi('eval_gui.ui', self)
        self.show()
        self.answers = []

        # Load the list of images and shuffle them
        # Note: Make sure images match in each folder
        # i.e. they are in the same order in each dir
        paths_zipped = list(zip(files.get_images(original_path), files.get_images(result_path)))
        shuffle(paths_zipped) # shuffle the list of (original, result) paths 
        original_paths, result_paths = zip(*paths_zipped) # Unzip into two different lists

        # Check if the number of images is the same 
        if len(original_paths) != len(result_paths): print("Different num of images"); sys.exit(0)

        # Dict to store each set of images
        self.img_paths = {
            "original": original_paths,
            "result" : result_paths
        }

        # Make paths dynamic from CLI args  
        self.fileNum = len(self.img_paths["original"])
        self.fileCount = 0

        print('Number of files: {}'.format(self.fileNum))

        # Binding the buttons to functions
        self.correctButton.clicked.connect(lambda: self.correct_image())
        self.nearButton.clicked.connect(lambda: self.near_image())
        self.incorrectButton.clicked.connect(lambda: self.incorrect_image())

        # Create the scenes for the 2D graphics viewers
        self.scenes = {
            "original" : QtGui.QGraphicsScene(),
            "result" : QtGui.QGraphicsScene()
        }

        # Bind the scenes to the correct objs
        self.original.setScene(self.scenes['original'])
        self.preprocessed.setScene(self.scenes['result'])

        # For each scene, draw the first image at th start
        for s_name, s_obj in self.scenes.items():
            self.__set_scene_image(s_name, self.img_paths[s_name][0])

    def __set_scene_image(self, scene, img_path):
        """
        This private function sets the pixmap of a scene 
        to the image provided. 
        """

        # Check if available scene in dict
        if scene not in ["original", "result"]:
            print("Given scene not defined."); return

        # Get the scene obj 
        scene_obj = self.scenes[scene]

        # Get the width and height for resizing
        width = self.original.width()
        height = self.original.height()

        # Try to open the image 
        with open(img_path, "rb") as img_buffer:
            image_widget = QtGui.QImage()
            image_widget.loadFromData(img_buffer.read())

            # Get the pixel map data
            px_map = QtGui.QPixmap.fromImage(image_widget)
            px_map_rezised = px_map.scaledToHeight(height-2)
            graphics_obj = QtGui.QGraphicsPixmapItem(px_map_rezised)
            scene_obj.addItem(graphics_obj)
            scene_obj.update()

    def next_image(self):
        """
        This function will update the images on the 
        boxes. To be called after an button interaction.
        """

        # Just exit if the count is over the img num
        if self.fileCount >= self.fileNum: return

        # Call the function to update the images on each 
        # graphics panel
        for s_name, s_obj in self.scenes.items():
            self.__set_scene_image(s_name, self.img_paths[s_name][self.fileCount])

    def correct_image(self):
        self.update(1)
        self.next_image()

    def near_image(self):
        self.update(2)
        self.next_image()

    def incorrect_image(self):
        self.update(0)
        self.next_image()

    def update(self, answer):

        print('Answer {}: {}'.format(self.fileCount + 1, answer))

        # Get the current filename (only if we're still in range of the images)
        if self.fileCount < self.fileNum:
            filename = files.get_filename(self.img_paths['original'][self.fileCount])
            self.answers.append([filename, answer])

        # Increase the pointer
        self.fileCount += 1 

        # Save the stuff when reached the end
        if self.fileCount >= self.fileNum:

            # Oepn
            with open('images.csv', 'w', newline='') as out:
                csv_out = csv.writer(out)
                csv_out.writerow(['filename', 'answer'])
                for row in self.answers:
                    csv_out.writerow(row)

            # Exit window and hence exit the program 
            self.close() 


if __name__ == '__main__':

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
    original_path = files.abspath(arguments['ORIGINALS'])
    result_path  = files.abspath(arguments['RESULTS'])

    # For now, just print out settings and  all the images in the root.
    print(Fore.BLUE + "Settings passed: ")
    print("Original directory..... %s" % original_path)
    print("Results directory...... %s\n" % result_path)

    # Check that both directories exist
    if os.path.lexists(original_path) and os.path.lexists(result_path):
        pass
    else:
        print(Fore.RED + "Path not found, one of the directories does not exist.")
        print(Style.RESET_ALL)
        sys.exit(0) # Use system's abort function

    # Reset colour
    print(Style.RESET_ALL)

    # Creating the GUI and  setting exit criteria
    app = QtGui.QApplication(sys.argv)
    window = MyWindow(original_path, result_path)
    sys.exit(app.exec_())