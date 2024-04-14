"""
A data extraction and cleaning pipeline which converts XML corpora into CoNNL-U corpora suitable for 
the project. 
"""

import speechact.korp as korp
import speechact.preprocess as pre
import speechact.core as sa
import bz2

DIR_RAW_DATA = 'raw data'
DIR_NO_DEPS = 'processed data no-deps'
DIR_NO_DEPS_CLEAN = 'processed data no-deps clean'
DIR_PROCESSED = 'processed data'
DIR_DATA_TO_ANNOTATE = 'data to annotate'

def process(corpus_name: str, genre: str, read_tail=False, parse_pos=True):

    # Print first lines from xml file.
    source_file = f'{DIR_RAW_DATA}/{corpus_name}.xml.bz2'
    pre.print_initial_lines(source_file, 30)

    # Parse from xml to CoNNL-U.
    target_file = f'{DIR_NO_DEPS}/{corpus_name}.connlu.bz2'
    print(f'Parsing xml "{source_file}" to CoNNL-U "{target_file}"')
    korp.Korp_CoNNLU_Converter(genre=genre, read_tail=read_tail).xmlbz2_to_connlubz2(source_file, target_file, 100000)
    pre.print_initial_lines(target_file, 30)

    # Clean up data
    source_file = target_file
    target_file = f'{DIR_NO_DEPS_CLEAN}/{corpus_name}.connlu.bz2'
    print(f'Cleaning up "{source_file}" to "{target_file}"')
    with bz2.open(source_file, mode='rt') as source, bz2.open(target_file, mode='wt') as target:
        pre.clean_up_conllu(source, target, print_progress=True)
    pre.print_initial_lines(target_file, 30)

    # Parse dependency relations.
    if parse_pos:
        source_file = target_file
        target_file = f'{DIR_PROCESSED}/{corpus_name}.connlu.bz2'
        print(f'Parsing dependency relations "{source_file}" to "{target_file}"')
        with bz2.open(source_file, mode='rt') as source, bz2.open(target_file, mode='wt') as target:
            pre.tag_dep_rel(source, target, True)
        pre.print_initial_lines(target_file, 30)


if __name__ == '__main__':
    process('flashback-mat', sa.Genre.INTERNET_FORUM.value, read_tail=True, parse_pos=False)