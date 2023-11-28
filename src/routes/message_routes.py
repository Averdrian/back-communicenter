from flask import Blueprint, request, make_response
from marshmallow import Schema, fields, ValidationError
from src.controllers import MessageController

message_routes = Blueprint('message_routes', __name__)
message_prefix = '/messages'

class SendMessageSchema(Schema):
    chat_id = fields.Integer(required=True)
    type = fields.String(required=True)
    message = fields.String(required=False)
    preview_url = fields.Bool(required=False)
    media_id = fields.Integer(required=False)
    user_id = fields.Integer(required=False) #TODO: EN UN FUTURO ESTO NO SE VA A HACER, CUANDO AÑADAMOS LOS AUTH
    

@message_routes.route('/send', methods=['POST'])
def send_message():
    response = MessageController.send_message(request.json)
    return make_response(response)