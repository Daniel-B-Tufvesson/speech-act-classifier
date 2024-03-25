# `auto-annotated data`
This directory contains the training data set for the final classifier. 

Many of the data files are not in the repository since they are too large (roughly 400 MB). 

## How the training set was created

### 1. Extract sentences from corpora
First I ran the `scripts/extract_training_data.py`to extract sentences from the corpora in `data/tagged data`. This extracts all the sentences (except for the first 1000) from each corpora and writes them to a single corpus file `extracted-sentences.conllu.bz2`. This file is not included in the repository since it is to large.

This resulted in a data set with 3 800 000 sentences.

### 2. Remove duplicates
Then I removed all the duplicate sentences, so that all sentences are unique. For example, if the original data contains two instances of "Hello there!", then only one instance was added to the data set.

I did this by running `scripts/remove_duplicates.py` on `extracted-sentences.conllu.bz2` which created `no duplicates.conllu.bz2`.

This resulted in a data set with 3 333 760 sentences. Meaning 466 240 sentences were duplicates.

### 3. Shuffle the sentences
The sentences were then shuffled so that they come in random order. I did this by running `scripts/shuffle_sentences.py` on `no duplicates.conllu.bz2` (not in repository), which created `shuffled.conllu.bz2` (not in repository).

### 4. Tag sentiment

### 5. Tag speech acts

### 6. Tag sentence embeddings

### 7. Balance data?