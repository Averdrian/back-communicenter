from database import db
from src.models import User, UserRole
from src.services import UserService
from flask_login import current_user, login_required
from src.utils.authentication import manager_required
from src.utils import hash_password

class UserController:


    @manager_required
    def register(user_data):
        try:
            #Email already exists, throw error
            if User.query.filter_by(email=user_data['email']).first():
                return {'message': 'Email already taken'}, 400

            UserService.create_user(user_data)

            return {'message': 'User created successfully'}, 201
        except Exception as e:
            # Error inserting into database
            db.session.rollback()
            return {'error': 'Failed to create user: ' + str(e)}, 500
        
    @manager_required
    def get_users(query_args):
        try:
            list_users = UserService.get_users(query_args.items())
            return {'users': [us.to_dict() for us in list_users]}, 200
        except Exception as e:
            return {'error': 'Failed to get the users: ' + str(e)}, 500
        
    @manager_required
    def get_user(user_id):
        try:
            user = UserService.get_user(user_id)
            return {'user': user.to_dict() }, 200
        except Exception as _:
            return {'error': 'User not found'}, 404
        
    @login_required
    def edit_user(user_id, new_user_data):
        try:
            UserService.edit_user(user_id, new_user_data)
            return {'success': True}, 204
            
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500
        
    @manager_required
    def delete_user(user_id):
        try:
            UserService.delete_user(user_id)
            return {'success': True}, 204
        except Exception as error:
            return {'success': False, 'message': str(error)}