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

# extract user info and create a user-dict

from os import walk
from xml.etree.ElementTree import parse
import json
from collections import defaultdict


def user(filenames):

    # iter over all xml
    path = "../../desccred/"
    jpath = "../../feats/usr/"
    
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
