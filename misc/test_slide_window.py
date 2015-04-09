# -*- coding: utf-8 -*-
import numpy as np
import cv2, argparse
import time
# This script is based on http://www.pyimagesearch.com/2015/03/23/sliding-windows-for-object-detection-with-python-and-opencv/ works.

def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in xrange(0, image.shape[0], stepSize):
        for x in xrange(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[0], x:x + windowSize[1]])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program is test the slide window function.')
    parser.add_argument('-i', '--image', help='Input: Path to image')
    parser.add_argument('-r', '--rows', help='Input: Height of slide window')
    parser.add_argument('-c', '--cols', help='Input: Width of slide window')
    parser.add_argument('-s', '--step', help='Input: The step of slide window')

    args = parser.parse_args()
    cols = int(args.cols)
    rows = int(args.rows)
    step = int(args.step)

    image = cv2.imread(args.image, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    counter = 0
    if image is not None:
        print image.shape
        for (x, y, window) in sliding_window(image, stepSize=step, windowSize=(rows, cols)):
            # if the window does not meet our desired window size, ignore it
            if window.shape[0] != rows or window.shape[1] != cols:
                continue

            counter += 1
            clone = image.copy()
            cv2.rectangle(clone, (x, y), (x + cols, y + rows), (0, 255, 0), 2)
            cv2.imshow("clone", clone)
            cv2.imshow("window", window)
            cv2.waitKey(1)
            time.sleep(0.025)

    else:
        print 'Can not read image %s' %(args.image)

    print 'Total windows: %d' %(counter)
