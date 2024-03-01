"""
This script assigns a new sent_id to each sentence across a set of several corpora. 
"""

from speechact.corpus import Corpus
import speechact.preprocess as dat
from speechact.preprocess import reindex

if __name__ == '__main__':
    source_files = dat.lines('processed data no-deps clean/data files.txt')
    target_dir = 'reindexed data'

    corpora = [Corpus(file, file.split('/')[-1].removesuffix('.connlu.bz2').removesuffix('-100k').removesuffix('-500k')) for file in source_files]

    reindex(corpora, target_dir)