"""
Some functions for handling and preprocess corpus data files.
"""

import bz2
from typing import TextIO
from typing import Generator
import stanza
import stanza.models.common.doc as doc
from stanza.utils.conll import CoNLL

import speechact.preprocess as dat
from speechact.corpus import Corpus

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


def print_initial_lines(file_name: str, n_lines = 30):
    """
    Read the first N lines in bz2 compressed file.
    """
    with bz2.open(file_name, mode='rt') as source:
        print(f'Printing the first {n_lines} in "{file_name}" ---------------------')

        i = 0
        for line in source:
            print(line)
            i += 1

            if i == n_lines:
                break

        print(f'Printed the first {i}/{n_lines} in {file_name} ----------------------')


def reindex(corpora: list[Corpus], target_dir: str, start_id=1):
    """
    Reindex each sentence in each corpus, and write them to new corpus files in the target
    directory.
    """
    print(f'Reindexing sentences from {len(corpora)} corpora to "{target_dir}"')

    import os
    assert os.path.isdir(target_dir), f'Directory does not exists: {target_dir}'

    # Reindex each sentence in each corpus, and write them to new files.
    sent_count = 0
    corp_count = 0
    sent_id = start_id
    for corpus in corpora:
        print(f'Reindexing corpus: "{corpus.name}"')

        target_file = f'{target_dir}/{corpus.name}.connlu.bz2'
        with bz2.open(target_file, mode='wt') as target:

            for sentence in corpus.sentences():

                # Update the ID.
                x_sent_id = sentence.get_meta_data('sent_id')
                sentence.set_meta_data('x_sent_id', x_sent_id)
                sentence.set_meta_data('sent_id', sent_id)

                # Write sentence to target file.
                target.writelines(sentence.sentence_lines)
                target.write('\n')

                sent_id += 1
                sent_count += 1

                # Print progress.
                if sent_count % 5000 == 0:
                    print(f'Reindexed {sent_count} sentences...')

        corp_count += 1

        print('Reindexing for corpus complete.')
        print('Printing first 30 lines:')
        dat.print_initial_lines(target_file, 30)
        print(f'Reindexed {corp_count}/{len(corpora)} corpora...')


    print(f'Reindexing complete. Assigned new ID to {sent_count} sentences.')


def merge_corpora(corpora: list[Corpus], target_file: str, start_id=1, print_progress=False):
    """
    Merge the corpora files in to a single file.
    """
    if print_progress: print(f'Merging {len(corpora)} corpora to {target_file}.')

    sent_id = start_id
    sent_count = 0
    with bz2.open(target_file, mode='wt') as target:

        for corpus in corpora:
            for sentence in corpus.sentences():

                # Update sentence meta data.
                x_sent_id = sentence.get_meta_data('sent_id')
                sentence.set_meta_data('x_sent_id', x_sent_id)
                sentence.set_meta_data('sent_id', sent_id)
                sentence.set_meta_data('corpus', corpus.name)

                # Write sentence to target.
                target.writelines(sentence.sentence_lines)
                target.write('\n')

                sent_id += 1
                sent_count += 1

                if print_progress and sent_count % 2000 == 0:
                    print(f'Merged {sent_count} sentences...')

    if print_progress: print(f'Merging complete. ')
