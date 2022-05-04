import pickle
import numpy as np
import json
import random
import nltk
import speech_recognition as sr
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from keras.models import load_model


# nltk word package
# nltk.download('punkt')
# nltk.download('wordnet')
model = load_model('model/chatter_model.h5')
knowledge = json.loads(open('json/knowledge.json').read())
words = pickle.load(open('pkl/words.pkl', 'rb'))
types = pickle.load(open('pkl/types.pkl', 'rb'))
WNL = WordNetLemmatizer()
r = sr.Recognizer()
user_info = json.loads(open('json/user_info.json').read())


# match the words in sentence to bag
def match_words(sentence, words):
    in_words = nltk.word_tokenize(sentence)
    in_words = [WNL.lemmatize(word.lower()) for word in in_words]
    bag = [0] * len(words)
    for s in in_words:
        flag = 0
        for i, w in enumerate(words):
            if s == w:
                bag[i] = 1
                flag = 1
        if not flag:
            i_max = 0
            bag_max = 0
            for i, w in enumerate(words):
                l = [0 if a.path_similarity(b) is None else a.path_similarity(b) for a in wordnet.synsets(s) for b in wordnet.synsets(w)]
                if len(l) > 0:
                    bag_max = max(l) if max(l) > bag_max else bag_max
                    i_max = i
            bag[i_max] = bag_max
    return np.array(bag)


# match the types for the sentence by pretrained model
def match_types(sentence, model):
    bag = match_words(sentence, words)
    res = model.predict(np.array([bag]))[0]
    results = [[i, r] for i, r in enumerate(res)]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for result in results:
        return_list.append({"type": types[result[0]], "probability": result[1]})
    return return_list


# special task special operation
def get_response(types, msg, knowledge_json):
    tag = types[0]['type']
    prob = types[0]['probability']
    list_knowledge = knowledge_json['knowledge']
    if tag == "task_affair":
        response = "do task_affair" + "\t---confidence {}".format(prob)
        task_affair()
    elif tag == "task_email":
        response = "do task_email" + "\t---confidence {}".format(prob)
        task_email()
    elif tag == "task_search" or prob < 0.5:
        response = "I will google for you about " + "\"" + msg + "\" " + "\t---confidence {}".format(prob)
        task_search(msg)
    else:
        for k in list_knowledge:
            if k['tag'] == tag:
                if tag == "greeting":
                    response = random.choice(k['out']).format(user_info['user_info']['name']) + "\t---confidence {}".format(prob)
                elif tag == "ask_user_info":
                    response = random.choice(k['out']).format(user_info['user_info']['name']) + "\t---confidence {}".format(prob)
                else:
                    response = random.choice(k['out']) + "\t---confidence {}".format(prob)
                break
    return response


# return the response
def chatbot_response(msg):
    ints = match_types(msg, model)
    res = get_response(ints, msg, knowledge)
    return res


# audio analyse
def speech2text():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said: " + text)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service" + format(e))


def Chatter2UI(msg):
    print(msg)


def UI2Chatter():
    user_in = input()
    return user_in


def task_affair():
    return 0


def task_email():
    return 0


def task_search(msg):
    return 0


# total chatter
def chatter():
    # check whether it is first meet
    if user_info['user_info']['first_meet'] == 1:
        Chatter2UI("Hello, nice to meet you! I am your chat bot.")
        Chatter2UI("As this is our first meeting, to provide a better assistance, I would like to ask you some question.")
        Chatter2UI("First, what is your name?")
        user_info['user_info']['name'] = UI2Chatter()
        Chatter2UI("Second, what is your gender?")
        user_info['user_info']['gender'] = UI2Chatter()
        Chatter2UI("OK, now you can ask me to do something or free talk with me.")
        user_info['user_info']['first_meet'] = 0
        json.dump(user_info, open('json/user_info.json', 'w'))
    else:
        Chatter2UI("Hello, I am here.")

    while True:
        user_input = UI2Chatter()
        msg = chatbot_response(user_input)
        Chatter2UI(msg)


if __name__ == '__main__':
    chatter()
