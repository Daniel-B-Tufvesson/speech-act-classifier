"""
Evalaute the classifiers.
"""

import speechact.classifier.base as cb
import speechact.corpus as corp
import sklearn.metrics as metrics
    

def evaluate(corpus: corp.Corpus, classifier: cb.Classifier, labels: list[str],
             print_classifications=False):
    """
    Evaluate the classifier on the CoNNL-U corpus.
    """
    all_correct_labels = []
    all_predicted_labels = []
    # correct = 0
    # total = 0
    for batch in corpus.batched_docs(100):

        # Get the correct labels for batch.
        correct_labels = [sentence.speech_act for sentence in batch.sentences]
        all_correct_labels += correct_labels

        # Do prediction.
        classifier.classify_document(batch)

        # Get the predicted labels for batch.
        predicted_labels = [sentence.speech_act for sentence in batch.sentences]
        all_predicted_labels += predicted_labels


    #     # Count labels.
    #     for correct_label, sentence in zip(correct_labels, batch.sentences):
    #         assert sentence.speech_act != None, f'Sentence does not have a speech act: {sentence.sent_id}'

    #         if print_classifications: 
    #             print(f'Predicted: {sentence.speech_act}, correct: {correct_label}, sentence: "{sentence.text}"')

    #         total += 1

    #         # Count correct labels.
    #         if sentence.speech_act == correct_label:
    #             correct += 1
    
    # # Compute accuracy.
    # accuracy = correct / total if total > 0 else 0
    
    # print('EVALUATION RESULTS')
    # print(f'Classified: {total} sentences.')
    # print(f'Accuracy: {accuracy}')

    report = metrics.classification_report(y_true=all_correct_labels,
                                           y_pred=all_predicted_labels,
                                           zero_division=0,
                                           labels=labels
                                           )
    
    print('Classification report:')
    print(report)

