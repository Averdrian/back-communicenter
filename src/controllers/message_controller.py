from flask import make_response
from src.services import MessageService
from app import logger, db
from flask import jsonify
import os
import requests
from src.models import Message, Chat
from datetime import datetime

class MessageController:
    
    def receive_message(message_json):
        try:
            
            message_data = MessageService.get_message_data(message_json)
            chat = MessageService.create_or_update_chat(message_data)
            MessageService.create_message(chat.id, message_data)
            
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
            url = "https://graph.facebook.com/{version}/{phone_id}/messages".format(version=os.getenv('WA_API_VERSION'), phone_id=os.getenv('WA_PHONE_ID'))
            
            
            json = {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": "34608489085",
                    "type": "text",
                    "text": message_json
                }
                        
            headers = {
                "Authorization": "Bearer {token}".format(token=os.getenv('WA_API_KEY')),
                'Content-Type': 'application/json'
            }

            response = requests.post(url=url,json=json, headers=headers)
            wamid = response.json()['messages'][0]['id']
            
            chat_id = Chat.query.filter_by(phone=34608489085).first().id
            message = Message(chat_id,{
                'content':{
                    'message': message_json['body'],
                },
                'type': 'text',
                'wamid': wamid,
                'timestamp': datetime.now().timestamp()
            })
            db.session.add(message)
            db.session.commit()
            return {'success': True}, 201
        except Exception as error:
            logger.error(str(error))
            db.session.rollback()
            return {'success': False, 'error': str(error)}, 500