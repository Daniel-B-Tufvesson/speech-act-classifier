"""
A rulebased speech act classifier. This uses syntactical information to classify sentences 
with speech acts according to a set of rules. These rules can either be predefined or 
trained.

These classifiers are shallow in the sense that they only look at the syntactic dependendent
words of the root word. 
"""

import stanza.models.common.doc as doc
from . import base
import speechact.annotate as anno
import enum
import speechact.corpus as corp
import collections as col
import speechact as sa

INTERROGATIVE_PRONOUNS = {'vilken', 'vilkendera', 'hurdan', 'vem', 'vad'}
INTERROGATIVE_ADVERBS = {'var', 'vart', 'när', 'hur'}
PRON_2ND_PERSON = {'du', 'ni'}

SUBJECT_RELS = {
    'csubj', 
    'csubj:outer', 
    'csubj:pass',
    'nsubj',
    'nsubj:outer',
    'nsubj:pass'
    }

class SyntBlock(enum.StrEnum):
    """
    The basic building blocks for the rules. These blocks represent functional syntactic
    information of a sentence. 
    """

    # Dependency blocks.
    SUBJECT = 'SUBJECT'
    SUBJECT_2ND = 'SUBJECT_2ND'  # 2nd person subject.
    INT_ADV = 'INT_ADV'  # 'interrogative adverbial'
    INT_PRON = 'INT_PRON'  # 'interrogative pronoun'

    # Root blocks.
    FIN_VERB = 'FIN_VERB'  # 'finite verb'
    FIN_VERB_IMP = 'FIN_VERB_IMP'  # 'finite verb imperative'
    SUP_VERB = 'SUP_VERB'  # 'supine'
    PART_VERB = 'PART_VERB'  # 'participle'
    ADVERB = 'ADVERB'
    NOUN = 'NOUN'
    ADJECTIVE = 'ADJECTIVE'
    NUMBER = 'NUMBER'
    PROPN = 'PROPN'

    # Special.
    NONE = 'NONE'
    """The token does not belong to any synt-block."""
    QUESTION_MARK = 'QUESTION_MARK'
    """The token is a question mark (?)."""
    PERIOD = 'PERIOD'
    """The token is a period (.)"""
    EXCLAMATION_MARK = 'EXCLAMATION_MARK'
    """The token is an exclamation mark (!)."""
    SENTIMENT = 'SENTIMENT'
    """The sentence expresses a non-neutral sentiment."""


class Rule:
    
    def __init__(self, speech_act: anno.SpeechActLabels, synt_blocks: list[SyntBlock],
                 strict = True):
        self.speech_act = speech_act
        self.synt_blocks = synt_blocks
        self.strict = strict
    
    def is_matching(self, synt_blocks: list[SyntBlock]) -> bool:
        """
        Check if the sequence of synt-blocks matches this rule. If this is a strict rule, 
        then all the blocks need to match exactly. If it is unstrict, then only some of
        the blocks need to be present in the correct order.
        """
        if self.strict:
            return self.is_matching_strict(synt_blocks)
        else:
            return self.is_matching_unstrict(synt_blocks)

    def is_matching_strict(self, synt_blocks: list[SyntBlock]) -> bool:
        """
        Check if the given sequence of synt-blocks is equal to the the one in this rule.
        """
        if len(self.synt_blocks) != len(synt_blocks):
            return False
        
        for block_1, block_2 in zip(self.synt_blocks, synt_blocks):
            if block_1 != block_2:
                return False
        
        return True

    def is_matching_unstrict(self, synt_blocks: list[SyntBlock]) -> bool:
        """
        Check if the given sequence of synt-blocks is present in the right order in 
        this rule.
        """
        if len(self.synt_blocks) > len(synt_blocks):
            return False
        
        this_index = 0
        for other_block in synt_blocks:
            if other_block == self.synt_blocks[this_index]:
                this_index += 1

                if this_index >= len(self.synt_blocks):
                    break

        # If not all the rules' synt-blocks match.
        if this_index < len(self.synt_blocks):
            return False
                
        return True
    


class RuleBasedClassifier(base.Classifier):
    """
    Classify speech acts based on a list of rules.
    """

    def __init__(self, ruleset_file: str|None = None) -> None:
        super().__init__()
        self.rules = []  # type: list[Rule]
        
        if ruleset_file != None:
            self.load_rules(ruleset_file)
    
    
    def load_rules(self, ruleset_file: str):
        """
        Load a set of rules from a json file.
        """

        # Read json file.
        import json
        with open(ruleset_file, "rt") as json_file:
            json_data = json.load(json_file)
        
        # Load each rule from json.
        json_rules = json_data['rules']
        for json_rule in json_rules:
            speech_act = json_rule['speech_act']
            json_blocks = json_rule['blocks']
            strict = json_rule.get('strict', False)

            # Convert to enum synt-blocks.
            synt_blocks = [SyntBlock(block) for block in json_blocks]

            self.new_rule(anno.SpeechActLabels(speech_act), synt_blocks, strict)
    
    def save_rules(self, ruleset_file: str):
        """
        Save the rules to a json file.
        """
        json_rules = []
        for rule in self.rules:
            json_rule = {
                'speech_act': rule.speech_act,
                'blocks': rule.synt_blocks
            }

            if rule.strict:
                json_rule['strict'] = True

            json_rules.append(json_rule)

        json_data = {
            'rules': json_rules
        }

        import json
        with open(ruleset_file, "wt") as json_file:
            json.dump(json_data, json_file, indent=4)
        
    def new_rule(self, speech_act: anno.SpeechActLabels, synt_blocks: list[SyntBlock],
                 strict = False):
        """
        Create and add a new rule to this classifier. 
        """

        # Check for duplicates.
        for other_rule in self.rules:
            if other_rule.is_matching(synt_blocks):
                raise ValueError(f'rule is already taken: {synt_blocks}')

        rule = Rule(speech_act, synt_blocks, strict)
        self.rules.append(rule)
    
    def find_rule(self, synt_blocks: list[SyntBlock], strict: bool|None = None) -> Rule|None:
        """
        Find the rule that is matching the synt-blocks.
        """
        for rule in self.rules:
            if strict == None and rule.is_matching(synt_blocks):
                return rule
            
            elif strict and rule.is_matching_strict(synt_blocks):
                return rule
            
            elif not strict and rule.is_matching_unstrict(synt_blocks):
                return rule
        
        return None

    def sort_rules(self):
        """
        Sort the rules in decreasing specificity. The most specific rule (i.e. the one with
        the most synt-blocks) is first. The least specific (i.e. the one with the fewest
        synt-blocks) will be last.
        """
        self.rules.sort(key=lambda rule: -len(rule.synt_blocks))

    @property
    def rule_count(self):
        """
        The number of rules.
        """
        return len(self.rules)
    
    def classify_sentence(self, sentence: doc.Sentence):
        """
        Classify the sentence with a speech act based on a list of rules.
        """
        speech_act = self.get_speech_act_for(sentence)
        sentence.speech_act = speech_act  # type: ignore

    def get_speech_act_for(self, sentence: doc.Sentence) -> anno.SpeechActLabels:
        """
        Classify the sentence without actually assigning it a speech act. The speech act
        is instead returned.
        """
        
        synt_blocks = self.to_synt_blocks(sentence)

        # Find the rule that matches the blocks.
        for rule in self.rules:
            if rule.is_matching(synt_blocks):
                return rule.speech_act
        
        # No matches found.
        return anno.SpeechActLabels.NONE

    def to_synt_blocks(self, sentence: doc.Sentence) -> list[SyntBlock]:
        """
        Compute the sequence of the synt-blocks for the sentence.
        """

        # Retrieve the root word and its dependencies.
        root = get_root(sentence)
        root_deps = get_deps(sentence, root)
        words = root_deps + [root]
        words.sort(key=lambda word: word.id)

        # Convert each word to a block.
        synt_blocks = []
        for word in words:

            # Ignore punctuations if there is no block for it.
            if word.pos == 'PUNCT' and word != sentence.words[-1]:
                continue

            synt_block = self.get_synt_block(word)
            
            # Ingore NONE blocks.
            if synt_block == SyntBlock.NONE:
                continue
            
            synt_blocks.append(synt_block)

        return synt_blocks

    
    def get_synt_block(self, word: doc.Word) -> SyntBlock:
        """
        Get the synt-block for the word.
        """

        if word.text == '?': return SyntBlock.QUESTION_MARK
        if word.text == '.': return SyntBlock.PERIOD
        if word.text == '!': return SyntBlock.EXCLAMATION_MARK

        if word.deprel == 'root':
            if word.pos == 'VERB' and word.feats != None:
                if 'VerbForm=Fin' in word.feats:
                    if 'Mood=Imp' in word.feats: return SyntBlock.FIN_VERB_IMP
                    else: return SyntBlock.FIN_VERB
                
                elif 'VerbForm=Part' in word.feats:
                    return SyntBlock.PART_VERB
                
                elif 'VerbForm=Sup' in word.feats:
                    return SyntBlock.SUP_VERB

            if word.pos == 'ADVERB': return SyntBlock.ADVERB
            if word.pos == 'NOUN': return SyntBlock.NOUN
            if word.pos == 'ADJ': return SyntBlock.ADJECTIVE
            if word.pos == 'NUM': return SyntBlock.NUMBER
            if word.pos == 'PROPN': return SyntBlock.PROPN
            else: return SyntBlock.NONE

        if word.lemma in INTERROGATIVE_PRONOUNS and word.pos == 'PRON': return SyntBlock.INT_PRON
        if word.lemma in INTERROGATIVE_ADVERBS and word.pos == 'ADVERB': return SyntBlock.INT_ADV

        if word.deprel in SUBJECT_RELS: 
            if word.lemma in PRON_2ND_PERSON: return SyntBlock.SUBJECT_2ND
            return SyntBlock.SUBJECT

        return SyntBlock.NONE




def get_root(sentence: doc.Sentence) -> doc.Word:
    """
    Retrieve the root word of the sentence.
    """
    for word in sentence.words:
        if word.deprel == 'root':
            return word
    
    raise ValueError(f'Sentence lacks a root: {sentence.sent_id}')


def get_deps(sentence: doc.Sentence, head: doc.Word) -> list[doc.Word]:
    """
    Retrieve the dependencies of this word, i.e. the words that have this word as a head.
    """
    deps = []
    for word in sentence.words:
        if word.head == head.id:
            deps.append(word)

    return deps


class TrainableRule(Rule):
    """
    A trainable rule is used by the trainable 
    """

    def __init__(self, synt_blocks: list[SyntBlock]):
        super().__init__(anno.SpeechActLabels.NONE, synt_blocks)
        self.counts = col.Counter()

    def increment_for(self, speech_act: anno.SpeechActLabels):
        """
        Increment the occurence of the given speech act. This is used during training.
        """
        self.counts[speech_act] += 1
    
    def refresh_label(self):
        """
        Refresh the speech act label so that it is the most common speech act from the 
        training.
        """
        self.speech_act = self.counts.most_common()[0][0]



class TrainableClassifier(RuleBasedClassifier):
    """
    A trainable rule-based classifier.
    """

    def __init__(self, ruleset_file: str | None = None):
        super().__init__(ruleset_file)

    def train(self, corpus: corp.Corpus):
        """
        Train the classifier on the corpus.
        """
        for sentence in corpus.stanza_sentences():
            assert sentence.speech_act != None, f'sentence {sentence.sent_id} does not have a speech act'  # type: ignore
            blocks = self.to_synt_blocks(sentence)

            if len(blocks) == 0:
                continue
            
            # Find matching rule, and increment to it.
            matching_rule = self.find_rule(blocks, strict=True)
            if matching_rule != None:
                assert type(matching_rule) == TrainableRule, 'rule is not a trainable rule.'
                matching_rule.increment_for(sentence.speech_act)  # type: ignore
            
            # No matching rule, create new rule.
            else:
                new_rule = TrainableRule(blocks)
                new_rule.strict = False
                new_rule.increment_for(sentence.speech_act)  # type: ignore
                self.rules.append(new_rule)
        
        # Refresh the labels for all rules.
        for rule in self.rules:
            if type(rule) == TrainableRule:
                rule.refresh_label()
        
        self.sort_rules()



class TrainableSentimentClassifier(TrainableClassifier):
    """
    A trainable rule-based classifier that also incorporates the SENTIMENT synt-block in
    the rules. This requires the sentences to be annotated with a sentiment_label.
    """

    def to_synt_blocks(self, sentence: doc.Sentence) -> list[SyntBlock]: 
        synt_blocks = super().to_synt_blocks(sentence)

        # Check sentiment and add as synt block.
        sentiment = sa.get_sentence_property(sentence, 'sentiment_label')
        if sentiment != sa.Sentiment.NEUTRAL:
            synt_blocks.append(SyntBlock.SENTIMENT)

        return synt_blocks


class TrainableSentimentClassifierV2(TrainableClassifier):
    """
    A trainable rule-based classifier that classifies assertives as expressives if they
    have a non-neutral sentiment. Note that the sentiment is not incorporated into the 
    rules as in TrainableSentimentClassifier.
    
    This requires the sentences to be annotated with a sentiment_label.
    """


    def classify_sentence(self, sentence: doc.Sentence):
        speech_act = self.get_speech_act_for(sentence)

        # Assertions with sentiment should be expressives.
        if speech_act == anno.SpeechActLabels.ASSERTION:
            sentiment = sa.get_sentence_property(sentence, 'sentiment_label')
            if sentiment != sa.Sentiment.NEUTRAL:
                speech_act = anno.SpeechActLabels.EXPRESSIVE

        sentence.speech_act = speech_act  # type: ignore
