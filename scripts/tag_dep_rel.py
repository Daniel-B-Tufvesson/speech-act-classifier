"""
Parse dependency tags for CoNLL-U sentences. The dependency tags are the Universal 
Dependency Relations: https://universaldependencies.org/u/dep/index.html

Usage: python tag_dep_rel.py <source corpus|directory> <target directory>
"""
# Example: python scripts/tag_dep_rel.py 'data/for-testing/dir2/test-set.conllu.bz2' 'data/for-testing/dir2/tagged'

from context import speechact
import bz2
import speechact.preprocess as pre
import sys
import os

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

    # Check the number of arguments passed
    if len(sys.argv) != 3:
        print('Usage: python tag_dep_rel.py <source corpus|directory> <target directory>')
        sys.exit(1)

    source = sys.argv[1]
    target_dir = sys.argv[2]

    if os.path.isfile(source):
        source_file = source
        target_name = os.path.basename(source_file)
        target_file = os.path.join(target_dir, target_name)

        print(f'Tagging dep rels for "{source_file}" to "{target_file}"')
        tag_bz2(source_file, target_file)
    
    elif os.path.isdir(source):
        source_files = pre.list_files(source)

        for source_file in source_files:
            target_name = os.path.basename(source_file)
            target_file = os.path.join(target_dir, target_name)
            print(f'Tagging dep rels for "{source_file}" to "{target_file}"')
            tag_bz2(source_file, target_file)
    else:
        print(f'Error: "{source}" is neither a file nor a directory')

            