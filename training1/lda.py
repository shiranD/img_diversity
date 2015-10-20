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

# computes the lda feature of a document given the chosen docs

from __future__ import print_function
from collections import defaultdict
from gensim import corpora, models
import numpy as np
from wordIt import extract_words


def lsaPrep(queries, data):

    train = "../ldas/trainset/"
    # prepare txt file for every topic
    for query in queries:
        query = "Quebec_Winter_Carnival"
        doc_set = data[query]

        f = open(train + query, "w")
        # create txt file for train
        i = 0
        for doc in doc_set:
            allf = ""
            tg = ""
            dsc = ""
            tit = ""
            
            try:
                tg = doc["tags"]
                if tg == None:
                    tg = ""                
               
            except:
                pass            
            
            try:
                dsc = doc["description"]
                if dsc == None:
                    dsc = ""

            except:
                pass
            
            #try:
                #tit = doc["title"]
                #if tit == None:
                    #tit = ""

            #except:
                #pass            
            
            allf = tg+" "+dsc+" "+tit
            if allf:
                f.write(str(i)+" en "+allf)
                f.write("\n")
                i+=1                 

    modelp = "../ldas/lsamodels/"
    # train each txt file
    for query in queries:

        corpus = corpora.TextCorpus(train + query)
        
        std = modelp+query+".dict"
        corpus.dictionary.save(std)
        dictionary = corpus.dictionary.load(std)
        
        stc = modelp+query+".mm"
        tfidf_trans = models.TfidfModel(corpus, id2word=dictionary)
        corpora.MmCorpus.serialize(stc ,tfidf_trans[corpus])
        tfidf_corpus = corpora.MmCorpus(stc)
        
        lsi_trans = models.LsiModel(corpus=tfidf_corpus, id2word=dictionary, num_topics=100)

        name = modelp + query + ".lsa"
        lsi_trans.save(name)


def lsaIt(doc, query):
    # retrun a 100 size vector populated with 
    # the topics it comtains
    
    
    modelp = "../ldas/lsamodels/"+query
    lsamodel = modelp + ".lsa"
    lsadict = modelp + ".dict"
    model = models.LsiModel.load(lsamodel)  # load existing model 
    dictionary = corpora.Dictionary.load(lsadict)
    tags = doc["tags"]
    if tags==None:
        tags = ""
    des =  doc["description"]
    if des==None:
        des = ""
    doc = tags + " " + des
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_lsi = model[vec_bow] # convert the query to LSI space 
    vec = 100 * [0]
    for i, (topic, prob) in enumerate(vec_lsi):
        vec[i] = prob
    return vec

def ldaPrep(queries, data):
    train = "../ldas/trainset/"
    # prepare txt file for every topic
    for query in queries:
        query = "agra_fort"
        doc_set = data[query]
        

        f = open(train + query, "w")
        # create txt file for train
        i = 0
        for doc in doc_set:
            allf = ""
            tg = ""
            dsc = ""
            tit = ""
            
            try:
                tg = doc["tags"]
                if tg == None:
                    tg = ""                
               
            except:
                pass            
            
            try:
                dsc = doc["description"]
                if dsc == None:
                    dsc = ""

            except:
                pass
            
            #try:
                #tit = doc["title"]
                #if tit == None:
                    #tit = ""

            #except:
                #pass            
            
            allf = tg+" "+dsc+" "+tit
            if allf:
                f.write(str(i)+" en "+allf)
                f.write("\n")
                i+=1                 

    modelp = "../ldas/models/"
    # train each txt file
    for query in queries:
        query = "agra_fort"
        
        corpus = corpora.MalletCorpus(train + query)
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        model = models.LdaModel(
            corpus_tfidf, id2word=corpus.id2word, alpha='auto', num_topics=20)        
        #a = model.num_terms
        #b = len(corpus.id2word.values())
        name = modelp + query + ".lda"
        model.save(name)

def ldaIt(doc, s, query):

    # for now only tags is under LDA filed #8
    model = "../ldas/models/" + query + ".lda"
    model = models.LdaModel.load(model)  # load existing model

    train = "../ldas/trainset/"
    id2word = corpora.Dictionary()  # decoding the model
    corpus = corpora.MalletCorpus(train + query)
    _ = id2word.merge_with(corpus.id2word)

    doc1 = extract_words(doc)
    doc_topic = id2word.doc2bow(doc1)  # extract topic for candidate
    doc_topics = model[doc_topic]
    docict = defaultdict(float)

    for topic, prob in doc_topics:  # dict candidate
        docict[topic] = float(prob)

    # add every time just the chosen and don't compute from scratch
    docs_topics = []

    for doc in s:
        query = id2word.doc2bow(extract_words(doc))  # extract topic for chosen
        docs_topics.append(model[query])
        

    # compute the similarity
    num_top = model.num_topics
    simi_vec = []

    # is not between 0-1 can go bigger since not normalized
    for a_doc in docs_topics:

        docdict = defaultdict(float)  # dict chosen
        for topic, prob in a_doc:
            docdict[topic] = float(prob)

        summ = 0
        for i in xrange(num_top):  # compute dist
            ll_doc = docdict[i]
            ll_cand = docict[i]
            summ+= (ll_doc - ll_cand)**2
        sim = np.sqrt(summ)

        simi_vec.append(sim)

    return simi_vec
