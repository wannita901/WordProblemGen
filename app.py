from flask import Flask, render_template, jsonify, url_for, make_response
from jinja2 import Template

from keras.preprocessing import sequence
from keras import backend as K
import numpy as np
import os 
import json

app = Flask(__name__)

from generate import gen_auto
from helper import create_token, creat_dataset, prob_to_class, load_object
from model import model2

@app.route("/example")
def example():
    return "Hello world"

@app.route("/")
def main():
    return render_template('main.html', out="")

@app.route("/generate")
def problem_generate():
    #config
    weight_predict='cnn_model1.h5'

    data = gen_auto(10)
    tokens = create_token(data['tokenizes'])
    testset = creat_dataset(tokens)
    testset = sequence.pad_sequences(testset, 20, dtype='int32', padding='post', truncating='pre', value=0.)
    cnn_model = model2()
    cnn_model.load_weights(weight_predict)
    cnn_model._make_predict_function()
    test_pred = cnn_model.predict(np.array(testset))
    test_pred_t = prob_to_class(test_pred)
    output = '{"problems":['
    dictionary, reverse_dictionary = load_object('dict.pl')
    for i in range(len(test_pred_t)):
        if test_pred_t[i]==0:
            continue
        output+= '{"pb":"' + str(("").join(tokens[i]).strip())
        output+= '","ans":"' + str(data['answers'][i]) + '"},'
    output = output[:-1] + ']}'
    K.clear_session()
    out = json.loads(output)
    #temp = Template('''<p>
    #    {% for problem in out.problems %}
    #        {{ problem.pb }} 
    #        </br>
    #        คำตอบ : {{ problem.ans }}
    #        </br>
    #        </br>
    #    {% endfor %}
    #    </p>''')
    return render_template('main.html', out = out)
    #return temp.render(out=out)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)