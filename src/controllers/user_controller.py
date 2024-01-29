from database import db
from src.models.user import User
from src.services import UserService

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