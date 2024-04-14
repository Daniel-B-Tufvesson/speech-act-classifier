"""
A script which removes duplicate sentences from a corpus. This creates a new corpus 
without duplicates.

Usage: python remove_duplicates.py <source corpus> <target corpus>
"""
# Example: python scripts/remove_duplicates.py 'data/for-testing/dir2/tagged/test-set.conllu.bz2' 'data/for-testing/dir2/tagged/test-set-no-dups.conllu.bz2'

from context import speechact
import speechact.preprocess as pre
import sys

if __name__ == '__main__':
    # Check the number of arguments passed
    if len(sys.argv) != 3:
        print('Usage: python remove_duplicates.py <source corpus> <target corpus>')
        sys.exit(1)

    source_file = sys.argv[1]
    target_file = sys.argv[2]

    pre.remove_duplicates(source_file, target_file, print_progress=True)