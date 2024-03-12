from database import db
from src.services import OrganizationService


class OrganizationController:
    
    
    def create(organization_data):
        try:
            OrganizationService.create_organization(organization_data)
            db.session.commit()
            return {'success': True}, 201
        except Exception as error:
            return {'success': False, 'message': str(error)}, 500
            
        
        