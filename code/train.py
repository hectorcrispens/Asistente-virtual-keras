import json
import numpy as np 
import pandas as pd

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tensorflow.keras.utils import to_categorical

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
df = pd.DataFrame({'words': corpus})
df.to_csv('corpus.csv')
size = len(corpus)+1

# Obtenemos los datos de entrada para entrenamiento
tok = Tokenizer()
tok.fit_on_texts(corpus)
tokens= tok.texts_to_sequences(p)

x_train = [np.add.reduce(to_categorical(X, size)) for X in tokens]
x_train = np.array(x_train)

# Obtenemos los datos de salida para el entrenamiento
clases = list(sorted(set(t)))
size_s = len(clases)+1

tok2 = Tokenizer()
tok2.fit_on_texts(clases)
tokens_s = tok2.texts_to_sequences(t)

y_train= [np.add.reduce(to_categorical(Y, size_s)) for Y in tokens_s]
y_train = np.array(y_train)

model = keras.Sequential()
model.add(keras.Input(shape=x_train[0].shape))
model.add(layers.Dense(30))
model.add(layers.Dense(60, activation='relu'))
model.add(layers.Dense(60, activation='relu'))
model.add(layers.Dense(len(y_train[0])))

# Compilamos el modelo, definiendo la función de coste y el optimizador.
model.compile(loss='mse', optimizer=keras.optimizers.SGD(lr=9), metrics=['acc'])

# Y entrenamos al modelo. Los callbacks 
model.fit(x_train, y_train, epochs=8000)

pred=model.predict(np.array([x_train[2]]))

# Guardar el Modelo
model.save('model.h5')



