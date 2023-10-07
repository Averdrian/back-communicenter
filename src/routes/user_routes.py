from app import app
from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, make_response, request, jsonify

from src.controllers.user_controller import UserController

user_routes = Blueprint('user_routes', __name__)


class CreateUserSchema(Schema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)


@user_routes.route('/signup', methods=['POST'])
def sign_up():
    try:
        create_user_schema = CreateUserSchema()
        user_data = create_user_schema.load(request.json)
    except ValidationError as error:
        return jsonify({'error': error.messages}), 400
        
    result = UserController.sign_up(user_data)

    return jsonify(result)

