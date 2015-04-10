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

def sliding_window(image, stepSize, windowSize):
    # slide a window across the image
    for y in xrange(0, image.shape[0], stepSize):
        for x in xrange(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[0], x:x + windowSize[1]])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    # parser.add_argument('-p', '--pos_list', help='Input: postive sample list.')
    # parser.add_argument('-n', '--neg_list', help='Input: negtive sample list.')
    parser.add_argument('-d', '--data', help='Input: test data list')
    parser.add_argument('-s', '--svm', help='Input: .dat file')
    parser.add_argument('-r', '--rows', help='Input: Height of slide window')
    parser.add_argument('-c', '--cols', help='Input: Width of slide window')
    parser.add_argument('-st', '--step', help='Input: The step of slide window')

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

    cols = rows = step = None
    if args.cols not None:
        cols = int(args.cols)
    else:
        print 'cols is None.'
        exit()

    if args.rows not None:
        rows = int(args.rows)
    else:
        print 'cols is None.'
        exit()

    if args.step not None:
        step = int(args.step)
    else:
        print 'cols is None.'
        exit()

    data_list = open(args.data)
    # Load SVM
    svm = cv2.SVM()
    svm.load(args.svm)
    for data_name in data_list:
        try:
            data_name = data_name.strip()
            image = cv2.imread(data_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
            if image is not None:
                for (x, y, window) in sliding_window(image, stepSize=step, windowSize=(rows, cols)):
                    if window.shape[0] != rows or window.shape[1] != cols:
                        continue
                    clone = image.copy()
                    cv2.rectangle(clone, (x, y), (x + cols, y + rows), (0, 255, 0), 2)
                    cv2.imshow("clone", clone)
                    cv2.imshow("window", window)
                    cv2.waitKey(1)
                    time.sleep(0.025)

            else:
                print 'Failed to load image file: %s' %(data_name)
                continue


        except:
            print 'Data: %s error' %(data_name)
            pass

    # pos_list = open(args.pos_list, 'r')
    # neg_list = open(args.neg_list, 'r')
    # create postive image list
    # sample_bucket = []
    # for file_name in pos_list:
    #     try:
    #         #.strip(): remove '/n' in the last of string.'
    #         file_name = file_name.strip()
    #         image = cv2.imread(file_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    #         if image is not None:
    #             pos_bucket.append(hog_opencv_feature(image))
    #         else:
    #             print 'Failed to load image file: %s' %(fileName)
    #             continue
    #     except:
    #         print 'loading error: %s ' %(str(fileName))
    #         continue
    #         for (x, y, window) in sliding_window(image, stepSize=step, windowSize=(rows, cols)):
    #             # if the window does not meet our desired window size, ignore it
    #             if window.shape[0] != rows or window.shape[1] != cols:
    #                 continue

    #             counter += 1
    #             clone = image.copy()
    #             cv2.rectangle(clone, (x, y), (x + cols, y + rows), (0, 255, 0), 2)
    #             cv2.imshow("clone", clone)
    #             cv2.imshow("window", window)
    #             cv2.waitKey(1)
    #             time.sleep(0.025)
    # pos_bucket = numpy.asarray(pos_bucket)

    # result = svm.predict_all(pos_bucket)
    # print result
