"""
A rulebased speech act classifier. This uses syntactical information to classify sentences 
with speech acts according to a set of predefined rules.
"""

import stanza.models.common.doc as doc
from . import base
import speechact.annotate as anno
import enum
import speechact.corpus as corp
import collections as col

INTERROGATIVE_PRONOUNS = {'vilken', 'vilkendera', 'hurdan', 'vem', 'vad'}

INTERROGATIVE_ADVERBS = {'var', 'vart', 'när', 'hur'}

SUBJECT_RELS = {
    'csubj', 
    'csubj:outer', 
    'csubj:pass',
    'nsubj',
    'nsubj:outer',
    'nsubj:pass'
    }

class SyntBlock(enum.StrEnum):

    # Dependency blocks.
    SUBJECT = 'subject'
    OBJECT = 'object'
    ADV_MOD = 'advmod'
    ADV_CL = 'advcl'
    INT_ADV = 'interrogative adverbial'
    INT_PRON = 'interrogative pronoun'
    OBL = 'oblique modifier'
    XCOMP = 'xcomp'
    CCOMP = 'ccomp'
    PARTICLE = 'particle'
    CONJ = 'conjunction'
    EXPL = 'expletive'
    NAME = 'name'
    DISLOCATED = 'dislocated'

    # Root blocks.
    FIN_VERB = 'finite verb'
    FIN_VERB_IMP = 'finite verb imperative'
    SUP_VERB = 'supine'
    PART_VERB = 'participle'
    ADVERB = 'adverb'
    NOUN = 'noun'
    ADJECTIVE = 'adjective'
    NUMBER = 'number'
    PROPN = 'proper noun'

    # Special.
    NONE = 'none'
    QUESTION_MARK = 'question mark'


class Rule:
    
    def __init__(self, speech_act: anno.SpeechActLabels, synt_blocks: list[SyntBlock],
                 strict = True):
        self.speech_act = speech_act
        self.synt_blocks = synt_blocks
        self.strict = strict
    
    def is_matching(self, synt_blocks: list[SyntBlock]) -> bool:
        if self.strict:
            return self.is_matching_strict(synt_blocks)
        else:
            return self.is_matching_unstrict(synt_blocks)

    def is_matching_strict(self, synt_blocks: list[SyntBlock]) -> bool:
        if len(self.synt_blocks) != len(synt_blocks):
            return False
        
        for block_1, block_2 in zip(self.synt_blocks, synt_blocks):
            if block_1 != block_2:
                return False
        
        return True

    def is_matching_unstrict(self, synt_blocks: list[SyntBlock]) -> bool:
        """
        Check if all the rule's synt-blocks are present in the given list of 
        synt-blocks.
        """
        if len(self.synt_blocks) > len(synt_blocks):
            return False
        
        this_index = 0
        for other_block in synt_blocks:
            if other_block == self.synt_blocks[this_index]:
                this_index += 1

                if this_index >= len(self.synt_blocks):
                    break

        # If not all the rule's synt-blocks match.
        if this_index < len(self.synt_blocks):
            return False
                
        return True
    


class RuleBasedClassifier(base.Classifier):

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
        with open(ruleset_file, "r") as json_file:
            json_data = json.load(json_file)
        
        # Load each rule from json.
        json_rules = json_data['rules']
        for json_rule in json_rules:
            speech_act = json_rule['speech_act']
            json_blocks = json_rule['blocks']
            strict = json_rule.get('strict', False)

            # Convert to enum synt-blocks.
            synt_blocks = [SyntBlock[block] for block in json_blocks]

            self.new_rule(anno.SpeechActLabels(speech_act), synt_blocks, strict)
    
    
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

    
    def classify_sentence(self, sentence: doc.Sentence):
        speech_act = self.get_speech_act_for(sentence)
        sentence.speech_act = speech_act  # type: ignore

    def get_speech_act_for(self, sentence: doc.Sentence) -> anno.SpeechActLabels:
        
        synt_blocks = self.to_synt_blocks(sentence)

        # Find the rule that matches the blocks.
        for rule in self.rules:
            if rule.is_matching(synt_blocks):
                return rule.speech_act
        
        # No matches found.
        return anno.SpeechActLabels.NONE

    def to_synt_blocks(self, sentence: doc.Sentence) -> list[SyntBlock]:

        # Retrieve the root word and its dependencies.
        root = get_root(sentence)
        root_deps = get_deps(sentence, root)
        words = root_deps + [root]
        words.sort(key=lambda word: word.id)

        # Convert each word to a block.
        synt_blocks = []
        for word in words:

            synt_block = self.get_synt_block(word)

            # Ignore punctuations if there is no block for it.
            if word.pos == 'PUNCT' and synt_block == SyntBlock.NONE:
                continue
            
            synt_blocks.append(synt_block)

        return synt_blocks

    
    def get_synt_block(self, word: doc.Word) -> SyntBlock:
        """
        Get the synt-block for the word (and its dependencies).
        """

        if word.text == '?': return SyntBlock.QUESTION_MARK

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

        if word.deprel in SUBJECT_RELS: return SyntBlock.SUBJECT
        if word.deprel == 'advmod': return SyntBlock.ADV_MOD
        if word.deprel == 'advcl': return SyntBlock.ADV_CL
        if word.deprel == 'xcomp': return SyntBlock.XCOMP
        if word.deprel == 'ccomp': return SyntBlock.CCOMP
        if word.deprel == 'obl': return SyntBlock.OBL
        if word.deprel == 'obj': return SyntBlock.OBJECT
        if word.deprel == 'conj': return SyntBlock.CONJ
        if word.deprel == 'compound:prt': return SyntBlock.PARTICLE
        if word.deprel == 'expl': return SyntBlock.EXPL
        if word.deprel == 'flat:name': return SyntBlock.NAME
        if word.deprel == 'dislocated': return SyntBlock.DISLOCATED

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

    def __init__(self, synt_blocks: list[SyntBlock]):
        super().__init__(anno.SpeechActLabels.NONE, synt_blocks)
        self.counts = col.Counter()

    def increment_for(self, speech_act: anno.SpeechActLabels):
        self.counts[speech_act] += 1
    
    def refresh_label(self):
        self.speech_act = self.counts.most_common()[0][0]



class TrainableClassifier(RuleBasedClassifier):
    """
    A trainable rule based classifier.
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
            
            # Find matching rule, and increment to it.
            matching_rule = self.find_rule(blocks, strict=True)
            if matching_rule != None:
                assert type(matching_rule) == TrainableRule, 'rule is not a trainable rule.'
                matching_rule.increment_for(sentence.speech_act)  # type: ignore
            
            # No matching rule, create new rule.
            else:
                new_rule = TrainableRule(blocks)
                new_rule.strict = True
                new_rule.increment_for(sentence.speech_act)  # type: ignore
                self.rules.append(new_rule)
        
        # Refresh the labels for all rules.
        for rule in self.rules:
            assert type(rule) == TrainableRule, 'rule is not a trainable rule.'
            rule.refresh_label()






            
