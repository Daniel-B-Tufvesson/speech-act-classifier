"""
An algorithmic speech act classifier. This uses syntactical information to classify sentences with speech acts.
"""


import stanza.models.common.doc as doc
import speechact.preprocess as preprocess
from . import base
import speechact.annotate as annotate
import enum

SUBJECT_RELS = {
    'csubj', 
    'csubj:outer', 
    'csubj:pass',
    'nsubj',
    'nsubj:outer',
    'nsubj:pass'
    }

INTERROGATIVE_PRONOUNS = {'vilken', 'vilkendera', 'hurdan', 'vem', 'vad'}

INTERROGATIVE_ADVERBS = {'var', 'vart', 'när', 'hur'}

class ClauseType(enum.StrEnum):
    """
    The main clause types a sentence can have, including 'none'.
    """

    DECLARATIVE = 'declarative'
    """
    Typically expresses an assertion.
    """

    ROGATIVE = 'ROGATIVE'
    """
    Typically expresses a yes or no question.
    """

    QUESITIVE = 'quesitive'
    """
    Typically expresses an open question.
    """

    DIRECTIVE = 'directive'
    """
    Typically expresses a directive (request, command).
    """

    EXPRESSIVE = 'expressive'
    """
    Typically expresses an expressive (emotion, feeling, value).
    """

    DESIDERATIVE = 'desiderative'
    """
    Typically expresses a wish.
    """

    SUPPOSITIVE = 'suppositive'
    """
    Typically expresses an assumption or hypothesis.
    """

    NONE = 'none'
    """
    The sentence does not have any of the speech acts.
    """

# Map clause types to speech acts.
clause_type_to_speech_acts = {
    ClauseType.DECLARATIVE: annotate.SpeechActLabels.ASSERTION,
    ClauseType.DIRECTIVE: annotate.SpeechActLabels.DIRECTIVE,
    ClauseType.ROGATIVE: annotate.SpeechActLabels.QUESTION,
    ClauseType.QUESITIVE: annotate.SpeechActLabels.QUESTION,
    ClauseType.EXPRESSIVE: annotate.SpeechActLabels.EXPRESSIVE,
    ClauseType.DESIDERATIVE: annotate.SpeechActLabels.EXPRESSIVE,
    ClauseType.SUPPOSITIVE: annotate.SpeechActLabels.HYPOTHESIS,
    ClauseType.NONE: annotate.SpeechActLabels.NONE
}

class PunctuationClassifier(base.Classifier):
    """
    Classify speech acts purely from punctuation.
    """

    def classify_sentence(self, sentence: doc.Sentence):
        speech_act = classify_from_punctation(sentence)
        sentence.speech_act = speech_act    # type: ignore

class ClauseClassifier(base.Classifier):
    """
    Classify speech acts purely from the clause type of the sentence.
    """

    def classify_sentence(self, sentence: doc.Sentence):
        clause_type = get_clause_type(sentence)
        speech_act = clause_type_to_speech_acts[clause_type].value
        sentence.speech_act = speech_act  # type: ignore



class RuleBasedClassifier(base.Classifier):
    
    def classify_document(self, document: doc.Document):
        for sentence in document.sentences:
            self.classify_sentence(sentence)

    def classify_sentence(self, sentence: doc.Sentence):
        speech_act = self.get_speech_act(sentence).value
        sentence.speech_act = speech_act  # type: ignore

    def get_speech_act(self, sentence: doc.Sentence) -> annotate.SpeechActLabels:

        # Try to classify based on clause type.
        clause_type = get_clause_type(sentence)
        if clause_type != ClauseType.NONE:
            return clause_type_to_speech_acts[clause_type]

        # Classify as assertion if sentence is a noun phrase.
        if is_sentence_np(sentence):
            return annotate.SpeechActLabels.ASSERTION
        
        # Unknown speech act.
        return annotate.SpeechActLabels.NONE


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
        return annotate.SpeechActLabels.ASSERTION.value


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


def get_clause_type(sentence: doc.Sentence) -> ClauseType:
    """
    Compute the clause type of the sentence.
    """

    if is_AF_clause(sentence):
        if has_expressive_in_base(sentence):
            return ClauseType.EXPRESSIVE
        elif starts_with_subjunctive(sentence, 'att'):
            return ClauseType.EXPRESSIVE
        elif starts_with_subjunctive(sentence, 'så'):
            return ClauseType.EXPRESSIVE
        elif starts_with(sentence, 'bara'):
            return ClauseType.DESIDERATIVE
        elif starts_with(sentence, 'om') or starts_with(sentence, ['tänk', 'om']):
            return ClauseType.SUPPOSITIVE
    
    elif is_FA_clause(sentence):
        if has_clause_base(sentence):
            if has_interrogative_base(sentence):
                return ClauseType.QUESITIVE
            else:
                return ClauseType.DECLARATIVE
        else:
            if starts_with_finite_verb(sentence):
                if get_subject(sentence) != None:
                    return ClauseType.ROGATIVE
                else:
                    return ClauseType.DIRECTIVE
            else:
                return ClauseType.DESIDERATIVE

    # Sentence does not have any known clause type.
    return ClauseType.NONE


def is_FA_clause(sentence : doc.Sentence) -> bool:
    finite_verb = get_finite_verb(sentence)
    if finite_verb is None:
        return False

    subject = get_subject(sentence)
    if subject == None:
        return True # To make this work, we assume a subject-less sentence is AF.

    # Subject should be after the finite verb.
    if subject.id > finite_verb.id:
        return True
    
    # Or the entire clause base should be the subject.
    clause_base = get_clause_base(sentence)

    # fixme: what if the subject is larger than one word?
    if len(clause_base) == 1 and clause_base[0] == subject:
        return True
    
    return False


def is_AF_clause(sentence : doc.Sentence) -> bool:
    finite_verb = get_finite_verb(sentence)
    if finite_verb is None:
        return False

    subject = get_subject(sentence)
    if subject == None:
        return False

    if subject.id > finite_verb.id:
        return False
    
    clause_base = get_clause_base(sentence)
    if len(clause_base) == 1 and clause_base[0] == subject:
        return False
    
    return True


def get_head(sentence : doc.Sentence) -> doc.Word:
    """
    Retrieve the head word in the sentence.
    """
    for word in sentence.words:
        if word.head == 0:
            return word
    
    raise ValueError('Sentence lacks a head.')


def get_finite_verb(sentence : doc.Sentence) -> doc.Word|None:
    """
    Retrieve the finite verb in the sentence. The finite verb must be the head in the 
    sentence.
    """
    head = get_head(sentence)

    # Make sure head is a verb.
    if head.pos != 'VERB':
        return None
    
    # Make sure finite verb.
    if head.feats == None or 'VerbForm=Fin' not in head.feats:
        return None

    return head


def starts_with_finite_verb(sentence: doc.Sentence) -> bool:
    """
    Check if the sentence starts with the finite verb.
    """
    finite_verb = get_finite_verb(sentence)

    if finite_verb == None:
        return False
    
    return finite_verb.id == 1

def get_subject(sentence: doc.Sentence) -> doc.Word|None:
    """
    Retrieve the subject of the sentence. This is a dependent of the sentence's head. 
    """

    # Find finite verb.
    finite_verb = get_finite_verb(sentence)
    if finite_verb == None:
        return None

    # Find the subject of the finite verb.
    for word in sentence.words:
        if word.head == finite_verb.id and word.deprel in SUBJECT_RELS:
            return word
    
    # Todo: fix subject relation for copular verbs.
    
    # No subject found.
    return None

def has_clause_base(sentence: doc.Sentence) -> bool:
    """
    Check if the sentence has a clause base. 
    """
    return len(get_clause_base(sentence)) > 0


def get_clause_base(sentence: doc.Sentence) -> list[doc.Word]:
    """
    Retrieve the clause base (swe: satsbas) of the sentence, i.e. the words before the 
    finite verb.
    """
    finite_verb = get_finite_verb(sentence)
    if finite_verb is None:
        raise ValueError('Sentence does not have a finite verb')
    
    clause_base = []
    for word in sentence.words:
        if word.id < finite_verb.id:
            clause_base.append(word)
    
    return clause_base


def has_expressive_in_base(sentence: doc.Sentence) -> bool:
    """
    Check if there is an expressive clause part in the clause base of the sentence.
    """
    clause_base = get_clause_base(sentence)
    if len(clause_base) == 0:
        return False

    # Check if base starts with adverbial phrase.
    if clause_base[0].text.lower() in ('vad', 'så'):
        return True

    # Todo: fix remaining variations of an expressive part.

    return False


def has_interrogative_base(sentence: doc.Sentence) -> bool:
    """
    Check if the clause base in the sentence is on interrogative form.
    """
    first_word_text = sentence.words[0].text.lower()
    return first_word_text in INTERROGATIVE_ADVERBS or first_word_text in INTERROGATIVE_PRONOUNS


def starts_with_subjunctive(sentence: doc.Sentence, word: str) -> bool:
    """
    Check if the sentence starts with the given subjunctive word.
    """
    # See https://universaldependencies.org/sv/pos/SCONJ.html

    first_word = sentence.words[0]

    # Check that the word matches.
    if first_word.text.lower() != word:
        return False
    
    # Check that it is subjunctive.
    return first_word.pos == 'SCONJ'


def starts_with(sentence: doc.Sentence, words: str|list[str]) -> bool:
    """
    Check if the sentence starts with the given word.
    """

    assert type(words) == str or type(words) == list

    # Check single word.
    if type(words) == str:
        first_word_text = sentence.words[0].text.lower()
        return first_word_text == words
    
    # Check several words.
    else:
        assert len(words) > 0

        # Check if the sentence starts with all the words.
        for index, word in enumerate(words):
            word_text = sentence.words[index].text.lower()
            if word_text != word:
                return False
            
        # Sentence starts with the words.
        return True
        

def is_sentence_np(sentence: doc.Sentence) -> bool:
    """
    Check if the sentence is a noun phrase.
    """
    # We assume it's an NP if the head word is a noun or proper noun.
    head_word = get_head(sentence)
    return head_word.pos == 'NOUN'# or head_word.pos == 'PROPN'

