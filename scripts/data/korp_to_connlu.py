"""
This code converts xml corpora from Språkbanken to the CoNNL-U format. The linquistic 
data is also converted to Universal Dependencies formalism. This involves:
- Converting the SUC POS-tags to UPOS-tags.
"""

from typing import TextIO
from typing import Generator
from typing import Any
import stanza
from stanza.utils.conll import CoNLL
import xml.etree.ElementTree as ET
import speechact.core as sac
import bz2

SentenceObject = list[dict[str, Any]]
SentenceComments = list[str]

class Korp_CoNNLU_Converter:

    def __init__(self, read_tail=True, genre: str|None=None) -> None:
        self.read_tail = read_tail
        self.genre = genre

    def xml_to_connlu(self, xml_corpus: TextIO, connlu_target: TextIO, max_sentences = -1):
        """
        Convert the Språkbanken xml corpus to a CoNLL-U file.
        """
        print('Converting xml corpus to CoNLL-U.')
        
        # Parse and process the data in batches.
        batch_count = 0
        sentence_count = 0
        for batched_doc in self.batched_xml_to_doc(xml_corpus, 1000, max_sentences):
            
            CoNLL.write_doc2conll(batched_doc, connlu_target)

            batch_count += 1
            sentence_count += len(batched_doc.sentences)
            print(f'batch: {batch_count}, sentence: {sentence_count}')

        
        print('Conversion complete.')


    def batched_xml_to_doc(self, xml_corpus: TextIO, batch_size: int, max_sentences = -1) -> Generator[stanza.Document, None, None]:
        """
        Generator function that yields batches of stanza.Documents that are parsed from
        the Språkbanken xml corpus.
        """

        # The number of sentences parsed so far.
        sentence_index = 0

        sentence_objects = []  # type: list[SentenceObject]
        sentence_comments = []  # type: list[SentenceComments]
        for xml_sentence, xml_text in self.xml_sentences(xml_corpus):

            sentence_object = self.to_sentence_object(xml_sentence)
            sentence_comment = self.to_sentence_comments(xml_sentence, xml_text)

            # Skip the sentence if there was a failure at extracting the sentence/comment data.
            # There is so much data, so we don't have to get hung up on extracting every single
            # piece of it!
            if len(sentence_comment) == 0:
                print(f'WARNING: sentence comments (index={sentence_index}) is empty. Skipping...')
                #print(f'XML sentence tree: {xml_sentence}')
                #print(f'XML text tree: {xml_text}')
                continue

            # Skip here as well.
            if len(sentence_object) == 0:
                print(f'WARNING: sentence object (index={sentence_index}, id={sentence_comment[0]}) is empty. Skipping...')
                #print(f'XML sentence tree: {xml_sentence}')
                #print(f'XML text tree: {xml_text}')
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

            # Yield the current batch if we have reached max sentences.
            if max_sentences != -1 and sentence_index == max_sentences:
                yield stanza.Document(sentences=sentence_objects, comments=sentence_comments)
                return
        
        # Yield remaining batch that is smaller than batch size.
        if len(sentence_objects) > 0:
            yield stanza.Document(sentences=sentence_objects, comments=sentence_comments)


    def xml_sentences(self, xml_corpus: TextIO) -> Generator[tuple[ET.Element, ET.Element], None, None]:
        """
        Generator which yeilds each <sentence> and their corresponding <text> as a 2-tuple of ET.Elements. 
        """
        tree = ET.iterparse(xml_corpus)
        for event, element in tree:
            if event == 'end' and element.tag == 'text':
                for xml_sentence in element.iter('sentence'):
                    yield xml_sentence, element
                
                # Clear to free up memory.
                element.clear()
                
    
    def to_sentence_object(self, xml_sentence: ET.Element) -> SentenceObject:
        """
        Extract the tokens and their data as CoNLL-U tokens in a dictionary format.
        """
        sentence = SentenceObject()
        token_index = 1
        
        # Determine which kind of token tag the sentence contains.
        token_tag = self.get_token_tag(xml_sentence)
        if token_tag is None:
            raise ValueError()

            return sentence

        for xml_token in xml_sentence.iter(token_tag):
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
            if self.read_tail:
                tail = xml_token.attrib.get('_tail', None)
                if tail is None:
                    token['misc'] = 'SpaceAfter=No'


            sentence.append(token)
            token_index += 1
        
        return sentence


    def to_sentence_comments(self, xml_sentence: ET.Element, xml_text: ET.Element) -> SentenceComments:
        """
        Extract the relevant sentence meta-data as CoNLL-U sentence comments.
        """
        comments = SentenceComments()

        comments.append(f'# sent_id = {xml_sentence.attrib["id"]}')
        comments.append(f'# text = {self.xml_tokens_to_text(xml_sentence)}')

        # Parse date.
        if 'date' in xml_text.attrib:
            comments.append(f'# date = {xml_text.attrib["date"]}')
        
        # Parse url.
        if 'url' in xml_text.attrib:
            comments.append(f'# url = {xml_text.attrib["url"]}')

        # Write genre if specified.
        if self.genre is not None:
            comments.append(f'# genre = {self.genre}')
        
        return comments
    

    def get_token_tag(self, xml_sentence: ET.Element) -> str|None:
        # Check if standard token tag.
        if xml_sentence.find('.//token') is not None:
            return 'token'
        
        # Check if legacy token tag.
        elif xml_sentence.find('.//w') is not None:
            return 'w'
        
        # If sentence contains no tokens, return none.
        else:
            return None


    def xml_tokens_to_text(self, sentence : ET.Element) -> str :
        """
        Collect all the xml tokens and concate them as a single text string.
        """
        sentence_text = ''

        # Determine which kind of token tag the sentence contains.
        token_tag = self.get_token_tag(sentence)
        if token_tag is None:
            return sentence_text

        # Append all words as a single string.
        for token in sentence.iter(token_tag):
            assert token.text != None, 'token must no be empty'

            sentence_text += token.text

            # Append whitespace.
            if not self.read_tail or '_tail' in token.attrib:
                sentence_text += ' '
        
        return sentence_text


    def xmlbz2_to_connlu(self, xml_bz2_filename: str, output_filename: str, max_sentences):
        print('xmlbz2_to_connlu')
        with bz2.open(xml_bz2_filename, mode='rt') as xml_corpus:
            with open(output_filename, mode='wt') as connlu_target:
                self.xml_to_connlu(xml_corpus, connlu_target, max_sentences)


    def xmlbz2_to_connlubz2(self, xml_bz2_filename: str, output_filename: str, max_sentences):
        print('xmlbz2_to_connlu')
        with bz2.open(xml_bz2_filename, mode='rt') as xml_corpus:
            with bz2.open(output_filename, mode='wt') as connlu_target:
                self.xml_to_connlu(xml_corpus, connlu_target, max_sentences)


#xmlbz2_to_connlu('raw data/familjeliv-adoption.xml.bz2', 'processed data/familjeliv-adoption_v2.connlu')

if __name__ == '__main__':
    #xmlbz2_to_connlubz2('raw data/familjeliv-adoption.xml.bz2', 'processed data/famtest.connlu.bz2', 100)
    #xmlbz2_to_connlubz2('raw data/familjeliv-allmanna-familjeliv.xml.bz2', 'processed data/familjeliv-allmanna-familjeliv.connlu.bz2', 100000)
    #xmlbz2_to_connlubz2('raw data/suc3.xml.bz2', 'processed data/suc3.connlu.bz2', 100000, read_tail = False)
    
    #Korp_CoNNLU_Converter(genre=sac.Genre.INTERNET_FORUM.value).xmlbz2_to_connlubz2('raw data/familjeliv-expert.xml.bz2', 'processed data/familjeliv-expert.connlu.bz2', 100000)
    #Korp_CoNNLU_Converter(genre=sac.Genre.NEWS_ARTICLE.value, read_tail=False).xmlbz2_to_connlubz2('raw data/gp2013.xml.bz2', 'processed data no-deps/gp2013-100k.connlu.bz2', 100000)

    pass

