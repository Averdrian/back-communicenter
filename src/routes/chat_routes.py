from flask import Blueprint, request, make_response
from marshmallow import Schema, fields, ValidationError
from src.controllers import ChatController

chat_routes = Blueprint('chat_routes', __name__)
chat_prefix = '/chat'

@chat_routes.route('/get',  methods=['GET'])
@chat_routes.route('/get/<float:last_timestamp>',  methods=['GET'])
def get_chats(last_timestamp = None) :
    statuses = request.args.get('statuses')
    if statuses: statuses = [int(status) for status in statuses.split(',')]

    response = ChatController.get_chats(last_timestamp, statuses)
    
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

@chat_routes.route('/statuses', methods=['GET'])
def get_statuses():
    response = ChatController.get_statuses()
    return make_response(response)