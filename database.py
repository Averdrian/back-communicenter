from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
DB_URI = 'postgresql://' + str(os.getenv('DB_USERNAME')) + ':' + str(os.getenv('DB_PASSWORD')) + '@' + str(os.getenv('DB_HOST')) + '/' + str(os.getenv('DB_NAME')) 