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
import warnings

SentenceObject = list[dict[str, Any]]
SentenceComments = list[str]

def xml_to_connlu(xml_corpus: TextIO, connlu_target: TextIO):
    """
    Convert the Språkbanken xml corpus to a CoNLL-U file.
    """
    print('Converting xml corpus to CoNLL-U.')
    
    # Initialize the stanza pipeline for dependency parsing.
    nlp_dep = stanza.Pipeline(lang='sv', processors='depparse', depparse_pretagged=True)

    # Parse and process the data in batches. 
    for batched_doc in batched_xml_to_doc(xml_corpus, 1000):
        tagged_doc = nlp_dep(batched_doc)
        CoNLL.write_doc2conll(tagged_doc, connlu_target)
    
    print('Conversion complete.')


def batched_xml_to_doc(xml_corpus: TextIO, batch_size: int) -> Generator[stanza.Document, None, None]:
    """
    Generator function that yields batches of stanza.Documents that are parsed from
    the Språkbanken xml corpus.
    """

    sentence_index = 0

    sentence_objects = []  # type: list[SentenceObject]
    sentence_comments = []  # type: list[SentenceComments]
    for xml_sentence, xml_text in xml_sentences(xml_corpus):

        sentence_object = to_sentence_object(xml_sentence)
        sentence_comment = to_sentence_comments(xml_sentence, xml_text)

        #print(f"{sentence_index}, {[token['text'] for token in sentence_object]}")

        # Skip the sentence if there was a failure at extracting the sentence/comment data.
        # There is so much data, so we don't have to get hung up on extracting every single
        # piece of it!
        if len(sentence_comment) == 0:
            warnings.warn(f'WARNING: sentence comments (index={sentence_index}) is empty. Skipping...')
            warnings.warn(f'XML sentence tree: {xml_sentence}')
            warnings.warn(f'XML text tree: {xml_text}')
            continue

        # Skip here as well.
        if len(sentence_object) == 0:
            warnings.warn(f'WARNING: sentence object (index={sentence_index}, id={sentence_comment[0]}) is empty. Skipping...')
            warnings.warn(f'XML sentence tree: {xml_sentence}')
            warnings.warn(f'XML text tree: {xml_text}')
            continue

        # Append sentence data to batch.
        sentence_objects.append(sentence_object)
        sentence_comments.append(sentence_comment)

        # Create document batch and yield it.
        if len(sentence_objects) == batch_size:
            yield stanza.Document(sentences=sentence_objects, comments=sentence_comments)

            # Reset the batch.
            sentence_objects = []  # type: list[SentenceObject]
            sentence_comments = []  # type: list[SentenceComments]
        
        sentence_index += 1

        
    
    # Yield remaining batch that is smaller than batch size.
    if len(sentence_objects) > 0:
        yield stanza.Document(sentences=sentence_objects, comments=sentence_comments)


# def xml_to_doc(xml_corpus : TextIO) -> stanza.Document:
#     """
#     Convert the Språkbanken xml corpus to a stanza.Document.
#     """
    
#     sentence_objects = []  # type: list[SentenceObject]
#     sentence_comments = []  # type: list[SentenceComments]
#     for xml_sentence, xml_text in xml_sentences(xml_corpus):
#         sentence_objects.append(to_sentence_object(xml_sentence))
#         sentence_comments.append(to_sentence_comments(xml_sentence, xml_text))

#         if len(sentence_objects) == 10:
#             break
    
#     return stanza.Document(
#         sentences=sentence_objects,
#         comments=sentence_comments
#     )


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


#xmlbz2_to_connlu('raw data/familjeliv-adoption.xml.bz2', 'processed data/familjeliv-adoption_v2.connlu')