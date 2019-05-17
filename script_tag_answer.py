# -*- coding: utf-8 -*-

import sys
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import nltk
import json
import scale
import pickle

st = StanfordNERTagger('../../stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz','../../stanford-ner-2018-10-16/stanford-ner.jar',encoding='utf-8')

def tag_answers_tag(fw, ner, pos, tag1):
    words = []
    tags = []
    answer= []
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
            answer.append(ner[i][0])
        elif c:
            a = c = 0
            z = '- '
        else:
            z = '- '
        tag = "|" + y + "|" + pos[i][1] + "|" + ner[i][1] + "|"+z
        words.append(ner[i][0].lower()+tag)
        i+=1
    #print(" ".join(words)+"\n")
    if len(words) and (not a or c):
        # non-empty with atleast one 'A' tag
    	fw.write(" ".join(words)+"\n")
    return " ".join(answer)

def tag_answers_word(fw, ner, pos, word1, pos1):
    words = []
    tags = []
    answer= []
    i = 0
    a = 0
    while i < len(ner):
        if ner[i][0][0].isupper():
            y = "U"
        else:
            y = "L"
        if a or ((ner[i][0][:len(word1)] == word1) and (not pos1 or
            pos[i][1][:len(pos1)] == pos1)):
            z = 'A '
            answer.append(ner[i][0])
            a = 1
        else:
            z = '- '
        tag = "|" + y + "|" + pos[i][1] + "|" + ner[i][1] + "|"+z
        words.append(ner[i][0].lower()+tag)
        i+=1
    #print(" ".join(words)+"\n")
    if len(words) and a:
        # non-empty with atleast one 'A' tag
    	fw.write(" ".join(words)+"\n")
    return " ".join(answer)

def preprocess(paragraphs, filename):
    #fr = open(sys.argv[1], 'r')
    fw = open(filename, "w+")
    #lines = fr.readlines()
    ans=[]
    syns=[]
    ants=[]
    syns_a=[]
    ants_a=[]
    for lines in paragraphs:
        for line in lines.strip().split("."):
            temp = word_tokenize(line)
            t = st.tag(temp)
            t1 = nltk.pos_tag(temp)
            ans.append(tag_answers_tag(fw, t, t1, 'ORGANIZATION'))
            ans.append(tag_answers_tag(fw, t, t1, 'LOCATION'))
            ans.append(tag_answers_tag(fw, t, t1, 'TIME'))
            ans.append(tag_answers_tag(fw, t, t1, 'DATE'))
            ans.append(tag_answers_tag(fw, t, t1, 'MONEY'))
            ans.append(tag_answers_tag(fw, t, t1, 'PERSON'))
            ans.append(tag_answers_tag(fw, t, t1, 'PERCENT'))
            ans.append(tag_answers_word(fw, t, t1, 'because',''))
            ans.append(tag_answers_word(fw, t, t1, 'mean','VB'))
            ans.append(tag_answers_word(fw, t, t1, 'state','VB'))
            ans.append(tag_answers_word(fw, t, t1, 'define','VB'))
            s = scale.synonym(t1)
            a = scale.antonym(t1)
            for i,j in s.items():
                syns.append(i)
                syns_a.append(j)
            for i,j in a.items():
                ants.append(i)
                ants_a.append(j)
    fw.close()
    pickle.dump(syns,open(filename[:-4]+"_syn.txt","wb"))
    pickle.dump(ants,open(filename[:-4]+"_ant.txt","wb"))
    pickle.dump(syns_a,open(filename[:-4]+"_syn_a.txt","wb"))
    pickle.dump(ants_a,open(filename[:-4]+"_ant_a.txt","wb"))
    answers = []
    for i in ans:
        if i != "":
            answers.append(i)
    return answers
