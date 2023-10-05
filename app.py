from flask import Flask, jsonify, make_response
from config import Config
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=os.getenv("FRONT_URL"))


app.config.from_object(Config)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/data', methods=['GET'])
def get_data():
    data = jsonify({'nombre': 'John', 'edad': 30, 'ciudad': 'Nueva York'})
    response = make_response(data, 202)
    return response

if __name__ == '__main__':
    app.run(port=8000)