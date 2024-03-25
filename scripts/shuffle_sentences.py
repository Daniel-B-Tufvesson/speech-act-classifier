
from context import speechact
import speechact.preprocess as pre

if __name__ == '__main__':
    print('Shuffling sentences...')
    
    source_file = 'data/auto-annotated data/no duplicates.conllu.bz2'
    target_file = 'data/auto-annotated data/shuffled.conllu.bz2'
    pre.shuffle_sentences(source_file, target_file)

    print('Shuffling complete')