import stanza.models.common.doc as doc


def set_sentence_speech_act(sentence: doc.Sentence, speech_act: str):
    """
    Set the speech act for the sentence. 
    """
    sentence._speech_act = speech_act  # type: ignore

# Add speech act property to Stanza Sentence class.
doc.Sentence.add_property(
    'speech_act', 
    default=None,
    getter=lambda self: self._speech_act,
    setter=set_sentence_speech_act
    )