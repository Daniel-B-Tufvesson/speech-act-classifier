"""
This script takes a CoNNL-U corpus file and tags each sentence with its sentiment.
"""

from context import speechact
import speechact.preprocess as pre
import speechact.corpus as corp
import bz2

def tag_corpus(bz2_source_file: str, target_file: str):
    print(f'Tagging sentences from "{bz2_source_file}" to "{target_file}".')

    corpus = corp.Corpus(bz2_source_file)

    with bz2.open(target_file, mode='wt') as target:
        pre.tag_sentiment(corpus, target, print_progress=True)

if __name__ == '__main__':
    source_file = 'data/auto-annotated data/shuffled.conllu.bz2'
    target_file = 'data/auto-annotated data/sentiment.conllu.bz2'

    tag_corpus(source_file, target_file)