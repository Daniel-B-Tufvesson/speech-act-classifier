"""
A module to aid the manual annotation process. This involves code for extracting sentence from CoNNL-U
files and then formatting them to a convenient format for the annotation tool to read. This also involves
code for analyzing the then annotated sentences, i.e. computing Cohen's kappa.
"""

import bz2
import os
import random
import sklearn.metrics as metrics
from typing import TextIO
import speechact.corpus as corp
import enum


UNANNOTATED_EXT = '💬'  # speech bubble emoji.
"""The file extension for unannotated sentence files."""

ANNOTATED_EXT = '✏️'  # pencil emoji
"""The file extension for annotated sentence files."""

class SpeechActLabels(enum.StrEnum):
    """
    The speech acts labels.
    """

    ASSERTION = 'assertion'
    """Expresses an assertion."""

    QUESTION = 'question'
    """Expresses a question."""

    DIRECTIVE = 'directive'
    """Expresses a command."""

    EXPRESSIVE = 'expressive'
    """Expresses an emotion, value or surprise."""

    HYPOTHESIS = 'hypothesis'
    """Expresses an assumption or hypothesis."""

    UNKNOWN = 'unknown'
    """It is unclear what speech act the sentence is expressing."""

    NONE = 'none'
    """The sentence does not express any of the given speech acts."""

    @staticmethod
    def get_labels() -> list[str]:
        return [label.value for label in SpeechActLabels]


class Sentence:
    """
    An annotated or unannatotated sentence. This only consist of the whole sentence, and not any token data.
    """

    def __init__(self, text: str, id: str, label: str|None = None):
        self.text = text
        self.id = id
        self.label = label


class SentencePair:
    """
    A pair of sentences.
    """
    
    def __init__(self, sentence_a: Sentence, sentence_b: Sentence) -> None:
        self.a = sentence_a
        self.b = sentence_b


class SentenceCorpus:
    """
    A corpus consisting of annotated or unannatotated sentences. This is only for reading data.
    """

    def __init__(self, file_name: str) -> None:
        assert os.path.isfile(file_name), f'Sentence corpus does not exist: "{file_name}"'
        self.file_name = file_name


    def load_sentences(self) -> list[Sentence]:
        sentences = []
        with open(self.file_name, mode='rt') as source:

            sentence_id = None
            sentence_text = None
            sentence_label = None

            line_number = 0
            for line in source:
                line_number += 1
                line = line.strip()

                if line == '':
                    
                    if sentence_id != None and sentence_text != None:
                        sentence = Sentence(sentence_text, sentence_id, sentence_label)
                        sentences.append(sentence)

                        sentence_id = None
                        sentence_text = None
                        sentence_label = None

                    elif sentence_id != None or sentence_text != None:
                        raise Exception(f'Newline but sentence data was not complete at line {line_number}')
                
                else:
                    # Parse sentence ID.
                    if line.startswith('# sent_id = '):
                        sentence_id = line.removeprefix('# sent_id = ')

                    # Parse sentence text.
                    elif line.startswith('# text = '):
                        sentence_text = line.removeprefix('# text = ')
                    
                    # Parse sentence label.
                    elif line.startswith('# speech_act = '):
                        sentence_label = line.removeprefix('# speech_act = ')
        
        # Store last sentence entry.
        if sentence_id != None and sentence_text != None:
            sentence = Sentence(sentence_text, sentence_id, sentence_label)
            sentences.append(sentence)

        return sentences


class AnnotatedCorpusPair:
    """
    A pair of annotated corpora. 
    """

    def __init__(self, corpus_a: SentenceCorpus, corpus_b: SentenceCorpus) -> None:
        self.corpus_a = corpus_a
        self.corpus_b = corpus_b



def read_n_sentences(source_file: str, n_sentences: int, sent_ids: set[str]) -> list[Sentence]:
    """
    Read the first N sentences from the CoNLL-U corpus.
    """
    sentences = []
    with bz2.open(source_file, mode='rt') as source:
        sent_text = None
        sent_id = None

        for line in source:
            if line == '\n':

                if sent_text and sent_id:

                    # Prevent sentence with taken ID.
                    if sent_id in sent_ids:
                        print(f'Skipping sentence {sent_id} "{sent_text}" because its ID is taken.')
                        sent_id = None
                        sent_text = None
                        continue

                    # Store the sentence.
                    sent_ids.add(sent_id)
                    sentence = Sentence(sent_text, sent_id)
                    sentences.append(sentence)

                    # Stop if max sentences is reached.
                    if len(sentences) == n_sentences:
                        break

            else:
                if line.startswith('# text ='):
                    sent_text = line

                elif line.startswith('# sent_id ='):
                    sent_id = line

    return sentences


def extract_sentences(source_files: list[str], target_dir: str, sent_per_source: int, 
                      sent_per_target: int, print_progress=False):
    """
    Extract the initial sentences from each corpora, scramble them, and distribute them into new 
    smaller corpus files. These smaller files contain only sent_id and text of the sentences. The 
    individual tokens or other meta-data are not extracted. Entries are separated with an empty line.
    The new files are uncompressed as regular txt files.
    """
    if print_progress: print('Extracting sentences to annotate.')

    # Make sure that the source files exist.
    for source_file in source_files:
        assert os.path.isfile(source_file), f'File does not exist: {source_file}'

    assert os.path.isdir(target_dir), f'Target directory does not exist: {target_dir}'

    # Keep track sentences IDs to prevent duplicates.
    sent_ids = set()

    # Read the N first sentences from each source file.
    sentences = []  # type: list[Sentence]
    for source_file in source_files:
        sentences += read_n_sentences(source_file, sent_per_source, sent_ids)

    # Shuffle them.
    random.seed = 42
    random.shuffle(sentences)

    # Write them to new target files.
    sentence_count = 0
    target_count = 1
    lines_to_write = []
    target_file = f'{target_dir}/sents_{target_count}.{UNANNOTATED_EXT}'
    for sentence in sentences:

        # Create new 
        if sentence_count != 0 and sentence_count % sent_per_target == 0:
            target_file = f'{target_dir}/sents_{target_count}.{UNANNOTATED_EXT}'

            # Write lines to file.
            with open(target_file, mode='wt') as target:
                target.writelines(lines_to_write)
                lines_to_write = []

            target_count += 1

        sentence_count += 1
        lines_to_write.append(sentence.id) # We assume they end with newlines.
        lines_to_write.append(sentence.text)
        lines_to_write.append('\n')

    if print_progress: print(f'Extraction complete. Extracted {len(sentences)} sentences.')


def compute_cohens_kappa_dir(directory_a: str, directory_b: str) -> float:
    """
    Compute Cohen's kappa between the two directories of annotated sentence corpora. Directory A contains
    the sentences annotated by annotator A. Directory B of those by annotator B.
    """

    # Retrieve the file names from directories.
    files_a = annotation_files_in_dir(directory_a)
    files_b = annotation_files_in_dir(directory_b)

    assert len(files_a) == len(files_b), f'Number of annotation files do not match. A: {len(files_a)}, B: {len(files_b)}'

    # Pair up file names.
    file_pairs = pair_up_annotation_files(files_a, files_b)

    # Load corpus pairs from file pairs.
    corpus_pairs = [AnnotatedCorpusPair(SentenceCorpus(file_a), SentenceCorpus(file_b)) for file_a, file_b in file_pairs.items()]

    return compute_cohens_kappa(corpus_pairs)


def compute_cohens_kappa_files(file_a: str, file_b: str) -> float:
    """
    Compute Cohen's kappa between two files of annotated sentences.
    """
    corpus_pair = AnnotatedCorpusPair(SentenceCorpus(file_a), SentenceCorpus(file_b))
    return compute_cohens_kappa([corpus_pair])


def compute_cohens_kappa(corpus_pairs: list[AnnotatedCorpusPair]) -> float:
    """
    Compute Cohen's kappa between the corpora pairs.
    """
    labels_a = []
    labels_b = []

    # Collect the labels from corpus pairs.
    for corpus_pair in corpus_pairs:
        try:
            sentences_a = corpus_pair.corpus_a.load_sentences()
            sentences_b = corpus_pair.corpus_b.load_sentences()

            assert len(sentences_a) == len(sentences_b), f'Number of sentences do not match. A: {len(sentences_a)}, B: {len(sentences_b)}'

            # Map B sentences to their IDs.
            id_to_sent_b = {sent.id: sent for sent in sentences_b}

            # Match A and B sentences with regards to their IDs.
            for sentence_a in sentences_a:
                sentence_b = id_to_sent_b.get(sentence_a.id)
                assert sentence_b != None, f'No B sentence with ID {sentence_a.id}'

                labels_a.append(sentence_a.label)
                labels_b.append(sentence_b.label)
        except Exception as e:
            raise Exception(f'Failed to pair sentences between "{corpus_pair.corpus_a.file_name}" and "{corpus_pair.corpus_b.file_name}" because "{e}"')
    
    assert len(labels_a) > 0, 'No labels for A'
    assert len(labels_b) > 0, 'No labels for B'
    assert len(labels_a) == len(labels_b), f'Number of labels do not match. A: {len(labels_a)}, B: {len(labels_b)}'
    
    # Compute Cohen's kappa.
    return metrics.cohen_kappa_score(labels_a, labels_b)


def annotation_files_in_dir(directory: str) -> list[str]:
    """
    Retrieve all the names of the annotated files in the directory. 
    """
    files_and_dirs = os.listdir(directory)
    return [os.path.join(directory, file) for file in files_and_dirs if os.path.isfile(os.path.join(directory, file)) and file.endswith(ANNOTATED_EXT)]


def pair_up_annotation_files(files_a: list[str], files_b: list[str]) -> dict[str, str]:
    """
    Pair up the annotation file names. For example a file from A named "sents_754-2024-03-05" will be
    paired with a file from B named "sents_754-2024-04-07".
    """
    assert len(files_a) == len(files_b), f'Number of file do not match. A: {len(files_a)}, B: {len(files_b)}'
    
    assert_duplicate_annotation_files(files_a)
    assert_duplicate_annotation_files(files_b)

    prefixes_b = {get_annotation_file_prefix(file_b): file_b for file_b in files_b}

    # Pair up files with identical prefixes.
    pairs = {}
    for file_a in files_a:
        prefix_a = get_annotation_file_prefix(file_a)
        file_b = prefixes_b.get(prefix_a)
        assert file_b != None, f'No mathing file for "{file_a}" with prefix "{prefix_a}"'

        pairs[file_a] = file_b
    
    return pairs


def assert_duplicate_annotation_files(files: list[str]):
    """
    Make sure that there are no duplicate annotation files in the list of files. Two files are duplicates
    if they start with the same sents_xxx prefix. For example, "sents_754-2024-03-05" and "sents_754-2024-04-07"
    are duplicates, while "sents_754-2024-03-05" and "sents_755-2024-03-05" are not.
    """
    unique_prefixes = set()
    for file in files:
        prefix = get_annotation_file_prefix(file)
        assert prefix not in unique_prefixes, f'Duplicate annotation file found starting with {prefix}'
    
    # No duplicates found :)


def get_annotation_file_prefix(file: str) -> str:
    """
    Get the sents_xxx prefix from the file name of an annotated sentences file. For example, "sents_755-2024-03-05"
    gives "sents_755".
    """
    name_without_path = file.split('/')[-1]
    prefix = name_without_path.split('-')[0]

    assert prefix.startswith('sents_'), f'Annotation file does not start with "sent_": "{file}"'

    return prefix


def generate_connlu_corpus(sent_corpora: list[SentenceCorpus], connlu_corpora: list[corp.Corpus],
                           target_file: TextIO, print_progress=False, exclude_labels: list[str]|None=None):
    """
    Generate a CoNNL-U corpus of sentences annotated with speech acts. This tries to match up all the
    sentences in the annotated sentence corpora, with the sentences in the CoNNL-U corpora with
    respect to their sent_ids. The generated corpora is written to the target_file.
    """
    
    if print_progress: 
        print(f'Generating speech act annotated corpus from {len(sent_corpora)} corpora.')
        if exclude_labels != None: print(f'Excluding labels: {exclude_labels}.')

    corpus_count = 0
    sentence_count = 0

    # Parse annotated sentences from each sentence corpus.
    for sent_corpus in sent_corpora:
        if print_progress: print(f'Parsing sentences from {sent_corpus.file_name}')
        corpus_count += 1
        try:

            # Match each annotated sentence to its CoNNL-U sentence.
            for annotated_sentence in sent_corpus.load_sentences():
                assert annotated_sentence.label != None, f'Sentence does not have a speech act label: {annotated_sentence.id}'

                # Skip sentence if it has an excluded label.
                if exclude_labels != None and annotated_sentence.label in exclude_labels:
                    continue

                # Find the CoNNL-U sentence.
                sent_id = int(annotated_sentence.id)
                connlu_sentence = corp.find_sentence_with_id(connlu_corpora, sent_id)
                assert connlu_sentence != None, f'CoNNL-U sentence with sent_id {sent_id} not found.'

                # Add the label to the sentence and write to target.
                connlu_sentence.set_meta_data('speech_act', annotated_sentence.label)
                connlu_sentence.write(target_file)

                # Print progress.
                sentence_count += 1
                if print_progress and sentence_count % 100 == 0:
                    print(f'Parsed {sentence_count} sentences...')

        except Exception as e:
            raise RuntimeError(f'Failed to parse sentence corpus "{sent_corpus.file_name}" because {e}')
        
    if print_progress: 
        print(f'Parsing complete! Parsed {corpus_count}/{len(sent_corpora)} corpora.')
        print(f'A total of {sentence_count} sentences.')
