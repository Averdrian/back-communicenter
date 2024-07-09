from flask import Blueprint, request, make_response
from marshmallow import Schema, fields, ValidationError
from src.controllers import MessageController
from datetime import datetime
import pytz
from werkzeug.exceptions import BadRequest



message_routes = Blueprint('message_routes', __name__)
message_prefix = '/messages'

class SendMessageSchema(Schema):
    chat_id = fields.Integer(required=True)
    type = fields.String(required=True)
    message = fields.String(required=False)
    preview_url = fields.Bool(required=False)
    media_id = fields.Integer(required=False)


@message_routes.route('/send', methods=['POST'])
def send_message():
    try:
        send_message_schema = SendMessageSchema()
        message_data = send_message_schema.load(request.json)

    except ValidationError as error:
        return make_response(({'error': error.messages}, 400))

    except BadRequest as error:
        return make_response(({'error': error.description}, 400))


    response = MessageController.send_message(message_data)
    return make_response(response)


@message_routes.route('/<chat_id>', methods=['GET'])
@message_routes.route('/<chat_id>/<float:timestamp>', methods=['GET'])
def get_messages(chat_id, timestamp=None):
    if timestamp is None: timestamp = datetime.now(pytz.timezone('Europe/Madrid')).timestamp()
    response = MessageController.get_messages(chat_id, timestamp)
    return make_response(response)