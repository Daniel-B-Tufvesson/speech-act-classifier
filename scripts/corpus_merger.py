"""
A script which merges several corpus files into a single file. All duplicate sentences will be 
removed (i.e. sentences that match exactly). The sentences will also recieve a new sent_id which
is an incremented integer. The original sent_id is saved as x_sent_id. The name of the corpus is 
also saved for each sentence.
"""

from context import speechact
import speechact.preprocess as pre
import speechact.corpus as corp

if __name__ == '__main__':
    corpora = [
        corp.Corpus('data/annotated data/dev-test-set.conllu.bz2'),
        corp.Corpus('data/annotated data/dev-train-set.conllu.bz2')
    ]

    target_file = 'data/annotated data/dev-set.conllu.bz2'
    pre.merge_corpora(corpora, target_file, print_progress=True, new_sent_ids=False)
    pre.print_initial_lines(target_file)