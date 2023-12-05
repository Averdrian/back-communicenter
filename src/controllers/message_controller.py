from src.services import MessageService
from database import db
from settings import logger
from src.models import Chat, Message
from datetime import datetime
from flask import jsonify
from settings import APPLICATION_TIMEZONE
import pytz

class MessageController:
    
    def get_messages(chat_id, timestamp):
        #If chat does not exist returns error
        chat = Chat.query.get(chat_id)
        if not chat: return {'success': False, 'error' : 'chat not found'}, 404
        
        #Transform date and get the messages messages
        date = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc).astimezone(APPLICATION_TIMEZONE)
        messages, more_messages = MessageService.get_messages(chat, date)
        
        #Transform all messages into dicts to return as json
        js_mess = [message.as_dict() for message in messages]
        
        #Timestamp of last message got
        last_timestamp = messages[-1].sent_at.timestamp() if len(messages) else datetime.now().timestamp()
        
        return {'success': True, 'last_timestamp': last_timestamp, 'messages': js_mess, 'more_messages': more_messages}, 200
    
    def receive_message(message_json):
        try:
            message_data = MessageService.get_message_data(message_json)
            chat = MessageService.create_or_update_chat(message_data)
            message_data['chat_id'] = chat.id

            MessageService.create_message(message_data)
            
            return {'success': True}, 201
            
        except Exception as error:
            logger.error(str(error))
            db.session.rollback()
            return {'success': False, 'error': str(error)}, 500
        
        
        
    def receive_status(status_json):
        try:
            status, wamid = MessageService.get_status_data(status_json)
            MessageService.update_status(wamid, status)
            return {'success': True}, 200
        except Exception as error:
            logger.error(str(error))
            db.session.rollback()
            return {'success': False, 'error': str(error)}, 500



    def send_message(message_json):
        
        try:
            if not MessageService.can_send(message_json) : return {'success' : False, 'error': 'The chat is expired'}, 403
            
            send_json = MessageService.prepare_message_body(message_json)
            success, wamid = MessageService.send_message(send_json)
            
            if not success : return {'success': False, 'error': "Error sending message"}
            
            message_json['wamid'] = wamid
            MessageService.create_message(message_json)
            
            return {'success': True}, 201
        except Exception as error:
            logger.error(str(error))
            db.session.rollback()
            return {'success': False, 'error': str(error)}, 500