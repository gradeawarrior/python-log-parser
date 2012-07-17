#!/usr/bin/env python
#
# Author: Peter Salas
# Project Name: Log Parser
# Date: 07/16/2012
# Description:
#
#	A python program to help familiarize myself with python. The goal of
#       the script is to search on several remote machines for any and every
#       file (given a remote directory) containing some search word.
#
#       usage: log-parser.py [-h] [-s [SERVERS]] [-u USER] [-v] [-x]
#        
#        Remote Log parser
#        
#        optional arguments:
#          -h, --help            show this help message and exit
#          -s [SERVERS], --servers [SERVERS]
#                                A file containing a list of servers to connect to
#          -u USER, --user USER  Optional user to authenticate as on remote system if
#                                different than local
#          -v, --verbose         Turns on verbose output
#          -x, --execute         Only when this is specified will it actually perform
#                                search across list of hosts. Otherwise, this will only
#                                report on the files that it would search but not
#                                actually execute the search.

import argparse;
import getpass;
import os;
import paramiko;
import subprocess;
import sys;


###################################
# Argument Parser and Other Setup #
###################################

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
parser.add_argument('-x', '--execute', action='store_true',
                    help="Only when this is specified will it actually perform search across list of hosts. Otherwise, this will only report on the files that it would search but not actually execute the search.")

args = parser.parse_args()
print args

## Setup ssh client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))


########
# Main #
########

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
        
        ## Execute Search
        if args.execute: read_files(host, files, args.user)
    
    
####################
# Helper Functions #
####################
    
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

def read_files(host, files=[], user=getpass.getuser()):
    """Reads remote files"""
    
    ssh.connect(host, username=user)
    sftp = ssh.open_sftp()
    
    try:
        for file in files:
            remote_file = sftp.open(file)
            linenum = 0
            
            print "\n\t####### Opening file:%s on %s@%s ######" %(file, user, host)
            if args.verbose: print "\n----- begin cut -----";
            
            try:
                for line in remote_file:
                    line = line.rstrip("\n")
                    linenum += 1
                    if args.verbose: print "%s: %s" %(linenum, line)
            finally:
                remote_file.close()
                
            if args.verbose: print "----- end cut -----";
    finally:
        sftp.close()
        ssh.close()
        

if __name__ == "__main__":
    main(sys.argv[1:])