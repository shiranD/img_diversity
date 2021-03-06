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

# this is the main test code to score iteratively each document
# can also be done in parallel per query if you want the parallel version
# email me dudy@ohsu.edu
# details are in “OHSU @ MediaEval: Adapting Textual Techniques to Multimedia Search” 
#, S. Dudy, S. Bedrick, MediaEval Benchmarking Initiative for Multimedia Evaluation 
#(IEEE satellite event), Wurzen, 2015.

import pickle
from random import shuffle, seed
from searchBest import argMax_XleftOvers
from topics import dict_topics
from imghtml import htmlwrite
from datetime import datetime
#import numpy as np

# take out np

topic_paths = ["../devset_topics.xml", "../testset_multi-topics.xml","../testset_one-topics.xml"]
topDict = dict_topics(topic_paths)
# load the weights

pathw = "weights_py/second"
with open(pathw, 'rb') as AutoPickleFile:
    wd, wr = pickle.load(AutoPickleFile)
#else:
    ## just cause we haven't run it entirely
    #wr_len = 29890
    #wd = np.random.randn(3)
    #wr = np.random.randn(wr_len)

datapath = "data/X_tag_cn"
with open(datapath, 'rb') as AutoPickleFile:
    X = pickle.load(AutoPickleFile)

#allQueries = X.keys()
#allQueries = sorted(allQueries)  # seed
#rnd_seed = "stay" # will is stay the same when I use predicting and learning?
#seed(rnd_seed)
#shuffle(allQueries) # for seed
#k = 10
#testQueries = allQueries[1::k]


pathRankings = "../rankings2/"
num_Docs = 20
eps = 1
querysRanks = {}
irl = []
cov = []
testQueries = ["agra_fort"]
for query in testQueries:
    doc_set = X[query]  # given a ordered doc set
    s = []
    s_id = []
    urls = []
    left = doc_set
    for i in xrange(len(doc_set)):

        ind, gain = argMax_XleftOvers(left, s, wd, wr, query)
        #if gain < eps:  # if the best gain is very small
         #   break
        s.append(left[ind])  # add to final rank
        s_id.append([left[ind]["id"], gain])  # add to final rank (take only id)
        urls.append(left[ind]["url_b"])
        del left[ind]  # remove from X\S
        if len(s) > num_Docs:  # if we chose more than num_Docs
            break
        print ind, str(datetime.now())
        
    querysRanks[query] = s_id # dict the ranks per query 
    print query, str(datetime.now())    
    if 1: #write an html per query with ordered urls
        ir_q, cov_q = htmlwrite(query, s_id, urls)
        irl.append(ir_q)
        cov.append(cov_q)
    print "total irrelevance rate: ", sum(irl)/len(irl)
    print "total coverage rate: ", sum(cov)/len(cov)
    
        

if 1: # submission format
    # get topics dict    
    topic_path = "../../devset_topics.xml"
    topDict = dict_topics(topic_path)
    res_path = pathRankings+"csluRanking.txt"
    fout = open(res_path, "w")
    run_id = "cslu"
    itern = "0"
    for query in testQueries: # for test set
        q_ranks = querysRanks[query]
        q_id = topDict[query]
        for i, (docno, score) in enumerate(q_ranks):
            fout.write("{0} {1} {2} {3} {4:"        ">.2f} {5}".format(
                            q_id.ljust(7),
                            itern.rjust(4), docno.rjust(10), \
                            str(i).rjust(5), score,\
                            run_id.rjust(10)
                            ))
            fout.write("\n")
    fout.close()
            
            
            
        
# we assume the scores are getting lower as we continue choosing more docs