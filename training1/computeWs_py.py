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

# this is the version to be used over computeWs.py

from __future__ import division
from math import exp
from lda import ldaIt, lsaIt
from cosine import CosineSimilarity
from cn import feat_field, eucDistance, batachariaDistance, canberraDistance, chisquareDistance, l1Distance
import json
from collections import Counter
import numpy as np
from wordIt import extract_words


#"""" open the dict that assigns every word
     #to its place in relevance vector"""
#json_file = "dict/Termdict"
#with open(json_file) as f1:
    #for line in f1:  # extract jsons
        #termdict = json.loads(unicode(line))


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
    
    doccsd, scsd = feat_field(doc, s, "csd")
    r3 = l1Distance(doccsd, scsd)
    
    dochog, shog = feat_field(doc, s, "hog")
    r4 = batachariaDistance(dochog, shog)    
    
    if 1:
        doccn, scn = feat_field(doc, s, "cn")
        r5 = eucDistance(doccn, scn)
        
        doccm, scm = feat_field(doc, s, "cm")
        r6 = canberraDistance(doccm, scm)
        
        doclbp, slbp = feat_field(doc, s, "lbp")
        r7 = chisquareDistance(doclbp, slbp)
        
        docglr, sglr = feat_field(doc, s, "glr")
        r8 = l1Distance(docglr, sglr) # or batachariaDistance   
               
    else:
        
        doccn, scn = feat_field(doc, s, "cn3")
        r5 = eucDistance(doccn, scn)       
        
        doccm, scm = feat_field(doc, s, "cm3")
        r6 = canberraDistance(doccm, scm)
        
        doclbp, slbp = feat_field(doc, s, "lbp3")
        r7 = chisquareDistance(doclbp, slbp)    
        
        docglr, sglr = feat_field(doc, s, "glr3")
        r8 = l1Distance(docglr, sglr) # # or batachariaDistance    
        

    return [r1, r2, r3, r4, r5, r6, r7, r8]


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


def compute_denom(doc_set, s, query, wd_q, wr_p, R):

    sumOfExp = 0
    for i, doc in enumerate(doc_set):
        hs_ofR = R[i]
        doc_rl = doc_it(doc)
        power = np.dot(wr_p, doc_rl) + np.dot(wd_q, hs_ofR)
        sumOfExp += exp(power)
        s.append(doc)  # update s

    return sumOfExp


def compute_wr(doc_set, s, query, wd_q, wr_p, R):
    # make sure dimentions work as the exp is scaler
    sumOfExp = 0
    
    for i, doc in enumerate(doc_set):
        hs_ofR = R[i]
        doc_rl = doc_it(doc)
        power = np.dot(wr_p, doc_rl) + np.dot(wd_q, hs_ofR)
        sumOfExp += doc_rl * exp(power)
        s.append(doc)  # update s

    return sumOfExp


def compute_wd(doc_set, s, query, wd_q, wr_p, R):

    sumOfExp = 0
    for i, doc in enumerate(doc_set):
        hs_ofR = R[i]
        doc_rl = doc_it(doc)
        power = np.dot(wr_p, doc_rl) + np.dot(wd_q, hs_ofR)
        sumOfExp += hs_ofR * exp(power)
        s.append(doc)  # update s

    return sumOfExp


def compute_num(doc, s, query, wd_q, wr_p, r):

    # just one current doc
    hs_ofR = r
    doc_rl = doc_it(doc)
    power = np.dot(wr_p, doc_rl) + np.dot(wd_q, hs_ofR)
    return exp(power)


def doc_it(a_doc, query):
    """"create relevance vector
        future use all fields from
        extract_words"""
    vec = lsaIt(a_doc, query)
    
    if a_doc["faceProportion"].isalpha():
        face = 1.0
    else:
        face = 1-float(a_doc["faceProportion"])
    vec.extend([face])

    if a_doc["tagSpecificity"].isalpha():
        tg = 0.0
    else:
        tg = float(a_doc["tagSpecificity"])
    vec.extend([tg])

    vec.extend([float(a_doc["uniqueTags"])])

    if a_doc["uniqueTags"].isalpha():
        tg = 0.0
    else:
        tg = float(a_doc["uniqueTags"])
    vec.extend([tg])

    if a_doc["locationSimilarity"].isalpha():
        untg = 0.0
    else:
        untg = 1-float(a_doc["locationSimilarity"])
    vec.extend([untg])

    if a_doc["bulkProportion"].isalpha():
        untg = 1.0
    else:
        untg = 1-float(a_doc["bulkProportion"])
    vec.extend([untg])
    
    
    #vec.extend([float(a_doc["visualScore"])])
    #vec.extend([1-float(a_doc["faceProportion"])])
    #vec.extend([float(a_doc["tagSpecificity"])])
    #vec.extend([float(a_doc["uniqueTags"])])
    #location = float(a_doc["locationSimilarity"])
    #if (1/location) > 1:
        #vec.extend([1])
    #else:
        #vec.extend([0])
    #vec.extend([float(a_doc["bulkProportion"])])

    
    # add img features
    
    cn = a_doc["csd"]
    cn = [float(i) for i in cn]
    vec.extend(cn)
    
    cn = a_doc["hog"]
    cn = [float(i) for i in cn]
    vec.extend(cn)    
    
    if 1:
        cn = a_doc["cn"]
        cn = [float(i) for i in cn]
        vec.extend(cn)
    
        cn = a_doc["cm"]
        cn = [float(i) for i in cn]
        vec.extend(cn)
    
        cn = a_doc["glr"]
        cn = [float(i) for i in cn]
        vec.extend(cn)

        
        cn = a_doc["lbp"]
        cn = [float(i) for i in cn]
        vec.extend(cn)
    else:
    
        cn = a_doc["cn3"]
        cn = [float(i) for i in cn]
        vec.extend(cn)    
        
        cn = a_doc["cm3"]
        cn = [float(i) for i in cn]
        vec.extend(cn)
        
        cn = a_doc["glr3"]
        cn = [float(i) for i in cn]
        vec.extend(cn) 
        
        cn = a_doc["lbp3"]
        cn = [float(i) for i in cn]
        vec.extend(cn)    
    
    return np.array(vec)
