# -*- coding: utf-8 -*-
import numpy as np
import itertools as it
from glob import glob
import cv2, sys, os, argparse

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

def print_hog_info(hog):
    print 'hog winSize: %s' %(str(hog.winSize))
    print 'hog blockSize: %s' %(str(hog.blockSize))
    print 'hog blockStride: %s' %(str(hog.blockStride))
    print 'hog cell size: %s' %(str(hog.cellSize))
    print 'hog num of bins: %s' %(str(hog.nbins))


def hog_opencv_feature(image, winSize=(64,128), blockSize=(16,16), blockStride=(8,8), cellSize=(8,8), nbins=9):
    # winSize, blockSize, blockStride, cellSize, nbins
    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)
    r = [[0,0]]
    descriptors = hog.compute(image, hog.blockStride, hog.cellSize, r)
    # print_size_info(image)
    # print_hog_info(hog)
    # print 'size of descriptors: %d' %(len(descriptors))
    return descriptors

if __name__ == "__main__":
    # command line argument:
    # Initial argument
    parser = argparse.ArgumentParser(description='This program is generate the hog feature into file.')
    parser.add_argument('-f', '--file', help='Input: The list of target images')
    parser.add_argument('-o', '--out', help='Output: The collection of hog features')

    args = parser.parse_args()
    input_file = args.file
    output_file = args.out

    print 'version: %s' %(cv2.__version__)

    fileList = open(input_file, 'r')
    if fileList is not None:
        descriptor_bucket = []

        for fileName in fileList:
            try:
                #.strip(): remove '/n' in the last of string.'
                fileName = fileName.strip()
                image = cv2.imread(fileName, cv2.CV_LOAD_IMAGE_GRAYSCALE)
                if image is not None:
                    print 'loading ... %s' %(fileName)
                    descriptor_bucket.append(hog_opencv_feature(image))
                else:
                    print 'Failed to load image file: %s' %(fileName)
                    continue


            except:
                print 'loading error: %s ' %(str(fileName))
                continue

        print len(descriptor_bucket)

