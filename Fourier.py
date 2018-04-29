""" 
File to carry out the Fourier Transform on images and produce a magnitude image to be analyised and altered.
The inverse Fourier Transform can be applied to the altered magnitude image to recreate the original image but sharper.
"""
import numpy as np
import utilities

# Load image and convert to grayscale
img = utilities.read_image("osc.jpg", "BGR2GRAY")
size = img.shape

# Fourier Transform
# CURRENTLY FOR ONLY ONE PIXEL takes a lot of time to cycle through for all the pixels in an image
def fourier(u, v, size):
    
    # get dimensions
    N = size[0] # rows
    M = size[1] # columns
    
    f = 0
    for x in range(M):
        for y in range(N):
            f += np.sum(img[x,y] * exp(j*2*pi * ((u*x)/N + (v*y)/M)))
    
    # get the magnitude from the value of F
    # MAGNITUDE(F) = SQRT( REAL(F)^2+IMAGINARY(F)^2 )
    magnitude = np.absolute(f)
    
    return magnitude


# Plot the magnitude image of the original image


# Analysis and alteration of the magnitude values matrix


# Inverse Fourier Transform 
# f(x,y) = SUM{ F(u,v)*exp(+j*2*pi*(u*x+v*y)/N) }
def inverse_fourier(alter_matrix):


# Plot the image from the new matrix
