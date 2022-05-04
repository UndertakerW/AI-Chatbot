import numpy as np
import random
import json
import pickle
import nltk
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizer_v2.gradient_descent import SGD
from nltk.stem import WordNetLemmatizer
import os

# nltk word package
# nltk.download('punkt')
# nltk.download('wordnet')
nltk.data.path.append(os.path.dirname(os.path.abspath('.')) + "\\nltk_data\\")

# initialize the dataset
# store the input words
words = []

# store the types of output
types = []

# combine the input and the output for training
combination = []

# ignore the punctuation for convenience
ignore_words = ['?', '!', ',']

# read the knowledge for training
knowledge_file = open('json/knowledge.json').read()
knowledge = json.loads(knowledge_file)

# initialize the lemmatizer
WNL = WordNetLemmatizer()

# extract the words with and combine with the output type
for in_type in knowledge['knowledge']:
    for in_words in in_type['in']:
        # split the sentence
        w = nltk.word_tokenize(in_words)
        words.extend(w)
        combination.append((w, in_type['tag']))
        if in_type['tag'] not in types:
            types.append(in_type['tag'])

# lemmatization for words to reduce the input dimension
words = [WNL.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
types = sorted(list(set(types)))

# print the knowledge need to be learn
print(len(combination), "pairs of combination")
print(len(types), "types of output")
print(len(words), "words of input in total")

# pack the input and output to file for agent to read
pickle.dump(words, open('pkl/words.pkl', 'wb'))
pickle.dump(types, open('pkl/types.pkl', 'wb'))

# initialize training data
train = []
output_empty = [0] * len(types)

for com in combination:
    # initialize words bag
    bag = [0] * len(words)

    in_words = com[0]

    # lemmatize each word
    in_words = [WNL.lemmatize(w.lower()) for w in in_words]

    # note the word in the words list
    for i, w in enumerate(words):
        bag[i] = 1 if w in in_words else 0

    # note the type in the types list
    output_type = list(output_empty)
    output_type[types.index(com[1])] = 1

    train.append([bag, output_type])

random.shuffle(train)
train = np.array(train, dtype=list)

train_x = list(train[:, 0])
train_y = list(train[:, 1])
print("Training data created")

# create the model
model = Sequential()
model.add(Dense(256, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(len(train_y[0]), activation='softmax'))

# use Stochastic gradient descent
sgd = SGD(lr=0.005, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# fit the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=300, batch_size=5, verbose=1)
model.save('model/chatter_model.h5', hist)

print("Model created")
