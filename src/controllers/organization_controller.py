from database import db
from src.services import OrganizationService
from settings import logger
from src.utils.authentication import admin_org_required, manager_required
class OrganizationController:
    
    @admin_org_required
    def create(organization_data):
        try:
            OrganizationService.create_organization(organization_data)
            db.session.commit()
            return {'success': True}, 201
        except Exception as error:
            return {'success': False, 'message': str(error)}, 500
            
    @admin_org_required
    def get_all():
        try:
            orgs = OrganizationService.get_all()
            orgs = list(map((lambda org: {'id':org.id, 'name': org.name}), orgs))
            
            return {'success': True, 'organizations': orgs}, 200
        except Exception as error:
            return {'success': False, 'error': 'Error getting organizations: ' + str(error)}, 500

    @manager_required   
    def edit_organization(organization_id, organization_data):
        try:
            OrganizationService.edit_organization(organization_id, organization_data)
            return {'success': True}, 204
        except Exception as e:
            return {'success': False, 'error': str(e)}, 500