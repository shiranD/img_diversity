#Copyright (c) 2015 Shiran Dudy.
#All rights reserved.

#Redistribution and use in source and binary forms are permitted
#provided that the above copyright notice and this paragraph are
#duplicated in all such forms and that any documentation,
#advertising materials, and other materials related to such
#distribution and use acknowledge that the software was developed
#by the CSLU. The name of the
#CSLU may not be used to endorse or promote products derived
#from this software without specific prior written permission.
#THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
#IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

# main training code

from __future__ import division
from random import shuffle, seed
from lda import ldaPrep
from computeWs import compute_hsofR, compute_denom, \
     compute_num, compute_wd, compute_wr, doc_it
import numpy as np
import pickle
from datetime import datetime

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
#ldaPrep(allQueries, X)


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
        wd_q = np.zeros(3)
        wr_q = np.zeros(wr_len)  # TBD how to represent
        doc_set = X[query]  # given a ordered doc set
        s = []

        for i, doc in enumerate(doc_set):

            if not s:  # if s is empty of docs
                s.append(doc)
                continue

            else:
                # compute wd_q for one
                hs_ofR = compute_hsofR(doc, s, query)
                # compute wr_q for one
                doc_r = doc_it(doc)
                # compute wd_q for rest
                wd_rest = compute_wd(doc_set[i:], s, query, wd_q, wr_q)
                # compute wr_q for rest
                wr_rest = compute_wr(doc_set[i:], s, query, wd_q, wr_q)
                # compute denominator
                denom = compute_denom(doc_set[i:], s, query, wd_q, wr_q)

            # subtract wd_q
            wd_q += wd_rest / denom - hs_ofR
            # subtract wr_q
            wr_q += wr_rest / denom - doc_r
            # update w's

            s.append(doc)
        print query
        print str(datetime.now())

    # update model weight vectors
    wd += eta * wd_q
    wr += eta * wr_q

    # calculate the loss
    loss = 0
    for query in queries:
        doc_set = X[query]  # given a ordered doc set
        s = []
        for i, doc in enumerate(doc_set):

            num = compute_num(doc, s, query, wd, wr)

            denom = compute_denom(doc_set[i:], s, query, wd, wr)

            loss += np.log(num / denom)

    # no minus sign was added since their gap is what matters
    if old_loss - loss < eps:
        break
    else:
        old_loss = loss

# store wd, wr
path = "weights/"
name = "first"
with open(path + name, 'wb') as AutoPickleFile:
    pickle.dump((wd, wr), AutoPickleFile)
