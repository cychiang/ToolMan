# -*- coding: utf-8 -*-
import cv2

if __name__ == "__main__":
    img = cv2.imread('/Users/cychiang/Desktop/samples/pedestrians/pedestrians128x64/per00924.ppm', cv2.CV_LOAD_IMAGE_GRAYSCALE)
    print img.shape
    cv2.imshow('ImageWindow',img)
    cv2.waitKey()
