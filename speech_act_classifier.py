"""
The main python file for this project.
"""

from enum import Enum

# Todo: remove.
DAT2_SPEECH_ACT_TAG = 'ACT'
"""The data tag indicating a speech act in the dat2 format."""

# Todo: rename to speech act names, and not clause type names.
# Todo: move to enum.
TYPE_ASSERTIVE = 'assertive'
"""Expresses an assertion."""

TYPE_INTERROGATIVE = 'interrogative'
"""Expresses a question."""

TYPE_DIRECTIVE = 'directive'
"""Expresses a command."""

TYPE_EXPRESSIVE = 'expressive'
"""Expresses an emotion, value or surprise."""

TYPE_SUPPOSITIVE = 'suppositive'
"""Expresses an assumption or hypothesis."""

def validate_speech_act_string(speech_act: str) -> bool:
    """
    Check if the given string matches any of the defined speech acts.
    """
    return (speech_act == TYPE_ASSERTIVE or speech_act == TYPE_INTERROGATIVE or 
            speech_act == TYPE_DIRECTIVE or speech_act == TYPE_EXPRESSIVE or 
            speech_act == TYPE_SUPPOSITIVE)


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