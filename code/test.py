import json
import numpy as np 

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

# CREAMOS LA RED NEURONAL CON KERAS
model = keras.models.load_model('model.h5')
model.summary()


data = "I need to create a new account";
data = text_to_word_sequence(data)
secuence = tok.texts_to_sequences(data)

encode = np.add.reduce(to_categorical(secuence, size))
print("secuence -> {0}".format(secuence))

print("-"*50)
print(np.argmax(to_categorical(secuence, size), axis=1))
print("-"*50)

a = np.rint(model.predict(np.array([encode])))
print(a)
i =np.argmax(a, axis=None, out=None)
print(tok2.sequences_to_texts(np.array([[i]])))




