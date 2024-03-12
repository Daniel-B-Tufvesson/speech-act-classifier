"""
Evalaute the classifiers.
"""

import speechact.classifier.base as cb
import speechact.corpus as corp
import sklearn.metrics as metrics
import pandas as pd
    

def evaluate(corpus: corp.Corpus, classifier: cb.Classifier, labels: list[str],
             print_missclassified: tuple[str, str]|None=None,
             draw_conf_matrix=False):
    """
    Evaluate the classifier on the CoNNL-U corpus.
    """

    # Collect all the correct and predicted labels.
    all_correct_labels = []
    all_predicted_labels = []
    missclassified = []
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

                    missclassified.append(sentence.text)


    # Compute accuracy.
    accuracy = metrics.accuracy_score(y_true=all_correct_labels, 
                                      y_pred=all_predicted_labels)
    print(f'Accuracy: {accuracy}')

    # Get classification report.
    report = metrics.classification_report(y_true=all_correct_labels,
                                           y_pred=all_predicted_labels,
                                           zero_division=0,
                                           labels=labels
                                           )
    print('Classification report:')
    print(report)

    # Compute confusion matrix.
    conf_matrix = metrics.confusion_matrix(y_true=all_correct_labels,
                                           y_pred=all_predicted_labels,
                                           labels=labels)
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
        print(f'{len(missclassified)} "{print_missclassified[0]}" sentences missclassified as "{print_missclassified[1]}".')
        print('Printing missclassified sentences:')
        for sentence_text in missclassified:
            print(sentence_text)
    

def plot_confusion_matrix(confusion_matrix, labels: list[str]):
    import matplotlib.pyplot as plt

    display = metrics.ConfusionMatrixDisplay(confusion_matrix,
                                             display_labels=labels)
    
    display.plot(xticks_rotation='vertical')
    plt.show()