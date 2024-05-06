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



# References

Teleman, U., Hellberg, S., & Andersson, E. (1999). *Svenska Akademiens grammatik* (1 ed., Vol. 4). Svenska Akademien.