from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, request, make_response
from flask_login import login_required
from werkzeug.exceptions import BadRequest
from settings import logger
from src.controllers import UserController

user_routes = Blueprint('user_routes', __name__)
user_prefix = '/users'


@user_routes.route('/', methods=['GET'])
def get_users():
    
    result = UserController.get_users(request.args)
    return make_response(result)    

@user_routes.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    response = UserController.get_user(user_id)
    return make_response(response)


class EditUserSchema(Schema):
    username = fields.String(required=False)
    email = fields.String(required=False)
    password = fields.String(required=False)
    role = fields.Integer(required=False)


@user_routes.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        edit_user_schema = EditUserSchema()
        user_data = edit_user_schema.load(request.json)

        response = UserController.edit_user(user_id, user_data)
        return make_response(response)
    
    except ValidationError as error:
        return make_response(({'error': error.messages}), 400)
    
    except BadRequest as error:
        return make_response(({'error': error.description}, 400))
    
@user_routes.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        response = UserController.delete_user(user_id)
        return make_response(response)
    except Exception as error:
        return make_response(({'error': str(error)}, 500))
    