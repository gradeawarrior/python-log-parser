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

import argparse;
import getpass;
import subprocess;
import sys;

parser = argparse.ArgumentParser(description='Remote Log parser')
parser.add_argument('-s', '--servers', nargs='?',
                    type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='A file containing a list of servers to connect to')
parser.add_argument('-u', '--user',
                    default=getpass.getuser(),
                    help='Optional user to authenticate as on remote system if different than local')
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Turns on verbose output")

args = parser.parse_args()
print args

def main(argv):
    """
        main():
                The main logic of the program. All logic goes through here
    """
    while args.servers:
        line = args.servers.readline()
        line = line.rstrip("\n")
        
        ## Exit if EOF
        if not line: break
        
        if args.verbose: print line
        
        ## Split line
        host = line.split()[0]
        folder = "."
        cmd = "ssh %s@%s find . | egrep \"\.log$\"" %(args.user, host)
    
        ## Find all log files on remote machine
        files = get_log_files(host, folder, args.user)
        
        print ">> There are %s files" %(len(files))
        if args.verbose: print "%s" %(files)
    
    
def get_log_files(host, folder=".", user=getpass.getuser()):
    """Retrieves all log files from remote server"""
    
    cmd = "ssh %s@%s find %s | egrep \"\.log$\"" %(args.user, host, folder)
    print "------ %s@%s ------" %(args.user, host)
    if args.verbose: print "$ %s" %(cmd)
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         close_fds=True)
    stdout, stderr = p.communicate()
    stdout = stdout.rstrip("\n")
    files = stdout.split("\n")
    
    # Remove empty entry in result. This happens when there are 0 results
    # from above remote shell command
    if len(files) == 1 and files[0] == "": files.pop()
    
    return files

if __name__ == "__main__":
    main(sys.argv[1:])