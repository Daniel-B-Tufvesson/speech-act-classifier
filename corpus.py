import os
from typing import Generator
import bz2

class Sentence:

    def __init__(self, sentence_lines: list[str]) -> None:
        self.sentence_lines = sentence_lines
    
    def get_meta_data(self, key: str) -> str:
        _key = f'# {key} = '
        for line in self.sentence_lines:
            if line.startswith(_key):
                return line.removeprefix(_key).strip()
        
        raise ValueError(f'Cannot find meta-data with key "{key}" in {self.sentence_lines}')


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
            
                


class Corpus:
    """
    A corpus which loads sentences from CoNNL-U file.
    """

    def __init__(self, file_name: str, name: str) -> None:
        assert os.path.isfile(file_name), f'Corpus file does not exist: "{file_name}"'

        self.file_name = file_name
        self.name = name

        self._sentence_count = None


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

