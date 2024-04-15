"""
Train an embedding-based classifier. 

Usage: python train_embedding_classifier.py <train corpus> <save model to file> <device> <batch size> <epochs> <use class weights> <load pre-existing model>
"""
# Example: python scripts/train_embedding_classifier.py 'data/train-set.conllu.bz2' 'models/neural/no-hidden/test-model.pth' cuda 32 10 True False
# Example: python scripts/train_embedding_classifier.py 'data/train-set.conllu.bz2' 'models/neural/no-hidden/test-model.pth' mps 32 10 True False

from context import speechact
import speechact.classifier.embedding as emb
import speechact.corpus as corp
import sys

if __name__ == '__main__':

    # Check the number of arguments passed
    if len(sys.argv) != 8:
        print('Usage: python train_embedding_classifier.py <train corpus> <save model to file> <device> <batch size> <epochs> <use class weights> <load pre-existing model>')
        sys.exit(1)
    
    train_corpus_file = sys.argv[1]
    model_name = sys.argv[2]
    device = sys.argv[3]
    batch_size = int(sys.argv[4])
    num_epochs = int(sys.argv[5])
    use_class_weights = bool(sys.argv[6])
    load_pre_existing = sys.argv[7] == 'True'

    print('Loading data...')
    train_corpus = corp.Corpus(train_corpus_file)
    train_data = emb.CorpusDataset(train_corpus)

    classifier = emb.EmbeddingClassifier(device=device)

    if load_pre_existing:
        print('Loading model.')
        classifier.load(model_name)

    print('Training network...')

    classifier.train(train_data,
                     batch_size=batch_size,
                     num_epochs=num_epochs,
                     use_class_weights=use_class_weights,
                     save_each_epoch=model_name)
    classifier.save(model_name)

    print('Training complete.')

