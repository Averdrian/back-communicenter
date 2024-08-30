from database import db
from src.models import Chat
from settings import logger
from src.services import ChatService
from src.utils.authentication import login_required
from socketio_instance import socketio
from src.models import ChatStatus
from settings import APPLICATION_TIMEZONE
from datetime import datetime
import pytz


class ChatController:
    
    @login_required
    def get_chats(last_timestamp, statuses):
        try:
            ChatService.set_chats_closed()
            if last_timestamp == None: last_timestamp = datetime.now(APPLICATION_TIMEZONE).timestamp()
            last_date = datetime.utcfromtimestamp(last_timestamp).replace(tzinfo=pytz.utc).astimezone(APPLICATION_TIMEZONE)
            chats, more_chats = ChatService.get_chats(last_date, statuses)
            last = chats[-1].last_message_at.timestamp() if len(chats) else datetime.now().timestamp()
            return {'success' : True, 'chats': [chat.to_dict() for chat in chats], 'more':more_chats, 'last_timestamp':last }, 200
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
        
        