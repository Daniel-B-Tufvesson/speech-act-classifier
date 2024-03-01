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
import random
from . import file_inspector as fi
import data_loading as dat

class Sentence:

    def __init__(self, text: str, id: str):
        self.text = text
        self.id = id


def extract_sentences(source_files: list[str], target_dir: str, sent_per_source: int, sent_per_target: int):
    print('Extracting sentences to annotate.')

    # Make sure that the source files exist.
    for source_file in source_files:
        assert os.path.isfile(source_file), f'File does not exist: {source_file}'

    assert os.path.isdir(target_dir), f'Target directory does not exist: {target_dir}'

    # Keep track sentences IDs to prevent duplicates.
    sent_ids = set()

    # Read the N first sentences from each source file.
    sentences = []  # type: list[Sentence]
    for source_file in source_files:
        sentences += read_n_sentences(source_file, sent_per_source, sent_ids)
    
    # Shuffle them.
    random.seed = 42
    random.shuffle(sentences)

    # Write them to new target files.
    sentence_count = 0
    target_count = 1
    lines_to_write = []
    target_file = f'{target_dir}/sents_{target_count}.💬'
    for sentence in sentences:
        
        # Create new 
        if sentence_count != 0 and sentence_count % sent_per_target == 0:
            target_count += 1
            target_file = f'{target_dir}/sents_{target_count}.💬'

            # Write lines to file.
            with open(target_file, mode='wt') as target:
                target.writelines(lines_to_write)
                lines_to_write = []

            break # Temp break.

        sentence_count += 1
        lines_to_write.append(sentence.id) # We assume they end with newlines.
        lines_to_write.append(sentence.text)
        lines_to_write.append('\n')
    
    print(f'Extraction complete. Extracted {len(sentences)} sentences.')



        
def read_n_sentences(source_file: str, n_sentences: int, sent_ids: set[str]) -> list[Sentence]:
    """
    Read the first N sentences from the CoNLL-U corpus.
    """
    sentences = []
    with bz2.open(source_file, mode='rt') as source:
        sent_text = None
        sent_id = None

        for line in source:
            if line == '\n':

                if sent_text and sent_id:

                    # Prevent sentence with taken ID.
                    if sent_id in sent_ids:
                        print(f'Skipping sentence {sent_id} "{sent_text}" because its ID is taken.')
                        sent_id = None
                        sent_text = None
                        continue
                
                    # Store the sentence.
                    sent_ids.add(sent_id)
                    sentence = Sentence(sent_text, sent_id)
                    sentences.append(sentence)

                    # Stop if max sentences is reached.
                    if len(sentences) == n_sentences:
                        break
                
            else:
                if line.startswith('# text ='):
                    sent_text = line

                elif line.startswith('# sent_id ='):
                    sent_id = line
        
    return sentences
                

if __name__ == '__main__':

    source_files = dat.lines('processed data no-deps clean/data files.txt')
    #source_files = [dat.absolute_path(file) for file in source_files]
    target_dir = 'data to annotate'

    # Extract 1000 sentences from each corpus, to files with 50 sentences each.
    extract_sentences(source_files, target_dir, sent_per_source=1000, sent_per_target=50)






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


# if __name__ == '__main__':

#     # WARNING: do not change any of the parameters here after the manual annotation work has
#     # started. This is because the sentence IDs are not unique across corpora, so by including
#     # some sentences we risk excluding others (because their IDs are identical). 
    
#     sent_ids = set()
#     n_sentences = 1000
#     target_file = 'data to annotate/data-to-annotate-v1.txt'

#     if os.path.isfile(target_file):
#         os.remove(target_file)  # Start with a fresh file.

   
#     source_files = [
#         'processed data/familjeliv-allmanna-familjeliv-100k.connlu.bz2',
#         'processed data/attasidor-99k.connlu.bz2',
#         'processed data/familjeliv-expert-100k.connlu.bz2',
#         'processed data/suc3-100k.connlu.bz2',
#         'processed data/gp2013-100k.connlu.bz2',
#         'processed data/bloggmix2017-100k.connlu.bz2',
#         'processed data/familjeliv-adoption-100k.connlu.bz2',
#         'processed data/romi-100k.connlu.bz2'
#     ]

#     for source_file in source_files:
#         extract_n_sentences_bz2(source_file, target_file, sent_ids, n_sentences)


