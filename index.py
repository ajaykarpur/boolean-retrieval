import sys
import getopt
import os, os.path
import string
import pickle
import collections
import nltk
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

class Index(object):
    def __init__(self, doc_directory, dict_filename, post_filename, k):
        self.k = k
        self.dict_filename = dict_filename
        self.post_filename = post_filename
        self.postings = collections.defaultdict(list)
        self.dictionary = {}
        self.create_postings(doc_directory)
        pickle.dump(self.dictionary, open(self.dict_filename, "wb"))

    def create_postings(self, dirname):
        stopwords = set(string.punctuation)
        if "stopwords" in os.listdir(os.path.dirname(dirname)):
            with open(os.path.dirname(dirname) + "\\stopwords") as s:
                stopwords = set(s.read().split()).union(stopwords)

        for count, doc_id in enumerate(os.listdir(dirname)):
            if count == self.k:
                break
            with open(dirname + "\\" + doc_id) as f:
                text = f.read()
                tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
                for token in tokens:
                    word = stemmer.stem(token).lower()
                    if word not in stopwords:
                        if self.postings[word][-1:] != [doc_id]:
                            self.postings[word].append(doc_id)
        
        with open(post_filename, 'w') as f:
            for word in self.postings:
                frequency = len(self.postings[word])
                offset = f.tell()
                self.dictionary[word] = frequency, offset
                
                positions = " ".join(sorted(self.postings[word], key=int))
                f.write(positions + "\n")

#-------------------------------------------------------------------------------

def usage():
    print "usage: " + sys.argv[0] + " -i directory-of-doc_directory -d dict_filename-file -p post_filename-file"

doc_directory = dict_filename = post_filename = k = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:k:')
except:
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)
        
for o, a in opts:
    if o == '-i':
        doc_directory = a
    elif o == '-d':
        dict_filename = a
    elif o == '-p':
        post_filename = a
    elif o == '-k':
        k = int(a)
    else:
        assert False, "unhandled option"
if doc_directory == None or dict_filename == None or post_filename == None:
    usage()
    sys.exit(2)
if k == None:
    k = len(os.listdir(doc_directory))

my_Index = Index(doc_directory, dict_filename, post_filename, k)