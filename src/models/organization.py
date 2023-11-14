from app import db


class Organization(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='users', lazy='joined')
    chats = db.relationship('Chat', backref='organization', lazy='joined')
    
    def __init__(self, name):
        self.name = name