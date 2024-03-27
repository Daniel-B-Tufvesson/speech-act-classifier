"""
This script generates an embedding file from a CoNLL-U corpus. An embedding is computed for each
sentence. These are Swedish SBERT embeddings.
"""
from context import speechact
import speechact.classifier.embedding as emb

if __name__ == '__main__':
    source_file = 'data/annotated data/dev-set-sentiment.conllu.bz2'
    target_file = 'data/annotated data/dev-set-embedding.bz2'

    emb.create_embeddings(source_file, target_file, print_progress=True)
    



