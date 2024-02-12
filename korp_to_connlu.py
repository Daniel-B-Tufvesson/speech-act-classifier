"""
This code converts xml corpora from Språkbanken to the CoNNL-U format. The linquistic 
data is also converted to Universal Dependencies formalism. This involves:
- Converting the SUC POS-tags to UPOS-tags.
- Re-parsing the dependency trees.
"""

from typing import TextIO
from typing import Generator
from typing import Any
import stanza
from stanza.utils.conll import CoNLL
import xml.etree.ElementTree as ET
import speech_act_classifier as sac
import bz2

SentenceObject = list[dict[str, Any]]
SentenceComments = list[str]

def xml_to_connlu(xml_corpus: TextIO, connlu_target: TextIO):
    """
    Convert the Språkbanken xml corpus to a CoNLL-U file.
    """
    
    # Initialize the stanza pipeline for dependency parsing.
    nlp = stanza.Pipeline(lang='sv', processors='depparse', depparse_pretagged=True)

    doc = xml_to_doc(xml_corpus)

    # Todo: parse dependencies.
    doc = nlp(doc)

    CoNLL.write_doc2conll(doc, connlu_target)


def xml_to_doc(xml_corpus : TextIO) -> stanza.Document:
    """
    Convert the Språkbanken xml corpus to a stanza.Document.
    """
    
    sentence_objects = []  # type: list[SentenceObject]
    sentence_comments = []  # type: list[SentenceComments]
    for xml_sentence, xml_text in xml_sentences(xml_corpus):
        sentence_objects.append(to_sentence_object(xml_sentence))
        sentence_comments.append(to_sentence_comments(xml_sentence, xml_text))

        if len(sentence_objects) == 10:
            break
    
    return stanza.Document(
        sentences=sentence_objects,
        comments=sentence_comments
    )

# todo: batch the document reading.


def xml_sentences(xml_corpus: TextIO) -> Generator[tuple[ET.Element, ET.Element], None, None]:
    """
    Generator which yeilds each <sentence> and their corresponding <text> as a 2-tuple of ET.Elements. 
    """
    
    # Whether the current line is inside a target xml block.
    is_inside_block = False

    # The currently accumulated xml-block.
    xml_block = ''

    # Used for identifying start and end of block.
    startTag = '<text'
    endTag = '</text'

    for xml_line in xml_corpus:
        xml_line = xml_line.strip()
        print(xml_line)

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

            xml_text = ET.fromstring(xml_block)
            for xml_sentence in xml_text.iter('sentence'):
                yield xml_sentence, xml_text

            # Reset the accumulated block.
            xml_block = ''
        
        # Accumulate line if inside block.
        elif is_inside_block:
            xml_block += xml_line
        

def to_sentence_object(xml_sentence: ET.Element) -> SentenceObject:
    """
    Extract the tokens and their data as CoNLL-U tokens in a dictionary format.
    """
    sentence = SentenceObject()
    token_index = 1
    for xml_token in xml_sentence.iterfind('token'):
        token = {}
        token['id'] = token_index
        token['text'] = xml_token.text
        token['upos'] = sac.suc_to_upos(xml_token.attrib['pos'])
        token['xpos'] = xml_token.attrib['pos']

        # Ignore dependencies.
        #token['head'] = xml_token.get('dephead', 0)  # 0 for root.
        #token['deprel'] = xml_token.attrib['deprel']


        # Parse lemma if available.
        if 'lemma' in xml_token.attrib:
            lemma = xml_token.attrib['lemma'].strip('|')
            if lemma != '':
                token['lemma'] = lemma

        # Parse feats if available.
        if 'ufeats' in xml_token.attrib:
            feats = xml_token.attrib['ufeats'].strip('|')
            if feats != '':
                token['feats'] = feats

        # Parse tail.
        tail = xml_token.attrib.get('_tail', None)
        if tail is None:
            token['misc'] = 'SpaceAfter=No'


        sentence.append(token)
        token_index += 1
    
    return sentence


def to_sentence_comments(xml_sentence: ET.Element, xml_text: ET.Element) -> SentenceComments:
    """
    Extract the relevant sentence meta-data as CoNLL-U sentence comments.
    """
    comments = SentenceComments()

    comments.append(f'# sent_id = {xml_sentence.attrib["id"]}')
    comments.append(f'# text = {xml_tokens_to_text(xml_sentence)}')

    # Parse date.
    if 'date' in xml_text.attrib:
        comments.append(f'# date = {xml_text.attrib["date"]}')
    
    # Parse url.
    if 'url' in xml_text.attrib:
        comments.append(f'# url = {xml_text.attrib["url"]}')
    
    return comments


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

# def batch_sentences(xml_corpus: TextIO) -> Generator[stanza.Document, None, None]:
#     """
#     Generator function that yields batches of the xml corpus as Stanza Documents.
#     Note: these are not annotated with any dependency relations.
#     """
#     pass




def xmlbz2_to_connlu(xml_bz2_filename: str, output_filename: str):
    print('xmlbz2_to_connlu')
    with bz2.open(xml_bz2_filename, mode='rt') as xml_corpus:
        with open(output_filename, mode='w') as connlu_target:
            xml_to_connlu(xml_corpus, connlu_target)


xmlbz2_to_connlu('raw data/familjeliv-adoption.xml.bz2', 'processed data/familjeliv-adoption_v2.connlu')