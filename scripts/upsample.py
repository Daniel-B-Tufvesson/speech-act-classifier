"""
This script upsamples the corpus so that there is an equal amount of sentences 
for each speech act label. The upsampled corpus is written to a new file.

Usage: python upsample.py <source corpus>
"""
# Example: python scripts/upsample.py 'data/for-testing/dir2/tagged/test-set.conllu.bz2'

from context import speechact
import speechact.corpus as corp
import speechact.preprocess as pre
import os
import bz2
import sys


if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) != 2:
        print('Usage: python upsample.py <source corpus>')
        sys.exit(1)

    source_file = sys.argv[1]

    source_corpus = corp.Corpus(source_file)
    target_dir = os.path.dirname(source_file)
    target_file = os.path.join(target_dir, f'{source_corpus.name}-upsampled.conllu.bz2')

    print(f'Upsampling "{source_file}" to "{target_file}.')

    with bz2.open(target_file, mode='wt') as target:
        pre.upsample(source_corpus, target)