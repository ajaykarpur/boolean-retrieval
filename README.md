# boolean-retrieval

index.py:
- Added an Indexer class to encapsulate the methods and data required for
  creating the index.
- Added a command line option -k, which accepts values of k for
  subsets of k documents.
- Added options to remove stopwords and numbers from the index.

search.py:
- Handled operators using the shunting yard algorithm.
- Implemented stacks using Python's collections.deque structure.

index.py              The code used to index the documents.
search.py             The code used to search through the documents, using sets.
broken-search.py 	  The code used to search through the documents, using lists and skip pointers.
dictionary.txt        A pickled dict structure in the format {"word": frequency, offset}
postings.txt          The postings in text format.
ESSAY.txt             Our answers to the essay questions.
README.txt            This document.
test.bat              Batch script to quickly run and evaluate the code.
test.sh               Shell script to quickly run and evaluate the code.
