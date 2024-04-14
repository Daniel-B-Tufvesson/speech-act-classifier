"""
Remove sentences from a corpus that also occur in another corpus.

'Usage: python remove_duplicates_from.py <remove from corpus> <check agains corpus> <write to corpus>'
"""
# Example: python scripts/remove_duplicates_from.py 'data/for-testing/dir1/dev-set.conllu.bz2' 'data/for-testing/dir1/test-set.conllu.bz2' 'data/for-testing/dir2/dev-set-no-dups.conllu.bz2'

from context import speechact
import speechact.preprocess as pre
import sys

if __name__ == '__main__':
    # Check the number of arguments passed
    if len(sys.argv) != 4:
        print('Usage: python remove_duplicates_from.py <remove from corpus> <check agains corpus> <write to corpus>')
        sys.exit(1)

    remove_from_file = sys.argv[1]
    check_against_file = sys.argv[2]
    target_file = sys.argv[3]

    pre.remove_duplicates_from_other(remove_from_file, 
                                     check_against_file, 
                                     target_file, 
                                     print_progress=True)