DESCRIPTION
===========

    A python program for my own self-learning. The challenge is to write a python
    program that will scan for log files on a set of remote hosts, and search for
    something in the file (e.g. errors). The program must support the situation
    that the remote file may be large (e.g. over a Gig).

Remote File Research
====================

    Based on the following online resources:

        http://stackoverflow.com/questions/68335/how-do-i-copy-a-file-to-a-remote-server-in-python-using-scp-or-ssh
        http://stackoverflow.com/questions/1596963/read-a-file-from-server-with-ssh-using-python
    
    I decided to use a combination of the subprocess libraries to make a remote
    system call to another unix system and search for all log files; and the
    paramiko library to open up a separate ssh/sftp connection to read the files.
    This was the easiest solution to implement, yet also allow me to explore the
    broader aspects of python programming.
    
    Another, and possibly more robust approach would be to do the file traversal
    logic purely in paramiko using the paramiko.SFTPClient libraries. More
    specifically, I would do the following calls to traverse the remote filesystem:
    
        import os, sys
        from stat import *
    
        for file in paramiko.list(path):
            mode = paramiko.stat(file).st_mode
            if S_ISDIR(mode):
                ## It's a directory
                # Traverse into this directory
            elif S_ISREG(mode)
                ## It's a file
                # If a log file, then read it
                
    See the directory-traverse.py script for a proof-of-concept file traversal
    on a local filesystem.