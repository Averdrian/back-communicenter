import os

class Config:
    PORT = int(os.getenv('FLASK_RUN_PORT', 8000))
    DEBUG = bool(os.getenv('DEBUG', True))
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + os.getenv('DB_USERNAME') + ':' + os.getenv('DB_PASSWORD') + '@' + os.getenv('DB_HOST') + '/' + os.getenv('DB_NAME') 
 