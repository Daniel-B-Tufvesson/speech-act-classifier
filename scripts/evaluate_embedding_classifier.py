"""
This script evaluates an embedding classifier.
"""

from context import speechact
import speechact.classifier.embedding as emb
import speechact.corpus as corp
import speechact.evaluation as eval
import speechact.annotate as anno

def train_model(data_file: str, model_name: str):
    print('Load classifier')
    classifier = emb.EmbeddingClassifier()

    print('Load dataset')
    corpus = corp.Corpus(data_file)
    dataset = emb.CorpusDataset(corpus)
    
    print('Train classifier')
    classifier.train(dataset, 32, print_progress=True)
    classifier.save(model_name)


def evaluate_model(data_file: str, model_name: str):
    print('Load classifier')
    classifier = emb.EmbeddingClassifier()
    classifier.load(model_name)

    print('Load dataset')
    corpus = corp.Corpus(data_file)

    labels = anno.SpeechActLabels.get_labels()

    print('Evaluate classifier')
    eval.evaluate(
        corpus,
        classifier,
        labels,
        draw_conf_matrix=True
    )


if __name__ == '__main__':
    # train_model(
    #     data_file='data/annotated data/dev-set-sentiment-test.conllu.bz2',
    #     model_name='models/neural/dev-model.pth'
    # )

    evaluate_model(
        data_file='data/annotated data/dev-set-sentiment-train.conllu.bz2',
        model_name='models/neural/dev-model.pth'
    )


    


