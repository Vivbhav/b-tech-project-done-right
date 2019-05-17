from nltk.corpus import wordnet
from nltk import word_tokenize

def wn_tag_converter(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def Path_Based_Similarity(word1, word2):
	sense1 = wordnet.synsets(word1[0].lower(), wn_tag_converter(word1[1]))
	sense2 = wordnet.synsets(word2[0].lower())
	overlap = 0.0
	max_overlap = 0.0
	flag = 0
	for i in sense1:
		for j in sense2:
			overlap = i.path_similarity(j)
			if overlap == None:
				continue
			if overlap > max_overlap:
				max_overlap = overlap
				pos1, pos2 = i, j
				flag = 1
	if flag == 1:
		return max_overlap, pos1.definition(), pos2.definition()
	else:
		return max_overlap, None, None

def check_sim(word1, word2):
	sim, word1_sense, word2_sense = Path_Based_Similarity(word1, word2)
    
	if word1_sense and word2_sense:
            return word1_sense
	else:
            return None
    
if __name__ == "__main__":
	main()
