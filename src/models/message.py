from app import db
from datetime import datetime
from enum import Enum   

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

#TODO: MENSAJE QUE REFERENCIE OTRO MENSAJE, O DARIA MUCHO PROBLEMA? -> PENSAR EN EL FRONT

class Message(db.Model):
    
    id = db.Column(db.BigInteger, primary_key=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chat.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), nullable=True)
    type = db.Column(db.SmallInteger, nullable=False)
    message = db.Column(db.Text, nullable=True)
    media_id = db.Column(db.BigInteger, nullable=True)
    mime_type = db.Column(db.String(20), nullable=True)
    wamid = db.Column(db.String(100), nullable=True)
    sent_at = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, chat_id, type, content):
        self.chat_id = chat_id
        self.type = type
        self.content = content
        self.sent_at = datetime.now()
        
    def __init__(self, chat_id, message_data) :
        self.chat_id = chat_id
        self.type = Message.getMessageType(message_data['type'])
        self.message = message_data['content']['message']
        self.media_id = message_data['content']['id'] if 'id' in message_data['content'] else None
        self.mime_type = message_data['content']['mime_type'] if 'mime_type' in message_data['content'] else None
        self.wamid = message_data['wamid']
        self.sent_at = datetime.fromtimestamp(message_data['timestamp'])
        
    def getMessageType(message_type : str) -> MessageType :
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
        return types[message_type].value if types[message_type] else MessageType.UNSUPPORTED.value
        


        
    