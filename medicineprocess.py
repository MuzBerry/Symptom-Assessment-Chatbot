import nltk

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model
model = load_model('model.h5')
import json
import random
intents = json.loads(open('medicine2.json', encoding='utf-8').read())
words = pickle.load(open('text.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

ignore_words = ['?','!','_','-','show','me','give','want']


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words if word not in ignore_words]
                        
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
  #  print(results)
    return_list = []
    for r in results:
        return_list.append({"MedicineNumber": classes[r[0]], "probability": str(r[1])})
    print(return_list)
    return return_list

def getResponse(ints, intents_json):
    
    list_of_intents = intents_json['intent']
    result = []

    for intent in ints:
        for i in list_of_intents:
         if(i['Medicine_Number']== intent["MedicineNumber"]):
             result.append({"Medicine_Number": i["Medicine_Number"],"Medicine Name":i["Medicine Name"], "Uses":i["Uses"], "Prescription": i["Prescription"], "MRP": i["MRP"]})

    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


final_res = chatbot_response("Show me Crocin Pain relief tablets")
print(final_res)






#six-1.16.0.dist-infopyth