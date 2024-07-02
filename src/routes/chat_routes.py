from flask import Blueprint, request, make_response
from marshmallow import Schema, fields, ValidationError
from src.controllers import ChatController

chat_routes = Blueprint('chat_routes', __name__)
chat_prefix = '/chat'


@chat_routes.route('',  methods=['GET'])
def all_chats() : 
    response = ChatController.get_all_chats()
    return make_response(response)

@chat_routes.route('/<int:chat_id>', methods=['GET'])
def get_chat(chat_id : int):
    response = ChatController.get_chat(chat_id)
    return make_response(response)

@chat_routes.route('/<int:chat_id>/read', methods=['POST'])
def read_messages(chat_id : int):
    response = ChatController.chat_read(chat_id)
    return make_response(response)


@chat_routes.route('/<int:chat_id>/status/<int:status>', methods=['PATCH'])
def update_status(chat_id : int, status : int):
    
    response = ChatController.update_status(chat_id, status)
    return make_response(response)