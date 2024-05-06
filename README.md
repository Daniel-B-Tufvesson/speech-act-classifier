# Automatic Speech Act Classification


## What are Speech Acts?
What is done through speaking? In a sense, a spoken utterance is just a string of vocal sounds. But in another sense, it is also a social action that has real effects on the world. For example, "Can you pass the salt?" is an act of requesting the salt, which can then result in obtaining the salt. These spoken actions are referred to as *speech acts*. We humans unconsciously understand and categorize speech acts all the time. The meaning of a speech act depends both on the syntax and semantics of the sentence and the conversational context in which it occurs.



## What is in this Repository?

### Classifier Models
This repository contains two different models for automatically classifying speech acts. These are classified out of context, meaning, they analyze the conversational structure but only individual sentences. Furthermore, they target Swedish sentences.

- **Rule-based classifier**: This classifier uses rules for classification. It relies primarily on syntax, but also sentiment. The model is json file consisting of rules: `models/rule-based.json`.

- **Embedding-based classifier**: This classifier uses sentence embeddings from SBERT and classifies them with a linear, single-layer neural network. The model is a pytorch file: `models/embedding-based.pth`.

### Data
These models have been trained on isolated, Swedish sentences originating from online discussion forums (familjeliv.se and flashback.se). I have hand-labeled these with their respective speech acts. The data sets are described in [data/README.md](data/README.md).



## What Speech Acts are Classified?
The models can classify the following speech acts, which are taken from *The Swedish Academy Grammar* (Teleman et al., 1999):

- **Assertive**: the speaker holds that the content of the sentence is true or at least true to a varying degree. For example: “They launched a car into space.”

- **Question**: the speaker requests information regarding whether or not something is true, or under what conditions it is true. For example: “Are you busy?” or “How much does the car cost?”.

- **Directive**: the speaker attempts to get the listener to carry out the action described by the sentence. For example: “Open the door!” or “Will you hold this for me?”

- **Expressive**: the speaker expresses some feeling or emotional attitude about the content of the sentence. For example: “What an adorable dog!” or “The Avengers are awesome!”


## Why does this exist?
I have created this as part of my bachelor's thesis in cognitive science. These classifiers are intended to be tools that can be used for linguistic analysis of large amounts of language data, also referred to as *corpus linguistics*. Here, they can be used for finding linguistic patterns of speech acts in transcribed conversations. 



# Usage
The classifiers operate on entire corpora. They take as input a CoNLL-U corpus and tag each sentence with their respective speech acts. These are then outputted as a new CoNLL-U corpus. 


## Classifying with Rules
Run [`tag_speech_acts_rulebased.py`](scripts/tag_speech_acts_rulebased.py) on the corpus you want to tag with speech acts. It takes three arguments:
1. The source corpus which contains the sentences to be tagged.
2. The target corpus to which the tagged sentences are written.
3. The rule set file which contains all the rules.

Example: `python scripts/tag_speech_acts_rulebased.py 'sentences.conllu.bz2' 'speech-acts.conllu.bz2' 'models/rule-based.json'`

Alternatively, you can use the [`rulebased.py`](speechact/classifier/rulebased.py) module if you instead want to integrate it into your code.

**Note:** the rule-based classifier requires the sentences in the source corpus to be annotated with sentiment. This is done with the `sentiment_label` which can have the values `neutral`, `positive`, or `negative`.


## Classifying with Embeddings
Currently, there is no script for tagging entire corpora similar to the rule-based classifier above. However, if you only want to integrate it with your code, you can use the [`embedding.py`](speechact/classifier/embedding.py) module.



# Directories
- `annotator` contains the annotation tool that was used for manually annotating the data set.
- `data` contains the data sets.
- `models` contains the rule sets and pytorch models.
- `notebooks` contains notebooks for evaluation, data visualization, etc.
- `scripts` contains scripts for pre-processing, training, and evaluation.
- `speechact` contains the core python codes.



# Training of the Models
The rule-based classifier was trained on the `data/dev-train-set-upsampled.conllu.bz2` data set.

The embedding-based classifier was trained on an automatically annotated corpus consisting of 3.8 million sentences. These were tagged using the rule-based classifier.



# Performance and Evaluation
The classifiers were evaluated on the `data/test-set-upsampled.conllu.bz2` data set. The evaluation can be replicated in [`evaluate_classifiers.ipynb`](notebooks/evaluate_classifiers.ipynb).

Table 1 shows that the embedding-based classifier overall performs better than the rule-based classifier. Table 2 shows that this is also the case for most of the class-specific measures. While the embedding-based classifier is better, this difference is only slight.  

<br>

Table 1: The accuracy and averaged F1 score for the classifiers and a baseline.
|             | Baseline | Rule |  Embedding    |
|-------------|----------|------|---------------|
| Accuracy    | .25      | .69  | **.74**       |
| Averaged F1 | .10      | .70  | **.74**       |

<br>
<br>

Table 2: Class-specific metrics for the classifiers. The highest measures are marked in bold.
|            | Precision  (Rule) | Precision  (Embedding) | Recall  (Rule) | Recall  (Embedding) | F1  (Rule) | F1  (Embedding) |
|------------|-------------------|------------------------|----------------|---------------------|------------|-----------------|
| Assertive  | .53               | **.60**                | **.74**        | .70                 | .62        | **.64**         |
| Question   | **.96**           | .94                    | .92            | **.93**             | **.94**    | .93             |
| Directive  | **.76**           | .72                    | .60            | **.75**             | .67        | **.73**         |
| Expressive | .64               | **.72**                | .51            | **.57**             | .57        | **.63**         |



# References

Teleman, U., Hellberg, S., & Andersson, E. (1999). *Svenska Akademiens grammatik* (1 ed., Vol. 4). Svenska Akademien.