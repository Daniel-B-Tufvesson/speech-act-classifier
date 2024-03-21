"""
This script upsamples the corpus so that there is an equal amount of sentences 
for each speech act label. The upsampled corpus is written to a new file.
"""

from context import speechact
import speechact.corpus as corp
import speechact.preprocess as pre
import os
import bz2


if __name__ == '__main__':
    source_file = 'data/annotated data/dev-set-sentiment-test.conllu.bz2'
    source_corpus = corp.Corpus(source_file)


    target_dir = os.path.dirname(source_file)
    target_file = os.path.join(target_dir, f'{source_corpus.name}-upsampled.conllu.bz2')

    print(f'Upsampling "{source_file}" to "{target_file}.')

    with bz2.open(target_file, mode='wt') as target:
        pre.upsample(source_corpus, target)