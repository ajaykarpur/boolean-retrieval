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
