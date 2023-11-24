from app import db
from datetime import datetime, timedelta
from enum import Enum
from app import logger
from src.models import Chat

class MessageType(Enum):
    TEXT = 1
    IMAGE = 2
    VIDEO = 3
    AUDIO = 4
    STICKER = 5
    DOCUMENT = 6
    LOCATION = 7
    CONTACT = 8
    REACTION = 9
    UNSUPPORTED = 10

class MessageStatus(Enum):
    PENDING = 0
    SENT = 1
    DELIVERED = 2
    READ = 3
    ERROR = 4
    

class Message(db.Model):

    id = db.Column(db.BigInteger, primary_key=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chat.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), nullable=True)
    type = db.Column(db.SmallInteger, nullable=False)
    message = db.Column(db.Text, nullable=True)
    media_id = db.Column(db.BigInteger, nullable=True)
    status = db.Column(db.SmallInteger, nullable=False, default=MessageStatus.PENDING.value)
    mime_type = db.Column(db.String(20), nullable=True)
    wamid = db.Column(db.String(100), nullable=True, unique=True)
    ref_wamid=db.Column(db.String(100), db.ForeignKey("message.wamid"), nullable=True, unique=False)
    sent_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, chat_id, message_data) :
        self.chat_id = chat_id
        self.type = Message.get_message_type(message_data['type'])
        self.message = message_data['content']['message'] if 'message' in message_data['content'] else None
        self.media_id = message_data['content']['id'] if 'id' in message_data['content'] else None
        self.mime_type = message_data['content']['mime_type'] if 'mime_type' in message_data['content'] else None
        self.wamid = message_data['wamid']
        self.sent_at = datetime.fromtimestamp(message_data['timestamp'])
        self.ref_wamid = message_data['ref_wamid'] if 'ref_wamid' in message_data else None
        

    @staticmethod
    def get_message_type(message_type : str) -> MessageType :
        types = {
            'text': MessageType.TEXT,
            'image': MessageType.IMAGE,
            'video': MessageType.VIDEO,
            'audio': MessageType.AUDIO,
            'sticker': MessageType.STICKER,
            'document': MessageType.DOCUMENT,
            'location': MessageType.LOCATION,
            'contacts' : MessageType.CONTACT,
            'reaction' : MessageType.REACTION,
            'unsupported' : MessageType.UNSUPPORTED
        }
        return types[message_type].value if message_type in types else MessageType.UNSUPPORTED.value
    
    @staticmethod
    def get_message_status(message_status : str) -> MessageStatus :
        statuses = {
            'sent' : MessageStatus.SENT,
            'delivered' : MessageStatus.DELIVERED,
            'read' : MessageStatus.READ,
        }
        return statuses[message_status].value if message_status in statuses else MessageStatus.ERROR.value