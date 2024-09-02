from src.models import Chat, ChatStatus, Message, MessageStatus, Organization
from database import db
from src.utils.messages_utils import base_headers_text, graph_messages_url
import requests
from settings import logger
from flask_login import current_user
from typing import List
from settings import PAGE_SIZE, CHAT_PAGE_SIZE
from datetime import datetime
class ChatService:
    
    
    def get_chats(last_date : datetime, statuses : List[str]) -> List[Chat] :
        chats = Chat.query
        
        chats = chats.filter(
            Chat.organization_id == current_user.organization_id,
            Chat.last_message_at < last_date,
        )
        if statuses: chats = chats.filter(Chat.status.in_(statuses))
        chats = chats.order_by(Chat.last_message_at.desc()).limit(CHAT_PAGE_SIZE).all()
        return chats, len(chats) == CHAT_PAGE_SIZE
    
    def get_or_create(chat_data : object) -> Chat:
                
        chat = Chat.query.filter(Chat.phone == chat_data['phone']).first()
    
        #If chat does not exist we create it
        if not chat:    
            
            organization = Organization.query.filter(Organization.wa_phone_id == chat_data['organization_phone_id']).first()
            chat = Chat(phone=chat_data['phone'], whatsapp_name=chat_data['whatsapp_name'], organization_id=organization.id)
            
            db.session.add(chat)
            db.session.commit()
            
        return chat
        
    
    def set_messages_read(chat : Chat) -> None:
        
        #We will set all messages that are not already read 
        
        messages = [message for message in chat.messages \
                        if message.user_id is None and message.status != MessageStatus.READ.value]
        
        json = {
            "messaging_product": "whatsapp",
            "status" : "read"
        }
        
        for message in messages:
            json['message_id'] = message.wamid
            requests.post(url=graph_messages_url(), json=json, headers=base_headers_text()) #Call graph api to set messages to read
            message.status = MessageStatus.READ.value #We also set the messages to read
        
        
        
        #Apply changes to database
        db.session.add_all(messages)
        db.session.commit()
        
        
    #This method does not commit the db session, usually this will be part of other commits
    def update_chat_status(chat : Chat, status) -> None: 
        chat.status = status
        db.session.add(chat)
        
    
    def set_chats_closed():

        Chat.query.filter(
            Chat.status.in_([ChatStatus.ANSWERED.value, ChatStatus.PENDING.value, ChatStatus.FIRST_PENDING.value, ChatStatus.SEEN.value, ChatStatus.FIRST_PENDING.value]),
            Chat.expires_at < datetime.now(),
            Chat.organization_id==current_user.organization_id
        ).update({'status' : ChatStatus.CLOSED.value})
        
        db.session.commit()
