"""
Code for printing corpus statistics to files.
"""

import speechact.corpus as corp
from typing import TextIO
import collections as col

def write_sentence_counts(corpora: list[corp.Corpus], target: TextIO):
    print('Writing sentences counts in corpora to target...')

    corp_count = 0
    for corpus in corpora:
        count = corpus.sentence_count

        target.write(corpus.name)
        target.write(f' {count}\n')

        corp_count += 1
        print(f'Counted sentences in {corp_count}/{len(corpora)}...')
    
    print('Writing complete.')


def speech_act_frequencies(corpus: corp.Corpus) -> col.Counter:
    counter = col.Counter()

    for sentence in corpus.sentences():
        counter[sentence.get_meta_data('speech_act')] += 1  # type: ignore
    
    return counter