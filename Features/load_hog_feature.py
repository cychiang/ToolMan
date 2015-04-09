# -*- coding: utf-8 -*-
import numpy as np
import cv2, argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program is load hog feature file and display the value.')
    parser.add_argument('-f', '--file', help='Input: The hog feature file.')
    args = parser.parse_args()
    input_file = args.file

    if input_file is not None:
        descriptor_bucket = np.load(input_file)
        for file_name in descriptor_bucket.files:
            print file_name

    else:
        print 'input file is none.'

