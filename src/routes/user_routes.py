from app import app
from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, make_response, request, jsonify

from src.controllers.user_controller import UserController

user_routes = Blueprint('user_routes', __name__)


class CreateUserSchema(Schema):
    username = fields.String(required=True)
    email = fields.String(required=True)


@user_routes.route('/users', methods=['POST'])
def create_user_route():
    try:
        create_user_schema = CreateUserSchema()
        user_data = create_user_schema.load(request.json)
    except ValidationError as error:
        return jsonify({'error': error.messages}), 400
        
    result = UserController.create_user(user_data)

    return jsonify(result)

