from database import db
from datetime import datetime
from enum import Enum
from settings import logger

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
    __tablename__ = "messages"
    

    id = db.Column(db.BigInteger, primary_key=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=True)
    type = db.Column(db.SmallInteger, nullable=False)
    message = db.Column(db.Text, nullable=True)
    media_id = db.Column(db.BigInteger, nullable=True)
    status = db.Column(db.SmallInteger, nullable=False, default=MessageStatus.PENDING.value)
    wamid = db.Column(db.String(100), nullable=True, unique=True)
    ref_wamid=db.Column(db.String(100), db.ForeignKey("messages.wamid"), nullable=True, unique=False)
    sent_at = db.Column(db.DateTime, nullable=False)
    user=db.relationship('User')

    def __init__(self, message_data) :
        self.chat_id = message_data['chat_id']
        self.user_id = message_data['user_id'] if 'user_id' in message_data else None
        self.type = Message.get_message_type(message_data['type'])
        self.message = message_data['message'] if 'message' in message_data else None
        self.media_id = message_data['media_id'] if 'media_id' in message_data else None
        self.wamid = message_data['wamid']
        self.sent_at = datetime.fromtimestamp(message_data['timestamp']) if 'timestamp' in message_data else datetime.now()
        self.ref_wamid = message_data['ref_wamid'] if 'ref_wamid' in message_data else None
        self.status = message_data['status'] if 'status' in message_data else MessageStatus.PENDING.value

    @staticmethod
    def get_message_type(message_type : str) -> int :
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
    def get_message_status(message_status : str) -> int :
        statuses = {
            'sent' : MessageStatus.SENT,
            'delivered' : MessageStatus.DELIVERED,
            'read' : MessageStatus.READ,
        }
        return statuses[message_status].value if message_status in statuses else MessageStatus.ERROR.value
    
    
    def set_status(self, status : MessageStatus) : 
        self.status = status.value

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'user_id' : self.user_id,
            'user_name' : self.user.username if self.user is not None else None,
            'type': MessageType(self.type).name,
            'message': self._get_message_text(),
            'media_id':self.media_id,
            'wamid':self.wamid,
            'sent_at':self.sent_at.strftime("%H:%M %d/%m/%Y"),
            'ref_wamid':self.ref_wamid,
            'status':MessageStatus(self.status).value
        }
        
        
    def _get_message_text(self):
        if(self.type == MessageType.LOCATION.value):
            coords = self.message[1:-1]
            return 'https://www.google.com/maps/search/?api=1&query={coords}'.format(coords=coords)
        
        else: return self.message