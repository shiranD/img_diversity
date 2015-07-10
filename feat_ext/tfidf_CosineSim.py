# compute tf-idf cosine similarity
from __future__ import division
import collections
import itertools
import numpy as np
import string
 
# TBD adjust to add doc at a time along with its new terms
class CosineSimilarity(object):

    
    def buildMat(self, docs):
        
        txt2 = list(itertools.chain.from_iterable(docs)) # flatten to unique
        coll_words = list(set(txt2))
        # create dict for matrix
        self.word2mat = {}
        d_mat2word = {}
        for i in xrange(len(coll_words)):
            self.word2mat[coll_words[i]]=i
            d_mat2word[i]=coll_words[i] # not sure needed
        self.mat = np.zeros((len(coll_words),len(docs)),dtype=float)
        for j, doc in enumerate(docs):
            self.termFrequency(doc, j)
        self.idfmat = self.mat.copy()
        self.inverseDocumentFrequency()
        self.coSine_Sim()  
        return self.coSim

    # step 1 : terrm frequency
    def termFrequency(self, document, num):
        counter=collections.Counter(document) # count frequency
        sum_term = len(document) # find norm coef
        for key in counter.keys():
            val = counter[key] / sum_term # normalize
            line_id = self.word2mat[key] # extract line
            self.mat[line_id,num] = val # update cell


    # step 2 : inverse doc frequency
    def inverseDocumentFrequency(self):
        # count how many occupied cells in each line (represents a word)
        # x = len(line)/1-count
        # idf = 1+log(x)
        #mat_tf_idf = []
        for i, line in enumerate(self.idfmat):
            allDocs = len(line)
            numOfDocswTerm = allDocs-sum(line==False) # only words that appear at least once can be
            idf = 1.0 + np.log(float(allDocs / numOfDocswTerm))
            self.idfmat[i, :] = line*idf
            

    # step 4 : Cosine similarity
    def coSine_Sim(self):
        #Cosine Similarity (d1, d2) =  1 - [Dot product(d1, d2) / ||d1|| * ||d2||]
        candidate_doc = self.idfmat[:,0].T
        chosen_docs = np.matrix(self.idfmat[:,1:])
        
        self.coSim = np.array(np.dot(candidate_doc,chosen_docs))[0]# modify matrix [[]]
        d1 = np.sum(np.abs(candidate_doc)**2)**(1./2)#  must be positive (take off abs?)
        for i, dot in enumerate(self.coSim):
            chosen = np.array(chosen_docs[:,i])
            d2 = np.sum(np.abs(chosen)**2)**(1./2)
            self.coSim[i]=1-dot/(d1*d2)
        

#def cosine_similarity(cand, chosen):
    #txt = [cand]+chosen
    #txt2 = list(itertools.chain.from_iterable(txt)) # flatten to unique
    #coll_words = list(set(txt2))
    ## create dict for matrix
    #d_word2mat = {}
    #d_mat2word = {}
    
    #for i in xrange(len(coll_words)):
        #d_word2mat[coll_words[i]]=i
        #d_mat2word[i]=coll_words[i] # not sure needed
    #mat = np.zeros((len(coll_words),len(txt)),dtype=float)
    #for j, doc in enumerate(txt):
        #mat = termFrequency(doc, j, mat, d_word2mat)
    #mat = inverseDocumentFrequency(mat)
    #similarity = coSine_Sim(mat[:,0].T, np.matrix(mat[:,1:]))  
    #return similarity



#if __name__ == "__main__":
# make class comment and pep and 