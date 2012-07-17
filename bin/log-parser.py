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
#        usage: log-parser.py [-h] [-s SERVER] [-u USER] [-v] [-x] SEARCH_TERM
#        
#        Remote Log parser
#        
#        positional arguments:
#          SEARCH_TERM    What to search for
#        
#        optional arguments:
#          -h, --help     show this help message and exit
#          -s SERVER      A file containing a list of servers to connect to
#          -u USER        Optional user to authenticate as on remote system if
#                         different than local
#          -v, --verbose  Turns on verbose output
#          -x, --execute  Only when this is specified will it actually perform search
#                         across list of hosts. Otherwise, this will only report on the
#                         files that it would search but not actually execute the
#                         search.
#

import argparse;
import getpass;
import os;
import paramiko;
import re;
import subprocess;
import sys;


###################################
# Argument Parser and Other Setup #
###################################

parser = argparse.ArgumentParser(description='Remote Log parser')
parser.add_argument('-s', metavar='SERVER', type=argparse.FileType('r'), default=sys.stdin,
                    help='A file containing a list of servers to connect to')
parser.add_argument('-u', metavar='USER', default=getpass.getuser(),
                    help='Optional user to authenticate as on remote system if different than local')
parser.add_argument('-v', '--verbose', action='store_true',
                    help="Turns on verbose output")
parser.add_argument('-x', '--execute', action='store_true',
                    help="Only when this is specified will it actually perform search across list of hosts. Otherwise, this will only report on the files that it would search but not actually execute the search.")
parser.add_argument('regular_expression', metavar="SEARCH_TERM",
                    help="What to search for")

args = parser.parse_args()
print args

## Compile Regular Expression
term = re.compile(args.regular_expression)

## Setup Reporting Variables
report = {}

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
    
        ## Find all log files on remote machine
        files = get_log_files(host, folder, args.user)
        
        print ">> There are %s files" %(len(files))
        if args.verbose: print "%s" %(files)
        
        ## Execute Search
        if args.execute: read_files(host, files, args.user)
        
        ## Pretty Print Report
        print_report()
    
    
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
                    
                    m = term.search(line)
                    if m:
                        print "!! Found occurence on line %s: %s" % (linenum, line)
                        add_report(args.regular_expression, host, file, linenum, line)
            finally:
                remote_file.close()
                
            if args.verbose: print "----- end cut -----";
    finally:
        sftp.close()
        ssh.close()
        
def add_report(type, host, file, linenum, line):
    """Adds to the internal reporting structure"""
    
    if report.has_key(type):
        if report[type].has_key(host):
            if report[type][host].has_key(file):
                report[type][host][file].append([linenum, line])
            else:
                report[type][host][file] = [linenum, line]
        else:
            report[type][host] = {}
    else:
        report[type] = {}
        
def print_report():
    """pretty print report to user"""
    
    print report

if __name__ == "__main__":
    main(sys.argv[1:])