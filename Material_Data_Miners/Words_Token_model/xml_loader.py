import os
from xml.dom import minidom

import pandas as pd

def load_xml2():
    path = "../data/xml/j.matdes.2012.09.027.xml"
    doc = minidom.parse(path)

    sections = doc.getElementsByTagName("ce:section")

    for section in sections:
        paras = section.getElementsByTagName("ce:para")

        for para in paras:
            nodes = para.childNodes
            text = ""
            for i in nodes:
                if i.nodeType == i.TEXT_NODE:
                    if len(i.data) > 0:
                        text = text + i.data.replace("\n", "")

                else:
                    ref_nodes = i.childNodes
                    for ref_node in ref_nodes:
                        if ref_node.nodeType == ref_node.TEXT_NODE:

                            if len(ref_node.data) > 0:

                                text = text + ref_node.data.replace("\n         ", "")

def load_xml(path):
    doc = minidom.parse(path)
    data = []

    sections = doc.getElementsByTagName("ce:section")
    # print(filename,len(paras))
    pn = 0
    for section in sections:
        paras = section.getElementsByTagName("ce:para")
        # print(len(nodes))
        ln = 0
        for para in paras:
            nodes = para.childNodes
            text = ""
            for i in nodes:
                if i.nodeType == i.TEXT_NODE:
                    if len(i.data) > 0:
                        text = text + i.data.replace("\n", "")
                    # print(i.data)
                else:
                    ref_nodes = i.childNodes
                    for ref_node in ref_nodes:
                        if ref_node.nodeType == ref_node.TEXT_NODE:
                            # print(ref_node)
                            if len(ref_node.data) > 0:
                                # text = text + i.data
                                text = text + \
                                       ref_node.data.replace("\n         ", "")
            data.append(
                {
                    'text': text,
                    'page_num': pn,
                    'line_num': ln,
                }
            )
            ln += 1
        pn += 1

    data = pd.DataFrame(data)
    return data

def load_xml3(path):
    doc = minidom.parse(path)
    data = []

    sections = doc.getElementsByTagName("ce:section")
    pn = 0
    for section in sections:
        paras = section.getElementsByTagName("ce:para")
        ln = 0
        for para in paras:
            nodes = para.childNodes
            text = ""
            for i in nodes:
                if i.nodeType == i.TEXT_NODE:
                    if len(i.data) > 0:
                        text = text + i.data.replace("\n", "")
                    # print(i.data)
                else:
                    ref_nodes = i.childNodes
                    for ref_node in ref_nodes:
                        if ref_node.nodeType == ref_node.TEXT_NODE:
                            # print(ref_node)
                            if len(ref_node.data) > 0:
                                # text = text + i.data
                                text = text + \
                                       ref_node.data.replace("\n         ", "")
            data.append(
                {
                    'text': text,
                    'page_num': pn,
                    'line_num': ln,
                }
            )
            ln += 1
        pn += 1


    return data