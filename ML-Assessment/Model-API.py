import pickle
from flask import Flask, request, jsonify
from Transformers import *

PIPELINE_FILE_NAME = 'Pipeline.pkl'
MODEL_FILE_NAME = 'Model.pkl'
# PRICE_RANGES = ("low", "medium", "high", "very high")

def load_work(pipeline_fn=PIPELINE_FILE_NAME, model_fn=MODEL_FILE_NAME):
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    pipeline, model = map(load, (pipeline_fn, model_fn))
    return pipeline, model

pipeline, model = load_work()

def prepare(data):
    data = data.copy()
    for col in data:
        if not isinstance(data[col], list):
            data[col] = [data[col]]
    data = pd.DataFrame(data, index=[0])
    prepared = pipeline.transform(data)
    return prepared

App = Flask(__name__)
@App.route("/predict_price_range", methods=['POST'])
def get_price_range():
    payload = request.get_json()
    print(payload)
    prepared_data = prepare(payload)
    prediction = model.predict(prepared_data)
    prediction = prediction.tolist()[0]
    response = jsonify({
#        'price_range': [prediction, f'({PRICE_RANGES[prediction]} cost)']
        'price_range': prediction
    })
    print(response)
    return response

if __name__ == '__main__':
    App.run()