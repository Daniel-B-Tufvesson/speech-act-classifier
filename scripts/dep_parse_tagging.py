"""
Parse dependency tags for CoNNL-U sentences. The dependency tags are the Universal 
Dependency Relations: https://universaldependencies.org/u/dep/index.html
"""

from context import speechact
import bz2
import speechact.preprocess as pre

def tag_bz2(source_file: str, target_file: str, **kwargs):
    """
    Tag a bz2 compressed connlu corpus. The tagged results are written to bz2 compressed
    connlu corpus as well. 
    """
    print('tag_bz2')
    with bz2.open(source_file, mode='rt') as source:
        with bz2.open(target_file, mode='wt') as target:
            pre.tag_dep_rel(source, target, print_progress=True, **kwargs)


if __name__ == '__main__':
    source_files = pre.lines('data/reindexed data/data files.txt')
    target_dir = 'data/tagged data'

    for source_file in source_files:
        target_file_name = source_file.split('/')[-1]
        target_file_path = f'{target_dir}/{target_file_name}'

        print(f'Tagging dep rels for "{source_file}" to "{target_file_path}"')
        tag_bz2(source_file, target_file_path)
        
            