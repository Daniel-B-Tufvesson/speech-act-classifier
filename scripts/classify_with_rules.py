"""
This script classifies sentences using the rule based classfier.
"""
from context import speechact
import speechact.classifier.rulebased as rb
import speechact.classifier.base as b
import speechact.evaluation as evaluation
import speechact.corpus as corp
import speechact.annotate as annotate

if __name__ == '__main__':
    corpus = corp.Corpus('data/annotated data/dev-set.connlu.bz2')
    labels = annotate.SpeechActLabels.get_labels()

    print()

    # Evaluate baseline MFC classifier.
    most_frequent = b.MostFrequentClassifier()
    most_frequent.train(corpora=[corpus])
    print(f'Most frequenct class is "{most_frequent.most_common}"')
    print()
    print('Baseline results:')
    evaluation.evaluate(corpus, most_frequent, labels)
    print()

    # Evaluate punctuation classifier.
    punctuation_classifier = rb.PunctuationClassifier()
    print('Punctuation classifier results:')
    evaluation.evaluate(corpus, punctuation_classifier, labels)
    print()

    # Evaluate clause classifier.
    clause_classifier = rb.ClauseClassifier()
    print('Clause classifier results:')
    evaluation.evaluate(corpus, clause_classifier, labels)
    print()