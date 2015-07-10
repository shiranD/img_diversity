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


def extractY(path2rvlc):
    """is not in use but
    for each document gets its relevance value
    0 or 1"""
    # dict all doc_id relevance result
    # can dict only irrelevant to save space
    y = {}
    for line in open(path2rvlc, "r").readlines():
        line = line.strip()
        key, val = line.split(",")
        y[key] = val
    return y


def extractXY(docs_path, _):

    """extracts information on every document for all queries
    input: document paths and relevance paths for relevance
    output: X - a dict of queries, each query is a rankedlist of docs
    and each doc is a dict of document fields"""
    jsonDocs = "../../feats/both/"
    f = []
    for (_, dirnames, filenames) in walk(docs_path):
        f.extend(filenames)
        break
    dictX = {}
    for filename in f:
        with open(jsonDocs + filename) as f1:
            X = []
            for line in f1:  # extract jsons
                line = json.loads(unicode(line))
                try:
                    d = line["tags"]
                    if d is not None:
                        d = line["tags"].encode("ascii", "ignore").lower()
                        d = rm_stop(d)  # remove stopwords
                        d = " ".join(d)
                        line["tags"] = d
                except:
                    pass

                # try:
                # d1 = line["title"]
                # if d1!=None:
                # d1 = line["title"].encode("ascii", "ignore").lower()
                # d1 = rm_stop(d1) # remove stopwords
                # us+=d1
                # except:
                # pass

                X.append(line)  # extract docs


        dictX[filename] = X
    if 0:
        dict_terms(dictX, f)

    return dictX


def dict_terms(dX, queries):
    
    """This function is only used to
    extract the sice of relevance weight vector
    by couting all unique terms in all data and assigning
    a dict for each token"""
    all_words = []
    for query in queries:
        docs = dX[query]
        for doc in docs:
            try:
                doc_words = doc[0].split()[1:]
                all_words.extend(doc_words)
            except:
                pass

    words = list(sorted(set(all_words)))  # sorted is not a must
    dictTerm = {}
    for i, word in enumerate(words):
        dictTerm[word] = i
    json_file = "dict/Termdict"
    with open(json_file, "w") as json_file:
        json_file.write(json.dumps(dictTerm))
