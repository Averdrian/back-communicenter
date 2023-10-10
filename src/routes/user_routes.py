from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, request, jsonify

from src.controllers.user_controller import UserController
from src.controllers.auth_controller import AuthController

user_routes = Blueprint('user_routes', __name__)


class SignUpSchema(Schema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)


@user_routes.route('/signup', methods=['POST'])
def sign_up():
    try:
        create_user_schema = SignUpSchema()
        user_data = create_user_schema.load(request.json)
        
    except ValidationError as error:
        return jsonify({'error': error.messages}), 400
        
    result = UserController.create(user_data)

    return jsonify(result)
