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

import pickle
import numpy as np
from Feat import feat_field, mahalDistance

# serial
wpath = "../"
outpath = "../cnn_hs/"
path = "data/lh"
#queries = open(fquery, "r")

with open(path, 'rb') as AutoPickleFile:
    X = pickle.load(AutoPickleFile)

for query in queries:
    query = query.strip() 
    qweights = wpath + query
    print "in q"
    with open(qweights, 'rb') as AutoPickleFile:
        HsR = pickle.load(AutoPickleFile)
    doc_set = X[query]  # given a ordered doc set
    cnnHs = []
    s = []
    for i, doc in enumerate(doc_set):
        if not s:
            s.append(doc)
            continue
        doccnn, scnn = feat_field(doc, s, "cnn2")
        r9 = mahalDistance(doccnn, scnn)
        new_hs = HsR[i-1]
        print new_hs
        new_hs.append(r9)
        new_hs/=abs(max(new_hs))
        print new_hs
        cnnHs.append(new_hs)
    pathq = outpath+query
    with open(pathq, 'wb') as AutoPickleFile:
        pickle.dump((cnnHs), AutoPickleFile) 