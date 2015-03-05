#!/usr/bin/python
import sys
import getopt
import os
import string
import pickle
import collections
import nltk
import re
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

class Indexer(object):
    def __init__(self, doc_directory, dict_filename, post_filename, k):
        self.k = k
        self.dict_filename = dict_filename
        self.post_filename = post_filename

        self.postings = collections.defaultdict(list)
        self.dictionary = {}
        self.all_doc_ids = []
        self.stopwords = set(string.punctuation)
        
        self.create_postings(doc_directory)
        self.write_files()

    def create_postings(self, dirname):
        """
        create a dict of words and their associated posting lists
        eg. {"bill": [1, 10, 109]}
        """

        def remove_stopwords(): # remove stopwords if given
            if "stopwords" in os.listdir(os.path.dirname(dirname)):
                with open(os.path.join(os.path.dirname(dirname), "stopwords")) as s:
                    self.stopwords = set(s.read().split()).union(self.stopwords)

        def remove_numbers(text):
            return text.translate(None, string.digits)

        remove_stopwords()

        for count, doc_id in enumerate(os.listdir(dirname)):
            if count == self.k: # use k documents to train
                break
            self.all_doc_ids.append(doc_id)
            with open(os.path.join(dirname, doc_id)) as f:
                text = f.read()
                text = remove_numbers(text)
                tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
                for token in tokens:
                    word = stemmer.stem(token).lower()
                    if word not in self.stopwords:
                        if self.postings[word][-1:] != [doc_id]: # check last doc_id for redundancy
                            self.postings[word].append(doc_id)

                        for subword in re.split('[- /]',token):
                            subword = stemmer.stem(subword).lower()
                            if subword not in self.stopwords:
                                if self.postings[subword][-1:] != [doc_id]: # check last doc_id for redundancy
                                    self.postings[subword].append(doc_id)

    def write_files(self):
        """
        write dictionary.txt and posting.txt
        make dictionary {"word": frequency, offset}, where frequency is the size
        of the posting list and offset is the location in postings.txt
        """
        with open(self.post_filename, 'w') as f: # write postings.txt
            for word in self.postings:
                frequency = len(self.postings[word])
                offset = f.tell() # location in the postings.txt file
                self.dictionary[str(word)] = frequency, offset
                
                positions = " ".join(sorted(self.postings[word], key=int)) # sort postings
                f.write(positions + "\n")

        pickle.dump(self.dictionary, open(self.dict_filename, "wb")) # write dictionary.txt
        print self.dictionary

        pickle.dump(self.all_doc_ids, open("all_doc_ids.txt", "wb"))


#-------------------------------------------------------------------------------
# added a new flag to accept values of k (for subsets of k documents)

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

my_index = Indexer(doc_directory, dict_filename, post_filename, k)