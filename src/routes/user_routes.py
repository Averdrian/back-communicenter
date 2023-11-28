from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, request, jsonify, make_response

from src.controllers import UserController

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
        return make_response(jsonify({'error': error.messages}), 400)
        
    result = UserController.create(user_data)

    return make_response(result)

