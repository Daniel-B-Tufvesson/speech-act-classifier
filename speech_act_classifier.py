"""
The main python file for this project.
"""


DAT2_SPEECH_ACT_TAG = 'ACT'
"""The data tag indicating a speech act in the dat2 format."""

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


# UD-POS tags from https://universaldependencies.org/u/pos/index.html
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
The POS-tags that are supported in this project. These are the 
Universal Dependencies POS-tags. 
"""

# SUC POS tags are taken from https://spraakbanken.gu.se/korp/markup/msdtags.html
# SUC_TO_UD_POS_TAGS = {
#     'AB': 'ADVERB',  # Adverb
#     'DT': 'DET',  # Determiner
#     'HA': 'ADVERB',  # Interrogative/Relative Adverb 
#     'HD': 'DET',  # Interrogative/Relative Determiner
#     'HP': 'PRON',  # Interrogative/Relative Pronoun
#     'HS': '????????',  # Interrogative/Relative Possessive
#     'IE': '',  # Infinitive Marker
#     'IN',  # Interjection
#     'JJ',  # Adjective
#     'KN',  # Conjunction
#     'NN',  # Noun
#     'PC',  # Participle
#     'PL',  # Particle
#     'PM',  # Proper Noun
#     'PN',  # Pronoun
#     'PP',  # Preposition
#     'PS',  # Possessive
#     'RG',  # Cardinal Number
#     'RO',  # Ordinal Number
#     'SN',  # Subjunction
#     'UO',  # Foreign Word
#     'VB'   # Verb
# }


def validate_pos_string(pos: str) -> bool:
    """
    Check if the given string matches any of the defined POS tags.
    """
    return pos in POS_TAGS