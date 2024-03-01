"""
This script extracts the first N sentences from each CoNNL-U corpus, scrambles them, and distributes
them into new smaller corpus files. These smaller files contain only sent_id and text of the sentences.
The individual tokens or other meta-data are not extracted. Entries are separated with an empty line.
The new files are uncompressed as a regular txt format.

These files are used for manual annotation of the sentences.
"""

from speechact.annotate import extract_sentences
import speechact.preprocess as dat

if __name__ == '__main__':

    source_files = dat.lines('processed data no-deps clean/data files.txt')
    target_dir = 'data to annotate'

    # Extract 1000 sentences from each corpus, to files with 50 sentences each.
    extract_sentences(source_files, target_dir, sent_per_source=1000, sent_per_target=50, print_progress=True)

