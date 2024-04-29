"""
This script tags a CoNLL-U corpus file with speech acts using the rule based classifier. The tagged
sentences are written to a new corpus file.

The corpus needs to be tagged with sentiment labels (sent_label).

Usage: python tag_speech_acts_rulebased.py <source corpus> <target corpus> <ruleset file>
"""
# Example: python scripts/tag_speech_acts_rulebased.py 'data/for-testing/dir2/dev-set-test-sentiment.conllu.bz2' 'data/for-testing/dir2/speech-acts.conllu.bz2'

from context import speechact
import speechact.classifier.rulebased as rb
import speechact.corpus as corp
import speechact.preprocess as pre
from stanza.utils.conll import CoNLL
import sys

if __name__ == '__main__':
    # Check the number of arguments passed
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print('Usage: python tag_speech_acts_rulebased.py <source corpus> <target corpus> <ruleset file>')
        sys.exit(1)

    source_file = sys.argv[1]
    target_file = sys.argv[2]

    if len(sys.argv) > 3:
        rule_file = sys.argv[3]
    else:
        rule_file = 'models/rule-based.json'

    classifier = rb.TrainableSentimentClassifierV2(ruleset_file=rule_file)
    source_corpus = corp.Corpus(source_file)
    
    with pre.open_write(target_file) as target:

        # Tag the corpus in batches.
        batch_count = 0
        sentence_count = 0
        for batch in source_corpus.batched_docs(1000):
            classifier.classify_document(batch)
            CoNLL.write_doc2conll(batch, target)

            batch_count += 1
            sentence_count += len(batch.sentences)
            print(f'batch: {batch_count}, sentences: {sentence_count}')

    print(f'Parsing complete. Parsed {sentence_count} sentences')