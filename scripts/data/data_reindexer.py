"""
This script assigns a new sent_id to each sentence across a set of several corpora. 
"""

import os
from speechact.corpus import Corpus
import bz2
import speechact.data as dat

def reindex(corpora: list[Corpus], target_dir: str, start_id=1):
    """
    Reindex each sentence in each corpus, and write them to new corpus files in the target
    directory.
    """
    print(f'Reindexing sentences from {len(corpora)} corpora to "{target_dir}"')

    assert os.path.isdir(target_dir), f'Directory does not exists: {target_dir}'

    # Reindex each sentence in each corpus, and write them to new files.
    sent_count = 0
    corp_count = 0
    sent_id = start_id
    for corpus in corpora:
        print(f'Reindexing corpus: "{corpus.name}"')

        target_file = f'{target_dir}/{corpus.name}.connlu.bz2'
        with bz2.open(target_file, mode='wt') as target:

            for sentence in corpus.sentences():

                # Update the ID.
                x_sent_id = sentence.get_meta_data('sent_id')
                sentence.set_meta_data('x_sent_id', x_sent_id)
                sentence.set_meta_data('sent_id', sent_id)

                # Write sentence to target file.
                target.writelines(sentence.sentence_lines)
                target.write('\n')

                sent_id += 1
                sent_count += 1

                # Print progress.
                if sent_count % 5000 == 0:
                    print(f'Reindexed {sent_count} sentences...')

        corp_count += 1

        print('Reindexing for corpus complete.')
        print('Printing first 30 lines:')
        dat.print_initial_lines(target_file, 30)
        print(f'Reindexed {corp_count}/{len(corpora)} corpora...')
        
    
    print(f'Reindexing complete. Assigned new ID to {sent_count} sentences.')


if __name__ == '__main__':
    source_files = dat.lines('processed data no-deps clean/data files.txt')
    target_dir = 'reindexed data'

    corpora = [Corpus(file, file.split('/')[-1].removesuffix('.connlu.bz2').removesuffix('-100k').removesuffix('-500k')) for file in source_files]

    reindex(corpora, target_dir)