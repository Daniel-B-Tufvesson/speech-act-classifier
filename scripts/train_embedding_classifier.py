"""

"""

from context import speechact
import speechact.classifier.embedding as emb
import speechact.corpus as corp

if __name__ == '__main__':
    #labels = [act.value for act in emb.SPEECH_ACTS]

    print('Loading data...')
    train_corpus = corp.Corpus('data/auto-annotated data/speech-acts.conllu.bz2')
    #train_corpus = corp.Corpus('data/annotated data/dev-set-sentiment-test.conllu.bz2')
    train_data = emb.CorpusDataset(train_corpus)


    print('Loading model.')
    classifier = emb.EmbeddingClassifier(device='cuda')
    model_name = 'models/neural/no-hidden/liu-projdator-model.pth'
    classifier.load(model_name)

    print('Training network...')

    classifier.train(train_data,
                     batch_size=16,
                     num_epochs=9,
                     use_class_weights=True,
                     save_each_epoch=model_name)
    classifier.save(model_name)

    print('Training complete.')
