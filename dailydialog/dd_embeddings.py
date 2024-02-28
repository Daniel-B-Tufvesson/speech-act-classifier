"""
Code for generating sentence embeddings from a from DailyDialog sentences.
"""

from typing import Generator
from typing import TextIO
from typing import Iterable
from sentence_transformers import SentenceTransformer
import torch
import bz2

def create_embeddings_from_file(source_file: str, target_file: str, compress_target = True):
    """
    Create embeddings of DailyDialog sentences from the source file. The embeddings
    are then written to the target file.
    """
    source = open(source_file, mode='rt')
    if compress_target: target = bz2.open(target_file, mode='wt')
    else: target = open(target_file, mode='wt')

    try: 
        sentences = read_sentences(source)
        create_embeddings(sentences, target)
    finally:
        source.close()
        target.close()


def create_embeddings(sentences: Iterable[str], target: TextIO):
    """
    Create embeddings of the sentences and write them to the target.
    """
    print('Creating embeddings.')
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Create and save embedding for each sentence.
    n_embeddings = 0
    for sentence in sentences:
        n_embeddings += 1
        embedding = model.encode(sentence)
        embedding = embedding.tolist()
        target.write(str(embedding))
        target.write('\n')

        if n_embeddings % 100 == 0:
            print(f'Encoded {n_embeddings} so far...')
    
    print(f'Created {n_embeddings}.')


def read_sentences(source: TextIO) -> Generator[str, None, None]:
    """
    Yield each sentence in the text source. The source should be formatted Daily Dialog file.
    """
    
    prev_line = None
    for line in source:

        # Yield sentence.
        if prev_line == '\n':
            yield line

        prev_line = line


def read_embeddings(source: TextIO) -> Generator[torch.Tensor, None, None]:
    """
    Yield each embedding in the text source as a tensor. The embeddings in the source should be
    separated by a newline. 
    """
    for line in source:
        tensor = torch.tensor(eval(line))
        yield tensor


if __name__ == '__main__':
    create_embeddings_from_file('dailydialog/formatted data/dd_train.txt',
                                'dailydialog/embeddings/dd_train.embed')
    
    # with open('dailydialog/embeddings/dd_test.embed') as source:
    #     for embedding in read_embeddings(source):
    #         print(embedding)
    #         input()
    
