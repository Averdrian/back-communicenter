from flask import Flask
from src.routes import auth_routes, message_routes, user_routes, webhook_routes, chat_routes
from src.routes import message_prefix, chat_prefix

def register_blueprints(app: Flask) -> None:
    app.register_blueprint(user_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(webhook_routes)
    app.register_blueprint(message_routes, url_prefix=message_prefix)
    app.register_blueprint(chat_routes, url_prefix=chat_prefix)