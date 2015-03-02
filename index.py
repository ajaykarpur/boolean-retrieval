import sys
import getopt

#-------------------------------------------------------------------------------

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

directory = dictionary = postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except:
    usage()
    sys.exit(2)
        
for o, a in opts:
    if o == '-i':
        directory = a
    elif o == '-d':
        dictionary = a
    elif o == '-p':
        postings = a
    else:
        assert False, "unhandled option"
if directory == None or dictionary == None or postings == None:
    usage()
    sys.exit(2)