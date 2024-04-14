"""
This script splits a CoNLL-U coprus into a training corpus file and a test corpus file.

Usage: python split_corpus.py <corpus> <target directory> <split fraction>
"""
# Example: python scripts/split_corpus.py 'data/for-testing/dir1/dev-set.conllu.bz2' 'data/for-testing/dir2' 0.8

from context import speechact
import speechact.corpus as corp
import speechact.preprocess as pre
import sys
import os

if __name__ == '__main__':
    # Check the number of arguments passed
    if len(sys.argv) != 4:
        print('Usage: python split_corpus.py <corpus> <target directory> <split fraction>')
        sys.exit(1)

    source_file = sys.argv[1]
    target_dir = sys.argv[2]
    split_fraction = float(sys.argv[3])

    source_corpus = corp.Corpus(source_file)

    test_file = os.path.join(target_dir, f'{source_corpus.name}-test.conllu.bz2')
    train_file = os.path.join(target_dir, f'{source_corpus.name}-train.conllu.bz2')

    pre.split_train_test(source_corpus, test_file, train_file, split_fraction, print_progress=True)