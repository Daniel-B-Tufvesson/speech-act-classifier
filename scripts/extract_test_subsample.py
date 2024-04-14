"""
Extract random sentences from a CoNLL-U corpus, and write them to a sentence corpus.

Usage: python extract_test_subsample.py <source corpus> <target sentence corpus> <N sentences>
"""
# Example: python scripts/extract_test_subsample.py 'data/for-testing/dir1/test-set.conllu.bz2' 'data/for-testing/dir1/test-set-subsample.💬 30'

from context import speechact
import speechact.corpus as corp
import random
import sys

if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) != 4:
        print('Usage: python extract_test_subsample.py <source corpus> <target sentence corpus> <N sentences>')
        sys.exit(1)

    source_file = sys.argv[1]
    target_file = sys.argv[2]
    n_sentences = int(sys.argv[3])

    # Load and shuffle sentences from CoNLL-U corpus.
    source_corpus = corp.Corpus(source_file)
    sentences = [sent for sent in source_corpus.sentences()]
    random.shuffle(sentences)

    # Write to sentence corpus.
    target = open(target_file, mode='wt')
    for i in range(n_sentences):
        sentence = sentences[i]
        target.write(f'# sent_id = {sentence.sent_id}\n')
        target.write(f'# text = {sentence.text}\n')
        target.write(f'# speech_act = {sentence.speech_act}\n')
        target.write('\n')
    
    target.close()


        
        