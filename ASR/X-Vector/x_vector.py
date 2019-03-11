#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 23:04:10 2019

@author: iseesaw

Achievement of x-vector extractor.

1. Create Model

2. Train Model

3. Extract i-vector
"""
import numpy as np
from keras.models import Sequential, Model
from keras.layers import Dense, AveragePooling1D
from TDNN_layer import TDNNLayer
from keras.utils import plot_model, to_categorical
from keras.callbacks import TensorBoard

speakerN = 100


def create():
    model = Sequential()

    model.add(TDNNLayer([-2, 2], sub_sampling=False, input_shape=(120,)))
    model.add(TDNNLayer([-3, 3], sub_sampling=True))

    model.add(Dense(512))
    model.add(Dense(1500))

    model.add(AveragePooling1D())

    model.add(Dense(512))
    model.add(Dense(512))

    model.add(Dense(speakerN, activation='softmax'))

    print(model.summary())
    plot_model(model, to_file='model/model.png', show_shapes=True)

    return model


def train():

    model = create()

    model.compile(optimizer='Adam',
                  loss="categorical_crossentropy", metrics=['accuracy'])

    X, Y = load()
    model.fit(x=X,
              y=Y,
              batch_size=64,
              epochs=100,
              verbose=2,
              callbacks=[TensorBoard(log_dir='model/log_dir')]
              )
    model.save('model/model.h5')


def load():
    X, Y = '', ''
    return X, Y


def get_xvector(utts):
    model = create()
    model.load_weights('model/model.h5')

    xvector_layer_model = Model(input=model.input,
                                output=model.get_layer('dense5').output
                                )
    xvector = xvector_layer_model.predict(utts)


if __name__ == '__main__':
    train()
