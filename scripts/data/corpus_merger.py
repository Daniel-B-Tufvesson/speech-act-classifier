"""
A script which merges several corpus files into a single file. All duplicate sentences will be 
removed (i.e. sentences that match exactly). The sentences will also recieve a new sent_id which
is an incremented integer. The original sent_id is saved as x_sent_id. The name of the corpus is 
also saved for each sentence.
"""

import bz2
from ...speechact import data as fi
from speechact.corpus import Corpus


def merge_corpora(corpora: list[Corpus], target_file: str, start_id=1):
    """
    Merge the corpora files in to a single file.
    """
    print(f'Merging {len(corpora)} corpora to {target_file}.')

    sent_id = start_id
    sent_count = 0
    with bz2.open(target_file, mode='wt') as target:

        for corpus in corpora:
            for sentence in corpus.sentences():

                # Update sentence meta data.
                x_sent_id = sentence.get_meta_data('sent_id')
                sentence.set_meta_data('x_sent_id', x_sent_id)
                sentence.set_meta_data('sent_id', sent_id)
                sentence.set_meta_data('corpus', corpus.name)

                # Write sentence to target.
                target.writelines(sentence.sentence_lines)
                target.write('\n')

                sent_id += 1
                sent_count += 1

                if sent_count % 2000 == 0:
                    print(f'Merged {sent_count} sentences...')

            

    print(f'Merging complete. ')


if __name__ == '__main__':
    corpora = [
        Corpus('processed data no-deps clean/familjeliv-adoption-100k.connlu.bz2', 'familjeliv-adoption'),
        Corpus('processed data no-deps clean/familjeliv-allmanna-ekonomi-100k.connlu.bz2', 'familjeliv-allmanna-ekonomi')
    ]

    target_file = 'merge corpora test.connlu.bz2'
    merge_corpora(corpora, target_file)
    fi.print_initial_lines(target_file)