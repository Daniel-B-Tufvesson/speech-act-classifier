"""
The main python file for this project.
"""

import enum
import stanza.models.common.doc as doc

def get_sentence_property(sentence: doc.Sentence, key: str) -> str|None:
    """
    Get a property from a Stanza Sentence. This property is stored as a
    comment in the sentence.
    """
    # Find the comment matching the key.
    key_str = f'# {key} = '
    for comment in sentence.comments:
        if comment.startswith(key_str):
            return comment.removeprefix(key_str)
    
    return None


def set_sentence_property(sentence: doc.Sentence, key: str, value: str):
    """
    Set a property from a Stanza Sentence. This property is stored as a
    comment in the sentence.
    """
    property_comment = f'# {key} = {value}'
    for comment_index, comment in enumerate(sentence.comments):
        if comment.startswith(f'# {key} = '):
            sentence.comments[comment_index] = property_comment
            break
    else:
        sentence.comments.append(property_comment)


def set_sentence_speech_act(sentence: doc.Sentence, speech_act: str):
    """
    Set the speech act for the sentence. 
    """
    sentence._speech_act = speech_act  # type: ignore


def get_sentence_speech_act(sentence: doc.Sentence):
    """
    Get the speech act for the sentence.
    """
    pass

# Add speech act property to Stanza Sentence class.
doc.Sentence.add_property(
    'speech_act', 
    default=None,
    getter=lambda sentence: get_sentence_property(sentence, 'speech_act'),
    setter=lambda sentence, value: set_sentence_property(sentence, 'speech_act', value)
    )

class SpeechActs(enum.Enum):
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


class Genre(enum.Enum):
    """
    The different genres which the data can belong to.
    """
    INTERNET_FORUM = 'internet_forum'

    INTERNET_BLOG = 'internet_blog'

    NEWS_ARTICLE = 'news_article'

    FICTION_NOVEL = 'fiction_novel'


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


class Sentiment(enum.StrEnum):
    """
    The three possible sentiments in sentiment analysis.
    """
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    NEUTRAL = 'neutral'

    @staticmethod
    def is_valid(sentiment: str) -> bool:
        return (sentiment == Sentiment.POSITIVE or 
                sentiment == Sentiment.NEGATIVE or
                sentiment == Sentiment.NEUTRAL)

