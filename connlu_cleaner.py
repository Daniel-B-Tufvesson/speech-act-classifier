"""
Cleans up CoNLL-U files by removing sentences that are improperly formatted. A sentence is
incorrectly formatted if it cannot be loaded by Stanza's CoNNL-U parser.
"""

import bz2
from typing import TextIO
from stanza.utils.conll import CoNLL

def clean_up_bz2(source_file: str, target_file: str):
    """
    Clean a bz2 compressed connlu corpus. The cleaned up version is saved to the target
    file as a compressed connlu corpus as well.
    """
    print('clean_up_bz2')

    with bz2.open(source_file, mode='rt') as source:
        with bz2.open(target_file, mode='wt') as target:
            clean_up(source, target)


def clean_up(source: TextIO, target: TextIO):
    """
    Clean up the input connlu corpus and save it to the target. 
    """
    print('Clean up corpus')

    lines = []
    error_count = 0
    sentence_count = 0
    for line in source:
        if line == '\n':

            # Skip line if there are multiple empty lines.
            if len(lines) == 0:
                continue

            sentence_count += 1

            # Try parsing sentence.
            try:
                CoNLL.load_conll(lines)

                # Sentence is ok. Write to file.
                target.writelines(lines)
                target.write('\n')

            except Exception as e:
                error_count += 1
                print('Failed to parse sentence: ', e)

            # Reset accumulated lines.
            lines = []
        else :
            lines.append(line)
        
    print(f'Cleaned up {sentence_count} sentences. Found {error_count}/{sentence_count} errors.')


if __name__ == '__main__':
    #clean_up_bz2('processed data no-deps/attasidor-100k.connlu.bz2', 'processed data no-deps/attasidor-100k-clean.connlu.bz2')
    clean_up_bz2('processed data no-deps/gp2013-100k.connlu.bz2', 'processed data no-deps/gp2013-100k-clean.connlu.bz2')
    pass