"""
A script that generates a CoNLL-U corpus with sentences annotated with speech acts. This takes
all the annotated sentences in a directory and tries to match them up with sentences from CoNLL-U
corpus files. 

Usage: python create_datasets.py <annotated sentences directory> <conllu corpora directory> <target file> <exclude_label_1,exclude_label_2,...>
"""
# Example: python scripts/create_dataset.py 'data/annotated data/evaluation annotations' 'data' 'data/stuff.conllu.bz2' 'unknown, unsure, hypothesis'

from context import speechact
import speechact.preprocess as pre
import speechact.annotate as annotate
import speechact.corpus as corp
import bz2
import sys

def generate_corpus(annotated_sents_dir: str, 
                    conllu_dir: str, 
                    target_file: str, 
                    exclude_labels: list[str]):
    print(f'Generate annotated CoNLL-U corpus from "{annotated_sents_dir}" and "{conllu_dir}')

    sent_files = pre.list_files(annotated_sents_dir, file_extension=annotate.ANNOTATED_EXT)
    connlu_files = pre.list_files(conllu_dir, file_extension='connlu.bz2')

    sent_corpora = [annotate.SentenceCorpus(file) for file in sent_files]
    connlu_corpora = [corp.Corpus(file) for file in connlu_files]

    with bz2.open(target_file, mode='wt') as target:
        annotate.generate_connlu_corpus(sent_corpora, 
                                        connlu_corpora, 
                                        target, 
                                        print_progress=True, 
                                        exclude_labels=exclude_labels)

    print(f'Corpora generated.')

if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print('Usage: python create_datasets.py <annotated sentences directory> <conllu corpora directory> <target file> <exclude_label_1,exclude_label_2,...>')
        sys.exit(1)
    
    annotated_sents_dir = sys.argv[1]
    conllu_dir = sys.argv[2]
    target_file = sys.argv[3]
    
    if len(sys.argv) == 5:
        exclude_labels = [label.strip() for label in sys.argv[4].split(',')]
    else:
        exclude_labels = []

    generate_corpus(annotated_sents_dir, conllu_dir, target_file, exclude_labels)
    pre.print_initial_lines(target_file, 100)
