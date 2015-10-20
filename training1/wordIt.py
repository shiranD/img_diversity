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

# simply process text fields 

def extract_words(doc):
    # remove stopwords
    tags = []
    desc = []
    title = []
    try:
        tags = doc["tags"].split()
    except:
        pass 
    
    # uncomment as soon as processed
    #try:
        #title = doc["title"].split()
    #except:
        #pass     

    #try:
        #desc = doc["description"].split()
    #except:
        #pass 
    
    return tags+title+desc