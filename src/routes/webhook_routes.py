from flask import Blueprint, request, jsonify, make_response
from marshmallow import Schema, fields, ValidationError
from src.controllers import WebhookController, MessageController
from werkzeug.exceptions import BadRequest

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
        return make_response(({'error': error.messages}), 400)
    
    except BadRequest as error:
        return make_response(({'error': error.description}, 400))
    
    
    response = make_response(WebhookController.verify(verify_data))

    return response


@webhook_routes.route('/webhook', methods=['POST'])
def recieve_message():
        
    if _is_status(request.json): response = MessageController.receive_status(request.json) # Webhook catches a status update to a message
    elif _is_message(request.json): response = MessageController.receive_message(request.json) # Webhook catches a new message
    else: response = {'success': False, 'error': 'unknown data received in webhook'}, 400 # Unknown data, should never be executed but who knows
    
    return make_response(response)



#Checks if the json contains the structure of a status update
def _is_status(req_json):
    return 'statuses' in req_json['entry'][0]['changes'][0]['value']
#Checks if the json contains the structure of a new message
def _is_message(req_json):
    return 'messages' in req_json['entry'][0]['changes'][0]['value']