"""
Cleans up CoNLL-U files by removing sentences that are improperly formatted. A sentence is
incorrectly formatted if it cannot be loaded by Stanza's CoNLL-U parser.
"""

from context import speechact
import bz2
import speechact.preprocess as pre
import sys

def clean_up_bz2(source_file: str, target_file: str):
    """
    Clean a bz2 compressed connlu corpus. The cleaned up version is saved to the target
    file as a compressed connlu corpus as well.
    """
    print('clean_up_bz2')

    with bz2.open(source_file, mode='rt') as source:
        with bz2.open(target_file, mode='wt') as target:
            pre.clean_up_conllu(source, target, print_progress=True)


if __name__ == '__main__':

    # Check the number of arguments passed.
    if len(sys.argv) != 3:
        print('Usage: python conllu_cleaner.py <source corpus> <target corpus>')
        sys.exit(1)
    
    source = sys.argv[1]
    target = sys.argv[2]

    if source == target:
        print('Error: target cannot be the same as the source')
    
    clean_up_bz2(source, target)
    pass

# Example: python conllu_cleaner.py 'data/dev-test-set.conllu.bz2' 'data/dev-test-set-clean.conllu.bz2'
# Alternatively: python scripts/conllu_cleaner.py 'data/dev-test-set.conllu.bz2' 'data/dev-test-set-clean.conllu.bz2'
