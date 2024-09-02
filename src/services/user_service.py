from database import db
from src.utils.hash_password import hash_password
from src.models import User, UserRole
from flask_login import current_user
from sqlalchemy.orm import Query
from settings import logger, USER_PAGE_SIZE

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
        

    def get_users(page:int, organization_id: int | None):
        users : Query = User.query
        #If the user is not from the admin organization he only can get his own organization users 
        if not current_user.organization.is_admin : users = users.filter_by(organization_id=current_user.organization_id) 
        elif organization_id: users = users.filter_by(organization_id=organization_id)
        users = users.group_by(User.organization_id, User.username, User.id)
        
        users = users.paginate(page=page, per_page=USER_PAGE_SIZE, error_out=False)
        
        return [user.to_dict() for user in users], users.pages
    
    def get_user(user_id: int) -> User:
        user_query : Query = User.query
        if not current_user.organization.is_admin: user = user.filter_by(organization_id=current_user.organization_id)
        user = user_query.get_or_404(user_id)
        return user
    
    def edit_user(user_id: int, user_data : dict) -> None:
        
        if 'password' in user_data:
            user_data['password'] = hash_password(user_data['password'])
        
        User.query.filter_by(id=user_id).update(user_data)
        db.session.commit()
        
        
    def delete_user(user_id : int) -> None:
        user : User = User.query.get(user_id) 
        db.session.delete(user)
        db.session.commit()