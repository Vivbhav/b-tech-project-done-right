import nltk 
from nltk.corpus import wordnet 
import check

pos_list = ['JJ','NN','RB','VB','VBG','VBN']
def synonym(words):
    synword = {}
    word_list = []
    for word in words:
        if word[1] in pos_list:
            word_list.append(word)
    for word in word_list:
        count_dict = {}
        if len(word_list) > 1:
            for wrd in [w for w in word_list if w != word]:
                definition = check.check_sim(word, wrd)
                count_dict[definition] = count_dict.get(definition, 0) + 1
            definition = max(count_dict, key=count_dict.get)
        else:
            definition = check.check_sim(word, "a")
        if definition:
            synword["Word that means: "+definition] = word[0] 
    return synword

def antonym(words):
    antword = {}
    for word1 in words:
        if word1[1] in pos_list:
            count = 0
            for word in wordnet.synsets(word1[0]):
                for l in word.lemmas():
                    if  l.antonyms() and count == 0:
                        antword["Antonym of: "+l.antonyms()[0].name()] = word1[0]
                        count = 1
                    break
    return antword

#answer is correct if synword.get(question) == text_entered_by_user
