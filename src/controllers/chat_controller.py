from database import db
from src.models import Chat, Message, MessageStatus
from settings import logger
from src.services import ChatService

class ChatController:
    
    def chat_read(chat_id: int) -> (dict, int):
        try:
            chat : Chat = Chat.query.get(chat_id)
            if not chat : return {'success': False, 'error': 'Chat not found'}, 404
            ChatService.set_messages_read(chat)
            
            return {'success': True}, 200
        
        except Exception as error:
            logger.error(str(error))
            db.session.rollback()
            return {'success': False, 'error': str(error)}, 500
        
        
    def get_chat(chat_id : int) -> (dict, int):
        try:
            chat = Chat.query.get_or_404(chat_id)
            return {'success' : True, 'chat': chat.to_dict()}, 200
        except Exception as _:
            return {'success' : False, 'error': 'Chat not found'}, 404
    