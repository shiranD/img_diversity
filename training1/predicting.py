import pickle
import numpy as np
from random import shuffle, seed
from searchBest import argMax_XleftOvers
# take out np

# load the weights
if 0:
    with open(path + name, 'rb') as AutoPickleFile:
        wd, wr = pickle.load(AutoPickleFile)
else:
    # just cause we haven't run it entirely
    wr_len = 29890
    wd = np.random.randn(3)
    wr = np.random.randn(wr_len)

datapath = "data/X"
with open(datapath, 'rb') as AutoPickleFile:
    X = pickle.load(AutoPickleFile)

allQueries = X.keys()
allQueries = sorted(allQueries)  # seed
# rnd_seed = "stay" # will is stay the same when I use predicting and learning?
# seed(rnd_seed)
# shuffle(allQueries) # for seed
k = 10
testQueries = allQueries[1::k]


pathRankings = "../rankings/"
num_Docs = 10
eps = 0.5
for query in testQueries:
    doc_set = X[query]  # given a ordered doc set
    s = []
    s_id = []
    left = doc_set
    for i in xrange(len(doc_set)):

        ind, gain = argMax_XleftOvers(left, s, wd, wr, query)
        if gain < eps:  # if the best gain is very small
            break
        s.append(left[ind])  # add to final rank
        s_id.append(str(left[ind]["id"]))  # add to final rank (take only id)
        del left[ind]  # remove from X\S
        if len(s) > num_Docs:  # if we chose more than num_Docs
            break

    with open(pathRankings + query, 'rb') as rankFile:
        for idnum in s_id:
            rankFile.write(idnum)
            rankFile.write("\n")
