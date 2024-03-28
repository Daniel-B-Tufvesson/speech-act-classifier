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
from typing import Generator

SPEECH_ACTS = [
    anno.SpeechActLabels.ASSERTION,
    anno.SpeechActLabels.QUESTION,
    anno.SpeechActLabels.DIRECTIVE,
    anno.SpeechActLabels.EXPRESSIVE
]
"""
The speech act labels to classify. Note that the HYPOTHESIS is not included.
"""

class CorpusDataset(tdat.Dataset):
    """
    A Pytorch compatible dataset for a speech act labeled Corpus.

    All sentences are loaded into memory. However, it is only the sent_id, text, and speech_act
    that is stored.
    """

    def __init__(self, corpus: corp.Corpus) -> None:
        super().__init__()

        # Load sentences.
        self.sentences = [anno.Sentence(s.text, str(s.sent_id), s.speech_act) for s in corpus.sentences()]


    def __len__(self) -> int:
        return len(self.sentences)


    def __getitem__(self, index) -> tuple[str, int]:
        sentence = self.sentences[index]
        speech_act_class_index = SPEECH_ACTS.index(sentence.label)
        #speech_act_tensor = SPEECH_ACT_TO_TENSOR[sentence.label]
        return sentence.text, speech_act_class_index


class DocumentDataset(tdat.Dataset):
    """
    A Pytorch compatible dataset for a speech act labeled Stanza Document.
    """

    def __init__(self, document: doc.Document) -> None:
        super().__init__()
        self.document = document
    

    def __len__(self) -> int:
        return len(self.document.sentences)


    def __getitem__(self, index) -> tuple[str, int]:
        sentence = self.document.sentences[index]
        speech_act_class_index = SPEECH_ACTS.index(sentence.speech_act)
        return sentence.text, speech_act_class_index
    

    def batched(self, batch_size: int) -> Generator[list[doc.Sentence], None, None]:
        batch = []
        for sentence in self.document.sentences:
            batch.append(sentence)

            if len(batch) == batch_size:
                yield batch
                batch = []


class EmbeddingClassifier (base.Classifier):

    def __init__(self) -> None:
        super().__init__()

        # Load embedding model.
        self.emb_model = stf.SentenceTransformer('KBLab/sentence-bert-swedish-cased', device='mps')

        # Create the neural network.
        input_size: int = self.emb_model.get_sentence_embedding_dimension() # type: ignore
        hidden_size = 64  
        output_size = len(SPEECH_ACTS)
        self.cls_model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )
        
        # Run on MPS.
        self.cls_model = self.cls_model.to('mps')


    def classify_document(self, document: doc.Document):
        doc_dataset = DocumentDataset(document)
        #data_loader = tdat.DataLoader(doc_dataset, batch_size=32, shuffle=False)

        self.cls_model.eval()
        with torch.no_grad():
            for batch in doc_dataset.batched(32):
                texts = [sent.text for sent in batch]

                embeddings = self.emb_model.encode(texts, convert_to_numpy=False,  # type: ignore
                                                   convert_to_tensor=True)
                outputs = self.cls_model(embeddings)

                # Assign outputs to sentences.
                for output, sentence in zip(outputs, batch):
                    class_index = torch.argmax(output)
                    speech_act = SPEECH_ACTS[class_index]
                    sentence.speech_act = speech_act  # type: ignore
                






    def classify_sentence(self, sentence: doc.Sentence):
        speech_act = self.get_speech_act_for(sentence)
        sentence.speech_act = speech_act  # type: ignore


    def get_speech_act_for(self, sentence: doc.Sentence|str) -> anno.SpeechActLabels:
        """
        Classify the speech act of the sentence. This only returns the speech act, and
        does not assign it to the 'speech_act' property of the sentence instance.
        """

        # Get sentence text from input.
        if isinstance(sentence, doc.Sentence):
            assert sentence.text != None, f'sentence.text == None for {sentence.sent_id}'
            text = sentence.text
        else:
            text = sentence
        
        # Create embedding and classify.
        embedding = self.emb_model.encode(text, convert_to_numpy=False)
        output = self.cls_model.forward(embedding)  # type: ignore
        class_index = torch.argmax(output)
        return SPEECH_ACTS[class_index]
        
    

    def train(self, data: CorpusDataset, batch_size: int, print_progress=True):
        """
        Train the classifier on labeled embeddings from an EmbeddingDataset.
        """
        criterion = nn.CrossEntropyLoss().to('mps')
        optimizer = optim.Adam(self.cls_model.parameters(), lr=0.001)

        train_loader = tdat.DataLoader(data, batch_size=batch_size, shuffle=True)

        # Train the network.
        num_epochs = 10
        for epoch in range(num_epochs):

            if print_progress: print(f'Epoch {epoch}/{num_epochs}')

            self.cls_model.train()
            running_loss = 0.0
            for inputs, labels in train_loader:
                labels = labels.to('mps')

                optimizer.zero_grad()

                embeddings = self.emb_model.encode(inputs, convert_to_numpy=False, convert_to_tensor=True)
                outputs = self.cls_model(embeddings)

                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
        
        if print_progress: print('Training complete')
        

    def save(self, file_name):
        """
        Save the model to a file. This is only saves the classification network and not the 
        embedding model.
        """
        print(f'Saving model to "{file_name}"')
        torch.save(self.cls_model.state_dict(), file_name)
    

    def load(self, file_name):
        """
        Load the model from a file. This only loads the classification network and not the
        embedding model.
        """
        print(f'Loading model from "{file_name}"')
        self.cls_model.load_state_dict(torch.load(file_name))
        