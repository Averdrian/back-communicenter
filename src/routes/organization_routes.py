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
    wa_phone_id = fields.Integer(required=True)
    wb_account_id = fields.Integer(required=True)
    wa_verify_token = fields.String(required=False)
    wa_api_key = fields.String(required=False)
    

@organization_routes.route('/create', methods=['POST'])
def send_message():
    try:
        create_organization_schema = CreateOrganizationSchema()
        organization_data = create_organization_schema.load(request.json)
        
    except ValidationError as error:
        return make_response(({'error': error.messages}), 400)
    
    except BadRequest as error:
        return make_response(({'error': error.description}, 400))
    
    response = OrganizationController.create(organization_data)
    return make_response(response)