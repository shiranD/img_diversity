from __future__ import division
import webbrowser

def dict_truth(q):
    dict_Gt = {}
    gt = "../../gt/dGT/"+q+" dGT.txt"
    for line in open(gt).readlines():
        docn, clst = line.split(",")
        dict_Gt[docn] = clst.strip()
        
    return dict_Gt, int(clst.strip())
        

def htmlwrite(query, docList, urls):
    
    true_dict, num_grp = dict_truth(query)
    outpath = "/Users/dudy/CSLU/image_ir/image_ir_src/rankings/"
    with open(outpath+query+'.html', 'w') as myFile:
        
        myFile.write('<!DOCTYPE html>')
        myFile.write('<html>')
        myFile.write('<head>')
        myFile.write('<title>Page Title</title>')
        myFile.write('</head>')
        myFile.write('<FONT FACE="hiragino maru gothic pro"><h1> %s</h1></FONT>'%(query))
        
        gt = [] # ground truth statistics
        for doc, url in docList:
            try:
                gt.append(true_dict[doc])
            except:
                gt.append("0")
        unqgrp = list(sorted(set(gt)))
        if unqgrp[0]=="0":
            unqgrp = unqgrp[1:]
            
            irrel = gt.count("0") / len(docList)
        else:
            irrel = 0.0
        coverage = len(unqgrp) / num_grp
        
        myFile.write('<FONT FACE="hiragino maru gothic pro"><p align="center">coverage = %0.2f, irrelevant = %0.2f\
        </p>'%(coverage, irrel))        
        for i, (doc, url) in enumerate(zip(docList, urls)):
                                              
            myFile.write('<FONT FACE="hiragino maru gothic pro"><p align="center">%s: doc # = %s, \
            score = %0.2f, grp = %s</p>'%(str(i), doc[0], doc[1], gt[i]))
            myFile.write('<center><IMG SRC=%s ALT="some text" WIDTH=256 HEIGHT=256></center>'%(url))
    
        myFile.write('</html>')
        myFile.close()
        
        filename = 'file://'+outpath + query +'.html'
        webbrowser.open_new_tab(filename)


if 0:
    query = "acropolis"
    urls = ["http://farm8.static.flickr.com/7362/9067739127_edda2711ca_b.jpg","http://farm6.static.flickr.com/5347/9069963392_977987e854_b.jpg","http://farm6.static.flickr.com/5347/9069963392_977987e854_b.jpg","http://farm6.static.flickr.com/5347/9069963392_977987e854_b.jpg"]
    s_id =[["9069963392", 2.1], ["9069963392", 3.1], ["9069963392", 4.6], ["9069963392", 5.4]]
    htmlwrite(query, s_id, urls)