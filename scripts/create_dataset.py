"""
A script that generates a CoNNL-U corpus with sentences annotated with speech acts. This takes
all the annotated sentences in a directory and tries to match them up with sentences from CoNNL-U
corpus files. 
"""

from context import speechact
import speechact.preprocess as pre
import speechact.annotate as annotate
import speechact.corpus as corp
import bz2

def generate_corpus(annotated_sents_dir: str, connlu_dir: str, target_file: str, exclude_labels: list[str]):
    print(f'Generate annotated CoNNL-U corpus from "{annotated_sents_dir}" and "{connlu_dir}')

    sent_files = pre.list_files(annotated_sents_dir, file_extension=annotate.ANNOTATED_EXT)
    connlu_files = pre.list_files(connlu_dir, file_extension='connlu.bz2')

    sent_corpora = [annotate.SentenceCorpus(file) for file in sent_files]
    connlu_corpora = [corp.Corpus(file) for file in connlu_files]

    with bz2.open(target_file, mode='wt') as target:
        annotate.generate_connlu_corpus(sent_corpora, connlu_corpora, target, print_progress=True, 
                                        exclude_labels=exclude_labels)

    print(f'Corpora generated.')

if __name__ == '__main__':
    annotated_sents_dir = 'data/annotated data/dev annotations'
    connlu_dir = 'data/tagged data'
    target_file = 'data/annotated data/dev-set.connlu.bz2'
    exclude_labels = [annotate.SpeechActLabels.UNKNOWN.value]

    generate_corpus(annotated_sents_dir, connlu_dir, target_file, exclude_labels)
    pre.print_initial_lines(target_file, 100)