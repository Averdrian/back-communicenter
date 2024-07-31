from database import db
from src.utils.hash_password import hash_password
from src.models import User, UserRole
from flask_login import current_user
from sqlalchemy.orm import Query
from settings import logger

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
        user : Query = User.query
        
        #If the user is not from the admin organization he only can get his own organization users 
        if not current_user.organization.is_admin : user = user.filter_by(organization_id=current_user.organization_id) 
        else : user = user.group_by(User.organization_id, User.id)
        for key, value in query_items:
            try: user = user.filter(getattr(User,key)==value)
            except Exception as _: continue #If a query item key does not exist in the object we ignore them
        return user.all()
    
    def get_user(user_id: int) -> User:
        user_query : Query = User.query
        if not current_user.organization.is_admin: user = user.filter_by(organization_id=current_user.organization_id)
        user = user_query.get_or_404(user_id)
        return user
    
    def edit_user(user_id: int, user_data : dict) -> None:
        User.query.filter_by(id=user_id).update(user_data)
        db.session.commit()