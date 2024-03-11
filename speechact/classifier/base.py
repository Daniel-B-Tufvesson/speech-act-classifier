"""
Base code for the classifier modules.
"""

import stanza.models.common.doc as doc
import abc
import speechact.corpus as corp
import collections as coll

class Classifier(abc.ABC):
    """
    Base class for the speech act classifiers.
    """

    def classify_document(self, document: doc.Document):
        """
        Classify all the sentences in the document. This assigns each
        sentence with a value to the 'speech_act' property.
        """
        for sentence in document.sentences:
            self.classify_sentence(sentence)

    @abc.abstractmethod
    def classify_sentence(self, sentence: doc.Sentence):
        """
        Classify a single sentences. This assigns the sentence with a
        valiue to the 'speech_act' property.
        """
        pass


class MostFrequentClassifier(Classifier):
    """
    The Most Frequent Class Classifier computes which speech act is most common 
    and classifies all sentences with that. This classifier is only used as a
    baseline.
    """

    def __init__(self) -> None:
        super().__init__()
        self.class_frequencies = coll.Counter()
        self.most_common = None


    def train(self, corpora: list[corp.Corpus], batch_size=100):
        """
        Train the classifier by computing the most frequent speech act.
        Note that this does not reset the previous training.
        """
        for corpus in corpora:
            for batch in corpus.batched_docs(batch_size):
                for sentence in batch.sentences:
                    assert sentence.speech_act != None, f'Sentence does not have a speech act {sentence.sent_id}'

                    self.class_frequencies[sentence.speech_act] += 1
        
        self.most_common = self.class_frequencies.most_common()[0][0]
    

    def classify_sentence(self, sentence: doc.Sentence):
        """
        Classify the sentence with the most frequent speech act.
        """
        sentence.speech_act = self.most_common  # type: ignore
