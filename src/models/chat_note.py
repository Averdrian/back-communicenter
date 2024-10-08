from database import db
from datetime import datetime


class ChatNote(db.Model):
    __tablename__ = "chat_notes"
    
    id=db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=True)
    note=db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.relationship('User', lazy='joined')
    
    def __init__(self, chat_id, user_id, note):
        self.chat_id = chat_id
        self.user_id = user_id
        self.note = note 

    
    def as_dict(self):
        return {
            "id" : self.id,
            "chat_id" : self.chat_id,
            "user_id" : self.user_id,
            "username" : self.user.username,
            "note": self.note
        }
    
    