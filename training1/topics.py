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

# this helps prediction part to write down each query's (which is a topic)
# creates a simple dictionary with topic-number assignment

from xml.etree.ElementTree import parse

def dict_topics(xml_paths):
    
    top_dict = {}
    # read xml and produce dict
    for xml_path in xml_paths:
        try:
            tree = parse(xml_path)
            troot = tree.getroot()     
            
            for child in troot:
                ch = child.getchildren()
                # notice there absolute gps coordinates too
                val = ch[0].text
                query = ch[1].text
                top_dict[val] = query            
                #top_dict[query] = val            
        except:
            print "no good", xml_path

        
    return top_dict



#xml_path = "../../devset_topics.xml"
#topDict = dict_topics(xml_path)