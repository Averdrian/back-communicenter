from flask import Flask, jsonify, make_response
import os

#Create the flask instance
app = Flask(__name__)

#Add the URL from the frontend to the cors policy
from flask_cors import CORS
CORS(app, origins=os.getenv("FRONT_URL"))

#Gets our Config object into the instance configuration
from config import Config
app.config.from_object(Config)

#Integrate SQLAlchemy to database and FlaskMigrate to migrations
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy(app)
from models.user import User #Import models to migrate them
migrate = Migrate(app, db, directory='src/migrations')


#Temporary routes, deleting soon
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/data', methods=['GET'])
def get_data():
    data = jsonify({'nombre': 'John', 'edad': 30, 'ciudad': 'Nueva York'})
    response = make_response(data, 202)
    return response


#Run the application
if __name__ == '__main__':
    app.run()