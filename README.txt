This is the README file for A0132198A-A0132729A's submission

== General Notes about this assignment ==

index.py:
- We added an Indexer class to encapsulate the methods and data required for
  creating the index.
- We added a command line option -k, which accepts values of k for
  subsets of k documents.
- We added options to remove stopwords and numbers from the index.

search.py:
- We handled operators using the shunting yard algorithm.
- We implemented stacks using Python's collections.deque structure.
- We were unable to get good accuracy using our skip pointers. In search.py,
  we then replaced the skip pointer and list implementation with an implementation
  using Python sets. We left our old implementation in broken-search.py. Please
  read through (and run) the broken-search.py code to see our implementation of
  the required skip pointer and list method.

== Files included with this submission ==
index.py              The code used to index the documents.
search.py             The code used to search through the documents, using sets.
broken-search.py 	  The code used to search through the documents, using lists and skip pointers.
dictionary.txt        A pickled dict structure in the format {"word": frequency, offset}
postings.txt          The postings in text format.
ESSAY.txt             Our answers to the essay questions.
README.txt            This document.
test.bat              Batch script to quickly run and evaluate the code.
test.sh               Shell script to quickly run and evaluate the code.

== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0132198A-A0132729A, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0132198A-A0132729A, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==

We consulted the NLTK website on the usage of the tokenizers.
http://www.nltk.org/_modules/nltk/tokenize.html

We consulted numerous StackOverflow posts for debugging.