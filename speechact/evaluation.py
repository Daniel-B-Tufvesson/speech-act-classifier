"""
Evalaute the classifiers.
"""

import speechact.classifier.base as cb
import speechact.corpus as corp
    

def evaluate(corpus: corp.Corpus, classifier: cb.Classifier):
    """
    Evaluate the classifier on the CoNNL-U corpus.
    """
    correct = 0
    total = 0
    for batch in corpus.batched_docs(100):
        correct_labels = [sentence.speech_act for sentence in batch.sentences]
        classifier.classify_document(batch)

        # Count correct labels.
        for correct_label, sentence in zip(correct_labels, batch.sentences):
            assert sentence.speech_act != None, f'Sentence does not have a speech act: {sentence.sent_id}'

            total += 1
            if sentence.speech_act == correct_label:
                correct += 1
    
    # Compute accuracy.
    accuracy = correct / total if total > 0 else 0
    
    print(f'accuracy: {accuracy}')