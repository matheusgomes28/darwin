# File containing all the
# analysis code such as the
# Fourier transform.
import cv2
import numpy as np
import filtering as fil


def fourier(image):
	"""
	This function will use OpenCV to 
	calculate the fourier transform of 
	an image.
	"""

	# Calculate FFT (amplitude and phase)
	dft = cv2.dft(np.float32(image), flags= cv2.DFT_COMPLEX_OUTPUT)

	# Shift DFT so frequency 0 is at center
	shift = np.fft.fftshift(dft)

	# Amplitude and Phase spectrum
	amp = 20*np.log(cv2.magnitude(shift[:,:,0], shift[:,:,1]))
	phase = cv2.phase(shift[:,:,0], shift[:,:,1])

	# Return both sprectra 
	return (amp, phase)


def get_laplacian(image_grey):
    """
    This function will calculate the laplacian
    given the grey scale image.
    """
    assert len(image_grey.shape) < 3
    
    # Approximation kernel
    kernel = np.array([[0,1,0], [1,-4,1], [0,1,0]])
    
    # Retrn convoluted image 
    return fil.image_conv(image_grey, kernel)


def get_err(grey_image):
	"""
	This function will get the ERR of an image
	using the method explained in the "Fourier
	Blurring" notebook. Note the the image 
	must be in grayscale.
	"""

	# Get the fourier spectrum with the above
	amp, phase = fourier(grey_image)

	# Get the f(0) value (or maximum)
	f0 = np.max(amp)

	# Get the energy of the amp spectrum
	E_f = np.sum(np.multiply(amp, amp))

	# Return tau = E_f/|f(0)|^2
	return E_f/np.power(np.abs(f0), 2) 


def equalise(grey_image):
    """
    This function will transfrom a grayscale 
    image through histogram equalisation using
    the methods described in the notebook
    "Histogram Equalisation" 

    Args: 
        image - numpy array representing the image.
    """
    
    # Generate the intensity histogram for the image
    hist = cv2.calcHist([grey_img],[0],None,[256],[0,256])
    
    # Calculate the cumulative probability for the image
    cf = np.cumsum(hist/(grey_img.shape[0] * grey_img.shape[1]))
    
    # Transform the intensities in the image
    for row in range(grey_img.shape[0]):
        for col in range(grey_img.shape[1]):
                grey_img[row, col] = cf[grey_img[row, col]] * 256
        
    # Generate the intensity histogram for the altered image
    new_hist = cv2.calcHist([grey_img],[0],None,[256],[0,256])

    # Calculate the cumulative probability of the altered image
    n_cf = np.cumsum(new_hist/(grey_img.shape[0] * grey_img.shape[1]))
    
    # Return the transformed image
    return grey_image

## Funciton definitions to get the histograms ##
def get_histogram(image):
    """
    This function will return the histogram
    of the given image using the OpenCV
    calcHist function.
    
    Args: 
        image - numpy array representing the image.
        
    Returns:
        Numpy matrix representing the histogram of image.
        Note each row is the histogram of each components.
    """
    # Get all the channels
    dims = image.shape # dimension of image (H, W, D)
    n_channels = 1 if len(dims) < 3 else dims[-1]
    n_pixels = dims[0]*dims[1]
    
    # Set the parameters accordignly
    channels = [0]
    sizes = [256]
    ranges = [0, 256]
    mask = None
    
    # Separate image into different components
    if n_channels > 1:
        components = [image[:,:,i] for i in range(n_channels)]
    else:
        components = [image]
        
    # Helper function to apply calcHist to a given image
    helper = lambda x : cv2.calcHist([x], channels, mask, sizes, ranges)
    
    # Now return the stacked results
    return np.hstack([helper(comp) for comp in components])/n_pixels

def manipulate(image, I, hist):
    """
    This funcion will take an image and the 
    average histogram generated from a dataset
    and manipulate the image's histogram to that
    of the average one.

    Args: 
        image - numpy array representing the image.
        I - List of numpy arrays of intensity locations
            in primitive form, e.g I = [(i,j)]
        hist - numpy array representing a histogram.

    Returns: 
        Numpy array representing altered image.
    """

    # Copy image 
    altered = image.copy()
    
    # For loop doing the transformation
    counter = 0 # Keep track of current index in I
    for i in range(256):
        N = int(hist[i])
      
        # Assign N first pixels to corresponding 
        # intensity        
        if N > 0: # Check whether assignments are actually made here
            altered[np.split(I[counter:counter+N], 2, axis=1)] = i
            
        # Update counter so we start from correct place in I 
        counter += N
        
    # Returned the modified image 
    return altered
