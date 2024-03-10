"""
An algorithmic speech act classifier. This uses syntactical information to classify sentences with speech acts.
"""


import stanza.models.common.doc as doc
import speechact.preprocess as preprocess
from . import base
import speechact.annotate as annotate

class RuleBasedClassifier(base.Classifier):
    
    def classify_document(self, document: doc.Document):
        for sentence in document.sentences:
            self.classify_sentence(sentence)

    def classify_sentence(self, sentence: doc.Sentence):
        # print('classify: ', sentence.text)

        # if is_FA_clause(sentence):
        #     print('FA clause!')

        # elif is_AF_clause(sentence):
        #     print('AF clause!')

        # else:
        #     print('Not AF nor FA!')

        speech_act = classify_from_punctation(sentence)
        sentence.speech_act = speech_act  # type: ignore


def classify_from_punctation(sentence: doc.Sentence) -> str:
    """
    Classify the sentence based on the punctation.
    """
    punctation = get_punctation(sentence)

    if punctation == '.':
        return annotate.SpeechActLabels.ASSERTION.value
    elif punctation == '?':
        return annotate.SpeechActLabels.QUESTION.value
    elif punctation == '!':
        return annotate.SpeechActLabels.EXPRESSIVE.value
    else:
        return annotate.SpeechActLabels.NONE.value


def get_punctation(sentence: doc.Sentence) -> str|None:
    """
    Get the major delimiting punctation of the sentence, e.g. '.', '?', '!',
    or nothing.
    """
    last_word = sentence.words[-1]
    if last_word.text == '.':
        return '.'
    elif last_word.text == '!':
        return '!'
    elif last_word.text == '?':
        return '?'
    else:
        return None


def is_FA_clause(sentence : doc.Sentence) -> bool:
    finite_verb = get_finite_verb(sentence)
    if finite_verb is None:
        print(f'Sentence lacks finite verb: {sentence.sent_id} "{sentence.text}"')
        return False


    return False


def is_AF_clause(sentence : doc.Sentence) -> bool:
    return False


def get_head(sentence : doc.Sentence) -> doc.Word:
    """
    Retrieve the head word in the sentence.
    """
    for word in sentence.words:
        if word.head == 0:
            return word
    
    raise ValueError('Sentence lacks head.')


def get_finite_verb(sentence : doc.Sentence) -> doc.Word|None:
    """
    Retrieve the finite verb in the sentence. The finite verb must be the head in the sentence.
    """
    head = get_head(sentence)

    # Make sure head is a verb.
    if head.pos != 'VERB':
        return None
    
    # Make sure finite verb.
    if head.feats == None or 'VerbForm=Fin' not in head.feats:
        return None

    return head


def get_subject(sentence: doc.Sentence) -> doc.Word|None:
    pass


def get_clause_base(sentence: doc.Sentence) -> list[doc.Word]:
    """
    Retrieve the clause base (swe: satsbas) of the sentence, i.e. the words before the finite verb.
    """
    finite_verb = get_finite_verb(sentence)
    if finite_verb is None:
        raise ValueError('Sentence does not have a finite verb')
    
    clause_base = []
    for word in sentence.words:
        if word.id < finite_verb.id:
            clause_base.append(word)
    
    return clause_base


