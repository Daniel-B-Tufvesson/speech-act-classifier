"""
Codes used for reading KORP corpora.
"""

import bz2

def test_read(file_name: str):
    """Print the first few lines of a compressed file."""
    with bz2.open(file_name, mode='r') as source:

        i = 0
        for line in source:
            print(line)
            i += 1

            if i > 60:
                break

#test_read('Data/familjeliv-adoption.xml.bz2')
            

def from_xml_to_compact(xml_filename: str, output_filename: str):
    """
    Convert an xml-corpus to a much more compact format with only the data we need.

    The new format is similar conllx. 

    The new format: 
    - Each row contains one token.
    - A token consists of an in-sentence ID, a word, and a POS tag. These are separated by a TAB escape character.
    - The tokens are grouped together to form sentences. 
    - Sentences are separated with empty lines.
    """
    pass