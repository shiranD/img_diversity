from __future__ import print_function
from collections import defaultdict
import gensim
import numpy as np

# upload corpus
# TBD turn to class and add a doc at a time
def lda(cand, docs):

    in_path1 = "description_train.txt"
    corpus = gensim.corpora.MalletCorpus(in_path1)
    
    train = 0
    if train:# train model
        for word_id, freq in next(iter(corpus)):
            print(corpus.id2word[word_id], freq)
    
            model = gensim.models.LdaModel(corpus, id2word=corpus.id2word, alpha='auto', num_topics=6) 
            model.save('athens.lda')
    else:
        model = gensim.models.LdaModel.load('athens.lda')# load existing model
    
    id2word = gensim.corpora.Dictionary() # decoding the model
    _ = id2word.merge_with(corpus.id2word)   
    
    cand = id2word.doc2bow(cand) # extract topic for candidate
    cand_topics = list(sorted(model[cand], key=lambda x: x[0])) 
    candict = defaultdict(float)
    
    for topic, prob in candict: # dict candidate
        candict[topic]=float(prob)  
    
    docs_topics = []# add every time just the chosen and don't compute from scratch
    for line in docs:
        query = id2word.doc2bow(line) # extract topic for chosen
        docs_topics.append(list(sorted(model[query], key=lambda x: x[0])))
    
    # compute the similarity
    num_top = model.num_topics
    simi_vec = []
    
    for a_doc in docs_topics:
        
        docdict = defaultdict(float) # dict chosen
        for topic, prob in a_doc:
            docdict[topic]=float(prob)
        
        summ = 0
        for i in xrange(num_top): # compute dist
            ll_doc = docdict[i]
            ll_cand = candict[i]
            summ+= (ll_doc-ll_cand)**2
        sim = np.sqrt(summ)
        
        simi_vec.append(sim)
    return simi_vec
    
    #if 0: # on test set
        #test_path = "description_test.txt"        
        #for line in open(test_path,"r").readlines():
            #query = line.split()
            #query = id2word.doc2bow(query)
            #a = list(sorted(model[query], key=lambda x: x[1])) # more important
            #pr = model.print_topic(a[-1][0]) # actual topic representation with terms
            
    
        #print problem
        # after recieveing 2 queries distribution
        # d1: (9,0.7)
        # use the formula to detemine the similarity value (sort by similar values)