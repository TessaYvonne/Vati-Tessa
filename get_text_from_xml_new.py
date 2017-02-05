import xml.dom.minidom
import re
import os
re.UNICODE

def get_text_from_xml_files(folder):
    thread_files = {}
    for filename in os.listdir(folder):
        file = folder + "/" + filename
        text = get_text_from_xml(file)
        thread_files[filename] = text
    return thread_files


def get_text_from_xml(file):

    alle_text = {}

    DOMTree = xml.dom.minidom.parse(file)
    collection = DOMTree.documentElement

    text_nodelist = collection.getElementsByTagName("text")
    postid_nodelist = collection.getElementsByTagName("postid")

    for text_node, postid_node in zip(text_nodelist, postid_nodelist):
        postid = postid_node.childNodes[0].data
        text = text_node.childNodes[0].data

        alle_text[postid] = text

    return(alle_text)