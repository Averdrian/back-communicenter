from database import db
from src.models import Chat
from settings import logger
from src.services import ChatNoteService


class ChatNoteController:
    
    def get_notes():
        pass
    
    def create_note(note_data):
        try:
            chat_note = ChatNoteService.create_note(note_data)
            db.session.commit()
            return {'success': True, 'note':chat_note.to_dict()}, 201
        except Exception as error:
            return {'success': False, 'message': str(error)}, 500
