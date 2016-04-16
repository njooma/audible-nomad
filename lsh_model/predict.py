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


servermodel = "/home/ec2-user/audible-nomad/model.p"
localmodel = "/Users/pymetrics/Audible/audible-nomad/model.p"

with open(servermodel, "rb") as fp:
    model = pickle.load(fp)

fh = model["fh"]
lshf = model["lsh"]
labels = model["labels"]
location = model["location"]


def predict_book_and_location(words_list):
    text = copy.deepcopy(words_list)
    
    snowball_stemmer = SnowballStemmer("english")
    text = stem_words(text, snowball_stemmer)
    text += get_ngrams(text, [2,3])
    corpus = [text]

    counts = corpus_to_counts(corpus)
    X = fh.transform(counts)

    pred = lshf.kneighbors(X, return_distance=False)[0]

    label = get_label(pred, labels)
    loc = get_location(pred, location)

    sync_data = books[label]["locations"][loc]
    sec = float(sync_data[2])
    ms_start = sec * 1000

    return label, ms_start