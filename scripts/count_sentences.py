"""
This script counts the sentences in each corpora and writes them to a file.
"""
from context import speechact
import speechact.corpus as corp
import speechact.corpstats as cs

if __name__ == '__main__':
    data_dir = 'data/reindexed data'
    corpora = corp.load_corpora_from_data_file(f'{data_dir}/data files.txt')

    with open(f'{data_dir}/sentence counts.txt', mode='wt') as target:
        cs.write_sentence_counts(corpora, target)