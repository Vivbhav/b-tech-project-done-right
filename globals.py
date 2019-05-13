use_glove = False
use_lstm = False
N=200 # each sentence has max N words
normalise = True


# define documents
inputFile = 'data/training.txt'
outputLabel = 'data/l_training.txt'
inputValidationFile = 'data/validation.txt'
outputValidationLabel = 'data/l_validation.txt'
testFile = 'data/Glove.txt'
testLabel = 'data/outputlabels.txt'
modelname = 'weights/model_3_best_weights.h5'
#npdict = 'ner_pos.json'
if use_glove:
    #glove vectors
    embedding_dict = 'data/glovedict.txt'
    M=300
else:
    #pos ner vectors
    embedding_dict = 'data/ner_pos.json'
    M=2
