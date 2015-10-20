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

# this is part of the prediction which is scoring the documents of a given test query

import numpy as np
from computeWs import compute_hsofR, doc_it
import operator


def argMax_XleftOvers(left, s, wd, wr, query):
    """grid search over ranked list to find most
       diverse and relevant doc at a time"""

    if len(s) == 0:
        return 0, 10.0 # choose the first one
    else:
        f_measures = []
        # compute f_measure to all left docs
        for i, doc in enumerate(left):
            doc = {u'nbComments': u'0', u'cn': [u'0.11766567164179105', u'0.0022447761194029849', u'0.062770149253731339', u'0.1366686567164179', u'0.056316417910447759', u'1.7910447761194031e-05', u'0.012674626865671642', u'0.00020298507462686568', u'0.00011940298507462687', u'0.60114029850746264', u'0.010179104477611941'], u'date_taken': u'2005-01-31T14:49:41Z', u'faceProportion': u'0.029029029029029', u'rank': u'143', u'poi': u'agra fort', u'id': u'50729250', u'tagSpecificity': u'0.581247562023133', u'title': u'Agra Fort', u'tags': 'travel india agra unesco worldheritage uttarpradesh', u'location': u'0,0', u'meanImageTagClarity': u'26.8629387557', u'username': u'Hyougushi', u'description': u'\u3059\u3079\u3066\u5927\u7406\u77f3\u3002 (20050129 Agra, Uttar Pradesh, INDIA) * UNESCO World Heritage * Agra Fort (1983) \u4e16\u754c\u907a\u7523\u300c\u30a2\u30fc\u30b0\u30e9\u57ce\u585e\u300d', u'views': u'0', u'locationSimilarity': u'0', u'meanTagRank': u'8062.62546455', u'uniqueTags': u'0.012318630168325283', u'license': u'5', u'userid': u'71481771@N00', u'meanPhotoViews': u'84.8545', u'visualScore': u'0.683108042839217', u'url_b': u'http://farm1.static.flickr.com/25/50729250_5a039d278e_b.jpg'}

            hs_ofR = compute_hsofR(doc, s, query)
            doc_r = doc_it(doc)
            f_measure = np.dot(wr, doc_r) + np.dot(wd, hs_ofR)
            f_measures.append([i, f_measure])

        # rank by highest f_measure
        f_measures.sort(key=operator.itemgetter(1), reverse=True)
        ind, gain = f_measures[0]
        #print ind, gain, str(left[ind]["id"])

        return ind, gain
