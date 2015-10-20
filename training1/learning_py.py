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

# the updated training code. This is the concept however, if there are
# many documents this part should be broken down to three parts since updating the
# loss is only when all queries were computed. For my purposes I took advantage of these
# independencies to run the code in parallel. (I did not upload the parallel version 
# but it you'd want you can email me dudy@ohsu.edu)
# details are in “OHSU @ MediaEval: Adapting Textual Techniques to Multimedia Search” 
#, S. Dudy, S. Bedrick, MediaEval Benchmarking Initiative for Multimedia Evaluation 
#(IEEE satellite event), Wurzen, 2015.

from __future__ import division
from collections import defaultdict
from random import shuffle, seed
from lda import ldaPrep, lsaPrep, lsaIt
from computeWs_py import compute_hsofR, compute_denom, \
     compute_num, compute_wd, compute_wr, doc_it
import numpy as np
import pickle
from datetime import datetime
import sys, os

#path = "data/X_test_all_1"
path = "data/lh"

if 1:
    from Xtraction3 import extractXY

    # extract features
    path2docs = "../../feats/both2/"

    # create dict word number and X
    X = extractXY(path2docs)
    with open(path, 'wb') as AutoPickleFile:
        pickle.dump((X), AutoPickleFile)
else:
    with open(path, 'rb') as AutoPickleFile:
        X = pickle.load(AutoPickleFile)

#sys.exit(os.EX_OK)
# divide set
allQueries = X.keys()
#allQueries = sorted(allQueries)  # seed
#rnd_seed = "stay"
#seed(rnd_seed)
#shuffle(allQueries) # for seed
#k = 10
#testQueries = allQueries[1::k]
#queries = list(set(allQueries) - set(testQueries))


# prepare lda
ldaPrep(allQueries, X)
#sys.exit(os.EX_OK)
#lsaPrep(allQueries, X)
sys.exit(os.EX_OK) 

path = "data/Hs_tag_cn"
if 0:
    #buit dicts for hs and doc
    HsR = {}
    for query in queries:
        #if query == "agra_fort":
         #   continue
        query == "agra_fort"
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
                doc_r = doc_it(doc, query)
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
if not os.path.exists(path):
    os.makedirs(path)
w_name = "second"
with open(path + name, 'wb') as AutoPickleFile:
    pickle.dump((wd, wr), AutoPickleFile)
