from database import db
from src.models import Chat
from settings import logger
from src.services import ChatNoteService
from flask_login import current_user, login_required


class ChatNoteController:

    @login_required
    def get_notes(chat_id):
        chat_notes = ChatNoteService.get_notes(chat_id)
        chat_notes = [note.as_dict() for note in chat_notes]
        return {'success' : True, 'notes': chat_notes}, 200


    @login_required
    def create_note(note_data):
        try:
            chat_note = ChatNoteService.create_note(note_data)
            return {'success': True, 'note':chat_note.as_dict()}, 201
        except Exception as error:
            return {'success': False, 'message': str(error)}, 500

    @login_required
    def delete_note(note_id):
        try:
            ChatNoteService.delete_note(note_id)
            return {'success': True}, 204

        except Exception as error:
            return {'success': False, 'message': str(error)}, 500
