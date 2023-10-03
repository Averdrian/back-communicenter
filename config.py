import os
class Config:
    PORT = int(os.getenv('FLASK_RUN_PORT', 8000))
    DEBUG = bool(os.getenv('DEBUG', True))
