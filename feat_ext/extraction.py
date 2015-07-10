from os import walk
from xml.etree.ElementTree import parse
import json


# open textual
ipath = "/Volumes/LaCie/devset/desctxt/solrIngestableData/xml_devset20154solr_image/txt"
opath = "../../feats/"
# extract all files from dir
f = []
for (dirpath, dirnames, filenames) in walk(ipath):
    f.extend(filenames)
    break

# iter over all xml

for fquery in f:
    #  open a json file
    query = fquery.split(".")[0]
    fpath = ipath+fquery    
    try:
        tree = parse(fpath)
    except:
        raise "Error"
    troot = tree.getroot() 
    # create json files per query    
    with open(opath+query, "w") as json_file:
        
        for child in troot:
            json_dict = {}
            ch = child.getchildren()
            for field in ch:
                val = field.text
                key = field.attrib.values()[0]
                json_dict[key] = val
            # dump to json
            json_file.write("{}\n".format(json.dumps(json_dict)))    
        


# open image
# tbd
#ipath = "/Volumes/LaCie/devset/desctxt/solrIngestableData/xml_devset20154solr_image/dsp"
