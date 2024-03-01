"""
Cleans up CoNLL-U files by removing sentences that are improperly formatted. A sentence is
incorrectly formatted if it cannot be loaded by Stanza's CoNNL-U parser.
"""

import bz2
import speechact.preprocess as pre

def clean_up_bz2(source_file: str, target_file: str):
    """
    Clean a bz2 compressed connlu corpus. The cleaned up version is saved to the target
    file as a compressed connlu corpus as well.
    """
    print('clean_up_bz2')

    with bz2.open(source_file, mode='rt') as source:
        with bz2.open(target_file, mode='wt') as target:
            pre.clean_up_connlu(source, target, print_progress=True)


if __name__ == '__main__':
    #clean_up_bz2('processed data no-deps/attasidor-100k.connlu.bz2', 'processed data no-deps/attasidor-100k-clean.connlu.bz2')
    clean_up_bz2('processed data no-deps/gp2013-100k.connlu.bz2', 'processed data no-deps/gp2013-100k-clean.connlu.bz2')
    pass