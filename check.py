from nltk.corpus import wordnet
from nltk import word_tokenize

def Path_Based_Similarity(word1, word2):
	sense1 = wordnet.synsets(word1)
	sense2 = wordnet.synsets(word2)
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
	sim, word1_sense, word2_sense = Path_Based_Similarity(word1.lower(), word2.lower())
    
	if word1_sense and word2_sense:
            return word1_sense
	else:
            return None
    
if __name__ == "__main__":
	main()
