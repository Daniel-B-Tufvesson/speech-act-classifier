"""
This script removes sentences of a specified speech act labels from a corpus. This 
changes original corpus file.
"""
# Example: python scripts/remove_labels.py 'data/for-testing/dir2/tagged/test-set.conllu.bz2' 'expressive, question'


from context import speechact
import speechact.corpus as corp
import speechact.annotate as anno
import os
import bz2
import sys


if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) != 3:
        print('Usage: python remove_labels.py <corpus> <label_1,label_2,...>')
        sys.exit(1)

    source_file = sys.argv[1]
    labels_to_remove = [label.strip() for label in sys.argv[2].split(',')]

    print(f'Removing sentences that are {labels_to_remove}, in "{source_file}"')
    
    source_corpus = corp.Corpus(source_file)
    directory = os.path.dirname(source_file)
    tmp_file = os.path.join(directory, f'{source_corpus.name}-tmp')

    # Write all sentences that do not have the given labels.
    with bz2.open(tmp_file, mode='wt') as target:
        written_sentences = 0
        total_sentences = 0
        for sentence in source_corpus.sentences():
            if sentence.get_meta_data('speech_act') not in labels_to_remove:
                sentence.write(target)
                written_sentences += 1
            total_sentences += 1

    # Overwrite original file.
    os.replace(tmp_file, source_file)

    print(f'Kept {written_sentences}/{total_sentences}.')

