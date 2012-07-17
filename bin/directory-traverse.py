#!/usr/bin/env python

#!/usr/bin/env python
#
# Author: Peter Salas
# Project Name: Directory Traversal
# Date: 07/16/2012
# Description:
#
#	A python program to help familiarize myself with python. The goal of
#       the script is to programmatically in python traverse a folder structure
#
#        usage: directory-traverse.py [-h] -d directory
#        
#        Directory traversal
#        
#        optional arguments:
#          -h, --help    show this help message and exit
#          -d directory  Directory to traverse


import argparse, os, sys
from stat import *

parser = argparse.ArgumentParser(description='Directory traversal')
parser.add_argument('-d', required=True, dest='directory', metavar='directory',
                    help='Directory to traverse')
args = parser.parse_args()
print args

def walktree(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname).st_mode
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)

def visitfile(file):
    print('visiting', file)

if __name__ == '__main__':
    walktree(args.directory, visitfile)