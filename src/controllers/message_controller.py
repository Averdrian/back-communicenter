from flask import make_response
from src.services import MessageService

class MessageController:
    
    
    def receiveMessage(message_json):
        
        try:
            response = MessageService.messageReceived(message_json)
            return response, 200
        except Exception as error:
            return {'error': str(error)}, 500
   
    