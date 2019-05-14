# -*- coding: utf-8 -*-

import sys
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import nltk
import json

st = StanfordNERTagger('../../stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz','../../stanford-ner-2018-10-16/stanford-ner.jar',encoding='utf-8')

def tag_answers(fw, ner, pos, tag1):
    words = []
    tags = []
    i = 0
    c = 0
    a = 1
    while i < len(ner):
        if ner[i][0][0].isupper():
            y = "U"
        else:
            y = "L"
        if ner[i][1] == tag1 and a:
            z = 'A '
            c = 1
        elif c:
            a = c = 0
            z = '- '
        else:
            z = '- '
        tag = "|" + y + "|" + pos[i][1] + "|" + ner[i][1] + "|"+z
        words.append(ner[i][0].lower()+tag)
        i+=1
    #print(" ".join(words)+"\n")
    if len(words) and not a:
        # non-empty with atleast one 'A' tag
    	fw.write(" ".join(words)+"\n")

def preprocess(paragraphs, filename):
    #fr = open(sys.argv[1], 'r')
    fw = open(filename, "w")
    #lines = fr.readlines()
    for lines in paragraphs:
        for line in lines.strip().split("."):
            temp = word_tokenize(line)
            t = st.tag(temp)
            t1 = nltk.pos_tag(temp)
            tag_answers(fw, t, t1, 'ORGANIZATION')
            tag_answers(fw, t, t1, 'LOCATION')
            tag_answers(fw, t, t1, 'TIME')
            tag_answers(fw, t, t1, 'DATE')
            tag_answers(fw, t, t1, 'MONEY')
            tag_answers(fw, t, t1, 'PERSON')
            tag_answers(fw, t, t1, 'PERCENT')
    fw.close()
