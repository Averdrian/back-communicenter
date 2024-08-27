from database import db
from src.models import Chat
from settings import logger
from src.services import ChatService
from src.utils.authentication import login_required
from socketio_instance import socketio
from src.models import ChatStatus

class ChatController:
    
    @login_required
    def get_chats():
        try:
            ChatService.set_chats_closed()
            chats = ChatService.get_chats()
            return {'success' : True, 'chats': [chat.to_dict() for chat in chats] }, 200
        except Exception as error:
            logger.error(str(error))
            return {'success': False, 'error' : 'Could not get chats'}, 500
        
    @login_required
    def chat_read(chat_id):
        try:
            chat : Chat = Chat.query.get(chat_id)
            if not chat : return {'success': False, 'error': 'Chat not found'}, 404
            ChatService.set_messages_read(chat)
            
            return {'success': True}, 200
        
        except Exception as error:
            logger.error(str(error))
            db.session.rollback()
            return {'success': False, 'error': str(error)}, 500
        
        
    @login_required
    def get_chat(chat_id):
        try:
            chat = Chat.query.get_or_404(chat_id)
            return {'success' : True, 'chat': chat.to_dict()}, 200
        except Exception:
            return {'success' : False, 'error': 'Chat not found'}, 404
    
    @login_required
    def update_status(chat_id, status):
        try:
            chat = Chat.query.get_or_404(chat_id)
            ChatService.update_chat_status(chat, status)
            db.session.commit()
            return {'success' : True, 'status':{'name':ChatStatus(status).status_name(), 'value':ChatStatus(status).value }},  200
        except Exception as error:
            logger.error(str(error))
            return {'success' : False, 'error' : 'Chat not found'}, 404
        
    @login_required
    def get_statuses():
        statuses = [{'name':status.status_name(), 'value':status.value} for status in ChatStatus]
        return {'success': True, 'statuses':statuses}, 200
        
    
    
    def send_change_status(organization_id, chat_id, status):
        socketio.emit('chat-status-'+str(organization_id), {'chat_id': chat_id, 'status': status.value, 'status_name': status.status_name()})
        
        