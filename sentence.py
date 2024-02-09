
from typing import Generator
import speech_act_classifier as sac

class Word:
    """
    A word (or token) consisting of a text string.
    """

    def __init__(self, text : str, 
                 pos : str|None = None) -> None:
        self.text = text
        self.pos = pos

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
        self.speech_act = None  # type: str|None
    
    def __str__(self) -> str:
        return repr(self.words)
    
    @property
    def word_count(self) :
        """
        The number of Words in this sentence. 
        """
        return len(self.words)

class Corpus:
    """
    A whole corpus consisting of a sequence of Sentences. The sentences are loaded
    on the go from a datx file.
    """ 

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
    
    def sentences(self) -> Generator[Sentence, None, None]:
        """
        Generator which yields each sentence in the corpus.
        """
        with open(self.file_name) as source:
            
            sentence = Sentence()
            line_number = 0
            
            for line in source:
                line_number += 1
                try: 

                    # Yield sentence on new line, and then create new sentence when continuing.
                    if line == '\n':

                        # Avoid yielding empty sentences.
                        # Sometimes an additional line may have snuck in.
                        if sentence.word_count > 0:
                            yield sentence
                            sentence = Sentence()

                    else:
                        line = line.strip()

                        # Parse line as speech act.
                        if line.startswith(sac.DAT2_SPEECH_ACT_TAG):
                            assert sentence.word_count > 0, 'sentence must have words.'

                            sentence.speech_act = Corpus.parse_line_as_speech_act(line)

                        # Parse line as ordinary word.
                        else:
                            sentence.words.append(Corpus.parse_line_as_word(line))
                    
                except RuntimeError as error:
                    raise RuntimeError(f'an error occurred while parsing line {line_number} ' \
                                       f'in file "{self.file_name}"') from error
                    

    @staticmethod
    def parse_line_as_word(line: str) -> Word:
        """
        Parse a datx line as a Word.
        """
        fields = line.split('\t')

        # Validate data.
        assert len(fields) == 3, f'line should contain 3 fields: "{line}"'
        assert fields[0].isdigit(), f'field [0] must be an integer: "{line}"'
        assert sac.validate_pos_string(fields[2]), f'invalid pos string "{fields[2]}" for field [2]: "{line}"' 

        return Word(text=fields[1], pos=fields[2])


    @staticmethod
    def parse_line_as_speech_act(line: str) -> str:
        """
        Parse a datx line as speech act string.
        """
        fields = line.split('\t')
        speech_act = fields[1]
        assert sac.validate_speech_act_string(speech_act), f'invalid speech act: {speech_act} for line: "{line}"'
        return speech_act
                

def test_corpus():
    # Test the corpus class on the familjeliv-adoption data.

    corpus = Corpus('processed data/familjeliv-adoption.dat1')
    for sentence in corpus.sentences():
        print(sentence)

if __name__ == '__main__':
    test_corpus()