from flask import Flask
import os
from config import Config


#Create the flask instance
app = Flask(__name__)


#Add the URL from the frontend to the cors policy
from flask_cors import CORS
CORS(app, origins=os.getenv("FRONT_URL"))

# Configurate logger level
import logging
logging.basicConfig(level=Config.LOGGING_LEVEL)

# Create logger object
logger = logging.getLogger('myapp')

# Agrega un manejador de archivos para el registro
file_handler = logging.FileHandler('app.log')
log_level = os.getenv('LOG_LEVEL', 'INFO')
file_handler.setLevel(logging.getLevelName(log_level))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#Gets our Config object into the instance configuration
app.config.from_object(Config)

#Integrate SQLAlchemy to database and FlaskMigrate to migrations
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory='src/migrations')


#Authentication, login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
# from src.models.user import User #Import models to migrate them
# from src.models.organization import Organization
# from src.models.chat import Chat
from src.models import *


#Add routes from blueprints to app
from src.routes import user_routes, auth_routes, webhook_routes
app.register_blueprint(user_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(webhook_routes)

#Run the application
if __name__ == '__main__':
    app.run()