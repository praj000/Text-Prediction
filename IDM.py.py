# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uydHR2cgxwuFRoUJ8M4oLeGNKbe0ZBkE
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x
import tensorflow as tf
tf.enable_eager_execution()
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow_datasets as tfds

data,info=tfds.load("imdb_reviews",with_info=True,as_supervised=True)
train,test=data["train"],data["test"]

X_train=[]
Y_train=[]
x_test=[]
y_test=[]
for a,b in train:
  X_train.append(str(a.numpy()))
  Y_train.append(b.numpy())
for i,j in test:
  x_test.append(str(i.numpy()))
  y_test.append(j.numpy())

def process_text(set1,set2,vocab_size=10,max_len=None,embedding=None):
  token=Tokenizer(num_words=vocab_size,oov_token="<OOV>")
  token.fit_on_texts(set1)
  word_index=token.word_index
  seq=token.texts_to_sequences(set1)
  test_seq=token.texts_to_sequences(set2)
  padded=pad_sequences(seq,padding="post",maxlen=max_len,truncating="post")
  test_seq=pad_sequences(test_seq,maxlen=max_len,padding="post",truncating="post")
  return (padded,test_seq)

vocab=10000
length=120
embedding=16
X_train,x_test=process_text(X_train,x_test,vocab_size=vocab,max_len=length,embedding=embedding)

Y_train=np.array(Y_train)
y_test=np.array(y_test)

def build (embed,train_data,e=None):
  X,y=train_data
  model=tf.keras.models.Sequential([
      tf.keras.layers.Embedding(vocab,embedding,input_length=length),
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(9,activation="relu"),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(1,activation="sigmoid")

  ])
  model.compile(loss="binary_crossentropy",optimizer="RMSprop",metrics=["accuracy"])
  model.fit(X,y,epochs=e,verbose=2,validation_split=0.2)
  return model

mod=build(10,(X_train,Y_train),3)

k=mod.predict(x_test)

import matplotlib.pyplot as plt
for i in range(1000):
  if y_test[i]==1:
    if k[i,0]>0.5:

      r="green"
    else:
      r="red"
  else:
    if k[i,0]<0.5:
      r="green"
    else:
      r="red"
  plt.scatter(i,k[i,0],c=r,marker="X")
  plt.scatter(i,y_test[i],c="aqua",marker="o")

plt.show()