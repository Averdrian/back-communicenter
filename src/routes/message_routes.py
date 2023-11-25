from flask import Blueprint, request, jsonify, make_response
from marshmallow import Schema, fields, ValidationError
from app import logger
from src.controllers import MessageController

message_routes = Blueprint('message_routes', __name__)
message_prefix = '/messages'

@message_routes.route('/send', methods=['POST'])
def send_message():
    response = MessageController.send_message(request.json)
    return make_response(response)