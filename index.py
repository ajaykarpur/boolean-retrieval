import sys
import getopt
import os, os.path
import nltk

class Index(object):
    def __init__(self, documents, dictionary, postings):
        self.dictionary_filename = dictionary
        self.postings_filename = postings
        self.create_dictionary(documents)
        self.create_postings(documents)

    def create_dictionary(self, dirname):
        for filename in os.listdir(dirname):
            f = open(dirname + "\\" + filename)
            print filename
            f.close()

    def create_postings(self, dirname):
        pass

#-------------------------------------------------------------------------------

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

documents = dictionary = postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except:
    usage()
    sys.exit(2)
        
for o, a in opts:
    if o == '-i':
        documents = a
    elif o == '-d':
        dictionary = a
    elif o == '-p':
        postings = a
    else:
        assert False, "unhandled option"
if documents == None or dictionary == None or postings == None:
    usage()
    sys.exit(2)

my_Index = Index(documents, dictionary, postings)