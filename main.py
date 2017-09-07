#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import collections
import json
import sys

training_filepath="lang_train.json"

def word_tokenize(text):
    # NOTE: This should be replaced by nltk's word_tokenization.
    return text.split(' ')

def load_training_data():
    "Return generator yielding {'lang': 'en', 'text': 'blablabla', 'subject': 'something'}"
    for line in open(training_filepath, 'rb'):
        try:
            yield json.loads(line)
        except Exception as e:
            print('Invalid line', line, e)

def load_test_data():
    "Return generator yielding {'text': 'blablabla', 'example': 1}"
    for line in sys.stdin:
        try:
            yield json.loads(line)
        except Exception as e:
            print('Invalid line', line, e)

def tokenize_data(data, key):
    "Return {'en': set('word', 'otherword'), ...}"

    tokenized_data = collections.defaultdict(set)

    for row in data:
        tokens = word_tokenize(row['text'])
        tokenized_data[row[key]].update(tokens)

    return tokenized_data


def score_test_words(test_words, training_data):
    "Return { 'en': 32, 'fr': 20, ... }"
    return [
        (lang, len(words.intersection(test_words)),)
        for lang, words in training_data.items()
    ]

def get_best_language_based_on_score(scored_test_words):
    scored_test_words.sort(key=lambda item: item[1])
    return scored_test_words[-1]

def get_languages_for_test_data(test_data, training_data):
    "Return {1: 'en', 3: 'fr'}"
    result = []
    for example, words in test_data.items():
        scored_words = score_test_words(words, training_data)
        language, score = get_best_language_based_on_score(scored_words)

        #print(language, scored_words)
        result.append({'example': example, 'lang': language, 'words': list(words), 'score': score})
    return result

def main():
    training_data = load_training_data()
    tokenized_training_data = tokenize_data(training_data, key='lang')

    test_data = load_test_data()
    tokenized_test_data = tokenize_data(test_data, key='example')

    for row in get_languages_for_test_data(tokenized_test_data, tokenized_training_data):
        print(json.dumps(row))


if __name__ == '__main__':
    main()
