"""
A neural classifier using SBERT embeddings to classify speech acts.
"""

import dd_embeddings as em
import bz2


def train(train_data_file: str, save_model_to: str):
    for epoch in range(2):
        source = bz2.open(train_data_file)
        


def evaluate(test_data_file: str):
    pass


if __name__ == '__main__':
    pass