import nltk 
from nltk.corpus import wordnet 
import random
import check

def synonym(words):
    synword = {}
    word_list = []
    for word in words:
        if 'JJ' in word[1]:
            word_list.append(word)
    for word in word_list:
        definition = check.check_sim(word[0], random.choice(word_list)[0])
        if definition:
            synword[definition] = word[0] 
    return synword

def antonym(words):
    antword = {}
    for word1 in words:
        if 'JJ' in word1[1]:
            count = 0
            for word in wordnet.synsets(word1[0]):
                for l in word.lemmas():
                    if  l.antonyms() and count == 0:
                        antword[l.antonyms()[0].name()] = word1[0]
                        count = 1
                    break
    return antword
