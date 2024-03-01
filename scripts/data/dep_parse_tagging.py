"""
Parse dependency tags for CoNNL-U sentences. The dependency tags are the Universal 
Dependency Relations: https://universaldependencies.org/u/dep/index.html
"""

import bz2
from speechact.preprocess import tag_dep_rel

def tag_bz2(source_file: str, target_file: str, **kwargs):
    """
    Tag a bz2 compressed connlu corpus. The tagged results are written to bz2 compressed
    connlu corpus as well. 
    """
    print('tag_bz2')
    with bz2.open(source_file, mode='rt') as source:
        with bz2.open(target_file, mode='wt') as target:
            tag_dep_rel(source, target, print_progress=True, **kwargs)


if __name__ == '__main__':
    #tag_bz2('processed data no-deps/gp2013-100k-clean.connlu.bz2', 'processed data/gp2013-100k.connlu.bz2')
    tag_bz2('processed data no-deps/familjeliv-adoption-100k-clean.connlu.bz2', 'processed data/familjeliv-adoption-100k.connlu.bz2')
    pass 
        
            