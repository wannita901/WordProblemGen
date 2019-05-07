from flask import Flask
from keras.preprocessing import sequence
from keras import backend as K
import numpy as np
app = Flask(__name__)

from generate import gen_auto
from helper import create_token, creat_dataset, prob_to_class, load_object
from model import model2

@app.route("/example")
def example():
    return "Hello world"

@app.route("/generate")
def problem_generate():
    #config
    weight_predict='cnn_model1.h5'

    data = gen_auto(10)
    testset = create_token(data['tokenizes'])
    testset = creat_dataset(testset)
    testset = sequence.pad_sequences(testset, 20, dtype='int32', padding='post', truncating='pre', value=0.)
    cnn_model = model2()
    cnn_model.load_weights(weight_predict)
    cnn_model._make_predict_function()
    test_pred = cnn_model.predict(np.array(testset))
    test_pred_t = prob_to_class(test_pred)
    output = ""
    dictionary, reverse_dictionary = load_object('dict.pl')
    for i in range(len(test_pred_t)):
        if test_pred_t[i]==0:
            continue
        output+="<p>" + str(("").join([reverse_dictionary[x] for x in testset[i] if x!=0]).strip())
        output+= '\n ans:' + str(data['answers'][i]) + "\n\n" + "</p>"
    K.clear_session()
    return output