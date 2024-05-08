# Data

The data sets consist of isolated, Swedish sentences originating from online discussion forums (familjeliv.se and flashback.se). I have hand-labeled these with their respective speech acts.

The data were retrieved from corpora by [Språkbanken](https://spraakbanken.gu.se/resurser/familjeliv) and are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.en). The original corpora were annotated in XML, but I formatted them to CoNLL-U. Furthermore, I have converted the POS-tags to Universal Dependencies POS-tags, as well as retagged the dependency relations to Universal Dependencies. 

## Data Files
These are all CoNLL-U corpora. They all consist of sentences manually annotated with speech acts. The sentences were also automatically annotated with sentiment (positive, negative, neutral), and its probability score.

* `dev-set.conllu.bz2` - The dev (or validation) set. 
* `dev-test-set.conllu.bz2` - A test split of the dev set. Used for developing the rule-based classifier.
* `dev-test-set-upsampled.conllu.bz2` - An upsampled version of dev-test-set.
* `dev-train-set.conllu.bz2` - A train split of the dev set. Used for training the rule-based classifier.
* `dev-train-set-upsampled.conllu.bz2` - An upsampled version of dev-train-set.
* `test-set.conllu.bz2` - The test set used for evaluating the classifiers.
* `test-set-upsampled.conllu.bz2` - An upsampled version of the test-set.

The train set is too large for GitHub, so it will be available somewhere else.

## Format
The corpora are formatted as CoNLL-U. 

```
# sent_id = 2200888
# text = Känns hoppfull med så många exempel.
# date = 2009-10-26 16:19:10
# url = http://www.familjeliv.se/forum/thread/48269320-bara-solsken-och-hopp/1#anchor-m3
# genre = internet_forum
# x_sent_id = 053044fa6
# speech_act = expressive
# sentiment_label = positive
# sentiment_score = 0.9705862402915955
1   Känns       känna|kännas    VERB    VB   Mood=Ind|Tense=Pres|VerbForm=Fin|Voice=Pass   0   root   _   _
2   hoppfull    hoppfull        ADJ	    JJ   Case=Nom|Definite=Ind|Degree=Pos|Gender=Com|Number=Sing   1   xcomp   _   _
3   med         med             ADP     PP   _   6   case   _   _
4   så          så              ADVERB  AB   _   5   advmod   _   _
5   många       _               ADJ     JJ   Case=Nom|Definite=Def,Ind|Degree=Pos|Gender=Com,Neut|Number=Plur   6   amod   _   _
6   exempel     exempel         NOUN    NN   Case=Nom|Definite=Ind|Gender=Neut|Number=Plur   1   obl   _   SpaceAfter=No
7   .           _               PUNCT   MAD   _   1   punct   _   _

```

