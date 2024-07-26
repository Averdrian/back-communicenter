from database import db
from src.utils.hash_password import hash_password
from src.models import User, UserRole
from flask_login import current_user
import os

class UserService:
    
    def create_user(user_data):
        
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        organization_id = user_data['organization_id']
        role = user_data['role'] if 'role' in user_data else UserRole.EMPLOYEE.value

        new_user = User(username=username, email=email, password=hash_password(password), organization_id=organization_id, role=role)

        # Adds the user to the session
        db.session.add(new_user)
        db.session.commit()
        

    def get_users(query_items):
        user = User.query

        #If the user is not from the admin organization he only can get his own organization users 
        if current_user.organization_id != int(os.getenv("ADMIN_ORG_ID")): user = user.filter_by(organization_id=current_user.organization_id) 
        
        for key, value in query_items:
            try: user = user.filter(getattr(User,key)==value)
            except Exception as _: continue #If a query item key does not exist in the object we ignore them
        return user.all()