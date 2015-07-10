# LDA corpus
# train partialy only on the same corpus and check
# main function that calls fear extraction with approprite data
import json
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from random import sample


tokenizer = RegexpTokenizer(r'\w+')
stopWords = stopwords.words('english')

def rm_stop(doc):
    doc = tokenizer.tokenize(doc)    
    new_doc = filter(lambda word: word not in stopWords, doc)
    return new_doc

json_path = "../../feats/txt/acropolis_athens"
out_path1 = "description_train.txt"
out_path2 = "description_test.txt"
f_train = open(out_path1,"w")
f_test = open(out_path2,"w")

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
            if line["description"]:
                d2 = line["description"].encode("ascii", "ignore").lower()
                #d1 = line["title"].encode("utf-8").lower()
                d2 = rm_stop(d2) # remove stopwords       
                X.append(d1+d+d2) # extract docs
            else:
                X.append(d1+d) # extract docs
                
                
        except:
            print "1"
    # split to test and train
    test_index = sample(range(len(X)), int(0.1*len(X)))
    k = 0
    for i in xrange(len(X)):
        if i in test_index:
            st = " ".join(X[i])+"\n"
            f_test.write(st)
            
        else:
            st = str(k)+" en "+" ".join(X[i])+"\n"
            f_train.write(st)
            k+=1
            
