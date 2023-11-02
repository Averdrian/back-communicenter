from flask import Blueprint, request, jsonify, make_response
from flask_login import login_required
from marshmallow import Schema, fields, ValidationError
from app import logger
from src.controllers.webhook_controller import WebhookController
from src.services.message_service import MessageService
import json

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
    logger.debug('Full: ' + str(request.json))

    message_data = MessageService.getMessageData(request.json)

    logger.debug(message_data)

    # logger.debug('Phone Number: ' + MessageService.getPhoneNumber(request.json))
    # logger.debug('Whatsapp Name: ' + MessageService.getWhatsAppName(request.json))
    # message_object = MessageService.getMessageObject(request.json)
    # # logger.debug('Message object: ' + str(message_object))
    # # logger.debug('Media URL: ' + str(MessageService.getMediaUrl(MessageService.getMediaId(message_object))))

    # logger.debug('Message_type: ' + MessageService.getMessageType(request.json))

    # media_url_object = MessageService.getMediaUrl(MessageService.getMediaId(message_object))
    # media_url_object = json.loads(media_url_object)

    # logger.debug(str(MessageService.getMediaImage(media_url_object['url'])))

    # return MessageService.getMediaImage(media_url_object['url'])

    # logger.info('URL: ' + media_url_object['url'])
    
    # # logger.debug('Message object: ' + str(MessageService.getMessageObject(request.json)))
    # # logger.debug('Mime_type: ' + MessageService.getFileMimeType(message_object))
    # return jsonify({'message': 'debug'}), 418

    return make_response(message_data, 200)