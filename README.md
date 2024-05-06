# Automatic Speech Act Classification

## What are Speech Acts?
What is done through speaking? In a sense, a spoken utterance is just a string of vocal sounds. But in another sense, it is also a social action that has real effects on the world. These spoken actions are referred to as *speech acts*. We humans unconsciously understand and categorize speech acts all the time. The meaning of a speech act depends both on the syntax and semantics of the sentence and the conversational context in which it occurs.

## What is in this Repository?

### Classifier Models
This repository contains two different models for automatically classifying speech acts. These are classified out of context, meaning, they analyze the conversational structure but only individual sentences. Furthermore, they target Swedish sentences.

- **Rule-based classifier**: This classifier uses rules for classification. It relies primarily on syntax, but also on sentiment.

- **Embedding-based classifier**: This classifier uses sentence embeddings from SBERT and classifies them with a linear, single-layer neural network.

### Data
These models have been trained on isolated, Swedish sentences originating from online discussion forums (familjeliv.se and flashback.se). I have hand-labeled these with their respective speech acts.

## What Speech Acts are Classified?
The models can classify the following speech acts, that are taken from *The Swedish Academy Grammar* (Teleman et al., 1999):

- **Assertive**: the speaker holds that the content of the sentence is true or at least true to a varying degree. For example: “They launched a car into space.”

- **Question**: the speaker requests information regarding whether or not something is true, or under what conditions it is true. For example: “Are you busy?” or “How much does the car cost?”.

- **Directive**: the speaker attempts to get the listener to carry out the action described by the sentence. For example: “Open the door!” or “Will you hold this for me?”

- **Expressive**: the speaker expresses some feeling or emotional attitude about the content of the sentence. For example: “What an adorable dog!” or “The Avengers are awesome!”

# Usage
Classification is done on entire corpora. The classifiers take as input a CoNLL-U corpus and tags each sentence with their respective speech acts. These are then outputted as a new CoNLL-U corpus. 

## Classifying with Rules
Run `scripts/tag_speech_acts_rulebased.py` on the corpus you want to tag with speech acts. It takes three arguments:
1. The source corpus which contain the sentences to be tagged.
2. The target corpus which the tagged sentences are written to.
3. The rule set file which contain all the rules.

Example: `python scripts/tag_speech_acts_rulebased.py 'sentences.conllu.bz2' 'speech-acts.conllu.bz2' 'models/rule-based.json'`

Alternatively, you can use the `speechact/classifier/rulebased.py` module if you instead want to integrate it into your code.

**Note:** the rule-based classifier requires the sentences in the source corpus to be annotated with sentiment. This is done with the `sentiment_label` which can have the values `neutral`, `positive`, or `negative`.

## Classifying with Embeddings
Currently, there is no script for tagging entire corpora similar to the rule-based classifier above. However, if you only want integrate it with your code, you can use the `speechact/classifier/embedding.py` module.

# Directories
- `annotator` contains the annotation tool that was used for manually annotating the data set.
- `data` contains the data sets.
- `models` contains the rule sets and pytorch models.
- `notebooks` contains notebooks for evaluation, data visualization, etc.
- `scripts` contains scripts for pre-processing, training, and evaluation.
- `speechact` contains the core python codes.


# References

Teleman, U., Hellberg, S., & Andersson, E. (1999). *Svenska Akademiens grammatik* (1 ed., Vol. 4). Svenska Akademien.