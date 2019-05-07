import os
import pickle
import ast
import numpy as np


def save_object(obj, filename):
    #overwrite 
    pickle.dump(obj, open( filename , "wb" ) , pickle.HIGHEST_PROTOCOL)
def load_object(filename):
    return pickle.load(open( filename, "rb" ))

def create_token(data):
    tokens_list = []
    for d in data:
        tokens_list.append(d)
    return tokens_list

def prob_to_class(data):
    f = np.zeros(len(data), dtype="int32")
    for i in range(len(data)):
        if data[i]>0.5:
            f[i]=1
    return f
    
dictionary, reverse_dictionary = load_object('dict.pl')
def creat_dataset(input_list):
    datas = list()
    for pb in input_list:
        data = []
        for word in pb:
            if word in list(dictionary.keys()):
                data.append(dictionary[word])
            else:
                data.append(dictionary["UNK"])
        datas.append(data)
    return datas