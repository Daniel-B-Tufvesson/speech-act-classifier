"""
The main python file for this project.
"""

from enum import Enum

# Todo: remove.
DAT2_SPEECH_ACT_TAG = 'ACT'
"""The data tag indicating a speech act in the dat2 format."""

class SpeechActs(Enum):
    """
    The speech acts to classify.
    """
    
    ASSERTION = 'assertion'
    """Expresses an assertion."""

    QUESTION = 'question'
    """Expresses a question."""

    DIRECTIVE = 'directive'
    """Expresses a command."""

    EXPRESSIVE = 'expressive'
    """Expresses an emotion, value or surprise."""

    HYPOTHESIS = 'hypothesis'
    """Expresses an assumption or hypothesis."""

    @staticmethod
    def is_valid(speech_act: str) -> bool:
        return (speech_act == SpeechActs.ASSERTION.value or 
                speech_act == SpeechActs.QUESTION.value or
                speech_act == SpeechActs.DIRECTIVE.value or
                speech_act == SpeechActs.HYPOTHESIS.value)


class Genre(Enum):
    """
    The different genres which the data can belong to.
    """
    INTERNET_FORUM = 'internet_forum'


# UPOS tags from https://universaldependencies.org/u/pos/index.html
POS_TAGS = (
    'ADJ',   # Adjective
    'ADP',   # Adposition
    'ADV',   # Adverb
    'AUX',   # Auxiliary
    'CCONJ', # Coordinating conjunction
    'DET',   # Determiner
    'INTJ',  # Interjection
    'NOUN',  # Noun
    'NUM',   # Numerical
    'PART',  # Particle
    'PRON',  # Pronoun
    'PROPN', # Proper noun
    'PUNCT', # Punctuation
    'SCONJ', # Subordinating conjunction
    'SYM',   # Symbol
    'VERB',  # Verb
    'X'      # Other
)
"""
The POS-tags that are supported in this project. These are the Universal Dependencies POS-tags. 
"""

# SUC POS tags are taken from https://spraakbanken.gu.se/korp/markup/msdtags.html.
# Conversion is based on https://universaldependencies.org/tagset-conversion/sv-suc-uposf.html.
SUC_TO_UPOS = {
    'AB': 'ADVERB',  # Adverb
    'DT': 'DET',  # Determiner
    'HA': 'ADVERB',  # Interrogative/Relative Adverb 
    'HD': 'DET',  # Interrogative/Relative Determiner
    'HP': 'PRON',  # Interrogative/Relative Pronoun
    'HS': 'DET',  # Interrogative/Relative Possessive
    'IE': 'PART',  # Infinitive Marker
    'IN': 'INTJ',  # Interjection
    'JJ': 'ADJ',  # Adjective
    'KN': 'CCONJ',  # Conjunction
    'MAD': 'PUNCT',
    'MID': 'PUNCT',
    'NN': 'NOUN',  # Noun
    'PAD': 'PUNCT',
    'PC': 'VERB',  # Participle
    'PL': 'PART',  # Particle
    'PM': 'PROPN',  # Proper Noun
    'PN': 'PRON',  # Pronoun
    'PP': 'ADP',  # Preposition
    'PS': 'DET',  # Possessive
    'RG': 'NUM',  # Cardinal Number
    'RO': 'ADJ',  # Ordinal Number
    'SN': 'SCONJ',  # Subjunction
    'UO': 'X',  # Foreign Word
    'VB': 'VERB'   # Verb
}

def suc_to_upos(suc_pos: str) -> str:
    """
    Convert a SUC POS-tag to UPOS.
    """
    return SUC_TO_UPOS[suc_pos]

def suc_to_ufeats(suc_feats: str) -> str:
    """
    Convert a string of SUC morphological features to universal features.
    """
    raise NotImplementedError()

def validate_pos_string(pos: str) -> bool:
    """
    Check if the given string matches any of the defined POS tags.
    """
    return pos in POS_TAGS