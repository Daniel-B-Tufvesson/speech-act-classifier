"""
A script which merges several corpus files into a single file. All duplicate sentences will be 
removed (i.e. sentences that match exactly). The sentences will also recieve a new sent_id which
is an incremented integer. The original sent_id is saved as x_sent_id. The name of the corpus is 
also saved for each sentence.
"""


import speechact.preprocess as pre
import speechact.corpus as corp

if __name__ == '__main__':
    corpora = [
        corp.Corpus('processed data no-deps clean/familjeliv-adoption-100k.connlu.bz2', 'familjeliv-adoption'),
        corp.Corpus('processed data no-deps clean/familjeliv-allmanna-ekonomi-100k.connlu.bz2', 'familjeliv-allmanna-ekonomi')
    ]

    target_file = 'merge corpora test.connlu.bz2'
    pre.merge_corpora(corpora, target_file, print_progress=True)
    pre.print_initial_lines(target_file)