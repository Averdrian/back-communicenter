from flask import Flask
import os

#Create the flask instance
app = Flask(__name__)


#Add the URL from the frontend to the cors policy
from flask_cors import CORS
CORS(app, origins=os.getenv("FRONT_URL"))

# #Configuration for logg
import logging
# Configurate logger level
logging.basicConfig(level=logging.DEBUG)

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
from config import Config
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

#Add routes from blueprints to app
from src.routes.user_routes import user_routes
from src.routes.auth_routes import auth_routes
app.register_blueprint(user_routes)
app.register_blueprint(auth_routes)

#Run the application
if __name__ == '__main__':
    app.run()