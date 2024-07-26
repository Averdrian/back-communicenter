from src.models.user import User
from src.utils.hash_password import check_password, generate_access_token
from flask_login import login_user, logout_user
from flask import jsonify

class AuthController:

    def login(login_data):

        try:
            user : User = User.query.filter_by(email=login_data['email']).first()

            if user and check_password(login_data['password'], user.password):
                login_user(user, remember=False)
                token = generate_access_token(user.id)

                return jsonify({'user': user.to_dict(), 'access_token': token}), 200
            
            else: return {'success' : False, 'error': 'Authentication error'}, 401

        except Exception as e:
            return {'success': False, 'error': 'Failed to login' + str(e)}, 500
        

    def logout():
        logout_user()
        return {'success': True}, 200