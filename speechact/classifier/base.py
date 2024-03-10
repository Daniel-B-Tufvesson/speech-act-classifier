"""
Base code for the classifier modules.
"""

import stanza.models.common.doc as doc
import abc

class Classifier(abc.ABC):
    """
    Base class for the speech act classifiers.
    """

    @abc.abstractmethod
    def classify_document(self, document: doc.Document):
        """
        Classify all the sentences in the document. This assigns each
        sentence with a value to the 'speech_act' property.
        """
        pass

    @abc.abstractmethod
    def classify_sentence(self, sentence: doc.Sentence):
        """
        Classify a single sentences. This assigns the sentence with a
        valiue to the 'speech_act' property.
        """
        pass