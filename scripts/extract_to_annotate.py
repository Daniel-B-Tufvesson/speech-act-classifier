"""
This script extracts the first N sentences from each CoNLL-U corpus, scrambles them, and distributes
them into new smaller corpus files. These smaller files contain only sent_id and text of the sentences.
The individual tokens or other meta-data are not extracted. Entries are separated with an empty line.
The new files are uncompressed as a regular txt format.

These files are used for manual annotation of the sentences.

Usage: python extract_to_annotate.py <source directory> <target directory> <N sentences per source> <N sentences per target>
"""

# Example: python scripts/extract_to_annotate.py 'data/for-testing/dir1' 'data/for-testing/dir2' 50 10

from context import speechact
import speechact.annotate as annot
import speechact.preprocess as pre
import sys

if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) != 5:
        print('Usage: python extract_to_annotate.py <source directory> <target directory> <N sentences per source> <N sentences per target>')
        sys.exit(1)

    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    n_sentences_source = int(sys.argv[3])
    n_sentences_target = int(sys.argv[4])

    source_files = pre.list_files(source_dir, file_extension='conllu.bz2')

    # Extract 1000 sentences from each corpus, to files with 50 sentences each.
    annot.extract_sentences(source_files, target_dir, n_sentences_source, 
                            n_sentences_target, print_progress=True)


