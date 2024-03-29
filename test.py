from globals import *


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

train_model = load_model(modelname)
with open(embedding_dict, "r") as gr:
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
        if lambai != N:
            i += " #"*(N-lambai)
        line = i.strip().split()[:N]
        embed = []
        for word in line:
            embedding_vector = np.array(embeddings_index.get(word, embeddings_index.get("#")))
            embed.append(list(embedding_vector))
        embedding_matrix.append(embed)
    InputLines = np.array(embedding_matrix)
    f_label = []
    for label in output_l:
      label = label.strip().split()
      label = [int(i) for i in label][:N]
      lambai2 = len(label)
      if lambai2 != N:
        label += [0]*(N-lambai2)
      f_label.append(label)
    labels = np.array(f_label)
    return InputLines, labels


testX, testY = test_data(testFile, testLabel)
loss, accuracy = train_model.evaluate(testX, testY, verbose=0)

preds = train_model.predict(testX)
print(preds[5])
print(max(preds[5]))

threshold = float(input())
output=[]
test=[]
for pred in range(len(preds)):
    output.append([])
    test.append(list(testY[pred]))
    for i in range(len(preds[pred])):
        if preds[pred][i] > threshold:
            output[-1].append(1)
        else:
            output[-1].append(0)

testY=list(testY)

for i in range(len(preds)):
    print("pred**************************************************************************************************************")
    print(output[i])
    print(sum(preds[i]))
    print(sum(output[i]))
    print("test--------------------------------------------------------------------------------------------------------------")
    print(test[i])
    print(sum(test[i]))
print(sum(preds[4]))
print(sum(preds[5]))
print('Accuracy: %f' % (accuracy*100))
print('Loss: %f' % (loss*100))
