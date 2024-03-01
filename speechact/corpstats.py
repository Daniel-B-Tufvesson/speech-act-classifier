"""
Code for printing corpus statistics to files.
"""

from . import corpus
from speechact.corpus import Corpus
from typing import TextIO

def write_sentence_counts(corpora: list[Corpus], target: TextIO):
    print('Writing sentences counts in corpora to target...')

    for corpus in corpora:
        count = corpus.sentence_count

        target.write(corpus.name)
        target.write(f' {count}\n')
    
    print('Writing complete.')


# if __name__ == '__main__':
#     data_dir = 'reindexed data'
#     corpora = corpus.load_corpora_from_data_file(f'{data_dir}/data files.txt')

#     with open(f'{data_dir}/sentence counts.txt') as target:
#         write_sentence_counts(corpora, target)