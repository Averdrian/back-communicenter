from src.services import MessageService
from app import logger, db

class MessageController:
    
    def receive_message(message_json):
        try:
            
            message_data = MessageService.get_message_data(message_json)
            chat = MessageService.create_or_update_chat(message_data)
            MessageService.create_message_webhook(chat.id, message_data)
            
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
            if not MessageService.can_send(message_json) : return {'success' : False, 'error': 'The chat is expired'}
            
            send_json = MessageService.prepare_message_body(message_json)
            success, wamid = MessageService.send_message(send_json)
            
            if not success : return {'success': False, 'error': "Error sending message"}
            
            MessageService.create_message_send(message_json, wamid)
            
            return {'success': True}, 201
        except Exception as error:
            logger.error(str(error))
            db.session.rollback()
            return {'success': False, 'error': str(error)}, 500