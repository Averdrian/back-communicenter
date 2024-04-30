from flask import Blueprint, request, make_response
from marshmallow import Schema, fields, ValidationError
from src.controllers import TemplateController

from settings import logger
from werkzeug.exceptions import BadRequest


template_routes = Blueprint('template_routes', __name__)
template_prefix = '/template'

@template_routes.route('/all', methods=['GET'])
def get_all():
    response = TemplateController.get_all()
    return make_response(response)
    
# class CreateTemplateSchema(Schema):
#     organization_id = fields.String(required=True)
#     name = fields.String(required=True)
#     text = 
    
# @template_routes.route('/create', methods=['POST'])
# def create():
    