from database import db
from src.services import OrganizationService
from settings import logger
from src.utils.authentication import admin_org_required, manager_required
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors;

class OrganizationController:
    
    
    @manager_required
    def get_organization(organization_id):
        try:
            organization = OrganizationService.get_organization(organization_id)
            return {'success': True, 'organization': organization.to_dict()}, 200
        except Exception as error:
            return {'success': False, 'message': 'User not found'}, 404
    
    @admin_org_required
    def create(organization_data):
        try:
            OrganizationService.create_organization(organization_data)
            db.session.commit()
            return {'success': True}, 201
        
        except errors.lookup(UNIQUE_VIOLATION) as error:
            logger.error("hola")
            return {'success': False, 'message': "Nombre de organización ya existente, prueba con otro"}, 400
        except Exception as error:
            return {'success': False, 'message': "Error al crear la organización"}, 500
            
            
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