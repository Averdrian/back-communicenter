from flask import Blueprint, request, jsonify, make_response
from marshmallow import Schema, fields, ValidationError
from app import logger
from src.controllers import WebhookController, MessageController

message_routes = Blueprint('message_routes', __name__)
message_prefix = '/messages'

@message_routes.route('/sendtmp', methods=['POST'])
def send_message_tmp():
    
    response = MessageController.send_message_tmp(request.json)
    return make_response(response)


@message_routes.route('/send', methods=['POST'])
def send_message():
    logger.debug(request.json)
    response = MessageController.send_message(request.json)
    return make_response(response)