from flask import Blueprint, request, make_response
from marshmallow import Schema, fields, ValidationError
from src.controllers import ChatController

chat_routes = Blueprint('chat_routes', __name__)
chat_prefix = '/chat'


@chat_routes.route('/<chat_id>/read', methods=['POST'])
def send_message(chat_id : int):
    response = ChatController.chat_read(chat_id)
    return make_response(response)