"""
A script which merges several corpus files into a single file. All duplicate sentences will be 
removed (i.e. sentences that match exactly). The sentences will also recieve a new sent_id which
is an incremented integer. The original sent_id is saved as x_sent_id. The name of the corpus is 
also saved for each sentence.
"""

from context import speechact
import speechact.preprocess as pre
import speechact.corpus as corp
import sys

if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) < 3:
        print('Usage: python merge_corpora.py <target corpus> <corpus 1> <corpus 2> ...')
        sys.exit(1)
    
    target_file = sys.argv[1]
    corpora = [corp.Corpus(file) for file in sys.argv[2:]]

    pre.merge_corpora(corpora, target_file, print_progress=True, new_sent_ids=False)
    pre.print_initial_lines(target_file)

# Example: python scripts/merge_corpora.py 'data/merged-set.conllu.bz2' 'data/dev-train-set.conllu.bz2' 'data/dev-test-set.conllu.bz2'