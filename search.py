#!/usr/bin/python
import sys
import getopt

#-------------------------------------------------------------------------------

def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

dictionary = postings = queries = output = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except:
    usage()
    sys.exit(2)
        
for o, a in opts:
    if o == '-d':
        dictionary = a
    elif o == '-p':
        postings = a
    elif o == '-q':
        queries = a
    elif o == '-o':
        output = a
    else:
        assert False, "unhandled option"
if dictionary == None or postings == None or queries == None or output == None:
    usage()
    sys.exit(2)