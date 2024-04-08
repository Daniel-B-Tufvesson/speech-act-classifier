"""
Extract random sentence from a test data corpus.
"""
from context import speechact
import speechact.corpus as corp
import random

if __name__ == '__main__':
    test_corpus = corp.Corpus('data/annotated data/test-set.conllu.bz2')
    sentences = [sent for sent in test_corpus.sentences()]
    random.shuffle(sentences)

    target = open('data/annotated data/test-set-subsample.💬', mode='wt')

    for i in range(50):
        sentence = sentences[i]
        target.write(f'# sent_id = {sentence.sent_id}\n')
        target.write(f'# text = {sentence.text}\n')
        target.write(f'# speech_act = {sentence.speech_act}\n')
        target.write('\n')
        
        