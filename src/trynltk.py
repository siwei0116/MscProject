import nltk
from nltk.util import everygrams

sentence = 'C00213 is a part'


def nGram(txt, n):  # To deal with phrases
    a = list(everygrams(nltk.word_tokenize(txt), max_len=3))
    b = [" ".join(word) for word in a]
    return b


print(nGram(sentence, 3))
