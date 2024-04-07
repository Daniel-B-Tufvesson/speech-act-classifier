"""
Remove sentences from a corpus that also occur in another corpus.
"""

from context import speechact
import speechact.preprocess as pre

if __name__ == '__main__':
    remove_from_file = 'data/auto-annotated data/speech-acts.conllu.bz2'
    check_against_file = 'data/annotated data/test-set.conllu.bz2'
    target_file = 'data/auto-annotated data/speech-acts-no-dup.conllu.bz2'
    pre.remove_duplicates_from_other(remove_from_file, check_against_file, 
                                     target_file, print_progress=True)