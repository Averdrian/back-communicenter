import os
import logging
from flask_login import LoginManager
from logging import Logger
import pytz

class Settings:
    PORT = int(os.getenv('FLASK_RUN_PORT', 8000))
    DEBUG = bool(os.getenv('DEBUG', False))
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    
PAGE_SIZE = 12
CHAT_PAGE_SIZE = 20
USER_PAGE_SIZE = 25
APPLICATION_TIMEZONE =  pytz.timezone('Europe/Madrid')
    
    
def create_logger() -> Logger:
    logging.basicConfig(level=Settings.LOG_LEVEL)
    logger = logging.getLogger('communicenter')

    #Add the file handler
    file_handler = logging.FileHandler('app.log')
    log_level = Settings.LOG_LEVEL
    file_handler.setLevel(logging.getLevelName(log_level))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


login_manager = LoginManager()
logger = create_logger()

