from __future__ import print_function
from collections import defaultdict
import gensim
import numpy as np
from wordIt import extract_words


def ldaPrep(queries, data):
    train = "../ldas/trainset/"
    # prepare txt file for every topic
    for query in queries:
        doc_set = data[query]

        f = open(train + query, "w")
        # create txt file for train
        for doc in doc_set:
            f.write(doc[8])
            f.write("\n")

    models = "../ldas/models/"
    # train each txt file
    for query in queries:
        corpus = gensim.corpora.MalletCorpus(train + query)
        model = gensim.models.LdaModel(
            corpus, id2word=corpus.id2word, alpha='auto', num_topics=6)
        name = models + query + ".lda"
        model.save(name)


def ldaIt(doc, s, query):

    # for now only tags is under LDA filed #8
    model = "../ldas/models/" + query + ".lda"
    model = gensim.models.LdaModel.load(model)  # load existing model

    train = "../ldas/trainset/"
    id2word = gensim.corpora.Dictionary()  # decoding the model
    corpus = gensim.corpora.MalletCorpus(train + query)
    _ = id2word.merge_with(corpus.id2word)

    doc1 = extract_words(doc)
    doc_topics = id2word.doc2bow(doc1)  # extract topic for candidate
    docict = defaultdict(float)

    for topic, prob in doc_topics:  # dict candidate
        docict[topic] = float(prob)

    # add every time just the chosen and don't compute from scratch
    docs_topics = []

    for doc in s:
        query = id2word.doc2bow(extract_words(doc))  # extract topic for chosen
        docs_topics.append(list(sorted(model[query], key=lambda x: x[0])))

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
            summ += (ll_doc - ll_cand)**2
        sim = np.sqrt(summ)

        simi_vec.append(sim)

    return simi_vec
