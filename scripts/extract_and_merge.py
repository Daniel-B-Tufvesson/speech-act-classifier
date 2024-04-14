"""
A script for extracting subsamples of sentences from multiple CoNLL-U files and merge
them into a single corpus file. 

Usage: python extract_and_merge.py <source directory> <target corpus> <skip N first>
"""
# Example: python scripts/extract_and_merge.py 'data/for-testing/dir1' 'data/for-testing/dir2/extracted_and_merged.conllu.bz2' 20

from context import speechact
import speechact.preprocess as pre
import bz2
import sys

if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) != 4:
        print('Usage: python extract_and_merge.py <source directory> <target corpus> <skip N first>')
        sys.exit(1)

    source_dir = sys.argv[1]
    target_file = sys.argv[2]
    skip_sentences = int(sys.argv[3])

    source_files = pre.list_files(source_dir, file_extension='.conllu.bz2')

    print(f'Extracting sentences to {target_file} from {len(source_files)} corpora.')

    with bz2.open(target_file, mode='wt') as target:
        for source_file in source_files:
            with bz2.open(source_file, mode='rt') as source:
              print(f'Extracting sentences from {source_file}')
              pre.extract_sub_sample(source, target, -1, skip_sentences, print_progress=True)

    print('Extraction complete')