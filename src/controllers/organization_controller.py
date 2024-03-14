from database import db
from src.services import OrganizationService
from settings import logger

class OrganizationController:
    
    
    def create(organization_data):
        try:
            OrganizationService.create_organization(organization_data)
            db.session.commit()
            return {'success': True}, 201
        except Exception as error:
            return {'success': False, 'message': str(error)}, 500
            
        
    def get_all():
        try:
            orgs = OrganizationService.get_all()
            orgs = list(map((lambda org: org.to_dict()), orgs))
            
            return {'success': True, 'organizations': orgs}, 200
        except Exception as error:
            return {'success': False, 'error': 'Error getting organizations: ' + str(error)}, 500
