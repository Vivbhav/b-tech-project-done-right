from globals import *


from numpy import array
from numpy import asarray
from numpy import zeros
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.layers import Flatten, InputLayer, Input
from keras.layers import Embedding
import matplotlib.pyplot as plt
import json
from keras.callbacks import ModelCheckpoint

from keras import regularizers,optimizers, initializers


# create a weight matrix for words in training docs
with open(embedding_dict, "r") as gr:
    embeddings_index = json.load(gr)
#embeddings_index["#"] = [5, 1]
def data_generator(batch_size,inputfile,outputfile,N):
    input_f = open(inputfile, encoding="utf8" )
    output_f = open(outputfile, encoding="utf8" )
    # Initialize a counter
    counter = 0
    while True:
        counter+=1
        input_l = []
        output_l = []
        li = 0
        x,y=input_f.readline(),output_f.readline()
        while x and li < batch_size:
            input_l.append(x)
            output_l.append(y)
            try:
                x,y=next(input_f),next(output_f)
                li += 1
            except:
                x,y='',''
        if li < batch_size:
            input_f.seek(0)
            output_f.seek(0)
            input_l += [input_f.readline() for _ in range(batch_size-li)]
            output_l += [output_f.readline() for _ in range(batch_size-li)]
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
        #f_label = [[0,1] if not i else [1,0] for i in f_label]
        labels = np.array(f_label)
        #if counter ==1:
        #    print(labels.shape)
        yield InputLines, labels

def define_model():
      # define model
      model = Sequential()
      """
      k = initializers.Constant(value=0.1)
      b = initializers.Constant(value=0)
      r = initializers.Constant(value=0.1)
      model.add(LSTM(N, batch_input_shape=(None, N, M), return_sequences=True,
          bias_initializer=b, recurrent_initializer=r, kernel_initializer=k))
      """
      if use_lstm:
        model.add(LSTM(N, batch_input_shape=(None, N, M), return_sequences=False))
      else:
        model.add(Flatten(input_shape=(N,M)))
      model.add(Dense(N, activation='relu'))
      model.add(Dense(N, activation='sigmoid',
          kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01)))
      return model

def main():
    model = define_model()
    weights = {0:125,1:1}
    for i in range(2,200):
        weights[i] = 125
    # compile the model
    adam = optimizers.Adam(lr=8e-03)
    model.compile(optimizer=adam, loss='binary_crossentropy', metrics=['accuracy'])
    # summarize the model
    print(model.summary())
    exit(0)
    checkpoint = ModelCheckpoint(modelname, monitor='loss', verbose=1, save_best_only=True, mode='min', period=1)
    # fit the model
    training_generator = data_generator(batch_size=64,inputfile=inputFile,
            outputfile=outputLabel, N=N)
    validation_generator = data_generator(batch_size=64,
            inputfile=inputValidationFile, outputfile=outputValidationLabel, N=N)
    history = model.fit_generator(training_generator, validation_data=validation_generator,
            epochs=10, callbacks=[checkpoint],#class_weight = weights,
            verbose=1,steps_per_epoch=9736//64,validation_steps=4868//64)
    #history = model.fit(trainX, trainY,validation_split = 0.4, epochs=30, batch_size=64, callbacks=[checkpoint], verbose=1)
    
   # evaluate the model
    
    from keras.models import load_model
    train_model = load_model(modelname)
    
    testX, testY = test_data(testFile, testLabel)
    loss, accuracy = train_model.evaluate(testX, testY, verbose=0)
    print('Accuracy: %f' % (accuracy*100))
    print('Loss: %f' % (loss*100))
    
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.legend(['train','validation'])
    plt.show()
    
if __name__ == '__main__':
    main()
