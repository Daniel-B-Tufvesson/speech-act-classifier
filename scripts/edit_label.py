"""
This script is used for editing a single speech_act label in an annotated CoNLL-U file.
"""
from context import speechact
import speechact.corpus as corp
import speechact.annotate as anno
import os
import bz2

if __name__ == '__main__':
    sent_id = 1300288
    new_speech_act = anno.SpeechActLabels.ASSERTION

    assert new_speech_act in anno.SpeechActLabels.get_labels(), f'Unsupported label: "{new_speech_act}"'

    corpus_file = 'data/annotated data/dev-set-sentiment.connlu.bz2'
    corpus = corp.Corpus(corpus_file)

    directory = os.path.dirname(corpus_file)
    temp_file = os.path.join(directory, f'{corpus}.conllu.bz2')

    edit_counts = 0
    with bz2.open(temp_file, mode='wt') as target:
        for sentence in corpus.sentences():

            if sentence.sent_id == sent_id and sentence.try_get_meta_date('speech_act') != new_speech_act:
                sentence.set_meta_data('speech_act', new_speech_act)
                edit_counts += 1

            sentence.write(target)

    os.replace(temp_file, corpus_file)

    print(f'Edited {edit_counts} sentence labels.')