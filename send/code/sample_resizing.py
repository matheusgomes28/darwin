# This file contain code for resizing
# samples found in the info.dat file
# for positive images.

import os,cv2, sys
import numpy as np

class NullInfoDataException(Exception):
    """
    This class represents the exception thrown
    when the info data is not present when
    trying to retrieve sample configurations.
    """

    def __init__(self, message, errors):
        
        # Call super init
        super(NullInfoDataException, self).__init__(message)
        
        # Now printing off what happened
        self.errors = errors
        
        print(self.message)


class Sample(object):
    """
    Class that represents a sample image
    containing positive occurrences
    in our dataset.
    """

    
    def __init__(self, data_line, info_file_path):
        """
        This method will simply set
        the data line (from info.data)
        so we can then get the faces
        from the picture and other info.
        """
        # Set instance vars
        self.__data = data_line
        self.__img_path = os.path.abspath(info_file_path) # Img file relative to info.dat
        self.__img_path = os.path.dirname(self.__img_path) # Get just the directory
        self.__count = None  # Number of faces in img file
        self.__faces = None  # [(x, y, w, h)] of each face in image

        # If data string was provided, get the faces
        # configs in the image
        if not (self.__data == None):
            
            configs = self.separate_info(self.__data)

            # Next line will get the folder where image is in
            # given the info from info.dat
            os.chdir(self.__img_path) # Working directory to info.dat dir
            # Working directory to where info.dat says image is in
            os.chdir(os.path.dirname(configs[0]))
            # Next line will get the filename
            location, name = os.path.split(configs[0])
            self.__img_path = os.path.join(os.getcwd(), name) # Now just use os to get the folder
            print(self.__img_path)

            self.__count = configs[1]
            self.__faces = configs[2] 
            
        
    def separate_info(self, data_line):
        """
        This function will get information on
        where the faces are in each positive 
        sample. Here we assume the lines are 
        in the right format (opencv info.data
        format).
        """
        # Raise exception if no data
        if (self.__data == None):
            raise NullInfoDataException("No info data is set.",None)
 
        # This will split on double spaces to get the path and
        # bounding box of faces in the image.
        configs = [i.strip() for i in self.__data.strip().split("  ")]

        
        # Now we just get the results 
        rel_path = configs[0]
        count = int(configs[1])
        boxes = configs[2:]

        # Now we get the bounding boxes as tuples (x, y, w, h)
        faces = [] # Stores face boxes in the image
        for i in range(count): # Count = len(boxes) - should be
            (x,y,w,h) = boxes[i].split(" ")
            (x,y,w,h) = (int(x), int(y), int(w), int(h))
            faces.append((x,y,w,h)) # append to face occurrence list 
        
        return (rel_path, count, faces)


    def get_face_objects(self):
        """
        This method will use the information provided
        to retrieve each face from the original sample
        and return the array containing all faces in 
        the image sample.
        """ 
 
        # Make sure face boxes is not empty
        if not self.__faces: return []

        # Open image as numpy array :
        img = cv2.imread(self.__img_path)
 
        # This loop will extract the face obj from
        # the images.
        face_objs = [] # Store numpy faces
        for (x, y, w, h) in self.__faces:
            cropped = img[y:y+h, x:x+w] # Get face portion
            face_objs.append(cropped)
        
        return face_objs       
                         
        



def rescale_image(img, x, y):
    """
    This funtion will use opencv
    to rescale an image by given
    scaling factors in x,y. This 
    uses the best method for 
    decimation and zooming.
    """

    # Get information about image
    (height, width, space) = img.shape

    # Now we get the desired scaling factors
    fx = x/width
    fy = y/height

    # Finally return the scaled image with 
    # area relation interpolation (best)
    return cv2.resize(img, (0,0), fx=fx, fy=fy,interpolation=cv2.INTER_AREA)

if __name__ == "__main__":
    # Open info.dat relative to root
    info_path = "/media/sf_OpenCV/images/positive/info.dat"
    info_file = open(info_path, "r")


    # Go through every image in the info file
    c_image = 0
    for line in info_file:
         
        # Now test the class we created
        sample = Sample(line, info_path)
        faces = sample.get_face_objects()


        for i in range(0, len(faces)):
            name = "img%s-%s.jpg" % (c_image, i)
            face = faces[i]

            # Now we resize images and save them
            resized = rescale_image(face, 50, 50)
            cv2.imwrite("/media/sf_OpenCV/resized/%s" % (name,), resized)

        c_image += 1 # for name purposes

  
    info_file.close() # close file
    print("Finished cropping & resizing all images...") 












