from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, request, make_response
from flask_login import login_required
from werkzeug.exceptions import BadRequest

from src.controllers import UserController

user_routes = Blueprint('user_routes', __name__)


class SignUpSchema(Schema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    organization_id = fields.Integer(required=True)

@login_required
@user_routes.route('/signup', methods=['POST'])
def sign_up():
    try:
        create_user_schema = SignUpSchema()
        user_data = create_user_schema.load(request.json)
        
    except ValidationError as error:
        return make_response(({'error': error.messages}), 400)
    
    except BadRequest as error:
        return make_response(({'error': error.description}, 400))
        
    result = UserController.register(user_data)

    return make_response(result)


@login_required
@user_routes.route('/users', methods=['GET'])
def get_users():
    
    result = UserController.get_users(request.args)
    return make_response(result)    