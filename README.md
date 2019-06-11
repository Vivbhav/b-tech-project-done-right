#Automatic Question Generation

##Installations and Downloads
<addr>
sudo -H pip3 install -r requirements.txt
sudo apt-get install python3-tk
python3 -c "import nltk; nltk.download('wordnet')"
git clone https://github.com/moonlightlane/QG-Net
SQuAD dataset (instructions provided in QG-Net readme)
Glove embeddings (https://nlp.stanford.edu/projects/glove)
</addr>

##About software
	
After all the installations, execute main.py using python3 to get a
window and by doing as instructed in that window you can test the
software. 

Data can be fetched from the internet using the terms provided or it can
be directly fed to the software by typing or providing a text file.

If a query is searched for the first time, the output will be
pre-processed and stored in a file. Pre-processing (especilly fetching
pos and ner tags) takes significant amount of time and it can be reduced
by storing pre-processed text. For demo purposes, there is a limit on
number of sentences to be preprocessed(tag_answer_rule_based.py:102),
this will help to speed up the demo.

Using the pre-processed data, all different types of questions can be
generated.

There are basically 3 approaches:
- Rule based
- ML based two models:
	- LSTM based
	- Basic Linear Layer based

In the main software, the rule based appraoch has been integrated. There
is no provision to use ML based approaches using software. By running
test.py or test_dense.py or test_lstm.py, one can get answer tags for
all words. Using tag_answers_dense.py preprocessing and answer tagging
can be done. Providing this file to QG-Net will give you 'Wh 'questions.
For other types of questions, rule based approach is the only way.

Generated question can be provided as a quiz or separate question answer
files can be generated. There are some scrolling issues on quiz screen.
For now this issue is avoided by limiting the number of question
displyer on screen(main.py:257).  If one chooses to write questions
answers in file, then answers must be checked manually. But a small
python script can easily be written (and is left for users ;p ). 

Many intermediate output files are generated during this process to
speed up question generation on repeated queries, analysing output,
using same data for different flow etc. It is recommended to have a
separate directory to avoid clutter.

##Code Files

cd codes

main.py code manages the control flow of the software and also the UI part.
multilistbox.py is for displaying the results table.

Ner-pos embedding for the words are stored in data/ner-pos.json

similarity.py calculates the similarity between two words and it is used
by vocab.py which generated vocabulary based (True/False) questions.

wiki.py is used to fetch data from wikipedia

As mentioned earlier, two different approaches were tried out. By making
appropriate changes in globals.py, one can easily switch between
execution of both approaches. The files train.py and test.py use
global.py to decide which model to train/test. As the approaches changed
drastically over time, we decided to have different codes to test the
files and hence test_lstm.py and test_dense.py were created. 

Using train.py, one can train the model. Use test_dense.py to generate
tag for each word and store the output in a file. Use this file with
tag_answer_dense.py to preprocess the data and mark answer tag.
Feeding this file to QG-Net will generate 'Wh type' questions.

Logic for generating fill in the blanks can be found in main.py, where
answer tags are given by the rule based logic.
