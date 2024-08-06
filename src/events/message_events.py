from src.models import Chat, Message, ChatStatus, MessageStatus
from database import db
from datetime import timedelta

class MessageEvents:


    def inserted(message : Message):
        chat : Chat = Chat.query.get(message.chat_id)
        chat.last_message_at = message.sent_at
        if message.user_id is None:
            chat.expires_at = message.sent_at + timedelta(days=1)
        chat.status = MessageEvents._new_chat_status(message, chat).value
        db.session.commit()
            
    def receive_status(chat_id : int, message_status: MessageStatus) -> None:
        chat : Chat = Chat.query.get(chat_id)
        if chat.status == ChatStatus.ANSWERED.value and message_status == MessageStatus.READ:
            chat.set_status(ChatStatus.SEEN)
            db.session.add(chat)
            db.session.commit()
        
        
    def _new_chat_status(message : Message, chat : Chat) -> ChatStatus:
        if message.user_id : status = ChatStatus.ANSWERED
        else : status = ChatStatus.FIRST_PENDING if len(chat.messages) == 1 or chat.status == ChatStatus.FIRST_PENDING == 1 else ChatStatus.PENDING #If messages has not user_id, its coming from customer, and if is the first message we put first pending, if not is just pending
        return status
            
            