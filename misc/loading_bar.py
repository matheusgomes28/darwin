from colorama import init as c_init # Colour init
from colorama import Style, Fore
import time  # For slowing things down a little bit
import os, sys

def update_line(text, chars=["\033[F","\r"]): 
    """
    This function will output text on
    the same line. I.e update the line
    with the new text using ANSII.

    Only use this for CLIs as info is printed to stdout.
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

if __name__ == "__main__":

	# Colour init for windows
	c_init()

	size = 20
	for i in range(size):
		update_line("Loading [" + "="*i + " "*(size-i) + "] {:d}%".format(int(100*(1+i)/size)))
		time.sleep(0.5)

	print("\nEnded")
