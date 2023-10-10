from src.models.user import User
from src.utils.hash_password import check_password
from flask_login import login_user, logout_user

class AuthController:

    def login(login_data):

        email = login_data['email']
        password = login_data['password']

        try:
            user = User.query.filter_by(email=email).first()

            if user and check_password(password, user.password):
                login_user(user)
                return 'success', 200
            
            else: return 'Authentication error', 401

        except Exception as e:
            return {'error': 'Failed to login' + str(e)}, 500
        

    def logout():
        logout_user()
        return 'success', 200