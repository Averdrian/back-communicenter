from src.models import Chat, Message, ChatStatus
from database import db
from datetime import timedelta

class MessageEvents:


    def inserted(message : Message):
        chat : Chat = Chat.query.get(message.chat_id)
        chat.last_message_at = message.sent_at
        if message.user_id is None:
            chat.expires_at = message.sent_at + timedelta(days=1)
        chat.status = MessageEvents._new_chat_status(message, chat)
        db.session.commit()
            
                
        
    def _new_chat_status(message : Message, chat : Chat) -> ChatStatus:
        
        if message.user_id : status = ChatStatus.ANSWERED
        else : status = ChatStatus.FIRST_PENDING if len(chat.messages) == 1 else ChatStatus.PENDING
        return status
            
            