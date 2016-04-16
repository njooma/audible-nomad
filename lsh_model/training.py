from __future__ import unicode_literals
from __future__ import absolute_import

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import FeatureHasher
from sklearn.neighbors import LSHForest
from sklearn.cross_validation import train_test_split
from collections import Counter
import numpy as np
import random
import pickle
import re
import string
import copy
from itertools import combinations
from nltk.stem import SnowballStemmer

from .utils import *


def train_model(filename):
    snowball_stemmer = SnowballStemmer("english")

    print "first pass through data..."
    corpus = []
    labels = []
    location = []
    for label, book in label_dict.items():
        words = map(lambda s: str(s.decode("ascii", "ignore")), 
                    books[book]["words"])
        for i, start in enumerate(range(len(words)-100)):
            text = get_section(words, start)
            text = stem_words(text, snowball_stemmer)
            text += get_ngrams(text, [2,3])
            corpus.append(text)
            labels.append(label)
            location.append(i)

    print "second pass..."
    n_samples = len(labels)
    for i in range(n_samples):
        text = copy.deepcopy(corpus[i])
        label = labels[i]
        loc = location[i]
        remove_words(text, random.randint(1, len(text)/4))
        fudge_up_words(text, random.randint(1, len(text)/4))
        corpus.append(text)
        labels.append(label)
        location.append(loc)

    print "third pass..."
    n_samples = len(labels)
    for i in range(n_samples):
        text = copy.deepcopy(corpus[i])
        label = labels[i]
        loc = location[i]
        remove_words(text, random.randint(1, len(text)/4))
        fudge_up_words(text, random.randint(1, len(text)/4))
        corpus.append(text)
        labels.append(label)
        location.append(loc)


    print "creating features..."
    counts = corpus_to_counts(corpus)
    fh = FeatureHasher(n_features=5000)
    X = fh.transform(counts)
    y = np.array(labels)
    locs = np.array(location)

    print "fitting model..."
    lshf = LSHForest()
    lshf.fit(X)

    model = {
        "fh": fh,
        "lsh": lshf,
        "labels": y,
        "location": locs
    }

    print "saving..."
    with open("model.p", "wb") as fp:
        pickle.dump(model, fp)









