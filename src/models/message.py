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

class Message(db.Model):
    
    id = db.Column(db.BigInteger, primary_key=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chat.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), nullable=True)
    type = db.Column(db.Enum(MessageType), nullable=False)
    content = db.Column(db.Text, nullable=False)
    wamid = db.Column(db.String(50), nullable=True)
    sent_at = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, chat_id, type, content):
        self.chat_id = chat_id
        self.type = type
        self.content = content
        self.sent_at = datetime.now()
        
    # def __init__(self, message_data) :
    #     # self.type = message_data.type
        
        
        
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
        return types[message_type] if types[message_type] else MessageType.UNSUPPORTED
        


        
    