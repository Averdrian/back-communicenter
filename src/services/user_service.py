from database import db
from src.utils.hash_password import hash_password
from src.models import User

class UserService:
    
    def create_user(user_data):
        
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        organization_id = user_data['organization_id']

        new_user = User(username=username, email=email, password=hash_password(password), organization_id=organization_id)

        # Adds the user to the session
        db.session.add(new_user)