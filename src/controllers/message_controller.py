from flask import make_response
from src.services import MessageService
from app import logger
from flask import jsonify

class MessageController:
    
    def receiveMessage(message_json):
        try:
            
            message_data = MessageService.getMessageData(message_json)
            chat = MessageService.createOrUpdateChat(message_data)
            MessageService.createMessage(chat.id, message_data)
            
            return {'success': True}, 201
            
        except Exception as error:
            logger.error(str(error))
            return {'success': False, 'error': str(error)}, 500
   
    