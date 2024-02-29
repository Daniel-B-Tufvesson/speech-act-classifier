"""
This script extracts the first N sentences from a CoNNL-U corpus and appends them to a text file.
Note that only two values are extracted:
    - sent_id
    - text
The individual tokens or other meta-data are not extracted.

Entries are separated with an empty line.
"""

import bz2
from typing import TextIO
import os

class Sentence:

    def __init__(self, text: str, id: int):
        self.text = text
        self.id = id


def extract_sentences(source_files: list[str], target_dir: str, sent_per_source: int, sent_per_target: int):
    print('Extracting sentences to annotate.')

# def extract_n_sentences_bz2(source_file: str, target_file: str, sent_ids: set[str], n_sentences):
#     """
#     Exract the first N sentences from coonly compressed corpus, and appending them to 
#     text file.
#     """

#     with bz2.open(source_file, mode='rt') as source:
#         with open(target_file, mode='at') as target:
#             extract_n_sentences(source, target, sent_ids, n_sentences)


# def extract_n_sentences(source: TextIO, target: TextIO, sent_ids: set[str], n_sentences):
#     """
#     Extract and append the first N sentences from the source to the target.
#     """
#     print(f'Extracting {n_sentences} from corpus.')

#     currentID = None
#     currentText = None
#     sentence_count = 0

#     for line in source:
#         if line == '\n':
            
#             # Write ID and sentence to target.
#             if currentID and currentText:

#                 if currentID in sent_ids:
#                     print(f'WARNING: Duplicate ID found: {currentID}, skipping sentence')
#                     currentID = None
#                     currentText = None
#                     continue

#                 sent_ids.add(currentID)               

#                 target.write(f'sent_id = {currentID}\n')
#                 target.write(f'text = {currentText}\n')
#                 target.write('\n')

#                 currentID = None
#                 currentText = None
#                 sentence_count += 1

#                 # Stop if reached max sentences.
#                 if sentence_count == n_sentences:
#                     break

#         else:
#             line = line.strip()
            
#             if line.startswith('# text ='):
#                 currentText = line.removeprefix('# text = ')

#             elif line.startswith('# sent_id ='):
#                 currentID = line.removeprefix('# sent_id = ')

#     print(f'Done! Extracted {sentence_count}/{n_sentences} from corpus.')


if __name__ == '__main__':

    # WARNING: do not change any of the parameters here after the manual annotation work has
    # started. This is because the sentence IDs are not unique across corpora, so by including
    # some sentences we risk excluding others (because their IDs are identical). 
    
    sent_ids = set()
    n_sentences = 1000
    target_file = 'data to annotate/data-to-annotate-v1.txt'

    if os.path.isfile(target_file):
        os.remove(target_file)  # Start with a fresh file.

   
    source_files = [
        'processed data/familjeliv-allmanna-familjeliv-100k.connlu.bz2',
        'processed data/attasidor-99k.connlu.bz2',
        'processed data/familjeliv-expert-100k.connlu.bz2',
        'processed data/suc3-100k.connlu.bz2',
        'processed data/gp2013-100k.connlu.bz2',
        'processed data/bloggmix2017-100k.connlu.bz2',
        'processed data/familjeliv-adoption-100k.connlu.bz2',
        'processed data/romi-100k.connlu.bz2'
    ]

    for source_file in source_files:
        extract_n_sentences_bz2(source_file, target_file, sent_ids, n_sentences)


