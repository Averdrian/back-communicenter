from flask import Blueprint, request, jsonify, make_response
from marshmallow import Schema, fields, ValidationError
from app import logger
from src.controllers import WebhookController, MessageController

webhook_routes = Blueprint('webhook_routes', __name__)


class VerifyTokenSchema(Schema):
    mode = fields.Str(data_key="hub.mode", required=True)
    verify_token = fields.Str(data_key="hub.verify_token", required=True)
    challenge = fields.Str(data_key="hub.challenge", required=True)

@webhook_routes.route('/webhook', methods=['GET'])
def verify_token():
    try:
        verify_token_schema = VerifyTokenSchema()
        verify_data = verify_token_schema.load(request.args)
    except ValidationError as error:
        return jsonify({'error': error.messages}), 400
    
    response = make_response(WebhookController.verify(verify_data))

    return response


@webhook_routes.route('/webhook', methods=['POST'])
def recieve_message():
    response = MessageController.receiveMessage(request.json)
    return make_response(response)