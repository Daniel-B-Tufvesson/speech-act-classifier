"""
This script classifies sentences using the rule based classfier.
"""
from context import speechact
import speechact.classifier.rulebased as rb
import speechact.classifier.base as b
import speechact.evaluation as evaluation
import speechact.corpus as corp

if __name__ == '__main__':
    corpus = corp.Corpus('data/annotated data/dev-set.connlu.bz2')

    print()
    punctuation_classifier = rb.PunctuationClassifier()
    print('Punctuation classifier results:')
    evaluation.evaluate(corpus, punctuation_classifier)
    print()

    most_frequent = b.MostFrequentClassifier()
    most_frequent.train(corpora=[corpus])
    print(f'Most frequenct class is "{most_frequent.most_common}"')
    print('Baseline results:')
    evaluation.evaluate(corpus, most_frequent)
    print()