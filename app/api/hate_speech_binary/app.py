from flask import Flask, request, jsonify
from keras.preprocessing import sequence
from keras.preprocessing.text import tokenizer_from_json
from keras.models import load_model
import json
import sys
import os

app = Flask(__name__)


def load_pretrained():
    model = load_model('./model/model.h5')
    with open('./model/tokenizer.json') as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)
    print('loaded')
    sys.stdout.flush()
    return model, tokenizer


def get_prediction(input_sentences):
    model, tokenizer = load_pretrained()
    classes = ["혐오", "정상"]
    labels = []
    predict = model.predict(sequence.pad_sequences(tokenizer.texts_to_sequences(input_sentences), maxlen=128))
    for i, pred in enumerate(predict):
        print(pred)
        sys.stdout.flush()
        if pred[0]>=0.99:
            labels.append({"sentence" : input_sentences[i], "label" : classes[0]})
        else:
            labels.append({"sentence" : input_sentences[i],"label" : classes[1]})
    return labels


@app.route("/wake", methods=['POST'])
def wake():
    return jsonify({'wake': 'wake'})


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        req_data = request.json
        print(req_data)
        sys.stdout.flush()
        input_sentences = req_data['input_sentences']
        labels = get_prediction(input_sentences)
        print(labels)
        sys.stdout.flush()
        return jsonify({'predictions': labels})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
