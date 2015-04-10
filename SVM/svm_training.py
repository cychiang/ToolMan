# -*- coding: utf-8 -*-
import cv2, argparse, os, numpy

# load data from file.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program is use SVM(support vector machine to training data. You have to specify POS. and NEG. data.')
    parser.add_argument('-p', '--postive', help='Input: postive .npz data')
    parser.add_argument('-n', '--negtive', help='Input: negtive .npz data')
    parser.add_argument('-o', '--output', help='Output: Name of output file.')

    args = parser.parse_args()

    if not os.path.exists(args.postive):
        print 'File: %s not exists.' %(args.postive)
        exit()
    if not os.path.exists(args.negtive):
        print 'File: %s not exists.' %(args.negtive)
        exit()

    postive_features = numpy.load(args.postive)
    negtive_features = numpy.load(args.negtive)

    print 'Size of postive data: %d' %(len(postive_features.files))
    print 'Size of negtive data: %d' %(len(negtive_features.files))

    # initial array
    training_data = []
    for postive_feature in postive_features.files:
        training_data.append(postive_features[postive_feature])

    for negtive_feature in negtive_features.files:
        training_data.append(negtive_features[negtive_feature])

    # convert list to numpy.ndarray
    training_data = numpy.asarray(training_data)

    # Initial training tags and set postive data into 1
    training_tags = numpy.zeros(len(training_data), dtype=numpy.int)
    training_tags[0:len(postive_features.files)] = 1
    # print info.
    print 'Size of tag data: %d' %(len(training_tags))
    print '-----------------------------'
    print 'Start training SVM...'
    svm_params = dict( kernel_type = cv2.SVM_LINEAR, svm_type = cv2.SVM_C_SVC, C = 1, gamma = 1 )

    svm = cv2.SVM()
    svm.train(training_data,training_tags, params=svm_params)
    svm.save(args.output)
