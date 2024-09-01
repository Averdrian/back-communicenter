from flask import Blueprint, request, make_response
from marshmallow import Schema, fields, ValidationError
from src.controllers import OrganizationController
from datetime import datetime
import pytz
from settings import logger
from werkzeug.exceptions import BadRequest


organization_routes = Blueprint('organization_routes', __name__)
organization_prefix = '/organization'



class CreateOrganizationSchema(Schema):
    name = fields.String(required=True)
    wa_phone_id = fields.Integer(required=False)
    wb_account_id = fields.Integer(required=False)
    wa_verify_token = fields.String(required=False)
    wa_api_key = fields.String(required=False)
    

@organization_routes.route('/create', methods=['POST'])
def create():
    try:
        logger.debug(request.json)
        create_organization_schema = CreateOrganizationSchema()
        organization_data = create_organization_schema.load(request.json)
        
    except ValidationError as error:
        return make_response(({'error': error.messages}), 400)
    
    except BadRequest as error:
        return make_response(({'error': error.description}, 400))
    
    response = OrganizationController.create(organization_data)
    return make_response(response)

@organization_routes.route('', methods=['GET'])
def get_organizations():
    page = request.args.get('page', 1, type=int)
    response = OrganizationController.get_organizations(page)
    return make_response(response)

@organization_routes.route('/<int:organization_id>', methods=['GET'])
def get_organization(organization_id):
    response = OrganizationController.get_organization(organization_id)
    return make_response(response)


@organization_routes.route('/all', methods=['GET'])
def get_all():
    response = OrganizationController.get_all()
    return make_response(response)


class EditOrganizationSchema(Schema):
    name = fields.String(required=False)
    wa_phone_id = fields.Integer(required=False)
    wb_account_id = fields.Integer(required=False)
    wa_verify_token = fields.String(required=False)
    wa_api_key = fields.String(required=False)
@organization_routes.route('/<int:organization_id>', methods=['PUT'])
def edit_organization(organization_id):
    try:
        edit_organization_schema = EditOrganizationSchema()
        organization_data = edit_organization_schema.load(request.json)

        response = OrganizationController.edit_organization(organization_id, organization_data)
        return make_response(response)
    
    except ValidationError as error:
        return make_response(({'error': error.messages}), 400)
    
    except BadRequest as error:
        return make_response(({'error': error.description}, 400))
