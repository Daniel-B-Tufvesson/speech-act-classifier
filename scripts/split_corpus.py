"""
This script splits a CoNLL-U file into a training corpus file and a test corpus file.
"""
from context import speechact
import speechact.corpus as corp
import speechact.preprocess as pre

if __name__ == '__main__':
    source_file = 'data/annotated data/dev-set.conllu.bz2'
    source_corpus = corp.Corpus(source_file)

    target_dir = 'data/annotated data'
    test_file = f'{target_dir}/{source_corpus.name}-test.conllu.bz2'
    train_file = f'{target_dir}/{source_corpus.name}-train.conllu.bz2'

    pre.split_train_test(source_corpus, test_file, train_file, 0.8, True)