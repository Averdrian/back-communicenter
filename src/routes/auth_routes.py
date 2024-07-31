from flask import Blueprint, request, make_response
from flask_login import login_required
from marshmallow import Schema, fields, ValidationError
from src.controllers.auth_controller import AuthController
from werkzeug.exceptions import BadRequest
from src.controllers import UserController

auth_routes = Blueprint('auth_routes', __name__)


class LogInSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)

@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        login_schema = LogInSchema()
        login_data = login_schema.load(request.json)

    except ValidationError as error:
        return make_response(({'error': error.messages}), 400)
    
    except BadRequest as error:
        return make_response(({'error': error.description}, 400))
    
    
    result = AuthController.login(login_data)

    return make_response(result)


@auth_routes.route('/logout', methods=['POST'])
@login_required
def logout():
    result = AuthController.logout()
    return make_response(result)


class SignUpSchema(Schema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    organization_id = fields.Integer(required=True)
    role = fields.Integer(required=False)

@auth_routes.route('/signup', methods=['POST'])
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

