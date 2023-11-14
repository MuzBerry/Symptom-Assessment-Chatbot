import json
import random
from keras.layers import Dense, Activation, Dropout
from keras.models import Sequential
import numpy as np
import pickle
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()


words = []
classes = []
documents = []
ignore_words = ['?', '!', '_', '-']
data_file = open('dataset2.json').read()
intents = json.loads(data_file)

for intent in intents['intents']:
    for pattern in intent["Disease"]:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['Disease_Num']))

        if intent['Disease_Num'] not in classes:
            classes.append(intent['Disease_Num'])

# print(len(words))

words = [lemmatizer.lemmatize(w.lower())
         for w in words if w not in ignore_words]
words = sorted(list(set(words)))
print(classes)
classes = sorted(list(set(classes)))


print(documents)


pickle.dump(words, open('textdisease1.pkl', 'wb'))
pickle.dump(classes, open('labelsdisease1.pkl', 'wb'))

training = []

output_empty = [0]*len(classes)

for doc in documents:
    bag = []

    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(
        word.lower()) for word in pattern_words]

    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)
# print(bag)
train_x = list(training[:, 0])
train_y = list(training[:, 1])
print((train_x))
print(len(train_y))

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y),
                 epochs=1000, batch_size=1, verbose=1)
model.save('model4.h5', hist)
