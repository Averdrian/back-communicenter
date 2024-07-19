from flask import Blueprint, request, make_response
from marshmallow import Schema, fields, ValidationError
from src.controllers import MessageController
from datetime import datetime
import pytz
from werkzeug.exceptions import BadRequest
from settings import logger



message_routes = Blueprint('message_routes', __name__)
message_prefix = '/messages'

class SendMessageSchema(Schema):
    chat_id = fields.Integer(required=True)
    type = fields.String(required=True)
    message = fields.String(required=False)
    preview_url = fields.Bool(required=False)
    media = fields.Raw(required=False)


@message_routes.route('/send', methods=['POST'])
def send_message():
    try:
        
        data = request.form.to_dict()
        media = request.files.get('media')
        
        if media:
            data['media'] = media 
        
        send_message_schema = SendMessageSchema()
        message_data = send_message_schema.load(data)



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


@message_routes.route('/id/<message_id>', methods=['GET'])
def get_message(message_id):
    response = MessageController.get_message(message_id)
    return make_response(response)