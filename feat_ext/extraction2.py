from os import walk
from xml.etree.ElementTree import parse
import json
import csv
from userCred import user, uploadJson



# open textual
ipath = "/Volumes/LaCie/devset/desctxt/solrIngestableData/xml_devset20154solr_image/"
ipath1 = "/Volumes/LaCie/devset/descvis/img/"
jsonUsr = "../../feats/usr/"

opath = "../../feats/both/"
# extract all files from dir
f = []
for (dirpath, dirnames, filenames) in walk(ipath):
    f.extend(filenames)
    break


# iter over all xml
#feats = [" CN.csv", " CM3x3.csv", " CM.csv", " CN3x3.csv", " CSD.csv", " GLRLM.csv", " GLRLM3x3.csv", " HOG.csv", " LBP.csv", " LBP3x3.csv" ]
feats = [" CN.csv"]
for fquery in f:
    # extract img feats
    cn = ipath1+fquery[:-4]+feats[0]
    dictCN = {}
    for line in open(cn,"r").readlines():
        vals =  line.strip().split(',')   
        dictCN[vals[0]] = vals[1:]
    
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
            
            # usr info
            idu = json_dict["userid"]
            pathU = jsonUsr+idu
            uDict = uploadJson(pathU)
            json_dict["tagSpecificity"]=uDict["tagSpecificity"]
            json_dict["uniqueTags"]=uDict["uniqueTags"]
            json_dict["visualScore"]=uDict["visualScore"]
            json_dict["faceProportion"]=uDict["faceProportion"]
            json_dict["locationSimilarity"]=uDict["locationSimilarity"]
            json_dict["meanImageTagClarity"]=uDict["meanImageTagClarity"]
            json_dict["meanPhotoViews"]=uDict["meanPhotoViews"]
            json_dict["meanTagRank"]=uDict["meanTagRank"]  
            idphoto = json_dict["id"]
            json_dict["cn"] = dictCN[idphoto]
            # dump to json
            json_file.write("{}\n".format(json.dumps(json_dict))) 
            
