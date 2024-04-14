"""
This script is used for editing a single speech_act label in an annotated CoNLL-U file.

Usage: python edit_label.py <corpus> <sent_id> <new label>
"""
# Example: python scripts/edit_label.py data/for-testing/dir2/tagged/test-set.conllu.bz2 2500664 expressive

from context import speechact
import speechact.corpus as corp
import speechact.annotate as anno
import os
import bz2
import sys

if __name__ == '__main__':
    # Check the number of arguments passed
    if len(sys.argv) != 4:
        print('Usage: python edit_label.py <corpus> <sent_id> <new label>')
        sys.exit(1)

    corpus_file = sys.argv[1]
    sent_id = int(sys.argv[2])
    new_speech_act = sys.argv[3]

    assert new_speech_act in anno.SpeechActLabels.get_labels(), f'Unsupported label: "{new_speech_act}"'

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
