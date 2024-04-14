"""
This script takes a CoNLL-U corpus file and tags each sentence with its sentiment.

Usage: python tag_sentiment.py <source corpus> <target corpus>
"""
# Example: python scripts/tag_sentiment.py 'data/for-testing/dir2/dev-set-test.conllu.bz2' 'data/for-testing/dir2/dev-set-test-sentiment.conllu.bz2'

from context import speechact
import speechact.preprocess as pre
import speechact.corpus as corp
import bz2
import sys

def tag_corpus(bz2_source_file: str, target_file: str):
    print(f'Tagging sentences from "{bz2_source_file}" to "{target_file}".')

    corpus = corp.Corpus(bz2_source_file)

    with bz2.open(target_file, mode='wt') as target:
        pre.tag_sentiment(corpus, target, print_progress=True)

if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) != 3:
        print('Usage: python tag_sentiment.py <source corpus> <target corpus>')
        sys.exit(1)

    source_file = sys.argv[1]
    target_file = sys.argv[2]

    tag_corpus(source_file, target_file)