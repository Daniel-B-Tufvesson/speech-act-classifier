"""
Some functions for loading CoNNL-U files into Stanza data structures.
"""

import bz2
from typing import TextIO
from typing import Generator
import stanza
import stanza.models.common.doc as doc
from stanza.utils.conll import CoNLL

def read_sentences_bz2(connlu_corpus_file: str, max_sentences = -1) -> Generator[doc.Sentence, None, None]:
    """
    Read and yield each sentence in a bz2 compressed CoNNL-U corpus. The yielded sentences are Stanza 
    Sentences.
    """
    with bz2.open(connlu_corpus_file, mode='rt') as source:
        for sentence in read_sentences(source, max_sentences=max_sentences):
            yield sentence


def read_sentences(connlu_corpus: TextIO, max_sentences = -1) -> Generator[doc.Sentence, None, None]:
    """
    Read and yield each sentence in the CoNNL-U corpus. The yielded sentences are Stanza Sentences.
    """
    for batched_doc in read_batched_doc(connlu_corpus, 100, max_sentences=max_sentences):
        
        for sentence in batched_doc.sentences:
            yield sentence


def read_batched_doc(connlu_corpus: TextIO, batch_size: int, max_sentences = -1) -> Generator[stanza.Document, None, None]:
    """
    Read a connlu corpus in batches. The batches are yielded as stanza.Documents. The batch size is given
    in the number of sentences.
    """
    
    lines = []  # The lines of the current batch.
    sentence_count = 0
    
    # Collect and batch the lines.
    for line in connlu_corpus:
        lines.append(line)

        if line == '\n':
            sentence_count += 1
        
        # Parse the batch as document and yield it.
        if sentence_count == batch_size or sentence_count == max_sentences:
            doc_conll, doc_comments = CoNLL.load_conll(lines)
            doc_dict, doc_empty = CoNLL.convert_conll(doc_conll)
            doc = stanza.Document(doc_dict, text=None, comments=doc_comments, empty_sentences=doc_empty)
            yield doc

            # Reset accumulated lines if we have not reached max.
            if sentence_count != max_sentences:
                lines = []
                sentence_count = 0

            # If reached max, stop parsing.
            else :
                return
    
    # Parse remaining lines.
    if len(lines) != 0:
        doc_conll, doc_comments = CoNLL.load_conll(lines)
        doc_dict, doc_empty = CoNLL.convert_conll(doc_conll)
        doc = stanza.Document(doc_dict, text=None, comments=doc_comments, empty_sentences=doc_empty)
        yield doc


def lines(txt_file_source: str) -> list[str]:
    """
    Read all lines in the text file and return them as a list of strings.
    """
    with open(txt_file_source, mode='rt') as source:
        lines = lines = [line.rstrip() for line in source.readlines()]
    return lines
