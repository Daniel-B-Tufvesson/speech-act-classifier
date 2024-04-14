"""
This script assigns a new sent_id to each sentence across a set of several corpora. 

Usage: python reindex_sentences.py <source directory> <target directory>
"""
# Example: python scripts/reindex_sentences.py 'data/for-testing/dir1' 'data/for-testing/dir2'

from context import speechact
import speechact.corpus as corp
import speechact.preprocess as pre
import sys

if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) != 3:
        print('Usage: python reindex_sentences.py <source directory> <target directory>')
        sys.exit(1)

    source_dir = sys.argv[1]
    target_dir = sys.argv[2]

    source_files = pre.list_files(source_dir)

    # Load the corpora. Also remove suffixes.
    corpora = [corp.Corpus(file, file.split('/')[-1].removesuffix('.connlu.bz2').removesuffix('-100k').removesuffix('-500k')) for file in source_files]
    
    pre.reindex(corpora, target_dir)
