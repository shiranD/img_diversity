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

# compute color similarity

def l1Distance(doc, s):
    
    simi_vec = []
    for a_doc in s:
                
        summ = 0
        for i in xrange(len(doc)): # compute dist
            ll_doc = a_doc[i]
            ll_cand = doc[i]
            summ+= np.abs(ll_doc-ll_cand)
        sim = summ
        simi_vec.append(sim) 
    return simi_vec   

def chisquareDistance(doc,s):
    
    simi_vec = []
    for a_doc in s:
                
        summ = 0
        for i in xrange(len(doc)): # compute dist
            ll_doc = a_doc[i]
            ll_cand = doc[i]
            summ+= (ll_doc-ll_cand)**2/(ll_doc+ll_cand)
        sim = summ /2
        simi_vec.append(sim) 
    return simi_vec     

def canberraDistance(doc, s):
    
    simi_vec = []
    for a_doc in s:
                
        summ = 0
        for i in xrange(len(doc)): # compute dist
            ll_doc = a_doc[i]
            ll_cand = doc[i]
            summ+= np.abs(ll_doc-ll_cand)/(np.abs(ll_doc)+np.abs(ll_cand))
        sim = summ
        simi_vec.append(sim) 
    return simi_vec   

def batachariaDistance(doc, s):
    
    simi_vec = []
    for a_doc in s:
                
        summ = 0
        for i in xrange(len(doc)): # compute dist
            ll_doc = a_doc[i]
            ll_cand = doc[i]
            summ+= np.sqrt(ll_doc)*np.sqrt(ll_cand)
        sim = np.sqrt(summ)
        simi_vec.append(sim) 
    return simi_vec    

def eucDistance(doc, s):
    
    simi_vec = []
    for a_doc in s:
                
        summ = 0
        for i in xrange(len(doc)): # compute dist
            ll_doc = a_doc[i]
            ll_cand = doc[i]
            summ+= (ll_doc-ll_cand)**2
        sim = np.sqrt(summ)
        simi_vec.append(sim) 
    return simi_vec
    
    
def feat_field(doc, s, feat):
    
    # convert to float
    doc = doc[feat]
    doccn = [float(i) for i in doc]
    docscn = []
    for doc in s:
        doc = doc[feat]
        doc = [float(i) for i in doc]  
        docscn.append(doc)
    return doccn, docscn


