""" Optic Disk Connection 

This script will open images in a dataset and 
detect the OD in each image. The resulting fitted
OD images will be saved in the OUTPUT directory.

Note: The input images must be normalised beforehand.

Usage:
    detect_od.py ROOT OUTPUT PCA

Arguments:
    ROOT            The root directory of the image dataset.
    OUTPUT          The output directory to save the analysis files.
    PCA 			The path to the PCA file
"""

import files # For the file management stuff
import os, sys, cv2 # For directory changing, sys stuff
import utilities as ut
import analysis as an
import numpy as np
from colorama import Style, Fore, init # Colouring CLI stuff
from docopt import docopt # CLI argument parser 
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from sklearn.mixture import GaussianMixture as GMM


# Main program here 
if __name__== "__main__":

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
	root_path = files.abspath(arguments['ROOT'])
	out_path = files.abspath(arguments['OUTPUT'])
	pca_path = files.abspath(arguments['PCA'])

	# For now, just print out settings and  all the images in the root.
	print(Fore.BLUE + "Settings passed: ")
	print("Root directory........ %s" % root_path)
	print("Output directory...... %s\n" % out_path)

	# Check that both directories exist
	if os.path.lexists(out_path) and os.path.lexists(root_path):
		pass
	else:
		print(Fore.RED + "Path not found, one of the directories does not exist.")
		print(Style.RESET_ALL)
		sys.exit(0) # Use system's abort function

	# Reset colour
	print(Style.RESET_ALL)

	# Load PCA
	PCA = np.loadtxt(pca_path)

	# Loading a list of image paths
	images = files.get_images(root_path) # Note line below resets the blue 
	print(Style.RESET_ALL + Fore.GREEN + "Number of images in the path: {:d}".format(len(images)))

	# Create the correlation array
	N = 450 # N is the square size of the image (make sure matches PCA sections)
	corr_array = np.zeros((N,N))

	# Settings (window size)
	width, height = 30, 30

	# Create the circular mask (from the center) to remove
	# the iamge circular boarders.
	Xs = np.ones((N,N))*np.arange(N)
	Ys = Xs.T
	r = 180 # Radius (from center) in pixels
	s = np.floor(N/2) # Displacement
	Xs, Ys = Xs - s, Ys - s
	Dist = Xs*Xs + Ys*Ys
	mask = Dist < r**2

	#############################################################
	# Params for fitting the curve to the image and displaying it
	max_weight = 5 # Max weights of points (0-max)
	Xs = np.linspace(0, 450, 2000) # The linspace X for drawing line

	# The hypothesis function 
	def func(x, a, b, c): # So we can fit a parabola 
		return a*x**2 + b*x + c

	# Loading all the images in the path and detecting the OD in them
	for i, img_path in enumerate(images):
		if i > 129 :
			original_image = ut.read_image(img_path, "BGR2GRAY")
			original_size = original_image.shape[0:2] # Stores the original size for later
			S = 450 # the square size of the image

			# Resize the image (with dims (450,450))
			img_resized = cv2.resize(original_image, (S,S), cv2.INTER_AREA)
			masked_img = img_resized*mask

			# Sliding algorithm (y,x is the center pixel)
			offset = np.max([width, height])//2 + 2 # The offset from the boarders
			for y in range(offset, N-offset, 5):
			    for x in range(offset, N-offset, 5):
			        
			        # Tuples to represent the window box
			        starts = np.array([y-height/2, x-width/2], dtype=int)
			        stops = np.array([starts[0]+height, starts[1]+width], dtype=int)
			        
			        window = masked_img[starts[0]:stops[0], starts[1]:stops[1]]

			        # PCA reconstruction
			        weights = np.dot(np.ravel(window), PCA)
			        recons = np.sum(weights*PCA, axis=1).astype("uint8")
			        
			        # Set the value of the comparing matrix
			        corr_array[y,x] = cv2.matchTemplate(recons.reshape(height,width), window, cv2.TM_CCOEFF)

			# Normalise the array
			corr_array[corr_array < 0] = 0 # Threshold by 0
			cv2.normalize(corr_array, corr_array, 0, 255, cv2.NORM_MINMAX)

			# Apply mask
			corr_array *= mask

			##########################
			###### Line Fitting ######
			##########################
			cv2.normalize(corr_array, corr_array, 0, max_weight, cv2.NORM_MINMAX)
			corr_array = np.round(corr_array)
			points = np.empty((2,0), dtype=int)

			for w in range(1, max_weight):
			    # Corresponding layer in depth matrix is bool repr.
			    # corresponding weight locations
			    coords = np.vstack(np.where(corr_array == w))
			    points = np.hstack((points, np.repeat(coords, w, axis=1)))

			# Fit the line parameters and get new Ys (based on the Xs)
			params, ppcov = curve_fit(func, points[0,:], points[1,:])
			b, c, d = params
			Ys = b*Xs**2 + c*Xs + d

			# Clip the lines (so we dont go off the img)
			points = np.vstack((Xs, Ys))
			x_clip = np.logical_or(Xs < 20, Xs > 420)
			y_clip = np.logical_or(Ys < 20, Xs > 420)
			clip = np.logical_not(np.logical_or(x_clip, y_clip))

			# Get the extrema (in resized)
			ext_y = -c/(2*b) 
			ext_x = b*ext_y**2 + c*ext_y + d

			# Multiply by the scalling factor
			factors = (original_size[0]/450, original_size[1]/450)
			#ext_x *= factors[1]
			#ext_y *= factors[0]
			# Maybe Change
			# original_size = (height, width), factors = (height, width)



			# Draw circle in the od 
			#cv2.circle(img_resized,(ext_x,ext_y), 10, (255,0,0), -1)

			################################
			## Getting the ROI for the OD ##
			################################
			# Get the initial region corner points
			size = S/2.5
			region_x1, region_y1 = int(max(ext_x - size/2, 0)), int(max(ext_y - size/2,0))
			region_x2, region_y2 = int(min(ext_x + size/2, S)), int(min(ext_y + size/2, S))

			# Get the region obtained (centered at the OD location we found
			# previosuly). The size of this region can be cahnged, but so far 
			# this size contains about 1/4 of the image area.
			region = img_resized[region_y1:region_y2,region_x1:region_x2]
			Z = region.reshape((-1))

			# Convert to np.float32 for the K-Means
			Z = np.float32(Z)

			# min od size
			od_size = 100


			try: 
				print("image: {}".format(i))
				# Define criteria, stop when threshold is reached or the max iter is reached
				criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
				K = 4 # Nubers of clusters

				# Perform K-Means with OpenCV's function
				ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

				# Now convert back into uint8, and make original image
				center = np.uint8(center)
				res = center[label.flatten()]
				k_means_region = res.reshape((img_resized[region_y1:region_y2,region_x1:region_x2].shape))

				# Apply the erosion 
				kernel = np.ones((7,7),np.uint8)
				erosion = cv2.erode(k_means_region,kernel,iterations = 1)

				###################################
				## Gaussian Mixture Models Stuff ##
				###################################

				# Get the maximum value of the erosion 
				m_colour = np.max(erosion)

				# Get the location of these points (Equivalent to I)
				Ys, Xs = np.where(erosion==m_colour)

				# First col is Ys, second col is Xs
				samples = np.vstack((Ys,Xs)).T

				# Cluster those points with GMM
				od_prob = GMM(n_components=1, covariance_type="diag")
				od_prob.fit(samples)

				# Get the scores for each sample in the GMM
				scores = od_prob.score_samples(samples)
				# Mean and std_dev for threshold calc
				mean = np.mean(scores)
				std = np.sqrt(np.var(scores))
				thresh = 1.5 # std_dev unit for threshol 

				# Apply the mask to the 
				filtered = scores > mean - 2*std
				locations = np.where(filtered)

				# The (x,y) in I which are within the threshold 
				rows = samples[locations]

				# get the remaining tuples in I
				Ys, Xs = rows[:, 0], rows[:, 1]

				# Create a dummy matrix to represent the data (0s everywhere,
				# except in the remaining (x,y)) 
				detected = np.zeros(erosion.shape, dtype="uint8")
				detected[Ys, Xs] = 255

				# Get the ROI corners
				rect = an.get_rect(detected) #(x1, y1, x2, y2)
				x1 = rect[0]; y1 = rect[1];
				x2 = rect[2]; y2 = rect[3];

				if x2-x1 < od_size:
					compensate = od_size - (x2-x1)
					x1 = int(max(0, x1-compensate/2))
					x2 = int(min(450, x2+compensate/2))
				if y2-y1 < od_size:
					compensate = od_size - (y2-y1)
					y1 = int(max(0, y1-compensate/2))
					y2 = int(min(450, y2+compensate/2))

			except:
				x1, y1 = int(max(ext_x - od_size/2, 0)), int(max(ext_y - od_size/2,0))
				x2, y2 = int(min(ext_x + od_size/2, S)), int(min(ext_y + od_size/2, S))

			# Get the original positions now
			x1 = int((region_x1 + x1)*factors[0]); y1 = int((region_y1 + y1)*factors[1])
			x2 = int((region_x1 + x2)*factors[0]); y2 = int((region_y1 + y2)*factors[1])

			# Now we save the OD
			od = original_image[y1:y2,x1:x2]
			cv2.imwrite(files.append_path(out_path, files.get_filename(img_path)+".jpg"), od)


			# Saving the figure and the line
			#my_dpi = 96 # DPA of YOUR monitor (for exact size)
			#fig = plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
			#ax = plt.gca()
			#ax.set_axis_off()
			#ax.imshow(img, cmap="gray")
			#ax.plot(Ys[clip], Xs[clip], color="blue")
			#fig.tight_layout(); 
			#plt.savefig(files.append_path(out_path, files.get_filename(img_path)+".jpg"), dpi=my_dpi)

			# Progress bar stuff
			cmd_size = 20 # Length of the loading bar in chars
			perc = (i+1)/len(images)	
			bar = int(np.round(perc*cmd_size))
			line = "Processing ["
			line += "="*bar + " "*(cmd_size-bar)
			line += "] {:d}%".format(int(np.round(perc*100)))
			ut.update_line(line) # Thins func will use carriage return
	print("\nFinished processing.")
