from src.services import MessageService, ChatService
from database import db
from settings import logger
from src.models import Chat
from datetime import datetime
from flask import jsonify
from settings import APPLICATION_TIMEZONE
import pytz
from src.events import MessageEvents
from flask_login import current_user
from socketio_instance import socketio
from src.models import ChatStatus

class MessageController:
    
    def get_message(message_id):
        message = MessageService.get_message(message_id)
        ret_json = MessageService.get_message_returning_data(message)
        return {'success' : True, 'message' : ret_json}, 200
        
        
    
    def get_messages(chat_id, timestamp):
        #If chat does not exist returns error
        chat = Chat.query.get(chat_id)
        if not chat: return {'success': False, 'error' : 'chat not found'}, 404
        
        #Transform date and get the messages messages
        date = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc).astimezone(APPLICATION_TIMEZONE)
        messages, more_messages = MessageService.get_messages(chat, date)
        
        #Transform all messages into dicts to return as json
        js_mess = [MessageService.get_message_returning_data(message) for message in messages]
        
        #Timestamp of last message got
        last_timestamp = messages[-1].sent_at.timestamp() if len(messages) else datetime.now().timestamp()
        
        return {'success': True, 'last_timestamp': last_timestamp, 'messages': js_mess, 'more_messages': more_messages}, 200
    
    
    def receive_message(message_json):
        try:
            message_data = MessageService.get_message_data(message_json)
            chat = ChatService.get_or_create({'phone':message_data['phone_number'], 'whatsapp_name': message_data['name'], 'organization_phone_id': message_data['organization_phone_id']})
            message_data['chat_id'] = chat.id

            message = MessageService.create_message(message_data)
            MessageEvents.inserted(message)
            
            
            mess = {'id' : message.id, 'chat_id' : message.chat_id}
            mess['new_chat_status'] = message.chat.status
            mess['new_chat_status_name'] = ChatStatus(message.chat.status).name
            logger.debug(message.chat.expires_at)
            mess['new_expires_at'] = str(message.chat.expires_at)
            socketio.emit('receive-message-'+str(message.chat.organization_id), mess)
                            
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
            
            send_json = MessageService.prepare_message_body(message_json)
            wamid = MessageService.send_message(send_json)
            
            message_json['wamid'] = wamid
            message_json['user_id'] = current_user.id
            message = MessageService.create_message(message_json)
            MessageEvents.inserted(message)
            
            ret = MessageService.get_message_returning_data(message)
            

            
            return {'success': True, 'message': ret}, 201
        except BaseException as error:
            logger.error(str(error))
            db.session.rollback()
            return {'success': False, 'error': str(error)}, 400