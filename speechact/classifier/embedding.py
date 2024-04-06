"""
Classify speech acts from SBERT sentence embeddings.
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
import collections as col
from typing import Callable

NetworkFactory = Callable[[int, int], nn.Module]

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
        
        # Count class frequencies.
        self.class_frequencies = col.Counter()
        for sentence in self.sentences:
            self.class_frequencies[sentence.label] += 1
        

    def __len__(self) -> int:
        return len(self.sentences)


    def __getitem__(self, index) -> tuple[str, int]:
        sentence = self.sentences[index]
        speech_act_class_index = SPEECH_ACTS.index(sentence.label)
        return sentence.text, speech_act_class_index
    
    def get_class_frequency(self, class_index):
        speech_act = SPEECH_ACTS[class_index]
        return self.class_frequencies[speech_act]


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


def linear_perceptron(input_size: int, output_size: int) -> nn.Module:
    return nn.Linear(input_size, output_size)


def softmax_perceptron(input_size: int, output_size: int) -> nn.Module:
    return nn.Sequential(
        nn.Linear(input_size, output_size),
        nn.Softmax(dim=1)
    )


def sigmoid_hidden_layer(input_size: int, output_size: int) -> nn.Module:
    hidden_size = 64
    return nn.Sequential(
        nn.Linear(input_size, hidden_size),
        nn.Sigmoid(),
        nn.Linear(hidden_size, output_size),
        nn.Softmax(dim=1)
    )

class EmbeddingClassifier (base.Classifier):

    def __init__(self, device='mps', network_factory: NetworkFactory|None = None) -> None:  # mps is the macbook's GPU.
        super().__init__()
        self.device = device

        # Load embedding model.
        self.emb_model = stf.SentenceTransformer('KBLab/sentence-bert-swedish-cased', device=device)

        # Create the neural network.
        input_size: int = self.emb_model.get_sentence_embedding_dimension() # type: ignore
        # hidden_size = 256  
        output_size = len(SPEECH_ACTS)

        # Create the network from the factory, or use default linear perceptron.
        if network_factory != None:
            self.cls_model = network_factory(input_size, output_size)
        else:
            self.cls_model = linear_perceptron(input_size, output_size)
        
        # Run on device.
        self.cls_model = self.cls_model.to(device)


    def classify_document(self, document: doc.Document):
        doc_dataset = DocumentDataset(document)

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

        self.cls_model.eval()
        
        # Create embedding and classify.
        embedding = self.emb_model.encode(text, convert_to_numpy=False)
        with torch.no_grad():
            output = self.cls_model.forward(embedding)  # type: ignore
        class_index = torch.argmax(output)
        return SPEECH_ACTS[class_index]
        
    

    def train(self, data: CorpusDataset, batch_size: int, num_epochs = 10,
              save_each_epoch: None|str = None, use_class_weights=False,
              loss_history: list[float]|None = None, dev_loss_history: list[float]|None = None,
              dev_data: CorpusDataset|None = None):
        """
        Train the classifier on labeled embeddings from an corpus.
        """

        import tqdm  # For progress bar.

        optimizer = optim.Adam(self.cls_model.parameters(), lr=0.001)
        criterion = nn.CrossEntropyLoss().to(self.device)

        # Use class weights.
        if use_class_weights:
            class_weights = [1.0 / data.get_class_frequency(i) for i in range(len(SPEECH_ACTS))]
            criterion.weight = torch.tensor(class_weights, dtype=torch.float32).to(self.device)
        
        # Handle training data.
        train_loader = tdat.DataLoader(data, batch_size=batch_size, shuffle=True)

        # Handle dev data.
        if dev_data != None:
            dev_loader = tdat.DataLoader(dev_data, batch_size=batch_size, shuffle=True)


        # Train the network.
        for epoch in range(num_epochs):

            self.cls_model.train()
            running_loss = 0.0
            for inputs, labels in tqdm.tqdm(train_loader, desc=f'Training: epoch {epoch+1}/{num_epochs}", unit="batch'):
                labels = labels.to(self.device)

                optimizer.zero_grad()

                # Do forward pass.
                embeddings = self.emb_model.encode(inputs, convert_to_numpy=False, convert_to_tensor=True)
                outputs = self.cls_model(embeddings)

                # Compute loss and backpropagate.
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
            
            # Save model.
            if save_each_epoch != None:
                self.save(save_each_epoch)
            
            # Calculate average loss for the epoch
            epoch_loss = running_loss / len(train_loader)
            print(f'Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss}')

            # Save the loss to history.
            if loss_history != None:
                loss_history.append(epoch_loss)
            
            # Compute loss on dev data.
            if dev_data != None:
                running_dev_loss = 0.0
                self.cls_model.eval()
                for inputs, labels in tqdm.tqdm(dev_loader, desc=f'Eval on dev data: epoch {epoch+1}/{num_epochs}", unit="batch'):
                    labels = labels.to(self.device)
                    embeddings = self.emb_model.encode(inputs, convert_to_numpy=False, convert_to_tensor=True)
                    outputs = self.cls_model(embeddings)
                    loss = criterion(outputs, labels)
                    running_dev_loss += loss.item()

                # Calculate average dev loss for the epoch
                dev_epoch_loss = running_dev_loss / len(dev_loader)
                print(f'Epoch {epoch+1}/{num_epochs}, Dev loss: {dev_epoch_loss}')

                # Save the dev loss to history.
                if dev_loss_history != None:
                    dev_loss_history.append(dev_epoch_loss)




            
        
        print('Training complete')
        

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
        