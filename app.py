from flask import Flask
import os
from settings import Settings, login_manager
from database import db, DB_URI
from config import configure_login_manager, configure_database, register_blueprints
from flask_cors import CORS


#Create the flask instance
app = Flask(__name__)

#Add the URL from the frontend to the cors policy
CORS(app, origins=os.getenv("FRONT_URL"))

#Gets our Config object into the instance configuration
app.config.from_object(Settings)

#Authentication, login manager
configure_login_manager(login_manager, app)

with app.app_context():
    register_blueprints(app)
    configure_database(app, db, DB_URI)

#Run the application
if __name__ == '__main__':
    app.run()