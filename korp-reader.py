"""
Codes used for reading KORP corpora.
"""

import bz2
from typing import Generator
import xml.etree.ElementTree as ET

def test_read(file_name: str):
    """Print the first few lines of a compressed file."""
    with bz2.open(file_name, mode='rt') as source:

        i = 0
        for line in source:
            print(line)
            i += 1

            if i > 60:
                break

#test_read('Data/familjeliv-adoption.xml.bz2')
            

def from_xml_to_compact_familjeliv_adoption(xml_bz2_filename: str, output_filename: str):
    """
    Convert an xml-corpus to a much more compact format with only the data we need.

    The new format is similar conllx. 

    The new format: 
    - Each row contains one token.
    - A token consists of an in-sentence ID, a word, and a POS tag. These are separated by a TAB escape character.
    - The tokens are grouped together to form sentences. 
    - Sentences are separated with empty lines.
    """

    """
    METHOD

    The structure of the corpus is as follows:
    <corpus>
        <forum>
            <thread>
                <text>
                    <paragraph>
                        <sentence>
                            <token>...</token>
                            <token>...</token>
                            <token>...</token>
                        </sentence>
                    </paragraph>
                </text>
            </hread>
        </forum>
    </corpus>

    Because the corpus is huge, we want to parse it in chunks. The <thread> block is a recurring
    encapsulated structure, which we can parse one at a time. 
    """

    print('from_xml_to_compact_familjeliv_adoption')
    
    n = 0
    for xml_block in xml_blocks(xml_bz2_filename, 'thread'):

        root = ET.fromstring(xml_block)
        for sentence in root.iter('sentence'):

            for token in sentence.iter('token'):
                print(token.text, token.attrib['pos'])


        n += 1
        if n == 1:
            break
    
    print('NUMBER OF BLOCKS: ', n)



            


def xml_blocks(xml_bz2_filename: str, xml_tag: str) -> Generator[str, None, None]:
    """
    Generator which yeilds each xml-block with the given tag. 
    """

    # Whether the current line is inside a target xml block.
    is_inside_block = False

    # The currently accumulated xml-block.
    xml_block = ''

    # Used for identifying start and end of block.
    startTag = '<' + xml_tag
    endTag = '</' + xml_tag

    with bz2.open(xml_bz2_filename, mode='rt') as source:

        for xml_line in source:
            xml_line = xml_line.strip()

            # Accumulate new block if start tag.
            if xml_line.startswith(startTag):

                assert not is_inside_block, 'cannot start a block inside another block'

                is_inside_block = True
                xml_block += xml_line
            
            # Yield accumulated block if end tag.
            elif xml_line.startswith(endTag):

                assert is_inside_block, 'must be inside a block to end it'

                is_inside_block = False
                xml_block += xml_line
                yield xml_block

                # Reset the accumulated block.
                xml_block = ''
            
            # Accumulate line if inside block.
            elif is_inside_block:
                xml_block += xml_line


from_xml_to_compact_familjeliv_adoption('Data/familjeliv-adoption.xml.bz2', '')