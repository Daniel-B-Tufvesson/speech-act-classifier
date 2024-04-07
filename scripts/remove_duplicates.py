"""
A script which removes duplicate sentences from a corpus. This creates a new corpus without duplicates.
"""

from context import speechact
import speechact.preprocess as pre

if __name__ == '__main__':
    source_file = 'data/annotated data/test-set.conllu.bz2'
    target_file = 'data/annotated data/test-set-no-duplicates.conllu.bz2'
    pre.remove_duplicates(source_file, target_file, print_progress=True)