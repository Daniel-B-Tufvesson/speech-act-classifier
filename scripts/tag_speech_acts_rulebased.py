"""
This script tags a CoNLL-U corpus file with speech acts using the rule based classifier. The tagged
sentences are written to a new corpus file.

The corpus needs to be tagged with sentiment labels (sent_label).
"""

from context import speechact
import speechact.classifier.rulebased as rb
import speechact.corpus as corp
import speechact.preprocess as pre
from stanza.utils.conll import CoNLL


if __name__ == '__main__':
    source_file = '' # todo: add file names.
    target_file = ''

    rule_file = 'models/trainable_rule_classifier_sentiment_2_large.json'
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