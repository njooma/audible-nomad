from __future__ import unicode_literals
from __future__ import absolute_import

from collections import Counter
import numpy as np
import random
import re
import string
import copy
import pickle
from itertools import combinations


serverbooks = "/home/ec2-user//audible-nomad/parsed_books.p"
localbooks = "/Users/pymetrics/Audible/audible-nomad/parsed_books.p"

with open(serverbooks, "rb") as fp:
    books = pickle.load(fp)
label_dict = {i: b for i, b in enumerate(books.keys())}



def get_section(words, start, seq=7, lines=10, skip=3):
    text = []
    for i in range(lines):
        beg = start + (i * (seq+skip))
        end = beg + seq
        text += words[beg:end]
    return text

def remove_words(words, n_words=3):
    for _ in range(n_words):
        try:
            idx = random.randint(0,len(words)-1)
            words.pop(idx)
        except:
            continue

chars = string.digits + string.ascii_letters + string.punctuation
def change_letter(word, n, char):
    s = list(word)
    s[n] = char
    return "".join(s)

def fudge_up_words(words, n_words=5):
    for _ in range(n_words):
        try:
            idx = random.randint(0, len(words)-1)
            word = words[idx]
            word_idx = random.randint(0, len(word)-1)
            char_idx = random.randint(0, len(chars)-1)
            words[idx] = change_letter(word, word_idx, chars[char_idx])
        except:
            continue

def stem_words(words, stemmer):
    return [stemmer.stem(w) for w in words] 

def get_ngrams(words, list_of_n):
    new_words = []
    for n in list_of_n:
        ngrams = map(lambda w: " ".join(w), 
                     zip(*[words[i:] for i in range(n)]))
        new_words.extend(ngrams)
    return new_words

def corpus_to_counts(corpus):
    return [Counter(x) for x in corpus]

def get_label(predicted, true_labels):
    c = Counter(map(lambda i: label_dict[i], true_labels[predicted]))
    return c.most_common(1)[0][0]

def hit_or_miss(predicted, label, train_labels):
    p = get_label(predicted, train_labels)
    a = label_dict[label]
    return 1 if p==a else 0

def get_location(predicted, train_locs, m=2):
    ls = train_locs[predicted]
    ls = ls[abs(ls - np.mean(ls)) < m * np.std(ls)]
    return int(np.mean(ls))

def distance_from_start(predicted, loc, train_locs):
    l = get_location(predicted, train_locs)
    return l - loc











