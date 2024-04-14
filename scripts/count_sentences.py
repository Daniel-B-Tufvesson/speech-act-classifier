"""
This script counts the sentences in each corpora in a specified directory and writes them 
to a file.

Usage: python count_sentences.py <directory>
"""
# Example: python scripts/count_sentences.py 'data'

from context import speechact
import speechact.corpus as corp
import speechact.corpstats as cs
import speechact.preprocess as pre
import sys

if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) != 2:
        print('Usage: python count_sentences.py <directory>')
        sys.exit(1)

    data_dir = sys.argv[1]
    
    corpus_files = pre.list_files(data_dir, file_extension='conllu.bz2')
    corpora = [corp.Corpus(file) for file in corpus_files]

    with open(f'{data_dir}/sentence counts.txt', mode='wt') as target:
        cs.write_sentence_counts(corpora, target)

