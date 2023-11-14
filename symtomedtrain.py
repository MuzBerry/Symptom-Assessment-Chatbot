import json
import random
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD


from keras.layers import Dense, Activation, Dropout
from keras.models import Sequential
import numpy as np
import pickle
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()


words = []
classes = []
documents = []
ignore_words = ['?', '!', '_', '-', '(', ')', 'treatment', 'of', 'prevention']
data_file = open('medicine4.json').read()
intents = json.loads(data_file)

for intent in intents['intent']:
    for pattern in intent["Uses"]:

        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['Medicine_Number']))

        if intent['Medicine_Number'] not in classes:
            classes.append(intent['Medicine_Number'])

# print(len(words))

words = [lemmatizer.lemmatize(w.lower())
         for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

print(classes)

print(documents)


pickle.dump(words, open('text3.pkl', 'wb'))
pickle.dump(classes, open('labels3.pkl', 'wb'))

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
                 epochs=1500, batch_size=1, verbose=1)
model.save('model3.h5', hist)
