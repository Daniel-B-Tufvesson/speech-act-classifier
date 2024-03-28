"""
This script excludes sentences of a specified speech act labels from a corpus. This 
changes original corpus file.
"""

from context import speechact
import speechact.corpus as corp
import speechact.annotate as anno
import os
import bz2


if __name__ == '__main__':

    # The speech acts to include.
    to_include = [
        anno.SpeechActLabels.ASSERTION,
        anno.SpeechActLabels.DIRECTIVE,
        anno.SpeechActLabels.EXPRESSIVE,
        anno.SpeechActLabels.QUESTION
    ]

    source_file = 'data/auto-annotated data/speech-acts.conllu.bz2'
    source_corpus = corp.Corpus(source_file)

    print(f'Excluding sentences that are not {to_include}, in "{source_file}"')

    directory = os.path.dirname(source_file)
    tmp_file = os.path.join(directory, f'{source_corpus.name}-tmp')

    with bz2.open(tmp_file, mode='wt') as target:
        written_sentences = 0
        total_sentences = 0
        for sentence in source_corpus.sentences():
            if sentence.get_meta_data('speech_act') in to_include:
                sentence.write(target)
                written_sentences += 1
            total_sentences += 1

    os.replace(tmp_file, source_file)

    print(f'Included {written_sentences}/{total_sentences}.')