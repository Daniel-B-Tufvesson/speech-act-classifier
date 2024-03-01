"""
Parse dependency tags for CoNNL-U sentences. The dependency tags are the Universal 
Dependency Relations: https://universaldependencies.org/u/dep/index.html
"""

import bz2
from typing import TextIO
from typing import Generator
import stanza
from stanza.utils.conll import CoNLL
import speechact.data as dat

def tag_bz2(source_file: str, target_file: str, **kwargs):
    """
    Tag a bz2 compressed connlu corpus. The tagged results are written to bz2 compressed
    connlu corpus as well. 
    """
    print('tag_bz2')
    with bz2.open(source_file, mode='rt') as source:
        with bz2.open(target_file, mode='wt') as target:
            tag(source, target, **kwargs)


def tag(source: TextIO, target: TextIO, **kwargs):
    """
    Tag a source connlu corpus with universal dependency relations. The tagged sentences are
    written to the target as connlu.
    """
    print('Tag corpus with dep tags')

    # Initialize the stanza pipeline for dependency parsing.
    nlp_dep = stanza.Pipeline(lang='sv', processors='depparse', depparse_pretagged=True, use_gpu=True)

    # Tag the corpus in batches.
    batch_count = 0
    sentence_count = 0
    for batched_doc in dat.read_batched_doc(source, 100, **kwargs):
        tagged_doc = nlp_dep(batched_doc)  # type: stanza.Document
        CoNLL.write_doc2conll(tagged_doc, target)

        batch_count += 1
        sentence_count += len(batched_doc.sentences)
        print(f'batch: {batch_count}, sentences: {sentence_count}')

        # Clear documents to free memory.
        # However, I'm not sure if this actually improves memory performance. Running the script 
        # (either at 100 or 1000 batchsize) seem to keep memory usage at ~1.2 GB.
        batched_doc.sentences = None
        tagged_doc.sentences = None
    
    print(f'Parsing complete. Parsed {sentence_count} sentences')


if __name__ == '__main__':
    #tag_bz2('processed data no-deps/gp2013-100k-clean.connlu.bz2', 'processed data/gp2013-100k.connlu.bz2')
    tag_bz2('processed data no-deps/familjeliv-adoption-100k-clean.connlu.bz2', 'processed data/familjeliv-adoption-100k.connlu.bz2')
    pass 
        
            