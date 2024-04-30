from src.models import ChatNote
from database import db
from flask_login import current_user

class ChatNoteService:
    
    
    def create_note(note_data : object) -> ChatNote:
        chat_note = ChatNote(chat_id=note_data['chat_id'], user_id=current_user.id, note=note_data['note'])
        db.session.add(chat_note)
        return chat_note
    
    
    # def get_all() -> list[Organization]:
    #     organizations = Organization.query.all()
    #     return organizations