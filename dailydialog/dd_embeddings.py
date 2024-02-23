"""
Code for generating sentence embeddings from a from DailyDialog sentences.
"""

from typing import Generator
from typing import TextIO
from sentence_transformers import SentenceTransformer
import torch

def create_embeddings(source_file: str, target_file: str):
    print('Creating embeddings.')
    model = SentenceTransformer("all-MiniLM-L6-v2")

    target = open(target_file, mode='wt')

    # Create and save embedding for each sentence.
    n_embeddings = 0
    for sentence in read_sentences(source_file):
        n_embeddings += 1
        embedding = model.encode(sentence)
        embedding = embedding.tolist()
        target.write(str(embedding))
        target.write('\n')

        #torch.save(embedding, target)

        if n_embeddings % 100 == 0:
            print(f'Encoded {n_embeddings} so far...')
        
        if n_embeddings == 1000:
            break
    
    target.close()
    
    print(f'Created {n_embeddings}.')


def read_sentences(source_file: str) -> Generator[str, None, None]:
    """
    Yield each sentence in the source file. The source file should be formatted Daily Dialog file.
    """
    
    with open(source_file) as source:
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
    # create_embeddings('dailydialog/formatted data/dd_test.txt',
    #                   'dailydialog/embeddings/dd_test.embed')
    
    with open('dailydialog/embeddings/dd_test.embed') as source:
        for embedding in read_embeddings(source):
            print(embedding)
            input()
