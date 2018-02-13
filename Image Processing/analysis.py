# File containing al the
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


def get_err(grey_image) :
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

