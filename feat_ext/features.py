# main function that calls fear extraction with approprite data
import json
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from tfidf_CosineSim import CosineSimilarity
from lda_train import lda


tokenizer = RegexpTokenizer(r'\w+')
stopWords = stopwords.words('english')

def rm_stop(doc):
    doc = tokenizer.tokenize(doc)    
    new_doc = filter(lambda word: word not in stopWords, doc)
    return new_doc


json_path = "../../feats/txt/acropolis_athens"
data = []
with open(json_path) as f:

    for line in f: # extract jsons            
        data.append(json.loads(unicode(line)))
        X = []
    for line in data:
        try:
            d = line["tags"].encode("ascii", "ignore").lower()
            d = rm_stop(d) # remove stopwords
            d1 = line["title"].encode("ascii", "ignore").lower()
            d1 = rm_stop(d1) # remove stopwords     
            dall = d1+d
            if line["description"]:
                d2 = line["description"].encode("ascii", "ignore").lower()
                #d1 = line["title"].encode("utf-8").lower()
                d2 = rm_stop(d2) # remove stopwords    
                dall+=d2
            X.append(dall) # extract docs
        except:
            print "1"
            
        X.append(d) # extract docs
        # assume that X[0] is the candidate
    r1 = CosineSimilarity().buildMat(X)
    r2 = lda(X[0], X[1:])
    print "H"
    # load the LDA model 
    # iterate the query agaisnt each of the rest of docs
    # r2 = implement the formula in paper
        