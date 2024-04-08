"""

"""

from context import speechact
import speechact.classifier.embedding as emb
import speechact.corpus as corp

if __name__ == '__main__':
    labels = [act.value for act in emb.SPEECH_ACTS]

    #train_corpus = corp.Corpus('data/auto-annotated data/speech-acts.conllu.bz2')
    train_corpus = corp.Corpus('data/annotated data/dev-set-sentiment-test.conllu.bz2')
    train_data = emb.CorpusDataset(train_corpus)


    classifier = emb.EmbeddingClassifier(device='cuda')

    classifier.train(train_data,
                     batch_size=32,
                     num_epochs=1,
                     use_class_weights=True)
    classifier.save('models/neural/no-hidden/liu-projdator-model.pth')
