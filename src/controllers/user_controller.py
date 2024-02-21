from database import db
from src.models import User, UserRole
from src.services import UserService
from flask_login import current_user, login_required

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
        
        
    #TODO: solo se muestren los usuarios de todas las companies si es de la organizacion de administracion (ahora estara como organization_id = 1)
    def get_users(query_args):
        
        user = User.query
        if current_user.organization_id != 1: user = user.filter_by(organization_id=current_user.organization_id)
        
        for clave, valor in query_args.items():
            try: user = user.filter(getattr(User,clave)==valor)
            except Exception as _: continue #Si un filtro del query string no tiene sentido lo ignoramos
        users = user.all()
            
        return {'users': [us.to_dict() for us in users]}, 200