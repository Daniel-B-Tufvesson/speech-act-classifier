"""
This script classifies sentences using the rule based classfier.
"""
from context import speechact
import speechact.classifier.rulebased as rb
import speechact.evaluation as evaluation
import speechact.corpus as corp

if __name__ == '__name__':
    classifier = rb.RuleBasedClassifier()
    corpus = corp.Corpus('data/annotated data/dev-set.connlu.bz2')
    evaluation.evaluate(corpus, classifier)