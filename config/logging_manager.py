from flask_login import LoginManager
from flask import Flask

def configure_login_manager(login_manager : LoginManager, app : Flask) -> None:
    login_manager.init_app(app)
