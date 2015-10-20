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

from os import walk
import json
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')
stopWords = stopwords.words('english')


def rm_stop(doc):
    """removes stopwords
    input: a string
    output: a list of words without stopwords"""
    doc = tokenizer.tokenize(doc)
    new_doc = filter(lambda word: word not in stopWords, doc)
    return new_doc


#def extractY(path2rvlc):
    #"""is not in use but
    #for each document gets its relevance value
    #0 or 1"""
    ## dict all doc_id relevance result
    ## can dict only irrelevant to save space
    #y = {}
    #for line in open(path2rvlc, "r").readlines():
        #line = line.strip()
        #key, val = line.split(",")
        #y[key] = val
    #return y


def extractXY(docs_path):

    """extracts information on every document for all queries
    input: document paths and relevance paths for relevance
    output: X - a dict of queries, each query is a rankedlist of docs
    and each doc is a dict of document fields"""
    jsonDocs = docs_path
    f = []
    for (_, dirnames, filenames) in walk(docs_path):
        f.extend(filenames)
        break
    dictX = {}
    f = ["lincoln_home"]
    
    for filename in f:
        with open(jsonDocs + filename) as f1:
            X = []
            for line in f1:  # extract jsons
                line = json.loads(unicode(line))
                try:
                    d = line["tags"] # process tags
                    if d is not None:
                        d = line["tags"].encode("ascii", "ignore").lower()
                        d = rm_stop(d)  # remove stopwords
                        d = " ".join(d)
                        line["tags"] = d
                except:
                    pass

                try:
                    d = line["description"] # process tags
                    if d is not None:
                        d = line["description"].encode("ascii", "ignore").lower()
                        d = rm_stop(d)  # remove stopwords
                        d = " ".join(d)
                        line["description"] = d
                except:
                    pass
                try:
                    d = line["title"] # process tags
                    if d is not None:
                        d = line["title"].encode("ascii", "ignore").lower()
                        d = rm_stop(d)  # remove stopwords
                        d = " ".join(d)
                        line["title"] = d
                except:
                    pass
                X.append(line)  # extract docs


        dictX[filename] = X
    if 0:
        dict_terms(dictX, f)

    return dictX


def dict_terms(dX, queries):
    
    """This function is only used to
    extract the size of relevance weight vector
    by couting all unique terms in all data and assigning
    a dict for each token"""
    all_words = []
    for query in queries:
        docs = dX[query]
        for doc in docs:
            tags = []
            desc = []
            title = []
            try:
                tags = doc["tags"].split()
                all_words.extend(doc_words)
            except:
                pass
            #try:
                #title = doc["title"].split()
                #all_words.extend(doc_words)
            #except:
                #pass
            try:
                desc = doc["description"].split()
                all_words.extend(doc_words)
            except:
                pass
            all_words+= tags+desc+title 
            
    words = list(sorted(set(all_words)))  # sorted is not a must
    print "len is: ", len(words)
    dictTerm = {}
    for i, word in enumerate(words):
        dictTerm[word] = i
    json_file = "dict/Termdict_desc"
    with open(json_file, "w") as json_file:
        json_file.write(json.dumps(dictTerm))
