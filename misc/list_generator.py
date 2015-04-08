# -*- coding: utf-8 -*-
from glob import glob
import argparse

def print_args_info(args):
    print 'File Path: %s' %(args.path)
    print 'Output File Name: %s' %(args.out)
    print 'Prefix Name: %s' %(args.prefix)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This program is generate the file list by given specific path.')
    parser.add_argument('-p', '--path', help='Input: The path you want to create file list.')
    parser.add_argument('-o', '--out', help='Output: The file list of specific path.')
    parser.add_argument('-x', '--prefix', help='Arguments: supported prefix name.')
    args = parser.parse_args()
    print_args_info(args)

    file_path = args.path
    out_file_name = args.out
    prefix_name = args.prefix

    if out_file_name is None:
        print 'None'
    else:

        file_path = file_path + '/*.' + prefix_name
        file_list = glob(file_path)
        if len(file_list) == 0:
            print 'no file.'
            exit()
        else:
            wf = open(out_file_name, 'w')
            for item in file_list:
                wf.write(item+'\n')
            wf.close()
