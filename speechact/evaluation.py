"""
Evalaute the classifiers.
"""

import speechact.classifier.base as cb
import speechact.corpus as corp
import sklearn.metrics as metrics
import numpy as np
import pandas as pd
from typing import Any

def evaluate(corpus: corp.Corpus, classifier: cb.Classifier, labels: list[str],
             print_missclassified: tuple[str, str]|None=None,
             draw_conf_matrix=False) -> dict[str, Any]:
    """
    Evaluate the classifier on the CoNNL-U corpus.
    """
    evaluation_results = {}

    # Collect all the correct and predicted labels.
    all_correct_labels = []
    all_predicted_labels = []
    misclassified = []
    for batch in corpus.batched_docs(100):

        # Get the correct labels for batch.
        correct_labels = [sentence.speech_act for sentence in batch.sentences]
        all_correct_labels += correct_labels

        # Do prediction.
        classifier.classify_document(batch)

        # Get the predicted labels for batch.
        predicted_labels = [sentence.speech_act for sentence in batch.sentences]
        all_predicted_labels += predicted_labels

        # Collect the missclassifed.
        if print_missclassified:
            for sentence, correct in zip(batch.sentences, correct_labels):
                if (correct == print_missclassified[0] and 
                    sentence.speech_act == print_missclassified[1]):

                    misclassified.append(sentence.text)
    
    evaluation_results['misclassified'] = misclassified


    # Compute accuracy.
    accuracy = metrics.accuracy_score(y_true=all_correct_labels, 
                                      y_pred=all_predicted_labels)
    evaluation_results['accuracy'] = accuracy
    print(f'Accuracy: {accuracy}')

    # Get classification report.
    report = metrics.classification_report(y_true=all_correct_labels,
                                           y_pred=all_predicted_labels,
                                           zero_division=0,
                                           labels=labels
                                           )
    print('Classification report:')
    print(report)

    # Get classification report as dictionary.
    report_dict = metrics.classification_report(y_true=all_correct_labels,
                                                y_pred=all_predicted_labels,
                                                zero_division=0,
                                                labels=labels,
                                                output_dict=True
                                                )
    evaluation_results['classification_report'] = report_dict

    # Compute confusion matrix.
    conf_matrix = metrics.confusion_matrix(y_true=all_correct_labels,
                                           y_pred=all_predicted_labels,
                                           labels=labels)
    evaluation_results['conf_matrix'] = conf_matrix
    conf_matrix_dframe = pd.DataFrame(conf_matrix,
                                      index = labels,
                                      columns = labels)
    print('Confusion matrix:')
    print(conf_matrix_dframe)

    # Plot the confusion matrix.
    if draw_conf_matrix:
        plot_confusion_matrix(conf_matrix, labels)

    # Print missclassified sentences.
    if print_missclassified:
        print()
        print(f'{len(misclassified)} "{print_missclassified[0]}" sentences missclassified as "{print_missclassified[1]}".')
        print('Printing missclassified sentences:')
        for sentence_text in misclassified:
            print(sentence_text)
    
    return evaluation_results
    

def plot_confusion_matrix(confusion_matrix, labels: list[str]):
    """
    Plot a confusion matrix and display it in a window. 
    """
    import matplotlib.pyplot as plt

    display = metrics.ConfusionMatrixDisplay(confusion_matrix,
                                             display_labels=labels)
    
    display.plot(xticks_rotation='vertical')
    plt.show()


def accuracy(corpus: corp.Corpus, classifier: cb.Classifier):
    all_correct_labels = []
    all_predicted_labels = []
    for batch in corpus.batched_docs(1000):
        # Get the correct labels for batch.
        correct_labels = [sentence.speech_act for sentence in batch.sentences]
        all_correct_labels += correct_labels

        # Do prediction.
        classifier.classify_document(batch)

        # Get the predicted labels for batch.
        predicted_labels = [sentence.speech_act for sentence in batch.sentences]
        all_predicted_labels += predicted_labels
    
    return metrics.accuracy_score(y_true=all_correct_labels, 
                                  y_pred=all_predicted_labels)


def get_misclassified(corpus: corp.Corpus, 
                      classifier: cb.Classifier,
                      expected_label: str,
                      predicted_label) -> list[str]:
    
    misclassified = []
    for batch in corpus.batched_docs(1000):
        # Get the correct labels for batch.
        correct_labels = [sentence.speech_act for sentence in batch.sentences]

        # Do prediction.
        classifier.classify_document(batch)

        for sentence, correct_label in zip(batch.sentences, correct_labels):
            if correct_label == expected_label and sentence.speech_act == predicted_label:
                misclassified.append(sentence.text)

    return misclassified


class TrainAccuracyHistory:
    def __init__(self, 
                 corpus: corp.Corpus, 
                 classifier: cb.Classifier, 
                 batch_size:int) -> None:
        self.corpus = corpus
        self.classifier = classifier
        self.batch_size = batch_size
        self.accuracies = []
        self.data_amount = []
    
    def compute_accuracy(self, batch_number: int):
        acc = accuracy(self.corpus, self.classifier)
        self.accuracies.append(acc)
        self.data_amount.append(batch_number * self.batch_size)
    