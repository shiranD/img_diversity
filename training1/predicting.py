import pickle
import numpy as np
from random import shuffle, seed
from searchBest import argMax_XleftOvers
from topics import dict_topics
from imghtml import htmlwrite
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
querysRanks = {}
for query in testQueries:
    doc_set = X[query]  # given a ordered doc set
    s = []
    s_id = []
    urls = []
    left = doc_set
    for i in xrange(len(doc_set)):

        ind, gain = argMax_XleftOvers(left, s, wd, wr, query)
        if gain < eps:  # if the best gain is very small
            break
        s.append(left[ind])  # add to final rank
        s_id.append([left[ind]["id"], gain])  # add to final rank (take only id)
        urls.append(left[ind]["url_b"])
        del left[ind]  # remove from X\S
        if len(s) > num_Docs:  # if we chose more than num_Docs
            break
        
    querysRanks[query] = s_id # dict the ranks per query
    if 1: #write an html per query with ordered urls
        htmlwrite(query, s_id, urls)

if 0: # submission format
    # get topics dict    
    topic_path = "../../devset_topics.xml"
    topDict = dict_topics(topic_path)
    res_path = "../ranking/csluRanking.txt"
    fout = open(res_path, "w")
    run_id = "cslu"
    itern = "0"
    for query, val in topDict.iteritems():
        q_ranks = querysRanks[query]
        q_id = topDict[query]
        for i, (docno, score) in enumerate(q_ranks):
            fout.write("{0} {1} {2} {3} {4} {5:.2f} {6}".format(
                            q_id.ljust(7),
                            itern.rjust(4), docno.rjust(20), \
                            str(i).rjust(5), score.rjust(20),\
                            run_id.rjust(10)
                            ))
            fout.write("\n")
            
            
            
        
# we assume the scores are getting lower as we continue choosing more docs