"""
A script for extracting sub samples of sentences in a CoNNL-U file.
"""

import bz2
import speechact.preprocess as pre

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
    replace_suffix = '500k-clean'
    new_suffix = '100k'
    n_sentences = 100000

    source_dir = 'processed data no-deps'
    target_dir = 'processed data no-deps clean'

    source_files = [
        "familjeliv-adoption-500k-clean.connlu.bz2",
        "familjeliv-allmanna-ekonomi-500k-clean.connlu.bz2",
        "familjeliv-allmanna-familjeliv-500k-clean.connlu.bz2",
        "familjeliv-allmanna-fritid-500k-clean.connlu.bz2",
        "familjeliv-allmanna-husdjur-500k-clean.connlu.bz2",
        "familjeliv-allmanna-hushem-500k-clean.connlu.bz2",
        "familjeliv-allmanna-kropp-500k-clean.connlu.bz2",
        "familjeliv-allmanna-noje-500k-clean.connlu.bz2",
        "familjeliv-allmanna-samhalle-500k-clean.connlu.bz2",
        "familjeliv-allmanna-sandladan-500k-clean.connlu.bz2",
        "familjeliv-anglarum-500k-clean.connlu.bz2",
        "familjeliv-expert-500k-clean.connlu.bz2",
        "familjeliv-foralder-500k-clean.connlu.bz2",
        "familjeliv-gravid-500k-clean.connlu.bz2",
        "familjeliv-kansliga-500k-clean.connlu.bz2"


        # "familjeliv-medlem-allmanna-500k-clean.connlu.bz2",
        # "familjeliv-medlem-foraldrar-500k-clean.connlu.bz2",
        # "familjeliv-medlem-planerarbarn-500k-clean.connlu.bz2",
        # "familjeliv-medlem-vantarbarn-500k-clean.connlu.bz2",
        # "familjeliv-pappagrupp-500k-clean.connlu.bz2",
        # "familjeliv-planerarbarn-500k-clean.connlu.bz2",
        # "familjeliv-sexsamlevnad-500k-clean.connlu.bz2",
        # "familjeliv-svartattfabarn-500k-clean.connlu.bz2", 
        # "flashback-dator-500k-clean.connlu.bz2", 
        # "flashback-droger-500k-clean.connlu.bz2", 
        # "flashback-ekonomi-500k-clean.connlu.bz2", 
        # "flashback-flashback-100k.connlu.bz2", 
        # "flashback-fordon-500k.connlu.bz2", 
        # "flashback-hem-500k.connlu.bz2", 
        # "flashback-politik-500k-clean.connlu.bz2", 
        # "flashback-samhalle-500k-clean.connlu.bz2", 
        # "flashback-sex-500k-clean.connlu.bz2", 
        # "flashback-sport-500k-clean.connlu.bz2", 
        # "flashback-vetenskap-500k-clean.connlu.bz2"
    ]

    for source_file in source_files:
        target_file = source_file.replace(replace_suffix, new_suffix)

        source_file = f'{source_dir}/{source_file}'
        target_file = f'{target_dir}/{target_file}'

        try:
            extract_sub_sample_bz2(source_file, target_file, n_sentences)
        except Exception as e:
            print(f'Exception occurred while extracting sub sample from {source_file}, exception: {e}')