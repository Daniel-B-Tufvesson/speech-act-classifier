"""
A script for extracting subsamples of sentences from several CoNLL-U files.

Usage: python subsample_corpora.py <target corpus/directory> <target directory> <number of sentences>
"""
# Example: python scripts/subsample_corpora.py 'data/for-testing/dir1' 'data/for-testing/dir2' 10

from context import speechact
import speechact.preprocess as pre
import sys
import bz2
import os


def extract_sub_sample_bz2(source_file: str, target_file: str, n_sentences: int):
    """
    Extract a sub sample of sentences from the CoNNL-U source file and write them to the target file.
    These files are compressed with bz2.
    """
    print(f'Extracting sub sample of {n_sentences} sentences from "{source_file}" to "{target_file}"')
    with bz2.open(source_file, mode='rt') as source:
        with bz2.open(target_file, mode='wt') as target:
            pre.extract_sub_sample(source, target, n_sentences, print_progress=True)


if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) != 4:
        print('Usage: python subsample_corpora.py <target corpus/directory> <target directory> <number of sentences>')
        sys.exit(1)

    source = sys.argv[1]
    target = sys.argv[2]
    n_sentences = int(sys.argv[3])

    # Extract a subsample from a single corpus.
    if os.path.isfile(source):
        name = os.path.basename(source)
        target_file = os.path.join(target, name)
        extract_sub_sample_bz2(source, target_file, n_sentences)

    # Extract subsamples from several corpora in a directory.
    elif os.path.isdir(source):
        source_files = pre.list_files(source, file_extension='conllu.bz2')

        for source_file in source_files:
            name = os.path.basename(source_file)
            target_file = os.path.join(target, name)

            try:
                extract_sub_sample_bz2(source_file, target_file, n_sentences)
            except Exception as e:
                print(f'Exception occurred while extracting sub sample from {source_file}, exception: {e}')
        
