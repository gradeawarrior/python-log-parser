#!/usr/bin/env python
#
# Author: Peter Salas
# Project Name: Log Parser
# Date: 07/16/2012
# Description:
#
#	A self-learning python script to help familiarize myself with python.
#       The goal of the script is to search on several remote machines for any
#       and every file (given a remote directory) containing some search word.
#

import sys;
import argparse;

parser = argparse.ArgumentParser(description='Remote Log parser')
parser.add_argument('-s', '--servers', nargs='?',
                    type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='A file containing a list of servers to connect to')
parser.add_argument('-u', '--user',
                    help='Optional user to authenticate as on remote system if different than local')
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Turns on verbose output")

args = parser.parse_args()
print args

while args.servers:
    line = args.servers.readline()
    line = line.rstrip("\n")
    
    ## Exit if EOF
    if not line: break
    
    if args.verbose: print line