from app import db
from src.models.user import User
from src.utils.hash_password import hash_password

class UserController:

    def create(user_data):

        username = user_data['username']
        email = user_data['email']
        password = user_data['password']

        try:
            #Email already exists, throw error
            if User.query.filter_by(email=email).first():
                return {'message': 'Email already taken'}, 400

            new_user = User(username=username, email=email, password=hash_password(password))

            # Adds the user to the session and commits into database
            db.session.add(new_user)
            db.session.commit()

            return {'message': 'User created successfully'}, 201
        except Exception as e:
            # Error inserting into database
            db.session.rollback()
            return {'error': 'Failed to create user: ' + str(e)}, 500