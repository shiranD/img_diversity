# extract user info

from os import walk
from xml.etree.ElementTree import parse
import json
from collections import defaultdict


def user(filenames):

    # iter over all xml
    path = "../../desccred/"
    jpath = "../../feats/usr/"
    # create a user-dict
    for fquery in filenames:
        fpath = path+fquery #  open a xml file
        tree = parse(fpath)
        jason = open(jpath+fquery[:-4], "w")
        troot = tree.getroot()
        usrDict = defaultdict(float)           
        for child in troot:            
            ch = child.getchildren()
            for field in ch:
                usrDict[field.tag] = field.text
            break
        jason.write("{}\n".format(json.dumps(usrDict))) 
        jason.close()

def uploadJson(path):
    for line in open(path,"r").readlines():
        return json.loads(line) 
