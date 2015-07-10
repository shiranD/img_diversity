import numpy as np

# compute color similarity

def cnDistance(doc, s):
    
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
    
    
def cn_field(doc, s):
    
    # convert to float
    doc = doc["cn"]
    doccn = [float(i) for i in doc]
    docscn = []
    for doc in s:
        doc = doc["cn"]
        doc = [float(i) for i in doc]  
        docscn.append(doc)
    return doccn, docscn
