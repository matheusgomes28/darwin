""" Generating Negatives with Videos

This script is supposed to facilitate the 
generation of negative samples by using 
frames in videos. This script will use openCV
to open a video, extract frames and crop them
appropriately in order to get all portions of
the image with the right window size given.


Usage:
    generating_negatives.py VIDPATH OUTPATH [-s START] [-i INT] [-f FRAMES] [-w WID] [-h HEI]
    generating_negatives.py --help

Arguments:
    VIDPATH                    Path of video to use.
    OUTPATH                    Output folder path for samples. 

Options:
    -s START --start=START     Frame number to start.
    -i INT --interval=INT      Interval in seconds between frames.
    -f FRAMES --frames=FRAMES  Number of frames to save.
    -w WID --width=WID         Width of each sample saved.
    -h HEI --height=HEI        Height of each sample saved.
    --help                     Display the whole usage string.
"""

import util, cv2, sys
from colorama import Fore, Style, init
from docopt import docopt



def save_frame(capture, num, path, w=100, h=100):
    """
    This function will save the current
    frame in the video capture to an image
    file.
    """
    
    # Video's dimensions
    width = int(capture.get(3))
    height = int(capture.get(4))


    # Get number of images (rows*cols) in each frame
    cols = int(width/w)
    rows = int(height/h)

    # Read specific frame
    capture.set(1, num) # set to nth frame
    ret, frame = capture.read()

    # Loop to split image into many window_size images
    for row in range(rows):
        for col in range(cols):
            # Gets the cropped image
            img = frame[h*row:(row+1)*h, w*col:(col+1)*w]

            name = "img%s-%s-%s.jpg" % (str(num), row, col)
            cv2.imwrite(util.abspath(path) + "/" + name, img)



if __name__ == "__main__":

    # Get arguments with docopt
    arguments = docopt(__doc__, version="1.0")
    init(convert=True) # Init Ansi conversion
    
    # Now parse the arguments
    vid_path    = arguments['VIDPATH']
    output_path = arguments['OUTPATH']

    # Optional args
    if arguments['--help']:
        print(Fore.GREEN)
        print()
        print(__doc__)
        print(Style.RESET_ALL) 
        sys.exit(0)

    if arguments['--start']: start = int(arguments['--start'])
    else: start = 0 # Default starting frame

    if arguments['--interval']: interval = float(arguments['--interval'])
    else: interval = 1 # Default interval val

    if arguments['--frames']: n_frames = int(arguments['--frames'])
    else: n_frames = 1000 # Default use 1000 frames
  
    if arguments['--width']: width = int(arguments['--width'])
    else: width = 100 # Default windows width

    if arguments['--height']: height = int(arguments['--height'])
    else: height = 100 # Default window heigh


    # Print welcome and setting:
    print(Fore.BLUE)
    print("Generating Negatives script... Settings are:\n")
    print("Video path: %s"% vid_path)
    print("Output folder path: %s" % output_path)
    print("Starting frame: %s" % start)
    print("Time interval: %s" % interval)
    print("Number of frames: %s" % n_frames)
    print("Width of samples: %s" % width)
    print("Height of samples: %s" % height)
    print(Style.RESET_ALL) # BAck to normal color


    # Open video here
    video_cap = cv2.VideoCapture(util.abspath(vid_path))
     
    # Calculate video stuff
    video_fps = video_cap.get(cv2.CAP_PROP_FPS)
    video_frames = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_gap = int(interval*video_fps)

    # Make sure there are sufficient frames in the video
    if (start + n_frames*frame_gap) > video_frames:
        print(Fore.RED, end='')
        print("Interval  or #frames to save too large for video duration.")
        print(Style.RESET_ALL)
        sys.exit(1) # Exit

    # Do the saving here
    print(Fore.GREEN) # change output to green
    for i in range(n_frames):
        
        # Current frame to use
        cur_frame = start + i*frame_gap
        
        # Display Progress
        percent = ((i+1)/n_frames)*100
        util.update_line("Current progress: %.2f%%." % percent)

        # Save the images 
        save_frame(video_cap, cur_frame, output_path, width, height)
    print(Style.RESET_ALL)
