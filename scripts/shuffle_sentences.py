"""
Shuffle sentences in a CoNLL-U corpus. The shuffled sentences are written to a new file.
"""
# Example: python scripts/shuffle_sentences.py 'data/for-testing/dir2/tagged/test-set.conllu.bz2' 'data/for-testing/dir2/tagged/test-set-shuffled.conllu.bz2'

from context import speechact
import speechact.preprocess as pre
import sys

if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) != 3:
        print('Usage: python shuffle_sentences.py <source corpus> <target corpus>')
        sys.exit(1)

    source_file = sys.argv[1]
    target_file = sys.argv[2]

    print('Shuffling sentences...')
    pre.shuffle_sentences(source_file, target_file)
    print('Shuffling complete')