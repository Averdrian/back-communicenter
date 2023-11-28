from flask import Flask
import os
from settings import Settings
from database import db

#Create the flask instance
app = Flask(__name__)

#Add the URL from the frontend to the cors policy
from flask_cors import CORS
CORS(app, origins=os.getenv("FRONT_URL"))

#Gets our Config object into the instance configuration
app.config.from_object(Settings)

#Authentication, login manager
from settings import login_manager
from config import configure_login_manager
configure_login_manager(login_manager, app)

with app.app_context():
    from config import register_blueprints, configure_database
    register_blueprints(app)
    configure_database(app, db)

#Run the application
if __name__ == '__main__':
    app.run()