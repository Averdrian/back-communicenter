from flask import make_response
from src.services import MessageService
from app import logger

class MessageController:
    
    
    def receiveMessage(message_json):
        try:
            response = MessageService.messageReceived(message_json)
            return response, 201
        except Exception as error:
            logger.error(str(error))
            raise(error)
            return {'error': str(error)}, 500
   
    