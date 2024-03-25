"""
A script for extracting sub samples of sentences from multiple CoNLL-U files and merge
them into a single corpus file. 
"""

from context import speechact
import speechact.preprocess as pre
import bz2

if __name__ == '__main__':

    skip_sentences = 1000  # Skip the first 1000 that are part of the test data.
    source_files = pre.lines('data/tagged data/data files.txt')
    target = 'data/auto-annotated data/extracted-sentences.conllu.bz2'

    print(f'Extracting sentences to {target} from {len(source_files)} corpora.')

    with bz2.open(target, mode='wt') as target:
        for source_file in source_files:
            with bz2.open(source_file, mode='rt') as source:
              print(f'Extracting sentences from {source_file}')
              pre.extract_sub_sample(source, target, -1, skip_sentences, print_progress=True)

    print('Extraction complete')