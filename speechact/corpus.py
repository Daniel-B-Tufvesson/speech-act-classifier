import os
import bz2
from typing import Generator
from typing import TextIO
import stanza.models.common.doc as doc

class Sentence:

    def __init__(self, sentence_lines: list[str]) -> None:
        self.sentence_lines = sentence_lines

    
    def get_meta_data(self, key: str) -> str:
        _key = f'# {key} = '
        for line in self.sentence_lines:
            if line.startswith(_key):
                return line.removeprefix(_key).strip()
        
        raise ValueError(f'Cannot find meta-data with key "{key}" in {self.sentence_lines}')
    

    def try_get_meta_date(self, key: str) -> str|None:
        """
        Try retrieving the meta data with the given key. If no value is found, None will be returned,
        instead of raising a ValueError.
        """
        try:
            return self.get_meta_data(key)
        except ValueError:
            return None


    def set_meta_data(self, key: str, value):
        _key = f'# {key} = '

        # Try replacing already existing meta-data.
        index = 0
        for line in self.sentence_lines:
            if line.startswith(_key):
                new_line = f'{_key}{value}\n'
                self.sentence_lines.pop(index)
                self.sentence_lines.insert(index, new_line)
                return
            else:
                index += 1
        
        # Insert new value if meta-data does not already exist.
        index = 0
        for line in self.sentence_lines:
            if not line.startswith('#'):
                new_line = f'{_key}{value}\n'
                self.sentence_lines.insert(index, new_line)
                break
            else:
                index += 1
            
    @property
    def sent_id(self) -> int:
        """
        The ID (sent_id) of the sentence. This assumes the ID is an integer, and won't work for 
        non-integer IDs. 
        """
        return int(self.get_meta_data('sent_id'))
    

    @property
    def speech_act(self) -> str:
        """
        The labeled speech act of the sentence.
        """
        return self.get_meta_data('speech_act')
    

    @property
    def text(self):
        """
        The text of the sentence as a string.
        """
        return self.get_meta_data('text')

    
    def write(self, target: TextIO):
        """
        Write this sentence to a target file as CoNLL-U. This also writes an additional newline at
        the end.
        """
        target.writelines(self.sentence_lines)
        target.write('\n')


class Corpus:
    """
    A corpus which loads sentences from CoNLL-U file (bz2 compressed).
    """

    def __init__(self, file_name: str, name: str|None = None) -> None:
        assert os.path.isfile(file_name), f'Corpus file does not exist: "{file_name}"'

        # Get name from filename instead.
        if name == None:
            name = os.path.basename(file_name).removesuffix('.bz2').removesuffix('.conllu')

        self.file_name = file_name
        self.name = name
        self._sentence_count = None
        self._first_id = None
        self._last_id = None


    def sentences(self) -> Generator[Sentence, None, None]:
        with bz2.open(self.file_name, mode='rt') as source:
            lines = []
            for line in source:

                # Empty line indicates end of sentence, so yield it.
                if line == '\n' and len(lines) != 0:
                    yield Sentence(lines)
                    lines = []
                else:
                    lines.append(line)
    
    @property
    def sentence_count(self) -> int:
        if self._sentence_count is None:
            count = 0
            for _ in self.sentences():
                count += 1
            self._sentence_count = count
        
        return self._sentence_count

    @property
    def first_id(self) -> int:
        """
        The ID (sent_id) of the first sentence.
        """
        if self._first_id == None:
            first_sentence = next(self.sentences())
            self._first_id = first_sentence.sent_id

        return self._first_id

    @property
    def last_id(self) -> int:
        """
        The ID (sent_id) of the first sentence.
        """
        if self._last_id == None:
            self._last_id = self.last_sentence.sent_id

        return self._last_id

    @property
    def last_sentence(self) -> Sentence:
        """
        The last sentence in the corpus.
        """
        last_sent = None
        for sent in self.sentences():
            last_sent = sent

        if last_sent == None:
            raise RuntimeError(f'Corpus has no sentences: f{self.file_name}')
        
        return last_sent

    def find_sentence_with_id(self, sent_id: int) -> Sentence|None:
        """
        Find the sentence with the sentence ID.
        """
        for sentence in self.sentences():
            if sentence.sent_id == sent_id:
                return sentence
        
        return None
    
    def batched_docs(self, batch_size) -> Generator[doc.Document, None, None]:
        """
        Yield batches of stanza documents of this corpus.
        """
        import speechact.preprocess as pre
        with bz2.open(self.file_name, mode='rt') as source:
            for batch in pre.read_batched_doc(source, batch_size):
                yield batch
    
    def stanza_sentences(self) -> Generator[doc.Sentence, None, None]:
        """
        Yield stanza sentences of this corpus.
        """
        for batch in self.batched_docs(1000):
            for sentence in batch.sentences:
                yield sentence
        
    


def load_corpora_from_data_file(data_file: str) -> list[Corpus]:
    """
    Load several corpora from a text file listing the file names of each corpus.
    """
    import speechact.preprocess as dat
    source_files = dat.lines(data_file)
    return [Corpus(file, file.split('/')[-1].removesuffix('.connlu.bz2').removesuffix('-100k').removesuffix('-500k')) for file in source_files]


def find_sentence_with_id(corpora: list[Corpus], sent_id: int) -> Sentence|None:
    """
    Find the sentence with the given ID among a list of corpora. It is assumed that a corpus has
    the sentence if its ID is >= the first ID and <= the last ID.
    """
    for corpus in corpora:

        if sent_id < corpus.first_id:
            continue

        if sent_id > corpus.last_id:
            continue

        return corpus.find_sentence_with_id(sent_id)