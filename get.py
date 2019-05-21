from numpy import array
from numpy import asarray
from numpy import zeros
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.layers import Flatten
from keras.layers import Embedding
import matplotlib.pyplot as plt
import json
from keras.callbacks import ModelCheckpoint

from keras.models import load_model
import numpy as np
nin = 100
Glovedict = 'data/ner_pos.json'
train_model = load_model('weights/best_bet_final.h5')
with open(Glovedict, "r") as gr:
  embeddings_index = json.load(gr)
def test_data(testFile, testLabel):
    input_f = open(testFile, encoding="utf8" )
    output_f = open(testLabel, encoding="utf8" )
    input_l = input_f.readlines()
    output_l = output_f.readlines()
    embedding_matrix = []
    for j in input_l:
        i = j.strip()
        lambai = len(i.split())
        if lambai != nin:
            i += " #"*(nin-lambai)
        line = i.strip().split()[:nin]
        embed = []
        for word in line:
            embedding_vector = np.array(embeddings_index.get(word, embeddings_index.get("#")))
            embed.append(list(embedding_vector))
        embedding_matrix.append(embed)
    InputLines = np.array(embedding_matrix)
    f_label = []
    for label in output_l:
      label = label.strip().split()[:nin]
      label = [int(i) for i in label]
      lambai2 = len(label)
      if lambai2 != nin:
        label += [0]*(nin-lambai2)
      f_label.append(label)
    labels = np.array(f_label)
    return InputLines, labels

loss1 = 0
accu = 0
fin = []
if True:
	testFile = 'data/testing1.txt'
	testLabel = 'data/l_testing1.txt'
	outputFIle = 'data/outputtest1.txt'
	fwr = open(outputFIle, 'w')
	testX, testY = test_data(testFile, testLabel)
	loss, accuracy = train_model.evaluate(testX, testY, verbose=0)
	print('Accuracy: %f' % (accuracy*100))
	print('Loss: %f' % (loss*100))
	loss1 += loss
	accu += accuracy
	preds = train_model.predict(testX)
	for pred in range(len(preds)):
		for i in range(len(preds[pred])):
			if testY[pred][i] == 1:
				fin.append(preds[pred][i])
	threshold = sum(fin)/(len(fin))
	for pred in range(len(preds)):
	  for i in range(len(preds[pred])):
	    if preds[pred][i] > threshold:
	      preds[pred][i] = 1
	    else:
	      preds[pred][i] = 0
	for i in range(len(preds)):
	    print("************************************pred*****************************************")
	    fwr.write(" ".join([str(int(j)) for  j in preds[i]]))
	    fwr.write("\n")
	    print(sum(preds[i]))
	    print("------------------------------------test-----------------------------------------")
	    print(testY[i])
	fwr.close()
#print(len(fin))
#print(min(fin))
print('Average Accuracy: %f' % ((accu/25)*100))
print('Average Loss: %f' % ((loss1/25)*100))

'''preds = train_model.predict(testX)
print(preds[5])
print(max(preds[5]))
threshold = float(input())
for pred in range(len(preds)):
  for i in range(len(preds[pred])):
    if preds[pred][i] > threshold:
      preds[pred][i] = 1
    else:
      preds[pred][i] = 0
for i in range(len(preds)):
    print("ored**************************************************************************************************************")
    print(" ".join([str(int(j)) for  j in preds[i]]))
    print(sum(preds[i]))
    print("test--------------------------------------------------------------------------------------------------------------")
    print(testY[i])'''
