from flask import Flask
import os
from settings import Settings, login_manager
from database import db, DB_URI
from config import configure_database, register_blueprints
from flask_cors import CORS
from dotenv import load_dotenv
from flask_socketio import SocketIO, send, emit
from socketio_instance import socketio
# import eventlet

# Load enviroment variables
load_dotenv()

#Create the flask instance
app = Flask(__name__)

#Add the URL from the frontend to the cors policy
frontend_url = os.getenv("FRONT_URL")
CORS(app, supports_credentials=True, origins=frontend_url)
# CORS(app)

#Gets our Config object into the instance configuration
app.config.from_object(Settings)

#Authentication, login manager
login_manager.init_app(app)


with app.app_context():
    # eventlet.monkey_patch()
    register_blueprints(app)
    configure_database(app, db, DB_URI)

socketio.init_app(app)

#Run the application
if __name__ == '__main__':
    socketio.run(app, port=8000)
    # app.run(port=8000, debug=True)
    
