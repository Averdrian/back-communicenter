from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from src.controllers.auth_controller import AuthController

auth_routes = Blueprint('user_routes', __name__)


class LogInSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)

@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        login_schema = LogInSchema()
        login_data = login_schema.load(request.json)

    except ValidationError as error:
        return jsonify({'error': error.messages}), 400
    
    result = AuthController.login(login_data)

    return jsonify(result)



@auth_routes.route('/logout', methods=['POST'])
def logout():
    result = AuthController.logout()
    return jsonify(result)