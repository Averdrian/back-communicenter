from app import db
from datetime import datetime


class Message(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chat.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), nullable=True)
    type = db.Column(db.SmallInteger, nullable=False)
    content = db.Column(db.Text, nullable=False)
    wamid = db.Column(db.String(50), nullable=True)
    sent_at = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, chat_id, type):
        self.chat_id = chat_id
        self.type = type
        self.sent_at = datetime.now()   