from src.models import Chat
from database import db
from datetime import timedelta

class MessageEvents:


    def inserted(message):
        chat = Chat.query.get(message.chat_id)
        if chat:
            chat.last_message_at = message.sent_at
            if message.user_id is None:
                chat.expires_at = message.sent_at + timedelta(days=1)
            db.session.commit()