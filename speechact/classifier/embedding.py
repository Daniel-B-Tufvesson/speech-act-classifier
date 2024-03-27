"""
Classify speech acts from sentence embeddings, e.g. SBERT embeddings.
"""

from . import base
import stanza.models.common.doc as doc
import speechact.annotate as anno
import speechact.corpus as corp
import speechact.preprocess as pre
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as tdat
import sentence_transformers as stf

SPEECH_ACTS_TENSORS = {
        anno.SpeechActLabels.ASSERTION:  torch.tensor([1, 0, 0, 0, 0], dtype=torch.int),
        anno.SpeechActLabels.QUESTION:   torch.tensor([0, 1, 0, 0, 0], dtype=torch.int),
        anno.SpeechActLabels.DIRECTIVE:  torch.tensor([0, 0, 1, 0, 0], dtype=torch.int),
        anno.SpeechActLabels.EXPRESSIVE: torch.tensor([0, 0, 0, 1, 0], dtype=torch.int),
        anno.SpeechActLabels.HYPOTHESIS: torch.tensor([0, 0, 0, 0, 1], dtype=torch.int),
    }
"""The speech act labels mapped to tensors."""


def create_embeddings(source_file: str, target_file: str, print_progress=False):
    """
    Create an embedding file from a CoNLL-U corpus. An embedding is computed for each sentence. 
    These are Swedish SBERT embeddings.
    """

    if print_progress: print(f'Creating embeddings from "{source_file}" to "{target_file}"')

    source_corpus = pre.open_corpus(source_file)
    target = pre.open_write(target_file)

    if print_progress: print('Loading SBERT model...')
    # Load model.
    model = stf.SentenceTransformer('KBLab/sentence-bert-swedish-cased', device='mps')
    if print_progress: print('SBERT loaded')

    # Compute and write embeddings.
    sentence_count = 0
    for sentence in source_corpus.sentences():
        sent_id = sentence.sent_id
        speech_act = sentence.speech_act

        embedding = model.encode(sentence.text).tolist()
        embedding_str = ', '.join(str(value) for value in embedding)

        target.write(f'{sent_id}\t{speech_act}\t{embedding_str}\n')

        sentence_count += 1
        if print_progress and sentence_count % 100 == 0: 
            print(f'Computed {sentence_count} sentence embeddings.')
    
    target.close()

    if print_progress: print(f'Complete. Computed {sentence_count} sentence embeddings.')
    

class EmbeddingDataset(tdat.Dataset):
    """
    Loads a data set from an embedding file.
 
    In the file, ach line represents a sentence, and consists of a sentence ID (an int), 
    the speech act label (a string), and an embedding (a string of comma separated float 
    values). These three fields are separated by tabs.
    """
    # Example of data format:
    # Sentence-ID   Speech-Act    Embedding
    # 390134        assertion     0.4213, -0.3124, 0.2313, ..., 0.431
    # 3123          expressive    0.3124, -0.3445, 0.9292, ..., 0.32144

    SENT_ID = 'sent id'
    SPEECH_ACT_LABEL = 'speech act'
    EMBEDDING = 'embedding'

    def __init__(self, embeddings_file: str):

        # Create data frame.
        self.data = pd.DataFrame(columns=[EmbeddingDataset.SENT_ID, 
                                          EmbeddingDataset.SPEECH_ACT_LABEL, 
                                          EmbeddingDataset.EMBEDDING])
        
        # Read data from file and place in data frame.
        import bz2
        with bz2.open(embeddings_file, mode='rt') as source:
            for line in source:
                fields = line.strip().split('\t')
                sent_id = fields[0]
                speech_act = fields[1]
                embedding = fields[2]

                # Convert embedding string to tensor.
                embedding_values = [float(value) for value in embedding.split(',')]
                embedding_tensor = torch.tensor(embedding_values, dtype=torch.float32)
                
                # Create row for data frame.
                row = {
                    EmbeddingDataset.SENT_ID: [sent_id],
                    EmbeddingDataset.SPEECH_ACT_LABEL: [speech_act],
                    EmbeddingDataset.EMBEDDING: [embedding_tensor]
                }

                self.data += pd.DataFrame(row)


    def __len__(self):
        return len(self.data)


    def __getitem__(self, index):
        speech_act = self.data.at[index, EmbeddingDataset.SPEECH_ACT_LABEL]
        speech_act_tensor = SPEECH_ACTS_TENSORS[speech_act]
        embedding_tensor = self.data.at[index, EmbeddingDataset.EMBEDDING]
        return embedding_tensor, speech_act_tensor


class ClassificationNetwork(nn.Module):
    """
    A simple neural network.
    """

    def __init__(self, input_size: int, hidden_size: int, output_size: int):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)


    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


class EmbeddingClassifier (base.Classifier):

    def __init__(self, embed_dimension) -> None:
        super().__init__()

        # Create the neural network.
        input_size = embed_dimension  
        hidden_size = 64  
        output_size = 5  # Number of speech act labels. 
        self.cls_model = ClassificationNetwork(input_size, hidden_size, output_size)


    def classify_sentence(self, sentence: doc.Sentence):
        speech_act = self.get_speech_act_for(sentence)
        sentence.speech_act = speech_act  # type: ignore


    def get_speech_act_for(self, sentence: doc.Sentence) -> anno.SpeechActLabels:
        """
        Classify the speech act of the sentence. This only returns the speech act, and
        does not assign it to the 'speech_act' property of the sentence instance.
        """

        
        # Convert embedding to tensor.
        pass
        
    

    def train(self, data: EmbeddingDataset, batch_size: int, print_progress=True):
        """
        Train the classifier on labeled embeddings from an EmbeddingDataset.
        """
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.cls_model.parameters(), lr=0.001)

        train_loader = tdat.DataLoader(data, batch_size=batch_size, shuffle=True)

        # Train the network.
        num_epochs = 10
        for epoch in range(num_epochs):

            if print_progress: print(f'Epoch {epoch}/{num_epochs}')

            self.cls_model.train()
            running_loss = 0.0
            for inputs, labels in train_loader:

                optimizer.zero_grad()
                outputs = self.cls_model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
        
        if print_progress: print('Training complete')
        
    
class SBERTClassifier(EmbeddingClassifier):
    """
    This classifier uses an SBERT model to compute embeddings for the input sentences.
    So it does not use any precomputed embeddings in sentence instances.
    """
    pass

