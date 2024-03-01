"""
A module for extracting sentences from CoNNL-U corpora to annotation files. 
"""

import bz2
import os
import random


UNANNOTATED_EXT = '💬'  # speech bubble emoji.
"""The file extension for unannotated sentence files."""

ANNOTATED_EXT = '✏️'  # pencil emoji
"""The file extension for annotated sentence files."""


class Sentence:

    def __init__(self, text: str, id: str):
        self.text = text
        self.id = id


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


def extract_sentences(source_files: list[str], target_dir: str, sent_per_source: int, 
                      sent_per_target: int, print_progress=False):
    """
    Extract the initial sentences from each corpora, scramble them, and distribute them into new 
    smaller corpus files. These smaller files contain only sent_id and text of the sentences. The 
    individual tokens or other meta-data are not extracted. Entries are separated with an empty line.
    The new files are uncompressed as regular txt files.
    """
    if print_progress: print('Extracting sentences to annotate.')

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
    target_file = f'{target_dir}/sents_{target_count}.{UNANNOTATED_EXT}'
    for sentence in sentences:

        # Create new 
        if sentence_count != 0 and sentence_count % sent_per_target == 0:
            target_file = f'{target_dir}/sents_{target_count}.{UNANNOTATED_EXT}'

            # Write lines to file.
            with open(target_file, mode='wt') as target:
                target.writelines(lines_to_write)
                lines_to_write = []

            target_count += 1

        sentence_count += 1
        lines_to_write.append(sentence.id) # We assume they end with newlines.
        lines_to_write.append(sentence.text)
        lines_to_write.append('\n')

    if print_progress: print(f'Extraction complete. Extracted {len(sentences)} sentences.')