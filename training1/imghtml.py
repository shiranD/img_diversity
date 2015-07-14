import webbrowser

def htmlwrite(query, docList, urls):
    
    outpath = "/Users/dudy/CSLU/image_ir/image_ir_src/rankings/"
    with open(outpath+query+'.html', 'w') as myFile:
        
        myFile.write('<!DOCTYPE html>')
        myFile.write('<html>')
        myFile.write('<head>')
        myFile.write('<title>Page Title</title>')
        myFile.write('</head>')
        myFile.write('<FONT FACE="hiragino maru gothic pro"><h1>Ranked List for %s Query</h1></FONT>'%(query))    
        for i, (doc, url) in enumerate(zip(docList, urls)):
            myFile.write('<FONT FACE="hiragino maru gothic pro"><p align="center">%s: doc # = %s and score = %0.2f</p>'%(str(i), doc[0], doc[1]))
            myFile.write('<center><IMG SRC=%s ALT="some text" WIDTH=256 HEIGHT=256></center>'%(url))
    
        myFile.write('</html>')
        myFile.close()
        
        filename = 'file://'+outpath + query +'.html'
        webbrowser.open_new_tab(filename)


query = "acropolis"
urls = ["http://farm8.static.flickr.com/7362/9067739127_edda2711ca_b.jpg","http://farm6.static.flickr.com/5347/9069963392_977987e854_b.jpg","http://farm6.static.flickr.com/5347/9069963392_977987e854_b.jpg","http://farm6.static.flickr.com/5347/9069963392_977987e854_b.jpg"]
s_id =[["9069963392", 2.1], ["9069963392", 3.1], ["9069963392", 4.6], ["9069963392", 5.4]]
htmlwrite(query, s_id, urls)