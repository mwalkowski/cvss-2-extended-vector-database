import os
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

#Settings
TOP_WORD_COUNT = 50
INPUT_FILE = os.path.join(os.getcwd(), 'input_data', 'cvss_2_3.csv')
OUTPUT_FILE = os.path.join(os.getcwd(), 'output_data', F'data_word_{TOP_WORD_COUNT}.csv')

INPUT_FILE_SEPARATOR = '|'


def load_data():
    with open(INPUT_FILE) as file:
        return [line.split(INPUT_FILE_SEPARATOR) for line in file]


def get_words_list(data):
    ps = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    filtered_sent = []
    m = re.compile('[a-z]+')

    for text in data:
        translator = str.maketrans('', '', string.punctuation)
        for word in word_tokenize(text[1].translate(translator)):
            if word not in stop_words and m.match(word):
                s = ps.stem(word)
                filtered_sent.append(s)

    return filtered_sent


def count_words_in_summary(text, top_words):
    ps = PorterStemmer()
    result = [0] * len(top_words)
    translator = str.maketrans('', '', string.punctuation)
    for word in word_tokenize(text.translate(translator)):
        s = ps.stem(word)
        if s in top_words:
            result[top_words.index(s)] += 1
    return [str(i/100) for i in result]


if __name__ == '__main__':
    print('Loading data...')
    data = load_data()
    print('Data loaded, creating words list...')

    dictionary = get_words_list(data)
    print('All used words', len(dictionary), 'counting frequency...')

    freq = nltk.FreqDist(dictionary)
    freq = {k: v for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True)}
    top_words = []
    print(F'Selecting top {TOP_WORD_COUNT} used words...')
    for key,val in freq.items():
        if len(top_words) < TOP_WORD_COUNT:
            top_words.append(key)

    print('Words selected, sorting alphabetically..')
    top_words = sorted(top_words)
    out = []

    print('Preparing output...')
    for d in data:
        r = count_words_in_summary(d[1], top_words)
        dict_len = len(r)
        r.extend(d[2:])
        if r not in out:
            out.append(u' '.join(r))

    print('Output data count', len(out))
    with open(OUTPUT_FILE, 'w') as out_file:
        for d in out:
            out_file.write(d)

    print('Output saved')

    max_len = 0
    with open(OUTPUT_FILE) as file:
        for line in file:
            max_len = len(line.split(' '))
            break

    print(F'X 1:{dict_len + 7}')
    print('All columns', max_len)
