from sentence import Sentence
from sentence import Word




def classify(sentence : Sentence):
    print('classify: ', sentence)



def test1():
    print('test1')

    # Create test sentence.
    sentence = Sentence()
    sentence.words.append(Word('Jag'))
    sentence.words.append(Word('har'))
    sentence.words.append(Word('en'))
    sentence.words.append(Word('bil'))
    sentence.words.append(Word('.'))

    # Test classification function.
    classification = classify(sentence)


if __name__ == '__main__':
    test1()