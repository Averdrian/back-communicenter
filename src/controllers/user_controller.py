from app import app, db
from flask import Blueprint
from src.models.user import User
class UserController:

    def create_user(user_data):
        username = user_data['username']
        email = user_data['email']
        new_user = User(username=username, email=email)
        try:
            # Añade el usuario a la sesión y realiza la inserción en la base de datos
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
        except Exception as e:
            # Manejo de errores en caso de fallo en la inserción
            db.session.rollback()
            return {'error': 'Failed to create user'}, 500