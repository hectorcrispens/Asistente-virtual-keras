import re
import pprint
#import gtts
import json
import random
import time
#from pynlp import PyNLP
import pandas as pd
import numpy as np

import speak.pyio as spk


import features.translate as trl
import features.weather as wtr
import features.datetime as dtm


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tensorflow.keras.utils import to_categorical

## CARGAR ARCHIVOS DEL DATASET E INTENTS

# Cargamos el dataset que nos proveera los datos para el entrenamiento de la red  
#df = pd.read_csv('neural/dataset.csv', index_col=0)

# Cargamos el archivo intents.json que nos provee respuestas y las classes
# import our chat-bot intents file
with open('intent.json') as json_data:
    intents = json.load(json_data)
    

# Crear el vocabulario a partir de todas las palabras del intents.json
train_text=""
p=[]
t=[]
for n in intents['intents']:
	p = p + n['patterns']
	t = t + [n['tag'] for x in range(len(n['patterns']))]
	train_text = train_text + " ".join(n['patterns']) + " ".join(n['responses'])

#Creacion del vocabulario
corpus= set(text_to_word_sequence(train_text))
corpus = list(sorted(corpus))
size = len(corpus)+1

# Obtenemos los datos de entrada para entrenamiento
tok = Tokenizer()
tok.fit_on_texts(corpus)

# Obtenemos los datos de salida para el entrenamiento
clases = list(sorted(set(t)))
size_s = len(clases)+1

tok2 = Tokenizer()
tok2.fit_on_texts(clases)

# CREAMOS LA RED NEURONAL CON KERAS
model = keras.models.load_model('model.h5')

## INICIAR EL ASISTENTE VIRTUAL

# El asistente informa que esta listo
spk.speak("virtual assistant is ready")


# Algunas variables necesarias
context = "conversation"
sound = True
history = []
bag = ''
spread = True

# Escaneo continuo de audio
while True:
    hope = True
    # Obtenemos un texto a partir del microfono
    data = spk.recordAudio()
    intent_get = []

    # Procesamos data con la red neuronal y decodifcamos el intents
    try:
        # PROCESAMIENTO DE LA RED NEURONAL
        # tokenizar por palabras
        token = text_to_word_sequence(data)
        # obtener la secuencia
        seq = tok.texts_to_sequences(token)
        # encode la secuencia
        encoded = np.add.reduce(to_categorical(seq, size))
        
        pred = model.predict(np.array([encoded]))
        
        seq2 = np.argmax(pred, axis=None, out=None)
        
        intent_get = tok2.sequences_to_texts(np.array([[seq2]]))
        intent_get = intent_get[-1]

        if spread:
            print("#" * 20 + " SUMMARY " + "#" * 20)
            print("\t Context: {0}".format(context))
            print("\t Hope: {0}".format(hope))
            print("\t Data: {0}".format(data))
            print("\t Bag: {0}".format(bag))
            print("\t Intent: {0}".format(intent_get))
            print("#" * 49)
            time.sleep(5)

        # CONTEXTO CONVERSATION
        if hope and context in ["conversation"] and data not in [""]:
            hope = False
            
                       
            for n in intents['intents']:
                if intent_get in n["tag"]:
                    resp = n["responses"][random.randint(0, len(n["responses"]) -1)]
                    spk.speak(resp, sound)
                    context = n["context"][0]

                    # Empezamos a listar las operaciones contextuales del Asistente
                    # Poner en silencio el asistente
                    if intent_get in ["shutup"]:
                        sound = False
                        
                    # Habilitar el sonido del asistente
                    if intent_get in ["speak"]:
                        sound = True
                    
                    # Pronostico del tiempo
                    if intent_get in ["weather"]:
                        datos = wtr.weather_app()
                        pprint(datos)

                    # Hora del dia
                    if intent_get in ["time"]:
                        spk.speak(dtm.time())

        # CONTEXTO TRADUCTION
        if hope and context in ["translate"]:
            hope = False
            print(intent_get in ["ready"])
            print("> " + bag)
            if intent_get in ["ready"]:
                text = trl.translate(bag)
                spk.speak(text, sound, lang="Es")
                context = "conversation"
                bag = ""
            else:
                print("entre al else")
                bag = bag + data
            time.sleep(5)

        history.append(data)
            

    except Exception as e:
        print("> exiting by exception")
        print(str(e))
        time.sleep(5)
        continue

                    

    
    # if re.search('weather|temperature', data):
    #     #city = data.split(' ')[-1]
    #     city = 'Santa Fe, AR'
    #     weather_data = spk.weather(city=city)
    #     print(weather_data)
    #     t2s(weather_data)
    #     continue
    # if re.search('news', data):
    #     news_data = spk.news()
    #     pprint.pprint(news_data)
    #     t2s(f"I have found {len(news_data)} news. You can read it. Let me tell you first 2 of them")
    #     t2s(news_data[0])
    #     t2s(news_data[1])
    #     break

    # if re.search('tell me about', data):
    #     topic = data[14:]
    #     wiki_data = spk.wikipedia(topic)
    #     print(wiki_data)
    #     t2s(wiki_data)
    #     break

    # if re.search('date', data):
    #     date = spk.tell_me_date()
    #     print(date)
    #     print(t2s(date))
    #     break

    # if re.search('time', data):
    #     time = spk.tell_me_time()
    #     print(time)
    #     t2s(time)
    #     break

    # if re.search('open', data):
    #     domain = data.split(' ')[-1]
    #     open_result = spk.website_opener(domain)
    #     print(open_result)
    #     break
            
    # else:
    #     t2s(data, 'en')
    #     continue
