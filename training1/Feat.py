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

from __future__ import division
import numpy as np
from scipy.spatial.distance import cdist
# compute color similarity

def mahalDistance(doc, s):
    
    maha_mean = []
    #x = np.array(doc)
    x = np.reshape(doc, (64, 64))
    for y in s:
        y = np.reshape(y, (64, 64))
        X = np.vstack([x,np.array(y)])
        V = np.cov(X.T)
        Vi = np.linalg.pinv(V)
        if 1:
            res = cdist(x,y,'mahalanobis', VI = Vi)
            out = np.mean(res)
        else:
            xy = x-y
            inner = np.dot(np.dot(xy, VI), xy.T)
            out = np.mean(np.diag(np.sqrt(inner)))
        maha_mean.append(out)
    return np.mean(maha_mean)

def feat_field(doc, s, feat):
    
    doc = doc[feat][:-1]
    
    #for num in doc:
	#try:
	    #if num!=u'0':
		#print float(num)
	    #else:
		#print 0.0
	#except:
	    #print "problem with ",num    
    
    # convert to float
    doccn = [float(i) for i in doc]
    docscn = []
    for doc in s:
        doc = doc[feat][:-1]
        doc = [float(i) for i in doc]  
        docscn.append(doc)
    return doccn, docscn
