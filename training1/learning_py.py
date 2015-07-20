from __future__ import division
from collections import defaultdict
from random import shuffle, seed
from lda import ldaPrep
from computeWs_py import compute_hsofR, compute_denom, \
     compute_num, compute_wd, compute_wr, doc_it
import numpy as np
import pickle
from datetime import datetime
import sys, os

path = "data/X"

if 0:
    from Xtraction3 import extractXY

    # extract features
    path2docs = "../../feats/both/"
    path2rlvnce = "../../gt/rGT/"

    # create dict word number and X
    X = extractXY(path2docs, path2rlvnce)
    with open(path, 'wb') as AutoPickleFile:
        pickle.dump((X), AutoPickleFile)
else:
    with open(path, 'rb') as AutoPickleFile:
        X = pickle.load(AutoPickleFile)

# divide set
allQueries = X.keys()
allQueries = sorted(allQueries)  # seed
rnd_seed = "stay"
seed(rnd_seed)
shuffle(allQueries) # for seed
k = 10
testQueries = allQueries[1::k]
queries = list(set(allQueries) - set(testQueries))


# prepare lda
# ldaPrep(allQueries, X)

path = "data/Hs"
if 0:
    #buit dicts for hs and doc
    HsR = {}
    for query in queries:
        if query == "agra_fort":
            continue
        
        doc_set = X[query]  # given a ordered doc set
        s = []
        docsR = []
        for i, doc in enumerate(doc_set):
            if not s:
                s.append(doc)
                continue
            hs_ofR = compute_hsofR(doc, s, query)
            docsR.append(hs_ofR)
            s.append(doc)
        HsR[query] = docsR
        print query
        
            
    with open(path, 'wb') as AutoPickleFile:
        pickle.dump((HsR), AutoPickleFile)
else:
    
    with open(path, 'rb') as AutoPickleFile:
        HsR = pickle.load(AutoPickleFile)       

#sys.exit(os.EX_OK) # code 0, all ok
# init parameters
iterNum = 1
wr_len = 29890
eta = 1
eps = 0.1
wd = np.zeros(3)
wr = np.zeros(wr_len)
old_loss = 0
# train
for a in xrange(iterNum):

    shuffle(queries)  # on queries

    for query in queries:
        if query == "agra_fort":
            continue        
        wd_q = np.zeros(3)
        wr_q = np.zeros(wr_len)  # TBD how to represent
        doc_set = X[query]  # given a ordered doc set
        s = []
        R = HsR[query]

        for i, doc in enumerate(doc_set):

            if not s:  # if s is empty of docs
                s.append(doc)
                continue

            else:
                # compute wd_q for one
                hs_ofR = R[i-1]
                # compute wr_q for one
                doc_r = doc_it(doc)
                # compute wd_q for rest
                wd_rest = compute_wd(doc_set[i:], s, query, wd_q, wr_q, R[i-1:])
                # compute wr_q for rest
                wr_rest = compute_wr(doc_set[i:], s, query, wd_q, wr_q, R[i-1:])
                # compute denominator
                denom = compute_denom(doc_set[i:], s, query, wd_q, wr_q, R[i-1:])

            # subtract wd_q
            wd_q += wd_rest / denom - hs_ofR
            # subtract wr_q
            wr_q += wr_rest / denom - doc_r
            # update w's
            s.append(doc)
            print i, str(datetime.now())
            
        print query, str(datetime.now())

        # update model weight vectors
        wd += eta * wd_q
        wr += eta * wr_q

    # calculate the loss
    loss = 0
    for query in queries:
        if query == "agra_fort":
            continue        
        doc_set = X[query]  # given a ordered doc set
        s = []
        R = HsR[query]
        
        for i, doc in enumerate(doc_set):
            if not s:
                continue

            num = compute_num(doc, s, query, wd, wr, R[i-1])

            denom = compute_denom(doc_set[i:], s, query, wd, wr, R[i-1:])

            loss += np.log(num / denom)

    # no minus sign was added since their gap is what matters
    if old_loss - loss < eps:
        break
    else:
        old_loss = loss

# store wd, wr
path = "weights_py/"
name = "second"
with open(path + name, 'wb') as AutoPickleFile:
    pickle.dump((wd, wr), AutoPickleFile)
