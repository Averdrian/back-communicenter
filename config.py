import os
import logging

class Config:
    PORT = int(os.getenv('FLASK_RUN_PORT', 8000))
    DEBUG = bool(os.getenv('DEBUG', False))
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + str(os.getenv('DB_USERNAME')) + ':' + str(os.getenv('DB_PASSWORD')) + '@' + str(os.getenv('DB_HOST')) + '/' + str(os.getenv('DB_NAME')) 
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')