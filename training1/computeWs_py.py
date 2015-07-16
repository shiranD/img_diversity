from __future__ import division
from math import exp
from lda import ldaIt
from cosine import CosineSimilarity
from cn import cn_field, cnDistance
import json
from collections import Counter
import numpy as np
from wordIt import extract_words


"""" open the dict that assigns every word
     to its place in relevance vector"""
json_file = "dict/Termdict"
with open(json_file) as f1:
    for line in f1:  # extract jsons
        termdict = json.loads(unicode(line))


path = "data/Hs"
with open(path, 'rb') as AutoPickleFile:
    HsR = pickle.load(AutoPickleFile)

def compute_hsofR(doc, s, query):
    """input: dict of doc
              chosen docs
              the query
        output: the diversity
                vector of the doc
                agaist the chosen"""
    Rmatrix = computeR(doc, s, query)
    hvector = computeHofR(Rmatrix)
    return np.array(hvector)


def computeR(doc, s, query):
    """compute different diversity features"""
    r1 = ldaIt(doc, s, query)
    docb, sb = bagwords(doc, s)
    r2 = CosineSimilarity().buildMat(docb, sb)
    doccn, scn = cn_field(doc, s)
    r3 = cnDistance(doccn, scn)
    return [r1, r2, r3]


def computeHofR(Rmat):
    """h function is min value
       of every feature"""
    num = 1
    vec = []
    if num == 1:  # take
        for feat in Rmat:
            vec.append(min(feat))
    return np.array(vec)


def bagwords(doc, s):
    """creats a list of tokens without
       stopwords"""
    ddoc = extract_words(doc)
    ddocs = []
    for doc in s:
        ddocs.append(extract_words(doc))

    return ddoc, ddocs


def compute_denom(doc_set, s, query, wd_q, wr_p):

    sumOfExp = 0
    for i, doc in enumerate(doc_set):
        hs_ofR = HsR[query][i]
        doc_rl = doc_it(doc)
        power = np.dot(wr_p, doc_rl) + np.dot(wd_q, hs_ofR)
        sumOfExp += exp(power)
        s.append(doc)  # update s

    return sumOfExp


def compute_wr(doc_set, s, query, wd_q, wr_p):
    # make sure dimentions work as the exp is scaler
    sumOfExp = 0
    
    for i, doc in enumerate(doc_set):
        hs_ofR = HsR[query][i]
        doc_rl = doc_it(doc)
        power = np.dot(wr_p, doc_rl) + np.dot(wd_q, hs_ofR)
        sumOfExp += doc_rl * exp(power)
        s.append(doc)  # update s

    return sumOfExp


def compute_wd(doc_set, s, query, wd_q, wr_p):

    sumOfExp = 0
    for i, doc in enumerate(doc_set):
        hs_ofR = HsR[query][i]
        doc_rl = doc_it(doc)
        power = np.dot(wr_p, doc_rl) + np.dot(wd_q, hs_ofR)
        sumOfExp += hs_ofR * exp(power)
        s.append(doc)  # update s

    return sumOfExp


def compute_num(doc, s, query, wd_q, wr_p):

    # just one current doc
    hs_ofR = HsR[query][len(s)]
    hs_ofR = compute_hsofR(doc, s, query)
    doc_rl = doc_it(doc)
    power = np.dot(wr_p, doc_rl) + np.dot(wd_q, hs_ofR)
    return hs_ofR * exp(power)


def doc_it(a_doc):
    """"create relevance vector
        future use all fields from
        extract_words"""
    words = extract_words(a_doc)
    counter = Counter(words)
    vec = len(termdict) * [0]
    l_doc = len(words)
    for (word, count) in counter.iteritems():
        # normalize
        vec[termdict[word]] = count / l_doc
    # add img features
    # cn
    cn = a_doc["cn"] # is normalized
    cn = [float(i) for i in cn]
    vec.extend(cn)
    return np.array(vec)
