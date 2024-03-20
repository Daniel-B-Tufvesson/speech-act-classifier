"""
This script classifies sentences using the rule based classfier.
"""
from context import speechact
import speechact.classifier.algorithmic as algo
import speechact.classifier.base as b
import speechact.evaluation as evaluation
import speechact.corpus as corp
import speechact.annotate as annotate
import speechact.classifier.rulebased as rule

if __name__ == '__main__':
    #corpus = corp.Corpus('data/annotated data/dev-set-sentiment.conllu.bz2')
    corpus = corp.Corpus('data/annotated data/dev-set.conllu.bz2')
    labels = annotate.SpeechActLabels.get_labels()

    print()

    # Evaluate baseline MFC classifier.
    most_frequent = b.MostFrequentClassifier()
    most_frequent.train(corpora=[corpus])
    print(f'Most frequenct class is "{most_frequent.most_common}"')
    print()
    print('Baseline results:')
    evaluation.evaluate(corpus, most_frequent, labels,
                        draw_conf_matrix=False)
    print()

    # # Evaluate punctuation classifier.
    punctuation_classifier = algo.PunctuationClassifier()
    print('Punctuation classifier results:')
    evaluation.evaluate(corpus, punctuation_classifier, labels,
                        draw_conf_matrix=False)
    print()

    # # Evaluate clause classifier.
    # clause_classifier = algo.ClauseClassifier()
    # print('Clause classifier results:')
    # evaluation.evaluate(corpus, clause_classifier, labels, 
    #                     #print_missclassified=('assertion', 'none'),
    #                     draw_conf_matrix=False)
    # print()

    # # Evaluate algorithmic classifier.
    # algo_classifier = algo.RuleBasedClassifier()
    # print('Algorithmic classifier results:')
    # evaluation.evaluate(corpus, algo_classifier, labels,
    #                     #print_missclassified=('directive', 'assertion'),
    #                     draw_conf_matrix=False)

    # # Evaluate rule based classifier.
    # rule_classifer = rule.RuleBasedClassifier(ruleset_file='models/ruleset_1.json')
    # print('Rule-based classifier results:')
    # evaluation.evaluate(corpus, rule_classifer, labels,
    #                     #print_missclassified=('directive', 'assertion'),
    #                     draw_conf_matrix=False)
    
    # Evaluate trainable rule based classifier.
    trainable_rule_classifier = rule.TrainableClassifier()
    test_corpus = corp.Corpus('data/annotated data/dev-set-test.conllu.bz2')
    train_corpus = corp.Corpus('data/annotated data/dev-set-train.conllu.bz2')
    trainable_rule_classifier.train(test_corpus)
    trainable_rule_classifier.save_rules('models/trained_rules.json')
    print('Trainable rule-based classifier results:')
    evaluation.evaluate(train_corpus, trainable_rule_classifier, labels,
                        print_missclassified=('directive', 'assertion'),
                        draw_conf_matrix=True)
