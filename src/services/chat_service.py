from src.models import Chat, Message, MessageStatus
from database import db
from src.utils.messages_utils import base_headers, graph_messages_url
import requests

class ChatService:
    
    
    def set_messages_read(chat : Chat) -> None:
        
        #We will set all messages that are not already read 
        messages : list(Message) = [message for message in chat.messages \
                                            if message.user_id is None and message.status is not MessageStatus.READ.value]
        
        json = {
            "messaging_product": "whatsapp",
            "status" : "read"
        }
        
        for message in messages:
            json['message_id'] = message.wamid
            requests.post(url=graph_messages_url, json=json, headers=base_headers)
            message.status = MessageStatus.READ.value
        
        
        
        #Apply changes to database
        db.session.add_all(messages)
        db.session.commit()