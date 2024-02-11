"""
Codes used for reading KORP corpora.
"""

import bz2
from typing import Generator
import xml.etree.ElementTree as ET
import speech_act_classifier as sac
import uuid
import stanza

def test_read(file_name: str):
    """Print the first few lines of a compressed file."""
    with bz2.open(file_name, mode='rt') as source:

        i = 0
        for line in source:
            print(line)
            i += 1

            if i > 60:
                break


def from_xml_to_connlu_familjeliv_adoption(xml_bz2_filename: str, output_filename: str):
    """
    Convert an xml-corpus to CoNNL-U.
    """

    print('from_xml_to_connlu_familjeliv_adoption')

    # Write to the output file.
    with open(output_filename, mode='w') as target_file:
        n = 0

        # Read every <thread> block.
        for xml_block in xml_blocks(xml_bz2_filename, 'thread'):

            root = ET.fromstring(xml_block)
            xml_text = root.find('text')

            assert xml_text is not None, '<text> not found in xml_block'

            # Read and format all sentences
            for sentence in root.iter('sentence'):

                # Create unique sentence ID.
                sent_id = str(uuid.uuid4())

                # Extract sentence specific meta-data.
                sentence_text = xml_tokens_to_text(sentence)
                date = xml_text.attrib['date']
                url = xml_text.attrib['url']
                genre = sac.Genre.INTERNET_FORUM.value

                # Write the sentence meta-data as CoNLL-U.
                target_file.write(f'# sent_id = {sent_id}\n')
                target_file.write(f'# text = {sentence_text}\n')
                target_file.write(f'# date = {date}\n')
                target_file.write(f'# url = {url}\n')
                target_file.write(f'# genre = {genre}\n')

                # Read and format all tokens in sentence.
                token_index = 1
                for token in sentence.iter('token'):

                    assert token.text != None, 'token must no be empty'
                    assert token.attrib['pos'] != None, 'pos attribute must be set'
                    # Todo: check if _tail has other values than \s and undefined.
                    
                    # Extract all word fields from xml.
                    form = token.text
                    lemma = token.attrib['lemma'].strip('|')
                    if lemma == '':
                        lemma = '_'
                    upos = sac.suc_to_upos(token.attrib['pos'])
                    xpos = token.attrib['pos']
                    feats = token.attrib['ufeats'].strip('|')
                    if feats == '':
                        feats = '_'
                    head = token.attrib.get('dephead', 0)  # 0 for root.
                    deprel = token.attrib['deprel']
                    deps = '_'
                    misc = '_' if '_tail' in token.attrib else 'SpaceAfter=No' # We assume the presence of _tail is enough.

                    # Write the fields as a single line.
                    word_line = f'{form}\t{lemma}\t{upos}\t{xpos}\t{feats}\t{head}\t{deprel}\t{deps}\t{misc}\n'
                    target_file.write(word_line)

                    token_index += 1

                # Add empty line at end of sentence.
                target_file.write('\n')

            n += 1
            if n == 1000:
                break
        
        print('NUMBER OF BLOCKS: ', n)


def from_xml_to_dat1_familjeliv_adoption(xml_bz2_filename: str, output_filename: str):
    """
    Convert an xml-corpus to dat1 which is a much more compact format with only the data we need.

    The dat1 format is similar conllx. 

    The dat1 format: 
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
    
    with open(output_filename, mode='w') as target_file:
        n = 0
        for xml_block in xml_blocks(xml_bz2_filename, 'thread'):

            root = ET.fromstring(xml_block)

            # Read and format all sentences
            for sentence in root.iter('sentence'):

                # Read and format all tokens in sentence.
                token_index = 1
                for token in sentence.iter('token'):

                    assert token.text != None, 'token must no be empty'
                    assert token.attrib['pos'] != None, 'pos attribute must be set'

                    dat1_token = to_token_dat1_string(token_index, token.text, token.attrib['pos'])
                    print(dat1_token)
                    target_file.write(dat1_token)
                    target_file.write('\n')
                    token_index += 1

                # Add empty line at end of sentence.
                target_file.write('\n')

            n += 1
            if n == 100:
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


def xml_tokens_to_text(sentence : ET.Element) -> str :
    sentence_text = ''

    # Append all words as a single string.
    for token in sentence.iter('token'):
        assert token.text != None, 'token must no be empty'

        sentence_text += token.text

        # Append whitespace.
        if '_tail' in token.attrib:
            sentence_text += ' '
    
    return sentence_text


def to_token_dat1_string(token_index: int, token_text: str, pos: str) -> str:
    """
    Format the token data to a dat1 string.
    """
    return f'{token_index}\t{token_text}\t{pos}'


def from_xml_to_unanot_sent_familjeliv_adoption():
    """
    Parse the xml file and output it as a unanot_sent file of unannotated sentences.
    """
    pass

#from_xml_to_unanot_sent_familjeliv_adoption('raw data/familjeliv-adoption.xml.bz2', 
#                                            'processed data/familjeliv-adoption.dat1')

from_xml_to_connlu_familjeliv_adoption('raw data/familjeliv-adoption.xml.bz2', 'processed data/familjeliv-adoption.connlu')