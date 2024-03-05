"""
Some functions for handling and preprocessing corpus data files.
"""

import bz2
from typing import TextIO
from typing import Generator
import stanza
import stanza.models.common.doc as doc
from stanza.utils.conll import CoNLL
import speechact.corpus as corp
import speechact.preprocess as dat

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
    Read a CoNNL-U corpus in batches. The batches are yielded as stanza.Documents. The batch size is given
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


def reindex(corpora: list[corp.Corpus], target_dir: str, start_id=1):
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
        print_initial_lines(target_file, 30)
        print(f'Reindexed {corp_count}/{len(corpora)} corpora...')


    print(f'Reindexing complete. Assigned new ID to {sent_count} sentences.')


def merge_corpora(corpora: list[corp.Corpus], target_file: str, start_id=1, print_progress=False):
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


def clean_up_connlu(source: TextIO, target: TextIO, print_progress=False):
    """
    Clean up the source CoNNL-U corpus and save it to the target. This is done by removing 
    sentences that are improperly formatted. A sentence is incorrectly formatted if it cannot 
    be loaded by Stanza's CoNNL-U parser.
    """
    if print_progress: print('Clean up corpus')

    lines = []
    error_count = 0
    sentence_count = 0
    for line in source:
        if line == '\n':

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

    if print_progress: print(f'Cleaned up {sentence_count} sentences. Found {error_count}/{sentence_count} errors.')


def extract_sub_sample(source: TextIO, target: TextIO, n_sentences: int, print_progress=False):
    """
    Extract a sub sample of sentences from the CoNNL-U source and write them to the target.
    """

    sentence_count = 0

    # Write lines from source to target.
    for line in source:
        target.write(line)

        # New line indicated end of sentence.
        if line == '\n':
            sentence_count += 1

            if print_progress and sentence_count % 2000 == 0:
                print(f'...extracted {sentence_count} sentences.')

            # Stop if reached max sample size.
            if sentence_count == n_sentences:
                break

    if print_progress: print(f'Extracted {sentence_count}/{n_sentences}.')


def tag_dep_rel(source: TextIO, target: TextIO, print_progress=False, **kwargs):
    """
    Tag a source CoNNL-U corpus with Universal Dependency relations. The tagged sentences are
    written to the target as CoNNL-U.

    The dependency tags are the Universal Dependency Relations: 
    https://universaldependencies.org/u/dep/index.html
    """
    if print_progress: print('Tag corpus with dep tags')

    # Initialize the stanza pipeline for dependency parsing.
    nlp_dep = stanza.Pipeline(lang='sv', processors='depparse', 
                              depparse_pretagged=True, depparse_batch_size=1000)

    # Tag the corpus in batches.
    batch_count = 0
    sentence_count = 0
    for batched_doc in dat.read_batched_doc(source, 200, **kwargs):
        tagged_doc = nlp_dep.process(batched_doc)
        CoNLL.write_doc2conll(tagged_doc, target)

        batch_count += 1
        sentence_count += len(batched_doc.sentences)
        if print_progress: print(f'batch: {batch_count}, sentences: {sentence_count}')

        # Clear documents to free memory.
        # However, I'm not sure if this actually improves memory performance. Running the script 
        # (either at 100 or 1000 batchsize) seem to keep memory usage at ~1.2 GB.
        batched_doc.sentences = None
        tagged_doc.sentences = None  # type: ignore

    if print_progress: print(f'Parsing complete. Parsed {sentence_count} sentences')