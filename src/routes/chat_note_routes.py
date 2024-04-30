from flask import Blueprint, request, make_response
from marshmallow import Schema, fields, ValidationError
from src.controllers import ChatNoteController
from src.utils.authentication import login_required
from werkzeug.exceptions import BadRequest
from settings import logger


chat_note_routes = Blueprint('chat_note_routes', __name__)
chat_note_prefix = '/chat/note'


class CreateNoteSchema(Schema):
    chat_id = fields.Integer(required=True)
    note = fields.String(required=True)

@chat_note_routes.route('/create', methods=['POST'])
def create_note():
    
    try:
        create_note_schema = CreateNoteSchema()
        note_data = create_note_schema.load(request.json)
                
    except ValidationError as error:
            return make_response(({'error': error.messages}, 400))
        
    except BadRequest as error:
        return make_response(({'error': error.description}, 400))
    
    
    response = ChatNoteController.create_note(note_data)
    return make_response(response)