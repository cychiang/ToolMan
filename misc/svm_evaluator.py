# -*- coding: utf-8 -*-
import cv2, argparse, os, numpy

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
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-p', '--pos_list', help='Input: postive sample list.')
    parser.add_argument('-n', '--neg_list', help='Input: negtive sample list.')
    parser.add_argument('-s', '--svm', help='Input: .dat file')

    args = parser.parse_args()

    if not os.path.exists(args.pos_list):
        print 'No postive list file.'
        exit()
    if not os.path.exists(args.neg_list):
        print 'No negtive list file.'
        exit()
    if not os.path.exists(args.svm):
        print 'No SVM training file. (.dat)'
        exit()

    pos_list = open(args.pos_list, 'r')
    neg_list = open(args.neg_list, 'r')
    # create postive image list
    pos_bucket = []
    neg_bucket = []
    for file_name in pos_list:
        try:
            #.strip(): remove '/n' in the last of string.'
            file_name = file_name.strip()
            image = cv2.imread(file_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)

            if image is not None:
                pos_bucket.append(hog_opencv_feature(image))
            else:
                print 'Failed to load image file: %s' %(fileName)
                continue
        except:
            print 'loading error: %s ' %(str(fileName))
            continue

    pos_bucket = numpy.asarray(pos_bucket)
    svm = cv2.SVM()
    svm.load(args.svm)
    result = svm.predict_all(pos_bucket)
    print result
    # create negtive image list
    for file_name in neg_list:
        try:
            #.strip(): remove '/n' in the last of string.'
            file_name = file_name.strip()
            image = cv2.imread(file_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)

            if image is not None:
                neg_bucket.append(hog_opencv_feature(image))
            else:
                print 'Failed to load image file: %s' %(fileName)
                continue
        except:
            print 'loading error: %s ' %(str(fileName))
            continue
    neg_bucket = numpy.asarray(neg_bucket)
    result = svm.predict_all(neg_bucket)
    print result
