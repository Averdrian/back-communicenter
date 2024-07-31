from flask import Flask
from src.routes import auth_routes, message_routes, user_routes, webhook_routes, chat_routes, organization_routes, template_routes, chat_note_routes
from src.routes import message_prefix, chat_prefix, organization_prefix, template_prefix, chat_note_prefix, user_prefix
from flask import jsonify

def register_blueprints(app: Flask) -> None:
    app.register_blueprint(user_routes, url_prefix=user_prefix)
    app.register_blueprint(auth_routes)
    app.register_blueprint(webhook_routes)
    app.register_blueprint(message_routes, url_prefix=message_prefix)
    app.register_blueprint(chat_routes, url_prefix=chat_prefix)
    app.register_blueprint(organization_routes, url_prefix=organization_prefix)
    app.register_blueprint(template_routes, url_prefix=template_prefix)
    app.register_blueprint(chat_note_routes, url_prefix=chat_note_prefix)
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify(error="Resource not found", message="The requested URL was not found on the server."), 404
