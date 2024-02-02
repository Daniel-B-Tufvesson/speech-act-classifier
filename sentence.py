

class Word:
    """
    A word consisting of a text string.
    """

    def __init__(self, text : str) -> None:
        self.text = text

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return self.text


class Sentence:
    """
    A sentence consisting of a sequence of Words.
    """

    def __init__(self) -> None:
        self.words = []
    
    def __str__(self) -> str:
        return repr(self.words)

class Corpus:
    """
    A whole corpus consisting of a sequence of Sentences.
    """ 

    def __init__(self) -> None:
        pass