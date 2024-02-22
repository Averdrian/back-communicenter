from database import db
from src.models import User, UserRole
from src.services import UserService
from flask_login import current_user, login_required

class UserController:

    def register(user_data):

        try:
            #Email already exists, throw error
            if User.query.filter_by(email=user_data['email']).first():
                return {'message': 'Email already taken'}, 400

            UserService.create_user(user_data)
            db.session.commit()

            return {'message': 'User created successfully'}, 201
        except Exception as e:
            # Error inserting into database
            db.session.rollback()
            return {'error': 'Failed to create user: ' + str(e)}, 500
        
        
    def get_users(query_args):
        try:
            list_users = UserService.get_users(query_args.items())
            return {'users': [us.to_dict() for us in list_users]}, 200
        except Exception as e:
            return {'error': 'Failed to get the users: ' + str(e)}, 500