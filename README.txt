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
    
Regular Expressions
===================
    
    Briefly looked over online regular expression documentation. Found that it's
    very similar to Perl regular expression, which is fundamental to programming
    in Perl to begin with!
    
        http://docs.python.org/howto/regex.html
        
    The program right now only does a very trivial regular expression check
    within the file on the remote system. More work and detail could be performed
    within the read_files() method to give us better results and thus a better
    report. However, the program was designed to search over a generic set
    of log files that may or may not have any correlation to other log files
    found under a given directory path.
    
log-parser Usage
================

    usage: log-parser.py [-h] [-s SERVER] [-u USER] [-v] [-i] [-x] SEARCH_TERM
    
    Remote Log parser
    
    positional arguments:
      SEARCH_TERM    What to search for
    
    optional arguments:
      -h, --help     show this help message and exit
      -s SERVER      A file containing a list of servers to connect to
      -u USER        Optional user to authenticate as on remote system if
                     different than local
      -v, --verbose  Turns on verbose output
      -i             Ignores case
      -x, --execute  Only when this is specified will it actually perform search
                     across list of hosts. Otherwise, this will only report on the
                     files that it would search but not actually execute the
                     search.
    
Example Execution
=================

    $ ./log-parser.py -s servers.txt -u psalas "\berror\b" -x
    Namespace(execute=True, ignorecase=False, regular_expression='\\berror\\b', server=<open file 'servers.txt', mode 'r' at 0x10d50a9c0>, user='psalas', verbose=False)
    ------ psalas@10.21.41.183 ------
    >> There are 0 files
    ------ psalas@10.21.41.236 ------
    >> There are 0 files
    ------ psalas@10.21.41.233 ------
    >> There are 0 files
    ------ psalas@m0010111.lab.ppops.net ------
    >> There are 45 files
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/curses/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/psych/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/gdbm/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/tk/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/pty/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/fiddle/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/ripper/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/racc/cparse/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/socket/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/readline/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/io/wait/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/io/nonblock/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/io/console/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/dbm/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/win32ole/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/syck/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/digest/sha1/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/digest/rmd160/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/digest/sha2/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/digest/md5/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/iconv/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/json/parser/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/json/generator/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/dl/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/syslog/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/openssl/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/bigdecimal/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/-test-/add_suffix/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/etc/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/ext/zlib/mkmf.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/ruby-1.9.3-p125/config.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/src/yaml-0.1.4/config.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/chmod.bin.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/make.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/gemsets.initial.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/rubygems.extract.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/install.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/rubygems.install.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/yaml/make.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/yaml/make.install.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/yaml/extract.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/yaml/configure.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/extract.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/gem.install.log on psalas@m0010111.lab.ppops.net ######
    
            ####### Scanning file:./.rvm/log/ruby-1.9.3-p125/configure.log on psalas@m0010111.lab.ppops.net ######
    
        ==================== Report ====================
        
        Regular Expression: \berror\b
        Number of Expressions: 1
        Number of Hosts Searched: 4
        Number of Log Files Searched: 45
        Number of lines where above condition was met: 413/26693