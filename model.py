from helper import save_object, load_object
import numpy as np

from keras.preprocessing import sequence
from keras.models import Sequential, Model
from keras.models import load_model
from keras.layers import Embedding, Reshape, Activation, Input, Dense, Masking
from keras.layers import Conv1D, TimeDistributed, Flatten, GRU, Dropout,Bidirectional
from keras.layers.merge import Dot
from keras.utils import np_utils
from keras.utils.data_utils import get_file
from keras.utils.np_utils import to_categorical
from keras.preprocessing.sequence import skipgrams
from keras.preprocessing import sequence
from keras import backend as K
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint

final_embeddings=load_object('skipgram_w16.pl')
dictionary, reverse_dictionary = load_object('dict.pl')
def model2():
    input1 = Input(shape=(20,))
    x = Embedding(len(dictionary),16,weights=[np.array(load_object('skipgram_w16.pl'))],trainable=True)(input1)
    x = Conv1D(25, 7, strides=1,padding='same', activation='relu')(x)
    x = TimeDistributed(Dense(5))(x)
    x = Flatten()(x)
    #x = GRU(10, activation='relu', recurrent_activation='hard_sigmoid')(x)
    x = Dense(30, activation='relu')(x)
    x = Dense(30, activation='relu')(x)
    x = Dropout(0.2, input_shape=(30,))(x)
    x = Dense(30, activation='relu')(x)
    x = Dropout(0.2, input_shape=(30,))(x)
    out = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=input1, outputs=out)
    model.compile(optimizer=Adam(lr=0.01),
                 loss='binary_crossentropy',
                 metrics=['accuracy'])
    return model