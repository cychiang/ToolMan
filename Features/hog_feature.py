# -*- coding: utf-8 -*-
import numpy as np
import itertools as it
from glob import glob
import cv2, sys, os

help_message = '''
USAGE: hog_feature.py <image_names> ...
This function is generate hog feature into file.
'''

def print_bins_info(bins):
    print 'cols: %d' %(len(bins))
    print 'rows: %d' %(len(bins[0]))
    print 'bins: %d' %(len(bins[0][0]))

def print_size_info(items):
    print 'cols: %d' %(len(items))
    print 'rows: %d' %(len(items[0]))

def count_array_info(array):
    print ''

def hog_feature(image, num_of_bin):
    gradient_x = cv2.Sobel(image, cv2.CV_32F, 1, 0)
    gradient_y = cv2.Sobel(image, cv2.CV_32F, 0, 1)
    mag, ang = cv2.cartToPolar(gradient_x, gradient_y)

    # quantizing binvalues in (0...num_of_bin)
    bins = np.int32(num_of_bin * ang/(2*np.pi))

    print 'print_size_info: image'
    print_size_info(image)
    print 'print_size_info: bins'
    print_size_info(bins)
    print 'print_bins_info: bins'
    print_bins_info(bins)

def hog_opencv_feature(image):
    hog = cv2.HOGDescriptor()
    r = [[0,0]]
    descriptors = hog.compute(image,hog.blockStride,hog.cellSize,r)
    print_size_info(image)
    print 'model path: %s' %(os.path.dirname(cv2.__file__))
    print 'hog blockStride: %s' %(str(hog.blockStride))
    print 'hog cell size: %s' %(str(hog.cellSize))
    print 'size of descriptors: %d' %(len(descriptors))


if __name__ == "__main__":
    print 'version: %s' %(cv2.__version__)

    for image_name in sys.argv[1:]:
        try:
            image = cv2.imread(image_name)
            if image is None:
                print 'Failed to load image file: %s' %(image)
                continue
            else:
                print 'loading ... %s' %(image_name)

            # hog_feature(image, 8)
            hog_opencv_feature(image)

        except:
            print 'loading error'
            continue




