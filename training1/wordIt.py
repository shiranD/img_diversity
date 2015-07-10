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