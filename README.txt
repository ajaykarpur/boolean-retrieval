This is the README file for A0132198A and A0132729A's submission

== General Notes about this assignment ==

We structured the code as follows:
- We added an Indexer class to encapsulate the methods and data required for
  creating the index.
- We added a command line option -k, which accepts values of k for
  subsets of k documents.
- We chose to remove stopwords from the index.

== Files included with this submission ==
index.py              The code used to index the documents.
search.py             The code used to search through the documents, using the index.
dictionary.txt        A pickled dict structure in the format {"word": frequency, offset}
postings.txt          The postings in text format.
ESSAY.txt             Our answers to the essay questions.
README.txt            This document.
test.bat              Batch script to quickly run and evaluate the code.
test.sh               Shell script to quickly run and evaluate the code.

== Statement of work ==

We, A0132198A and A0132729A, collaborated on this assignment. We otherwise have
followed the CS 3245 Information Retrieval class guidelines for homework
assignments.

== References ==

We consulted the NLTK website on the usage of the tokenizers.
http://www.nltk.org/_modules/nltk/tokenize.html