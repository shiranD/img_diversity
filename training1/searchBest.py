import numpy as np
from computeWs import compute_hsofR, doc_it
import operator


def argMax_XleftOvers(left, s, wd, wr, query):
    """grid search over ranked list to find most
       diverse and relevant doc at a time"""

    if len(s) == 0:
        return 0, 10  # choose the first one
    else:
        f_measures = []
        # compute f_measure to all left docs
        for i, doc in enumerate(left):
            hs_ofR = compute_hsofR(doc, s, query)
            doc_r = doc_it(doc)
            f_measure = np.dot(wr, doc_r) + np.dot(wd, hs_ofR)
            f_measures.append([i, f_measure])

        # rank by highest f_measure
        f_measures.sort(key=operator.itemgetter(1), reverse=True)
        ind, gain = f_measures[0]
        print ind, gain, str(left[ind]["id"])

        return ind, gain
