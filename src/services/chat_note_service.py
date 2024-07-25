from src.models import ChatNote
from database import db
from flask_login import current_user, login_required

class ChatNoteService:
    
    @login_required
    def create_note(note_data : object) -> ChatNote:
        chat_note = ChatNote(chat_id=note_data['chat_id'], user_id=current_user.id, note=note_data['note'])
        db.session.add(chat_note)
        db.session.commit()
        return chat_note
    
    @login_required
    def get_notes(chat_id : int) -> list[ChatNote] | None : 
        chat_notes = ChatNote.query.filter_by(chat_id=chat_id).order_by(ChatNote.created_at)
        return chat_notes