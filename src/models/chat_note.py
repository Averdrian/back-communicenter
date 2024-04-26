from database import db



class ChatNote(db.Model):
    __tablename__ = "chat_notes"
    
    id=db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.BigInteger, db.ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=True)
    message=db.Column(db.Text, nullable=False)
    
    
    def __init__(self):
        #TODO:
        pass
    
    
    def to_dict(self):
        #TODO:
        pass
    
    