from app import db
from src.models.user import User
from src.utils.hash_password import hash_password, check_password

class UserController:

    def sign_up(user_data):
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        try:

            #Email already exists, throw error
            if User.query.filter_by(email=email).first():
                return {'message': 'Email already taken'}, 400

            new_user = User(username=username, email=email, password=hash_password(password))

            # Añade el usuario a la sesión y realiza la inserción en la base de datos
            db.session.add(new_user)
            db.session.commit()

            return {'message': 'User created successfully'}, 201
        except Exception as e:
            # Manejo de errores en caso de fallo en la inserción
            db.session.rollback()
            return {'error': 'Failed to create user: ' + str(e)}, 500